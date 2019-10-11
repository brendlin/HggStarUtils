#!/usr/bin/env python

##
## This macro takes a file produced using pennSoftLepton using PassEvent functions.
##

import ROOT,sys,os
import TAxisFunctions as taxisfunc
import PyAnalysisPlotting as anaplot
import PlotFunctions as plotfunc
import PyHelpers
import HggStarHelpers
import math
from datetime import datetime
from array import array
import gc
import re
ROOT.RooMsgService.instance().setSilentMode(True)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)

mllyPeakLow = 122.
mllyPeakHigh = 128.
mllyBlindLow = 120.
mllyBlindHigh = 130.
categories = ["muons","resolved","merged"]
ncat = len(categories)
peakcut = ['(HGamEventInfoAuxDyn.m_lly > 122000)','(HGamEventInfoAuxDyn.m_lly < 128000)']
categorycuts = ['(HGamEventInfoAuxDyn.yyStarChannel == 1)','(HGamEventInfoAuxDyn.yyStarChannel == 2)','(HGamEventInfoAuxDyn.yyStarChannel == 3)']
categories_to_run = [0] #specify which category to run over. can't run all at once because of memory issues :(
max_iterations = [2,2,2]
CRtoSR_data_scale = [1,1,1]
using_CR = False
significance_mode = 1 #significance mode: 0 - s/sqrt(b); 1 - low stats significance

sig_chain = ROOT.TChain("CollectionTree")
tmp_chain = ROOT.TChain("CollectionTree")
bkg_chain = ROOT.TChain("CollectionTree")

workspace = ROOT.RooWorkspace("ws","ws")
lower_range = 105
upper_range = 160
obsVar = workspace.factory('m_yy[%d,%d]'%(lower_range,upper_range))
obsVar.setRange("all",lower_range,upper_range)
obsVar.setRange("lower",lower_range,120)
obsVar.setRange("lower_unc",lower_range+10,120)
obsVar.setRange("upper",130,upper_range)
obsVar.setRange("upper_unc",130,upper_range-10)
obsVar.setRange("peak", mllyPeakLow, mllyPeakHigh)
obsVar.setRange("unit", 0, 1)

BkgArgList = ROOT.RooArgList('parlist')
BkgArgList.add(obsVar)
BkgArgList.add(workspace.factory('a1[-0.0128,-100,100]'))
function = workspace.factory( "RooExponential::function(m_yy,a1)")

model = workspace.factory( "SUM::model( nBkg[20,100000]*function )" )

frame = obsVar.frame()

class Variable:
    def __init__( self , name = 'x', sign = '>', nbins = 55, min = 105, max =  160, var_title = "m_lly",  n_points = 5, scan_min = 0, scan_max = 5, root_name = "var"):
        self.name = name
        self.sign = sign
        self.nbins = nbins
        self.min = min
        self.max = max
        self.var_title = var_title
        self.n_points = n_points
        self.scan_min = scan_min
        self.scan_max = scan_max
        self.root_name = root_name
        
        self.n_points_orig = n_points
        
    def SetFineGrid(self):
        self.n_points = self.n_points_orig
    
    def SetCoarseGrid(self):
        self.n_points = self.n_points_orig/10
        
    def GetPoints(self,n):
        points = []
        increment = (self.scan_max-self.scan_min)/float(n)
        for i in range(n):
            points.append(self.scan_min + i*increment)
        return points
        
