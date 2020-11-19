
import ROOT
ROOT.gROOT.LoadMacro('dscb.C')

treename = 'CollectionTree'

from HggStarHelpers import StandardPlotLabels,StandardSampleMerging
mergesamples = StandardSampleMerging
labels = StandardPlotLabels

from HggStarHelpers import YEAR,GetFbForMCNormalization,ChannelEnum,CategoryEnum
theyear = YEAR.y2015161718
fb = GetFbForMCNormalization(theyear)

massOffset = 0.09

# These are the preselection cuts
cuts = [
    'HGamEventInfoAuxDyn.isPassedEventSelection',
    ]

cutcomparisons = {
    # '#mu#mu#gamma'      :['HGamEventInfoAuxDyn.yyStarChannel == %d'%(CHANNEL.DIMUON              )],
    # 'ee#gamma resolved' :['HGamEventInfoAuxDyn.yyStarChannel == %d'%(CHANNEL.RESOLVED_DIELECTRON )],
    # 'ee#gamma merged'   :['HGamEventInfoAuxDyn.yyStarChannel == %d'%(CHANNEL.MERGED_DIELECTRON   )],
    '#font[52]{ee} resolved low-p_{T#font[52]{t}}':['HGamEventInfoAuxDyn.yyStarCategory == %d'%(CategoryEnum.GGF_RESOLVED_DIELECTRON   )],
    '#font[52]{ee} merged high-p_{T#font[52]{t}}':['HGamEventInfoAuxDyn.yyStarCategory == %d'%(CategoryEnum.HIPTT_MERGED_DIELECTRON   )],
    }

variables = [
    '(HGamEventInfoAuxDyn.m_lly+%.0f)/1000.'%(massOffset*1000),
    ]

histformat = {
    '(HGamEventInfoAuxDyn.m_lly+%.0f)/1000.'%(massOffset*1000):[48,113,137,'m_{ll#gamma} [GeV]'],
    }

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

from HggStarHelpers import weightscale_hyystar,SherpaKfactor1p3,SF_80fb,SF_139fb,SF_signalxN

def weightscale(tfile) :
    weight = weightscale_hyystar(tfile)
    weight = weight* SF_139fb(tfile)
    return weight

