
# Usage: plottrees.py 1 1 --config plottrees_SidebandFits.py --data data%.root --ratio --poisson --batch --outdir c01_sbFit

import HggStarHelpers
from HggStarHelpers import YEAR,GetFbForMCNormalization
from HggStarHelpers import ChannelEnum,CategoryEnum
import StudyConfSnippets
from HggStarHelpers import StandardSampleMerging as mergesamples
from HggStarHelpers import StandardHistFormat as histformat

import ROOT
ROOT.gROOT.LoadMacro('dscb.C')

treename = 'CollectionTree'

class REGION :
    CR1 = 0
    CR2 = 1
    SR = 2
    SR_VBF = 3
    OBJ_CR = 4

###
# Change this to check out different channels / years:
###
import sys
channel = int(sys.argv[1])
category = int(sys.argv[2])
region = REGION.SR
higgsSF = 100
theyear = YEAR.y2015161718
doMesonCuts = True
doDetailedVariables = False
mll_range = [110,160]
doAddSignal = True
##
# End configuration.
##

fb = GetFbForMCNormalization(theyear)

histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [int(mll_range[1]-mll_range[0]),
                                                 mll_range[0],mll_range[1],'m_{ll#gamma} [GeV]']

leptonObj = {ChannelEnum.DIMUON: 'Muons',
             ChannelEnum.RESOLVED_DIELECTRON:'Electrons',
             ChannelEnum.MERGED_DIELECTRON:  'Electrons',
             }.get(channel,None)

plottext = HggStarHelpers.GetPlotText(channel,category)
plottext[0] = plottext[0].replace('channel','')
if region == REGION.SR_VBF :
    plottext = plottext.replace('channel','VBF category')

from HggStarHelpers import StandardPlotLabels as labels
labels['AllHiggs'] = 'H#rightarrow#gamma*#gamma%s'%('^{ }#times^{ }%d'%(higgsSF) if higgsSF != 1 else '')
if region == REGION.SR :
    labels['data'] = 'Data Sideband'

cuts = [
    'HGamEventInfoAuxDyn.isPassedObjSelection', # object selection
    'HGamEventInfoAuxDyn.isPassedEventSelection', # object selection
#     'HGamElectronsAuxDyn.pt[0] < 40000.',
    ]

if channel :
    cuts.append('HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel))

if category :
    cuts.append('HGamEventInfoAuxDyn.yyStarCategory == %d'%(category))

if region in [REGION.CR1, REGION.CR2, REGION.SR, REGION.SR_VBF] :
    cuts += [
        '(HGamEventInfoAuxDyn.m_lly > %d000 && HGamEventInfoAuxDyn.m_lly < %d000)'%(mll_range[0],mll_range[1]),
        'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.3', # new cuts
        'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.3', # new cuts
        ]

blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]

##
## Standard Variables
##
variables = [
    'HGamEventInfoAuxDyn.m_lly/1000.',
    ]