class OptimizationSequence:
    def __init__( self , year = "unknown", category = 0, variables = [], options = [], sgnf_mode = 0):
        self.year = year
        self.category = category
        self.variables = variables
        self.options = options
        self.sgnf_mode = sgnf_mode #method for calculating significance
        self.cuts = []
        self.cut_points = []
        self.iteration = 0
        self.cur_cut_point = 0 #specifies which element in the significance list gives max significance
        self.cur_cut_sign = '>'
        self.next_cut_point = 0 #specifies which element in the significance list gives max significance - for last iteration over variables
        self.sig_yields = []
        self.bkg_yields = []
        self.sig_unc = []
        self.bkg_unc = []
        self.sig_histo = None
        self.bkg_histo = None
        self.var_sequence = []
        self.previous_max_sgnf = 0.0
        
    def InitCuts(self): #set initial cuts for optimization
        initial_cuts = []
        initial_cuts.append(categorycuts[self.category])
        for cut in self.options.cuts: #first add cuts unrelated to optimization
            NoOptimizationCut = True
            if not self._allowedCut(cut):
                continue
            for variable in self.variables: 
                if variable.name in cut:
                    NoOptimizationCut = False
            if NoOptimizationCut:
                initial_cuts.append(cut)
        for variable in self.variables: #now deal with cuts which we will optimize
            if not self._allowedCut(variable.name):
                continue
            InitialCutSet = False
            for cut in self.options.cuts:
                if self._allowedCut(cut) and (variable.name in cut): #we already have initial cut value for this variable from config - use it
                    InitialCutSet = True
                    initial_cuts.append(cut)
            if not InitialCutSet:
                if variable.sign == '>':
                    initial_cuts.append('('+variable.name + variable.sign + str(variable.scan_min)+')') #no initial cut value set for the variable - set it at scan_min
                else:
                    initial_cuts.append('('+variable.name + variable.sign + str(variable.scan_max)+')') #no initial cut value set for the variable - set it at scan_max
                    
        self.cuts.append(initial_cuts)
    
    def SetNextCuts(self, cuts):
        self.cuts.append(cuts)
            
    def AddYields(self, signal, variable, yields, uncertainties, histo):
        if signal:
            self.sig_yields.append(yields)
            self.sig_unc.append(uncertainties)
            self.sig_histo = histo
            self.var_sequence.append(variable)
        else:
            self.bkg_yields.append(yields)
            self.bkg_unc.append(uncertainties)
            self.bkg_histo = histo
            
    def GetVarSequence(self):
        return self.var_sequence
    
    def GetCurrentVariable(self):
        return self.var_sequence[self.iteration]
    
    def SetSgnfMode(self,mode):
        self.sgnf_mode = mode
    
    def GetCurrentSignificance(self):
        s = self.sig_yields[self.iteration][self.cur_cut_point]
        b = self.bkg_yields[self.iteration][self.cur_cut_point]
        return self.CalcSignificance(s,b)
    
    def GetDeltaSignificance(self):
        return self.GetCurrentSignificance() - self.previous_max_sgnf
    
    def GetSignificances(self, iteration = 0):
        significances = []
        for i in range(len(self.sig_yields[iteration])):
            s = self.sig_yields[iteration][i]
            b = self.bkg_yields[iteration][i]
            significance = self.CalcSignificance(s,b)
            significances.append(significance)
        return significances
    
    def GetCurrentSignificances(self):
        return self.GetSignificances(self.iteration)
    
    def GetCurrentSignals(self):
        return self.sig_yields[self.iteration]
    def GetCurrentBackgrounds(self):
        return self.bkg_yields[self.iteration]
    
    def GetAllSignificances(self):
        significances = []
        for i in range(self.iteration+1):
            significances.append(self.GetSignificances(i))
        return significances
    
    def GetAllMaxSignificances(self):
        significances = []
        for i in range(len(self.sig_yields)):
            s = self.sig_yields[i][self.cut_points[i]]
            b = self.bkg_yields[i][self.cut_points[i]]
            max_significance = self.CalcSignificance(s,b)
            significances.append(max_significance)
        return significances
    
    def GetAllMaxSignifErrors(self):
        errors = []
        for i in range(len(self.sig_unc)):
            serr = self.sig_unc[i][self.cut_points[i]]
            berr = self.bkg_unc[i][self.cut_points[i]]
            s = self.sig_yields[i][self.cut_points[i]]
            b = self.bkg_yields[i][self.cut_points[i]]
            error = self.CalcSignificanceError(s,b,serr,berr)
            errors.append(error)
        return errors
    
    def GetAllYields(self, signal):
        yields = []
        if signal:
            for i in range(len(self.sig_yields)):
                yields.append(self.sig_yields[i][self.cut_points[i]])
        else:
            for i in range(len(self.bkg_yields)):
                yields.append(self.bkg_yields[i][self.cut_points[i]])
        return yields
    
    def GetAllErrors(self, signal):
        errors = []
        if signal:
            for i in range(len(self.sig_unc)):
                errors.append(self.sig_unc[i][self.cut_points[i]])
        else:
            for i in range(len(self.bkg_unc)):
                errors.append(self.bkg_unc[i][self.cut_points[i]])
        return errors
    
    def CalcSignificance(self,s,b):
        if self.sgnf_mode == 0:
            return s/math.sqrt(b)
        elif self.sgnf_mode == 1:
            return math.sqrt(2.0*( (s+b)*math.log(1+s/float(b)) - s ))
        else:
            print "ERROR: OptimizationSequence: unknown significance mode " + self.sgnf_mode
            sys.exit(1)
            
    def CalcSignificanceError(self,s,b,serr,berr):
        df_over_ds = 0.0
        df_over_db = 0.0
        if self.sgnf_mode == 0:
            df_over_ds = 1/math.sqrt(b)
            df_over_db = -0.5*s/math.sqrt(b*b*b)
        elif self.sgnf_mode == 1:
            df_over_ds = math.sqrt(2.0)*math.log(1+s/float(b))/math.sqrt( (s+b)*math.log(1+s/float(b)) - s )
            df_over_db = math.sqrt(2.0)*(math.log(1+s/float(b)) - s*(b+s)/(b*b*(s/float(b)+1)) )/ math.sqrt( (s+b)*math.log(1+s/float(b)) - s )
        else:
            print "ERROR: OptimizationSequence: unknown significance mode " + self.sgnf_mode
            sys.exit(1)
        return math.sqrt(df_over_ds*df_over_ds*serr*serr + df_over_db*df_over_db*berr*berr)
    
    def GetAllCuts(self):
        return self.cuts
    
    #def GetAllSigHistos(self):
        #return self.sig_histos
    
    #def GetAllBkgHistos(self):
        #return self.bkg_histos
    
    def GetSigHisto(self):
        return self.sig_histo
    
    def GetBkgHisto(self):
        return self.bkg_histo
    
    def GetCategory(self):
        return self.category
    
    def GetYear(self):
        return self.year
    
    def GetIterations(self):#total iterations
        return self.iteration+1
    
    def GetIteration(self):#current iteration
        return self.iteration
    
    def GetCurrentCuts(self):
        cur_cuts = []
        try:
            cur_cuts = self.cuts[self.iteration]
        except IndexError:
            print "ERROR: OptimizationSequence: current cuts are not defined! This should never happen"
            sys.exit(1)
        return cur_cuts
    
    def SetCurrentCutPoint(self, point):
        self.cur_cut_point = point
        self.cut_points.append(point)
        
    def SetCurrentCutSign(self,sign):
        self.cur_cut_sign = sign

    def SetNextCutPoint(self, point):
        self.next_cut_point = point
        
    def GetCutPoints(self):
        return self.cut_points
    
    def GetCutPoint(self):
        return self.cur_cut_point
    
    def GetCutSign(self):
        return self.cur_cut_sign
        
    def NextIteration(self):
        self.previous_max_sgnf = self.GetCurrentSignificance()
        self.iteration = self.iteration+1
    
    def PreviousIteration(self):
        if self.iteration>0:
            self.iteration = self.iteration-1
            del self.cuts[-1]
            
    def AddLastIteration(self):
        self.AddYields(True, self.var_sequence[-1], self.sig_yields[-1],self.sig_unc[-1],self.sig_histo) #copy last yields
        self.AddYields(False, self.var_sequence[-1], self.bkg_yields[-1],self.bkg_unc[-1],self.bkg_histo) #copy last yields
        self.SetCurrentCutPoint(self.next_cut_point) #update cut point
                
    def _allowedCut(self,cut):

        if self.category+1 == 1 and ("Electron" in cut or "Track" in cut): #muons
            return False
        elif self.category+1 == 2 and ("Muon" in cut or "Track" in cut): #resolved
            return False
        elif self.category+1 == 3 and ("Muon" in cut or "Electron" in cut): #merged
            return False
        return True
    
    def AllowedVariable(self,var_name):
        return self._allowedCut(var_name)
    
