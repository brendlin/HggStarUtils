#!/usr/bin/env python

import ROOT
import PlotFunctions as plotfunc
import TAxisFunctions as taxisfunc
import PyAnalysisPlotting as anaplot
import os 

categories = [
    #None,
    'GGF_DIMUON',              # 1
    'GGF_RESOLVED_DIELECTRON', # 2
    'GGF_MERGED_DIELECTRON',   # 3
    'VBF_DIMUON',              # 4
    'VBF_RESOLVED_DIELECTRON', # 5
    'VBF_MERGED_DIELECTRON',   # 6
    'HIPTT_DIMUON',              # 7
    'HIPTT_RESOLVED_DIELECTRON', # 8
    'HIPTT_MERGED_DIELECTRON',   # 9
    ]

CategoryNames_ysy = {
    'GGF_DIMUON'             :'Inclusive Dimuon',
    'GGF_RESOLVED_DIELECTRON':'Inclusive Resolved Electron',
    'GGF_MERGED_DIELECTRON'  :'Inclusive Merged Electron',
    'VBF_DIMUON'             :'VBF Dimuon',
    'VBF_RESOLVED_DIELECTRON':'VBF Resolved Electron',
    'VBF_MERGED_DIELECTRON'  :'VBF Merged Electron',
    'HIPTT_DIMUON'             :'High-pTThrust Dimuon',
    'HIPTT_RESOLVED_DIELECTRON':'High-pTThrust Resolved Electron',
    'HIPTT_MERGED_DIELECTRON'  :'High-pTThrust Merged Electron',
    }