def afterburner(can) :
    import PlotFunctions as plotfunc
    import TAxisFunctions as taxisfunc
    import ROOT
    import math

    # Fix fb label for 2015-only and 2016-only (see important notes above)
    if theyear in [YEAR.y2015,YEAR.y2016] :
        fb = {YEAR.y2015:3.2,YEAR.y2016:33.0}.get(theyear)
        text_can = can
        if plotfunc.GetTopPad(can) :
            text_can = plotfunc.GetTopPad(can)
        for prim in text_can.GetListOfPrimitives() :
            if '_text' in prim.GetName() :
                for entry in prim.GetListOfPrimitives() :
                    if '36.2' in entry.GetLabel() :
                        entry.SetLabel(entry.GetLabel().replace('36.2','%.1f'%(fb)))
        text_can.Modified()


    # print list(plotfunc.GetTopPad(can).GetListOfPrimitives())
    hist = plotfunc.GetTopPad(can).GetPrimitive('pad_top_data')
    ratioplot = hist.Clone()
    ratioplot.GetYaxis().SetTitle('pull')
    ratioplot.GetXaxis().SetTitle('m_{ll#gamma} [GeV]')

    print 'Expecting to open a file bkgParameters.txt'
    bkg_parameters = open ('bkgParameters.txt')

    function = {
        1:'ExpPoly2',
        2:'Power Law',
        3:'ExpPoly2',
        4:'Power Law',
        5:'Exponential',
        6:'Power Law',
        7:'Power Law',
        8:'Power Law',
        9:'Power Law',
        }.get(category)

    expr = {
        'ExpPoly3':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100 + [3]*(x - 100)/100*(x - 100)/100))',
        'ExpPoly2':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100))',
        'ExpPoly2':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100))',
        'Exponential':'[0]*exp(x*[1])',
        'Power Law':'[0]*TMath::Power((x*1),[1])',
        }.get(function)

    f_bkg = ROOT.TF1(function,expr,mll_range[0],mll_range[1])
    f_bkg.SetTitle('Bkg (%s)'%function)

    translation = {
        'c1':'muons_incl_2015-18',
        'c2':'resolved_incl_2015-18',
        'c3':'merged_incl_2015-18',
        'c4':'muons_vbf_2015-18',
        'c5':'resolved_vbf_2015-18',
        'c6':'merged_vbf_2015-18',
        'c7':'muons_highptt_2015-18',
        'c8':'resolved_highptt_2015-18',
        'c9':'merged_highptt_2015-18',
        }

    parameters = dict()
    for i in bkg_parameters.readlines() :
        i = i.replace('\n','')
        if not i or i[0] == '#' :
            continue
        key = i.split()[0]
        for t in translation.keys() :
            key = key.replace(translation[t],t)
        parameters[key] = float(i.split()[2])

    cstr = 'c%d'%(category)
    if function in ['ExpPoly3','ExpPoly2'] :
        par = parameters['a1_%s'%(cstr)]
        f_bkg.SetParameter(1,par)
    if function in ['ExpPoly3','ExpPoly2'] :
        par = parameters['a2_%s'%(cstr)]
        f_bkg.SetParameter(2,par)
    if function in ['ExpPoly3'] :
        par = parameters['a3_%s'%(cstr)]
        f_bkg.SetParameter(3,par)
    if function in ['Power Law'] :
        par = parameters['lambda_%s'%(cstr)]
        f_bkg.SetParameter(1,par)
    if function in ['Exponential'] :
        par = parameters['slope_%s'%(cstr)]
        f_bkg.SetParameter(1,par)

    f_bkg.SetParameter(0,1)
    integral = f_bkg.Integral(mll_range[0],mll_range[1])
    f_bkg.SetParameter(0,parameters['nbkg_%s'%(cstr)]/float(integral))
    f_bkg.SetLineColor(ROOT.kBlue)
    f_bkg.SetLineWidth(2)
    plotfunc.AddHistogram(can,f_bkg,'l')

    # Pull!
    for i in range(ratioplot.GetNbinsX()+2) :
        bc1 = hist.GetBinContent(i)
        bc2 = f_bkg.Eval(hist.GetBinCenter(i)) #ref_hist.GetBinContent(i)
        be1 = hist    .GetBinErrorLow(i) if (bc1 > bc2) else hist    .GetBinErrorUp(i)
        be2 = 0 # ref_hist.GetBinErrorLow(i) if (bc2 > bc1) else ref_hist.GetBinErrorUp(i)

        if (be1**2 + be2**2) :
            ratioplot.SetBinContent(i,(bc1-bc2)/math.sqrt(be1**2+be2**2))
        ratioplot.SetBinError(i,1)

        if 120 < hist.GetBinCenter(i) and hist.GetBinCenter(i) < 130 :
            ratioplot.SetBinContent(i,-99)

    plotfunc.AddHistogram(can.GetPrimitive('pad_bot'),ratioplot,drawopt='pE1')

    #
    # Add signal and Hyy:
    print 'Expecting to open a file resonance_paramList.txt'
    f_paramList = open('resonance_paramList.txt')

    for i in f_paramList.readlines() :
        i = i.replace('\n','')
        parameters[i.split()[0]] = float(i.split()[1])

    if doAddSignal :
        f_sig = ROOT.TF1('H#rightarrow#gamma*#gamma parameterization',ROOT.dscb,80,180,7)

        # The numbering of resonance_paramList is offset by 1.
        c = category - 1
        f_sig.SetParameter(1,parameters['sigmaCBNom_SM_m125000_c%d'%(c)])
        f_sig.SetParameter(2,parameters['alphaCBLo_SM_m125000_c%d'%(c)])
        f_sig.SetParameter(3,parameters['alphaCBHi_SM_m125000_c%d'%(c)])
        f_sig.SetParameter(4,parameters['nCBLo_SM_c%d'%(c)])
        f_sig.SetParameter(5,parameters['nCBHi_SM_c%d'%(c)])
        f_sig.SetParameter(6,parameters['muCBNom_SM_m125000_c%d'%(c)])

        # Normalize correctly
        f_sig.SetParameter(0,1)
        integral = f_sig.Integral(80,180)
        integral_sig = parameters['sigYield_SM_m125000_c%d'%(c)]
        f_sig.SetParameter(0,integral_sig*hist.GetBinWidth(1)/float(integral)) # bin width!!

        h_hyy = None
        nhyy = parameters.get('hyy_%s'%(cstr),0)
        if nhyy :
            h_hyy = ROOT.TH1F('h_hyy','Bkg^{ }+^{ }H#rightarrow#gamma#gamma',40,120,130)
            sig_int = f_sig.Integral(105,160)
            for i in range(h_hyy.GetNbinsX()) :
                bcenter = h_hyy.GetBinCenter(i+1)
                bcontent = f_sig.Eval(bcenter)*nhyy/float(sig_int) + f_bkg.Eval(bcenter)
                h_hyy.SetBinContent(i+1,bcontent)

            h_hyy.SetLineColor(ROOT.kGreen+1)
            h_hyy.SetLineStyle(7)
            h_hyy.SetLineWidth(2)
            plotfunc.AddHistogram(can,h_hyy,'l')

        integral_hyy = 1
        h_sig = ROOT.TH1F('h_sig','Sig^{ }+^{ }Bkg',40,120,130)
        if nhyy :
            h_sig.SetTitle('Sig^{ }+^{ }Bkg^{ }+^{ }H#rightarrow#gamma#gamma')
        for i in range(h_sig.GetNbinsX()) :
            bcenter = h_sig.GetBinCenter(i+1)
            h_sig.SetBinContent(i+1,f_sig.Eval(bcenter) + f_bkg.Eval(bcenter))
        h_sig.SetLineColor(ROOT.kRed)
        plotfunc.AddHistogram(can,h_sig,'l')

    ranges = plotfunc.AutoFixYaxis(plotfunc.GetTopPad(can))
    plotfunc.SetYaxisRanges(plotfunc.GetTopPad(can),0.001,ranges[1])

    # Set ratio range; add dotted line at 1
    if plotfunc.GetBotPad(can) :
        taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(can),-3.999,3.999)
        xmin,xmax = None,None
        for i in plotfunc.GetBotPad(can).GetListOfPrimitives() :
            if issubclass(type(i),ROOT.TH1) :
                xmin = i.GetXaxis().GetBinLowEdge(1)
                xmax = i.GetXaxis().GetBinLowEdge(i.GetNbinsX()+1)
        if xmin != None :
            line = ROOT.TLine(xmin,0,xmax,0)
            line.SetLineStyle(2)
            plotfunc.GetBotPad(can).cd()
            line.Draw()
            plotfunc.tobject_collector.append(line)

    plotfunc.MakeLegend(can,0.60,0.65,0.92,0.90,totalentries=4)

    # put these back on top:
    plotfunc.AddHistogram(can,f_bkg,'l')
    if doAddSignal and h_hyy :
        plotfunc.AddHistogram(can,h_hyy,'l')
    plotfunc.AddHistogram(can,hist)
    plotfunc.FormatCanvasAxes(can)

    return