def Shorten(name):
    name = name.replace('HGam','')
    name = name.replace('EventInfoAuxDyn.','')
    name = name.replace('AuxDyn','')
    return name

def Simplify(name):
    name = name.replace('[','_')
    name = name.replace(']','_')
    name = name.replace('/','_over_')
    name = name.replace('(','_')
    name = name.replace(')','_')
    return name

def LaTeXfy(cuts):
    pretty_cuts = []
    for cut in cuts:
        if "yyStarChannel" in cut or "isPassedEventSelection" in cut or "cutFlow" in cut:
            continue
        
        name = re.split('<|>',cut)[0].lstrip("(")
        if name in options.histformat:
            root_name = options.histformat[name][7]
            cut = cut.replace(name,root_name)

                
        cut = cut.replace(')','')
        cut = cut.replace('(','')
        cut = cut.replace("#","\\")
        if " [GeV]" in cut:
            cut = cut.replace(" [GeV]","")
            cut = cut + " GeV"
        #if '/' in cut:
            #cut = cut.replace('/',"}{")
            #cut = "\\frac{" + cut
            #cut = cut.replace('>',"}>")
            #cut = cut.replace('<',"}<")
        cut = "$"+cut+"$"
        pretty_cuts.append(cut)
    return pretty_cuts 
    