xp = '((x-132.5)/(160-105))'
functions_ysy = {
    'GGF_DIMUON'               :{'yj':'[p0] + [p1]*(x-132.5)/(160-105)','llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    #'GGF_RESOLVED_DIELECTRON'  :{'yj':'[p0] + [p1]*%s + [p2]*%s*%s + [p3]*%s*%s*%s'%(xp,xp,xp,xp,xp,xp),'llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    'GGF_RESOLVED_DIELECTRON'  :{'yj':'[p0] + [p1]*TMath::Exp(-[p2]*%s)'%(xp),'llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    'GGF_MERGED_DIELECTRON'    :{'yj':'[p0] + [p1]*(x-132.5)/(160-105) + [p2]*(x-132.5)*(x-132.5)/((160-105)*(160-105))','llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    'VBF_DIMUON'               :{'yj':'[p0] + [p1]*(x-132.5)/(160-105)','llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    'VBF_RESOLVED_DIELECTRON'  :{'yj':'[p0] + [p1]*(x-132.5)/(160-105)','llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    'VBF_MERGED_DIELECTRON'    :{'yj':'[p0] + [p1]*(x-132.5)/(160-105)','llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    'HIPTT_DIMUON'             :{'yj':'[p0] + [p1]*(x-132.5)/(160-105)','llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    'HIPTT_RESOLVED_DIELECTRON':{'yj':'[p0] + [p1]*(x-132.5)/(160-105)','llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
    'HIPTT_MERGED_DIELECTRON'  :{'yj':'[p0] + [p1]*(x-132.5)/(160-105)','llj':'[p0] + [p1]*(x-132.5)/(160-105)'},
}

##################################################################################
def GetMaxBinError(hist,binmin,binmax) :
    the_max = 0
    #print 'nbinsx:',hist.GetNbinsX()
    for i in range(hist.GetNbinsX()) :
        if hist.GetBinCenter(i+1) < binmin :
            continue
        if hist.GetBinCenter(i+1) > binmax :
            continue
        if hist.GetBinContent(i+1) == 0 :
            the_max = 2
            continue
        err = hist.GetBinError(i+1)/hist.GetBinContent(i+1)
        if err > the_max :
            the_max = err
    return the_max

    # rebin until your smallest error is uh small

##################################################################################
def FindRebinFactors(hist) :
    # find factors
    factors = []
    for bin in range(hist.GetNbinsX()) :
        if bin < 2 :
            continue
        if hist.GetNbinsX() / float(bin) == hist.GetNbinsX() / bin :
            factors.append(bin)
    # print 'Possible rebin factors:',factors
    return factors

##################################################################################
def RebinUntilSmallErrors(hist1,hist2,binmin,binmax,errormax=0.3,do_rebin=True) :

    factors = FindRebinFactors(hist1)

    for fac in factors :
        blah = hist1.Clone()
        blah.SetName('blah')
        blah.Rebin(fac)

        blah2 = 0
        if hist2 :
            blah2 = hist2.Clone()
            blah2.SetName('blah2')
            blah2.Rebin(fac)

        if GetMaxBinError(blah,binmin,binmax) > errormax :
            continue
        if blah2 and GetMaxBinError(blah2,binmin,binmax) > errormax :
            continue
        # print 'picked',fac
        if do_rebin :
            if hist2 :
                hist2.Rebin(fac)
            hist1.Rebin(fac)
            # print 'rebinned'
        break
    # print 'fac',fac
    return fac

########################################################

offset = 1

style = plotfunc.SetupStyle()
style.SetErrorX(0.5)

def integral(hist,f,l) :
    return hist.Integral(hist.FindBin(f+0.000001),hist.FindBin(l-0.000001))


def DoRescaleProcedure(gen,bkg,name,ci,c) :
    cans = []
    if integral(gen,105,160) == 0 :
        return [],0,1,1
    if integral(bkg,105,160) == 0 :
        return [],0,1,1

    # Print the "before" picture
    cans.append(plotfunc.RatioCanvas('UntouchedRatio_%02d_%s_%s'%(ci,c,name),'%d_%s_%s'%(ci,c,name),600,500))
    gen_rebin = plotfunc.AddHistogram(cans[-1],gen)
    bkg_rebin = bkg.Clone()
    bkg_rebin.SetName(bkg_rebin.GetName()+'_forRebinning')
    
    if bkg_rebin.Integral() < 200 :
        RebinUntilSmallErrors(gen_rebin,bkg_rebin,binmin=105,binmax=160,errormax=1)
    gen_rebin.Scale(integral(bkg_rebin,105,160)/integral(gen_rebin,105,160))
    
    unused,gen_bkg_ratio = plotfunc.AddRatio(cans[-1],bkg_rebin,gen_rebin)
    taxisfunc.AutoFixAxes(cans[-1])
    taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(cans[-1]),minzero=True)
    taxisfunc.SetXaxisRanges(cans[-1],105,160)
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(cans[-1]),0,3)
    plotfunc.SetAxisLabels(cans[-1],'m_{ll#gamma} [GeV]','entries','ratio')


    # Fit the ratio of the CR and the GEN with a line
    function = ROOT.TF1('%d_%s'%(ci,c),functions_ysy[c][name],105,160)
    function.SetLineColor(ROOT.kBlue)
    if (integral(bkg,105,160) >= 50) :
        gen_bkg_ratio.Fit('%d_%s'%(ci,c))
    else :
        print 'Not enough events to do a fit! Setting parameters to 1,0.'
        function.SetParameters(1,0)

    gen_integral = integral(gen,105,160)

    gen_before = gen.Clone()
    gen_before.SetTitle(gen_before.GetName()+'_before')
    gen_before.SetTitle('GEN unweighted')

    gen_result = gen.Clone()
    gen_result.SetLineColor(ROOT.kRed+1)
    gen_result.SetMarkerSize(1)
    gen_result.SetLineWidth(2)
    gen_result.SetTitle(gen_result.GetName()+'_rescaled')

    # Multiply the GEN by the function
    function.SetRange(gen.GetBinLowEdge(1),gen.GetBinLowEdge(gen.GetNbinsX()+1))
    gen_result.Multiply(function)
    gen_result.SetTitle('GEN reweighted')

    # The multiplication above changes the integral, so you
    # have to calculate an "integral factor" to correct for this.
    integral_factor = gen_integral / float(integral(gen_result,105,160))

    #Tools.RebinUntilSmallErrors(gen_result,bkg,binmin=105,binmax=160,errormax=1)
    #gen_before.Rebin(10)
    gen_before.SetMarkerColor(ROOT.kGray)
    gen_before.SetFillColor(ROOT.kGray)
    gen_before.SetLineColor(ROOT.kGray)
    gen_before.SetLineWidth(2)
    #gen_result.Rebin(10)
    #bkg.Rebin(10)
    bkg.SetTitle(name.replace('y','#gamma^{}'))
    if integral(gen_result,105,160) :
        gen_before.Scale(integral(bkg,105,160)/integral(gen_before,105,160))
        gen_result.Scale(integral(bkg,105,160)/integral(gen_result,105,160))

    # Print the "after" (rescaled) result
    cans.append(plotfunc.RatioCanvas('rescaled_%02d_%s_%s'%(ci,c,name),'%d_%s_%s_rescaled'%(ci,c,name),600,500))
    plotfunc.AddHistogram(cans[-1],gen_before)
    plotfunc.AddHistogram(cans[-1],bkg)
    plotfunc.AddRatio(cans[-1],gen_result,bkg,divide='pull')
    plotfunc.MakeLegend(cans[-1],0.64,0.70,0.74,0.87,option=['f','pl','f'])
    taxisfunc.AutoFixAxes(cans[-1])
    taxisfunc.SetXaxisRanges(cans[-1],105,160)
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(cans[-1]),-4,4)
    plotfunc.SetAxisLabels(cans[-1],'m_{ll#gamma} [GeV]','entries','pull')

    pars = []
    for i in range(function.GetNpar()) :
        pars.append(function.GetParameter(i))
    return cans,pars,integral_factor


def main(options,args) :

    llj_file = ROOT.TFile(options.llj,'read')
    yj_file = ROOT.TFile(options.yj,'read')
    gen_file = ROOT.TFile(options.gen,'read')
    
    outfile = ROOT.TFile('out.root','RECREATE')

    cans = []
    for i_cat,c in enumerate(categories) :

        tmp = []

        gen = gen_file.Get('Template_c%d' %(i_cat+offset)).Clone()
        yj  = yj_file .Get('DataCR_yj_c%d'%(i_cat+offset))
        llj = llj_file.Get('DataCR_llj_c%d'%(i_cat+offset))

        gen.SetTitle('ll#gamma')

        print c, gen.Integral(), yj.Integral(), llj.Integral()
        #continue

        data_blinded = gen_file.Get('Sidebands_c%d'%(i_cat+offset))
        data_integral = integral(data_blinded,105,160)

        outfile.cd()
        data_blinded.Write()

        gen.Sumw2(); yj.Sumw2(); llj.Sumw2();

        # Get the parameters for the reweighting procedure
        yj_newcans,yj_pars,yj_integral_factor = DoRescaleProcedure(gen,yj,'yj',i_cat+offset,c)
        llj_newcans,llj_pars,llj_integral_factor = DoRescaleProcedure(gen,llj,'llj',i_cat+offset,c)
        tmp += yj_newcans
        tmp += llj_newcans

        # Get the fractions of lly, yj, llj
        fractions_file = open(options.fractions,'read')
        for l,line in enumerate(fractions_file) :
            if c not in line :
                continue
            print c,l,line
            yj_frac = float(line.split()[-1])
            llj_frac = float(line.split()[-2])
            lly_frac = 1-yj_frac-llj_frac
        fractions_file.close()
        print lly_frac,yj_frac,llj_frac

        # The full reweighting function
        norm_parameters = [lly_frac,yj_frac,yj_integral_factor,llj_frac,llj_integral_factor]
        yj_expr = functions_ysy[c]['yj']
        llj_expr = functions_ysy[c]['llj']
        par_num = 5
        for ii in range(len(yj_pars)) :
            yj_expr = yj_expr.replace('[p%d]'%(ii),'[%d]'%(par_num))
            par_num += 1
        for ii in range(len(llj_pars)) :
            llj_expr = llj_expr.replace('[p%d]'%(ii),'[%d]'%(par_num))
            par_num += 1

        expr = '[0] + [1]*[2]*(%s) + [3]*[4]*(%s)'%(yj_expr,llj_expr)
        print expr

        function = ROOT.TF1('%d_%s'%(i_cat+offset,c),expr,105,160)
        for ii,par in enumerate(norm_parameters + yj_pars + llj_pars) :
            function.SetParameter(ii,par)

        data_integral = float(integral(data_blinded,105,120) + integral(data_blinded,130,160) )
        gen_integral = float(integral(gen,105,120)+integral(gen,130,160) )

        if gen_integral == 0 :
            print 'ERROR! GEN Integral for category %s is 0!'%(c)
            return

        rebin = 1


        # lly for stack
        gen_lly_stack = gen.Clone(); gen_lly_stack.SetName(gen_lly_stack.GetName()+'_lly_forStack')
        gen_lly_stack.Rebin(rebin)

        # yj for stack
        gen_yj_stack = gen.Clone(); gen_yj_stack.SetName(gen_yj_stack.GetName()+'_yj_forStack')
        gen_yj_stack.SetTitle('#gamma^{}#font[12]{j}')
        yj_expr = functions_ysy[c]['yj']
        par_num = 2
        for ii in range(len(yj_pars)) :
            yj_expr = yj_expr.replace('[p%d]'%(ii),'[%d]'%(par_num))
            par_num += 1
        function_yj = ROOT.TF1('%d_%s'%(i_cat+offset,c),'[0]*[1]*(%s)'%(yj_expr),105,160)
        print yj_expr
        function_yj.SetParameter(0,yj_frac)
        function_yj.SetParameter(1,yj_integral_factor)
        for ii,par in enumerate(yj_pars) :
            function_yj.SetParameter(ii+2,par)
        function_yj.SetRange(gen.GetBinLowEdge(1),gen.GetBinLowEdge(gen.GetNbinsX()+1))
        gen_yj_stack.Multiply(function_yj)
        gen_yj_stack.Rebin(rebin)

        # llj for stack
        gen_llj_stack = gen.Clone(); gen_llj_stack.SetName(gen_llj_stack.GetName()+'_llj_forStack')
        gen_llj_stack.SetTitle('#font[12]{llj}')
        llj_expr = functions_ysy[c]['llj']
        par_num = 2
        for ii in range(len(llj_pars)) :
            llj_expr = llj_expr.replace('[p%d]'%(ii),'[%d]'%(par_num))
            par_num += 1
        function_llj = ROOT.TF1('%d_%s'%(i_cat+offset,c),'[0]*[1]*(%s)'%(llj_expr),105,160)
        print llj_expr
        function_llj.SetParameter(0,llj_frac)
        function_llj.SetParameter(1,llj_integral_factor)
        for ii,par in enumerate(llj_pars) :
            function_llj.SetParameter(ii+2,par)
        function_llj.SetRange(gen.GetBinLowEdge(1),gen.GetBinLowEdge(gen.GetNbinsX()+1))
        gen_llj_stack.Multiply(function_llj)
        gen_llj_stack.Rebin(rebin)
        anaplot.PrepareBkgHistosForStack([gen_llj_stack,gen_yj_stack,gen_lly_stack],'')

        gen_integral_postRW = float(integral(gen,105,120)+integral(gen,130,160))

        # full thing.
        function.SetRange(gen.GetBinLowEdge(1),gen.GetBinLowEdge(gen.GetNbinsX()+1))
        gen.Multiply(function)

        # scale everything
        gen_lly_stack.Scale( lly_frac * data_integral / gen_integral_postRW )
        gen_yj_stack.Scale( data_integral / gen_integral_postRW )
        gen_llj_stack.Scale( data_integral / gen_integral_postRW )
        gen.Scale( data_integral / gen_integral_postRW )

        main_can = plotfunc.RatioCanvas('Mimic_Plot_%02d_%s'%(i_cat+offset,c),'Mimic plot',600,500)
        plotfunc.AddHistogram(main_can,gen_llj_stack)
        plotfunc.AddHistogram(main_can,gen_yj_stack)
        plotfunc.AddHistogram(main_can,gen_lly_stack)
        plotfunc.Stack(main_can)

        outfile.cd()
        gen.Write()

        # Print the final plots, below.

        #print Tools.FindRebinFactors(gen)
        gen.Rebin(rebin)
        data_blinded.Rebin(rebin)
        data_blinded.SetTitle('Data')
        data_blinded.SetBinErrorOption(ROOT.TH1.kPoisson)
        gen.SetMarkerSize(0); gen.SetLineColor(1); gen.SetLineWidth(2); gen.SetFillColor(1)
        gen.SetFillStyle(3254);
        gen.SetTitle('SM')
        plotfunc.AddHistogram(main_can,gen,drawopt='E2')
        taxisfunc.AutoFixAxes(main_can)
        p_chi2 = None

        if False :
            # RATIO
            plotfunc.AddRatio(main_can,data_blinded,gen)
            plotfunc.SetAxisLabels(main_can,'m_{ll#gamma} [GeV]','entries','ratio')
            anaplot.RatioRangeAfterBurner(main_can)
        else :
            # PULL
            unused,pull = plotfunc.AddRatio(main_can,data_blinded,gen,divide='pull')
            plotfunc.SetAxisLabels(main_can,'m_{ll#gamma} [GeV]','entries','pull')
            nbins = 0
            chi2 = 0

            # Get the chi-square
            for i in range(pull.GetNbinsX()) :
                bc = pull.GetBinCenter(i+1)
                if 120 < bc and bc < 130 :
                    pull.SetBinContent(i+1,-99)
                    continue
                chi2 += pull.GetBinContent(i+1)*pull.GetBinContent(i+1)
                nbins += 1
            anaplot.RatioRangeAfterBurner(main_can)
            p_chi2 = ROOT.TMath.Prob(chi2, nbins - 1)

        the_text = [plotfunc.GetAtlasInternalText(),
                    plotfunc.GetSqrtsText(13)+', '+plotfunc.GetLuminosityText(139.0),
                    CategoryNames_ysy[c]
                    ]
        if p_chi2 != None :
            the_text.append('p(#chi^{2}) = %.2f%%'%(p_chi2*100))
        plotfunc.DrawText(main_can,the_text,.2,0.62,.61,.90,totalentries=4)
        plotfunc.MakeLegend(main_can,0.70,0.67,0.92,0.90,ncolumns=2,option=['f','f','f','f','p'])
        taxisfunc.SetXaxisRanges(main_can,105,160)
        taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(main_can),forcemin=0.0001)
        tmp.append(main_can)

        for can in tmp :
            plotfunc.FormatCanvasAxes(can)

        anaplot.UpdateCanvases(tmp)
        os.system('mkdir -p c%02d_%s'%(i_cat,c))
        for can in tmp :
            can.Print('c%02d_%s/%s.pdf'%(i_cat,c,can.GetName()))
            can.Print('c%02d_%s/%s.eps'%(i_cat,c,can.GetName()))

        cans += yj_newcans
        cans += llj_newcans


        if options.nobatch :
            raw_input('pause')

    return


if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    p.add_option('--nobatch',action='store_true',default=False,dest='nobatch',help='run in batch mode')
    p.add_option('--gen',type='string',default='',dest='gen',help='generator-level file')
    p.add_option('--yj',type='string',default='',dest='yj',help='yj file')
    p.add_option('--llj',type='string',default='',dest='llj',help='llj file')
    p.add_option('--fractions',type='string',default='Fractions.txt',dest='fractions',help='Text file containing the fractions of lly, ljy, llj')

    options,args = p.parse_args()

    if not options.gen or not options.yj or not options.llj or not options.fractions :
        print 'Error - please specify --gen --yj and --llj files, as well as a text file containing the fractions.'
        fractions_ex = '''
Inclusive Dimuon             0.08 0.040
Inclusive Resolved Electron  0.08 0.277
Inclusive Merged Electron    0.11 0.014
VBF Dimuon                   0.08 0.040
VBF Resolved Electron        0.08 0.277
VBF Merged Electron          0.11 0.014
High-\ptt Dimuon             0.06 0.147
High-\ptt Resolved Electron  0.08 0.491
High-\ptt Merged Electron    0.06 0.014
...
'''
        print 'Example fractions file:'
        print fractions_ex
        import sys; sys.exit()

    ROOT.gROOT.SetBatch(not options.nobatch)

    main(options,args)