def afterburner(can) :
    import PlotFunctions as plotfunc
    import TAxisFunctions as taxisfunc
    import ROOT

    line = ROOT.TLine(113,0,137,0)
    line.SetLineStyle(2)
    can.cd()
    line.Draw()
    plotfunc.tobject_collector.append(line)

    hists = []
    i = 0
    for p in can.GetListOfPrimitives() :
        if issubclass(type(p),ROOT.TH1) :
            p.SetTitle(p.GetTitle().replace('AllHiggs, ',''))
            if i == 0 :
                p.SetMarkerStyle(24)
                i += 1
            hists.append(p)

    parameters = dict()

    print 'Expecting to open a file resonance_paramList.txt'
    f_paramList = open('resonance_paramList.txt')

    for i in f_paramList.readlines() :
        i = i.replace('\n','')
        parameters[i.split()[0]] = float(i.split()[1])
    
    # The numbering of resonance_paramList is offset by 1.
    category = 2
    f_sig = ROOT.TF1('Model',ROOT.dscb,80,180,7)
    f_sig.SetNpx(500)
    f_sig.SetName('signal_function_1')
    f_sig.SetTitle('remove')
    f_sig.SetLineWidth(2)
    f_sig.SetLineColor(ROOT.kBlue)

    c = category - 1
    f_sig.SetParameter(1,parameters['sigmaCBNom_SM_m125000_c%d'%(c)])
    f_sig.SetParameter(2,parameters['alphaCBLo_SM_m125000_c%d'%(c)])
    f_sig.SetParameter(3,parameters['alphaCBHi_SM_m125000_c%d'%(c)])
    f_sig.SetParameter(4,parameters['nCBLo_SM_c%d'%(c)])
    f_sig.SetParameter(5,parameters['nCBHi_SM_c%d'%(c)])
    f_sig.SetParameter(6,massOffset+parameters['muCBNom_SM_m125000_c%d'%(c)])

    # Normalize correctly
    f_sig.SetParameter(0,1)
    integral = f_sig.Integral(113,137)
    integral_sig = 1 # parameters['sigYield_SM_m125000_c%d'%(c)]
    #f_sig.SetParameter(0,integral_sig*hists[0].GetBinWidth(1)/float(integral)) # bin width!!
    f_sig.SetParameter(0,hists[0].GetBinWidth(1)/float(integral)) # bin width!!
    plotfunc.AddHistogram(can,f_sig,drawopt='l')


    # The numbering of resonance_paramList is offset by 1.
    category = 9
    f_sig2 = ROOT.TF1('Model',ROOT.dscb,80,180,7)
    f_sig2.SetNpx(500)
    f_sig2.SetName('signal_function')
    f_sig2.SetTitle('remove')
    f_sig2.SetLineWidth(2)
    f_sig2.SetLineColor(ROOT.kRed)

    c = category - 1
    f_sig2.SetParameter(1,parameters['sigmaCBNom_SM_m125000_c%d'%(c)])
    f_sig2.SetParameter(2,parameters['alphaCBLo_SM_m125000_c%d'%(c)])
    f_sig2.SetParameter(3,parameters['alphaCBHi_SM_m125000_c%d'%(c)])
    f_sig2.SetParameter(4,parameters['nCBLo_SM_c%d'%(c)])
    f_sig2.SetParameter(5,parameters['nCBHi_SM_c%d'%(c)])
    f_sig2.SetParameter(6,massOffset+parameters['muCBNom_SM_m125000_c%d'%(c)])

    # Normalize correctly
    f_sig2.SetParameter(0,1)
    integral = f_sig2.Integral(113,137)
    integral_sig = 1 # parameters['sigYield_SM_m125000_c%d'%(c)]
    #f_sig2.SetParameter(0,integral_sig*hists[0].GetBinWidth(1)/float(integral)) # bin width!!
    f_sig2.SetParameter(0,hists[0].GetBinWidth(1)/float(integral)) # bin width!!
    plotfunc.AddHistogram(can,f_sig2,drawopt='l')

    plotfunc.MakeLegend(can,0.61,0.74,0.84,0.93,
                        totalentries=2,ncolumns=1,skip=['remove me'])
    entry = ROOT.TH1F('asdf','asdf',1,0,1)
    can.GetPrimitive('legend').AddEntry(entry,'^{ }Model','l')
    #entry = can.GetPrimitive('legend').GetEntry(can.GetName()+'_signal_function')
    #entry.SetObject(h_entry)
    can.GetPrimitive('legend').SetMargin(0.2) # or whatever

    can.GetPrimitive(can.GetName()+'_text').Delete()
    text_lines = [plotfunc.GetAtlasInternalText(status='Simulation Internal')]
    text_lines += [plotfunc.GetSqrtsText(13)]
    text_lines += ['H#rightarrow#gamma*#gamma, m_{H} =^{ }125.09 GeV']
    plotfunc.DrawText(can,text_lines,0.2,0.74,0.5,0.93,totalentries=3)

    #plotfunc.AutoFixYaxis(can,ignorelegend=True,ignoretext=True)
    plotfunc.SetYaxisRanges(can,-0.01,0.18)

    can.SetBottomMargin(0.12)
    for i in can.GetListOfPrimitives() :
        if hasattr(i,'GetXaxis') :
            i.GetXaxis().SetTitleOffset(1.05)
        if hasattr(i,'GetYaxis') :
            i.GetYaxis().SetTitleOffset(1.40)


    plotfunc.SetAxisLabels(can,'m_{ll#gamma} [GeV]','Fraction of Events / 0.5 GeV')
    can.RedrawAxis()
    can.Modified()
    can.Update()