def WriteTable(f,cuts, significances,signif_errors,sig_yields,sig_errors,bkg_yields,bkg_errors):
    pretty_cuts = []
    for cut in cuts:
        pretty_cuts.append(LaTeXfy(cut))
    ncols = len(pretty_cuts[0])
    nrows = len(pretty_cuts)
    
    f.write("\\begin{tabular}{ |c|c|c|c|c|c|c|c|c| } \n\\hline\n")
    f.write("\\multicolumn{"+str(ncols)+"}{|c|}{Cuts} & S & B & $S/\sqrt{B}$\\\\\n\\hline\n")
    
    for i in range(nrows):
        for j in range(ncols):
            f.write(pretty_cuts[i][j] + "\t&\t")
        f.write(str(round(sig_yields[i],4)) + " \pm " + str(round(sig_errors[i],4)) + " \t&\t ")
        f.write(str(round(bkg_yields[i],4)) + " \pm " + str(round(bkg_errors[i],4)) + " \t&\t ")
        f.write(str(round(significances[i],4)) + " \pm " + str(round(signif_errors[i],4)) + " \\\\\n")
    f.write("\\hline\n")
    f.write("\\end{tabular}\n")
    
def PlotIteration(optimization):
    variable = optimization.GetCurrentVariable()
    title = Simplify(optimization.GetYear() + "_" + categories[optimization.GetCategory()]+"_"+str(optimization.GetIteration())+"_"+variable.name)
    iteration = optimization.GetIteration()
    significances = optimization.GetCurrentSignificances()
    sig_histo = optimization.GetSigHisto()
    bkg_histo = optimization.GetBkgHisto()
    
    c = plotfunc.RatioCanvas(variable.name + "_" + str(iteration),variable.name + "_" + str(iteration),500,600)
    sig_histo_var = sig_histo.ProjectionY(title + "_sig",0,sig_histo.GetNbinsX()+1)
    bkg_histo_var = bkg_histo.ProjectionY(title + "_bkg",0,bkg_histo.GetNbinsX()+1)
    sig_histo_var.Scale(1/sig_histo_var.Integral())
    bkg_histo_var.Scale(1/bkg_histo_var.Integral())
    sig_histo_var.SetTitle("signal mc")
    bkg_histo_var.SetTitle("data")
    plotfunc.AddHistogram(c,bkg_histo_var)
    plotfunc.AddHistogram(c,sig_histo_var)
    sgnf_graph = ROOT.TGraph(len(significances),array('d',variable.GetPoints(len(significances))),array('d',significances))
    sgnf_graph.SetTitle("sgnf")
    sgnf_graph.SetName(str(iteration))
    npoints = len(significances)
    sgnf_graph.GetXaxis().Set(npoints+1,variable.GetPoints(npoints)[0],variable.GetPoints(npoints)[-1]+(variable.GetPoints(npoints)[1]-variable.GetPoints(npoints)[0]))

    plotfunc.AddHistogram(plotfunc.GetBotPad(c),sgnf_graph)
    plotfunc.SetAxisLabels(c,variable.root_name,"arbitrary units","S/#sqrt{B}")
    plotfunc.FullFormatCanvasDefault(c,optimization.options.fb)
    plotfunc.MakeLegend(c,.65,.73,.8,.93)
    c.Print("plots/" + title + ".png")
    
    bkg_histo_var.SetDirectory(0)
    sig_histo_var.SetDirectory(0)
    del plotfunc.tobject_collector[:]
    gc.collect()
            
def PlotMlly(optimization, prefix):
    sig_histo = optimization.GetSigHisto()
    bkg_histo = optimization.GetBkgHisto()
    cut_point = optimization.GetCutPoint()
    cut_sign = optimization.GetCutSign()
    
    c = plotfunc.RatioCanvas(prefix,prefix,500,600)
    if cut_sign == '>':
        if prefix == "init_cuts":
            cut_point = -1
        sig_histo_mlly = sig_histo.ProjectionX("sig",cut_point+1,sig_histo.GetNbinsY()+1)
        bkg_histo_mlly = bkg_histo.ProjectionX("bkg",cut_point+1,bkg_histo.GetNbinsY()+1)
    else:
        if prefix == "init_cuts":
            cut_point = sig_histo.GetNbinsY()
        sig_histo_mlly = sig_histo.ProjectionX("sig",0,cut_point+1)
        bkg_histo_mlly = bkg_histo.ProjectionX("bkg",0,cut_point+1)
        
    sig_histo_mlly.SetTitle("signal mc")
    bkg_histo_mlly.SetTitle("data")
    plotfunc.AddHistogram(c,bkg_histo_mlly)
    plotfunc.AddHistogram(c,sig_histo_mlly)
    GetNBkgPeakParams(bkg_histo_mlly,False)
    fit_curve = frame.getCurve()
    fit_curve.SetTitle("fit")
    chi = round(frame.chiSquare(),2)
    plotfunc.AddHistogram(c,fit_curve,"L")
    pull_hist = frame.pullHist()
    j=0
    for i in range(pull_hist.GetN()):
        if j >= pull_hist.GetN():
            break
        x = ROOT.Double(0)
        y = ROOT.Double(0)
        pull_hist.GetPoint(j,x,y)
        if x > mllyBlindLow and x < mllyBlindHigh:
            pull_hist.RemovePoint(j)
        else:
            j = j + 1
    pull_hist.GetXaxis().SetLimits(lower_range,upper_range)
    plotfunc.AddHistogram(plotfunc.GetBotPad(c),pull_hist)
    plotfunc.SetAxisLabels(c,"m_{ll#gamma} [GeV]","events","pull")
    plotfunc.FullFormatCanvasDefault(c,optimization.options.fb)
    plotfunc.MakeLegend(c,.65,.73,.8,.93)
    plotfunc.DrawText(c,"#chi^{2}/ndof="+ str(chi),0.2,0.70,0.5,0.75)
    c.Print("plots/" + prefix + "_" + categories[optimization.GetCategory()] + "_" + optimization.GetYear() + ".png")
    
    

def GetNBkgPeakParams(histo, integrate):
    datasb = ROOT.RooDataHist('data','',ROOT.RooArgList(obsVar),histo,1.)
    workspace.var('nBkg').setMax(int(2*histo.Integral()))

    
    model.fitTo(datasb
                    ,ROOT.RooFit.Extended()
                    ,ROOT.RooFit.Range("lower,upper")
                    ,ROOT.RooFit.Minimizer('Minuit2')
                    ,ROOT.RooFit.Strategy(1)
                    ,ROOT.RooFit.SumW2Error(False)
                    ,ROOT.RooFit.Offset(1)
                    ,ROOT.RooFit.Save((not integrate))
                    )
    
    if integrate:
        nBkg = workspace.var('nBkg').getValV()
        nBkgPeak = workspace.pdf('function').createIntegral(ROOT.RooArgSet(obsVar),ROOT.RooArgSet(obsVar),0,"peak").getVal()*nBkg
        
        model.fitTo(datasb
                    ,ROOT.RooFit.Extended()
                    ,ROOT.RooFit.Range("lower_unc,upper")
                    ,ROOT.RooFit.Minimizer('Minuit2')
                    ,ROOT.RooFit.Strategy(1)
                    ,ROOT.RooFit.SumW2Error(False)
                    ,ROOT.RooFit.Offset(1)
                    ,ROOT.RooFit.Save((not integrate))
                    )
        
        nBkg = workspace.var('nBkg').getValV()
        nBkgPeakLow = workspace.pdf('function').createIntegral(ROOT.RooArgSet(obsVar),ROOT.RooArgSet(obsVar),0,"peak").getVal()*nBkg
        
        model.fitTo(datasb
                    ,ROOT.RooFit.Extended()
                    ,ROOT.RooFit.Range("lower,upper_unc")
                    ,ROOT.RooFit.Minimizer('Minuit2')
                    ,ROOT.RooFit.Strategy(1)
                    ,ROOT.RooFit.SumW2Error(False)
                    ,ROOT.RooFit.Offset(1)
                    ,ROOT.RooFit.Save((not integrate))
                    )
        
        nBkg = workspace.var('nBkg').getValV()
        nBkgPeakUp = workspace.pdf('function').createIntegral(ROOT.RooArgSet(obsVar),ROOT.RooArgSet(obsVar),0,"peak").getVal()*nBkg
        uncertainty = (abs(nBkgPeak-nBkgPeakLow) + abs(nBkgPeak-nBkgPeakUp))/2.0
        return [nBkgPeak,uncertainty]
    else:
        plotOptions_sb_all = [ROOT.RooFit.Range("all"), ROOT.RooFit.NormRange("lower,upper"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative)]
        datasb.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
        model.plotOn(frame,*(plotOptions_sb_all))

def GetNBkgPeak(histo):
    return GetNBkgPeakParams(histo,True)

def GetNEvents(signal,options,year,category,variable,optimization) :
    histo = ROOT.TH2F()
    if signal:
        file_list_sig = options.signal.split(',')
        for i,f in enumerate(file_list_sig):
            sig_chain.Add(f)
            tf = ROOT.TFile(f)
            weight = options.weightscale(ROOT.TFile(f))
            weight = weight * options.fb
            if options.fb == 80.49: #combine all years in mc, hack for mc16a+d, should not be used for mc16e
                weight = weight * HggStarHelpers.SF_80fb(tf) 
            cur_histo = ProcessTrees(options,signal,category,variable,optimization)
            cur_histo.Scale(weight)
            if i == 0:
                histo = cur_histo
            else:
                histo.Add(cur_histo)
            sig_chain.Reset()
    else:
        histo = ProcessTrees(options,signal,category,variable,optimization)


    scan_yields = []
    uncertainties = []
    npoints = histo.GetNbinsY()

    scan_point_min = variable.scan_min
    scan_point_max = variable.scan_max
    increment = (scan_point_max-scan_point_min)/float(npoints)
    
    cut_point = 0
    if variable.sign == '<':
        cut_point = npoints-1 #to integrate over whole distribution by default
    
    for j in range(1,npoints+1):
        for i,cut in enumerate(optimization.GetCurrentCuts()):
            if variable.name in cut:
                if ('>' in cut and float(cut.split('>')[-1].rstrip(")")) == scan_point_min + (j-1)*increment) or ('<' in cut and float(cut.split('<')[-1].rstrip(")")) == scan_point_min + j*increment): #we already have a cut on this variable which maximized significance, need to save it for significance calculation
                    cut_point = j-1
        Yaxis = histo.GetYaxis()
        histo_title = year + "_" + categories[category] + str(optimization.GetIteration()) + "_" +str(signal) + "_" +str(j) + "_" + variable.name + "_" + str(Yaxis.GetBinLowEdge(j))
        if variable.sign == '>':
            histo_variable = histo.ProjectionX(histo_title,j,histo.GetNbinsY()+1)
        else:
            histo_variable = histo.ProjectionX(histo_title,0,j)
        NPeak = 0
        uncertainty = 0.0
        if signal:
            root_unc = ROOT.Double()
            NPeak = histo_variable.IntegralAndError(0,histo_variable.GetNbinsX()+1,root_unc)
            uncertainty = root_unc
        else:
            NPeakWithErr = GetNBkgPeak(histo_variable)
            NPeak = NPeakWithErr[0]
            if using_CR:
                NPeak = NPeak*CRtoSR_data_scale[category]
            uncertainty = NPeakWithErr[1]
                
        scan_yields.append(NPeak)
        uncertainties.append(uncertainty)
        histo_variable.SetDirectory(0)
    optimization.AddYields(signal,variable,scan_yields,uncertainties,histo)
    if signal: #crude way of doing this only once per iteration
        optimization.SetCurrentCutPoint(cut_point)
        if '<' in cut:
            optimization.SetCurrentCutSign('<')
    histo.SetDirectory(0)
            
def AdjustCuts(optimization,variable):
    increment = (variable.scan_max-variable.scan_min)/float(variable.n_points)
    significances = optimization.GetCurrentSignificances()
    sgnf_max = 0
    sgnf_max_point = 0
    sgnf_max_i = 0
    if variable.sign == '<':
        sgnf_max = significances[variable.n_points-1] #this is to make _upper_ bound of value the default, as opposed to '>' case where lower bound (usually 0) should be the default
        sgnf_max_i = variable.n_points-1
        sgnf_max_point = variable.scan_min + variable.n_points*increment
        
        
    for i in range(variable.n_points):
        scan_point = variable.scan_min + i*increment
        if variable.sign == '<':
            scan_point = scan_point + increment #if the sign is '<' should select bin upper edge to cut, e.g. for bin edges 2,3 the cuts are var>2 for '>', and var<3 for '<'
        sgnf = significances[i]
        if sgnf>sgnf_max:
            sgnf_max = sgnf
            sgnf_max_point = scan_point 
            sgnf_max_i = i
    
    new_cuts = []
    for cut in optimization.GetCurrentCuts():
        if variable.name in cut:
            if float(re.split('<|>',cut)[-1].rstrip(")")) == sgnf_max_point:
                optimization.SetNextCuts(optimization.GetCurrentCuts()) #did not change cuts - significance only goes down with this cut
                return False 
            new_cuts.append('('+variable.name + variable.sign + str(sgnf_max_point)+')')
        else:
            new_cuts.append(cut)
    print "Adjusting cuts to:",new_cuts
    optimization.SetNextCuts(new_cuts)
    optimization.SetNextCutPoint(sgnf_max_i)
    return True
                
                
def ProcessTrees(options,signal,category,variable,optimization):
    chain = bkg_chain
    if signal:
        chain = sig_chain
    cuts = [] #cuts specific for variable, e.g. if we already have a cut on photon pt, we want to relax it when scanning photon pt significance
    for cut in optimization.GetCurrentCuts():
        if using_CR and not signal and "HGamEventInfoAuxDyn.isPassedEventSelection" in cut: #for CR, should remove this requirement for data
            continue
        if variable.name not in cut:
            cuts.append(cut)
    weight=''
    histo_title = optimization.GetYear() + "_" + categories[category] + "_" + str(optimization.GetIteration()) + "_" +str(signal) + "_" + Simplify(variable.name)
    if(signal) :
        weight = options.weight
        if ''.join(cuts+peakcut+options.truthcuts) :
            weight = (weight+'*(%s)'%(' && '.join(cuts+peakcut+options.truthcuts).lstrip('& ').rstrip('& '))).lstrip('*')
    else :
        if ''.join(cuts+options.blindcut) :
            weight = '('+' && '.join(cuts+options.blindcut).lstrip('& ').rstrip('& ')+')'
    chain.Draw(variable.name + ':HGamEventInfoAuxDyn.m_lly/1000' + '>>' + histo_title + '('+ str(variable.nbins) + ',' + str(variable.min) + ',' + str(variable.max) + ',' + str(variable.n_points) + ',' + str(variable.scan_min) + ',' + str(variable.scan_max) + ')', weight,'egoff')
    histo = ROOT.gDirectory.Get(histo_title)
    histo.SetDirectory(0)
    return histo

def main(options,args) :
    
    time_start=datetime.now()
    
    plotfunc.SetupStyle()
    
    file_list_sig = options.signal.split(',')
    file_list_bkg = options.data.split(',')
    #for f in file_list_sig :
        #sig_chain.Add(f)
    for f in file_list_bkg :
        bkg_chain.Add(f)
    
    variable_names = options.variables
    variables = []
    for name in variable_names:
        histformat = options.histformat[name[:-1]]
        n_var_bins = histformat[0]
        var_min = histformat[1]
        var_max = histformat[2]
        var_title = histformat[3]
        n_scan_points = histformat[4]
        scan_point_min = histformat[5]
        scan_point_max = histformat[6]
        root_name = histformat[7]
        variables.append(Variable(name[:-1],name[-1],n_var_bins,var_min,var_max,var_title,n_scan_points,scan_point_min,scan_point_max,root_name))
    
    year = "unknown_year"
    if(options.fb==36.18):
        year="2015_16"
    if(options.fb==43.59):
        year="2017"  
    if(options.fb==80.49):
        year="2015_16_17" 
    
    time_init = datetime.now()
    times_per_cat = []
    for category in categories_to_run:
        optimization = OptimizationSequence(year,category,variables,options,significance_mode)
        optimization.InitCuts()
        
        #for variable in variables:
            #variable.SetCoarseGrid()
 
        previous_adjust = True
        first_iteration = True
        
        for i in range(max_iterations[category]):
            for variable in variables:
                if not optimization.AllowedVariable(variable.name):
                    continue

                if options.signal :
                    GetNEvents(True,options,year,category,variable,optimization)
                if options.data :
                    GetNEvents(False,options,year,category,variable,optimization)
                    
                #if first_iteration:
                    #PlotMlly(optimization,"init_cuts") #if uncommenting will run out of mem :(
                first_iteration = False
 
                delta = optimization.GetDeltaSignificance()
                print "***********************************************************"
                print "***********************************************************"
                print "***********************************************************"
                print "***********************************************************"
                print "category:",categories[category]
                print "cuts:", optimization.GetCurrentCuts() #set of current optimized cuts, independent for each category
                print "significance:", optimization.GetCurrentSignificance()
                print "significance change wrt previous iteration:",delta
                print "adjusted cuts?", previous_adjust
                print "***********************************************************"
                print "***********************************************************"
                print "***********************************************************"
                print "***********************************************************"
                PlotIteration(optimization)
                
                #fsgn = open("2D_sgn_" + year + "_" + categories[category] + ".txt","a+")
                #fsig = open("2D_sig_" + year + "_" + categories[category] + ".txt","a+")
                #fbkg = open("2D_bkg_" + year + "_" + categories[category] + ".txt","a+")
                #significances = optimization.GetCurrentSignificances()
                #signals = optimization.GetCurrentSignals()
                #backgrounds = optimization.GetCurrentBackgrounds()
                #for k in range(len(significances)):
                    #fsgn.write(str(significances[k]) + " \t ") 
                    #fsig.write(str(signals[k]) + " \t ") 
                    #fbkg.write(str(backgrounds[k]) + " \t ") 
                #fsgn.write("\n")
                #fsgn.close()
                #fbkg.write("\n")
                #fbkg.close()
                #fsig.write("\n")
                #fsig.close()
                
                previous_adjust = AdjustCuts(optimization,variable) #this will alter cuts, adjusting it to optimal values starting from optimized values for previous iteration
                variable.SetFineGrid()
                optimization.NextIteration()
                #if abs(delta) < 0.0001 and previous_adjust:
                    #break
                
        if previous_adjust:
            optimization.AddLastIteration()
        else:
            optimization.PreviousIteration()
               
        PlotMlly(optimization, "best_cuts")
        
        f = open("optimization_results_" + year + "_" + categories[category] + ".txt","w+")
        WriteTable(f,optimization.GetAllCuts(),optimization.GetAllMaxSignificances(),optimization.GetAllMaxSignifErrors(),optimization.GetAllYields(True),optimization.GetAllErrors(True),optimization.GetAllYields(False),optimization.GetAllErrors(False))
        f.close()
        
        times_per_cat.append(datetime.now())

            
    print "Finished. CPU times:"
    print "Initialization: ", time_init - time_start
    for i,time in enumerate(times_per_cat):
        if i == 0:
            print "Category ", categories[categories_to_run[i]] + ":",  time - time_init
        else:
            print "Category ", categories[categories_to_run[i]] + ":",  time - times_per_cat[i-1]

    return

if __name__ == '__main__':

    p = anaplot.TreePlottingOptParser()
    options,args = p.parse_args()

    if not options.variables :
        print 'Error! Please specify a variable!'
        sys.exit()
        
        
    if(not ROOT.xAOD.Init().isSuccess()): print "Failed xAOD.Init()"

    main(options,args)
    
    ROOT.xAOD.ClearTransientTrees()



    

  

