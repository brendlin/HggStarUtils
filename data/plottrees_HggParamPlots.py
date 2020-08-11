
# Usage: plottrees.py 2 2 --config plottrees_HggParamPlots.py --data mc16%346214%.root,mc16%343981%.root --ratio --batch --outdir HyyParameterizationCheck_c02

import HggStarHelpers
from HggStarHelpers import YEAR,ChannelEnum,CategoryEnum
import StudyConfSnippets
from HggStarHelpers import StandardSampleMerging as mergesamples
from HggStarHelpers import StandardHistFormat as histformat

import ROOT
ROOT.gROOT.LoadMacro('dscb.C')

treename = 'CollectionTree'

###
# Change this to check out different channels / years:
###
import sys
channel = int(sys.argv[1])
category = int(sys.argv[2])
theyear = YEAR.y2015161718
##
# End configuration.
##

histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [40,115,135,'m_{ll#gamma} [GeV]']

if category in [5,6,8] :
    histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [20,115,135,'m_{ll#gamma} [GeV]']

fb = HggStarHelpers.GetFbForMCNormalization(theyear)

from HggStarHelpers import GetPlotText
plottext = GetPlotText(channel,category)

from HggStarHelpers import StandardPlotLabels as labels

cuts = [
    'HGamEventInfoAuxDyn.isPassedObjSelection', # object selection
    'HGamEventInfoAuxDyn.isPassedEventSelection', # object selection
    ]

if channel :
    cuts.append('HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel))

if category :
    cuts.append('HGamEventInfoAuxDyn.yyStarCategory == %d'%(category))

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'
## IMPORTANT NOTE: If 2015-only or 2016-only, we use RandomRunNumbers to put this
## into action for mc16a. This is because RandomRunNumbers is how triggers are turned on/of in mc16a
## (See other important note in HggStarHelpers.GetFbForMCNormalization)
weight = HggStarHelpers.AddRandomRunNumberToWeightInCaseOf2015or2016(weight,theyear)

def weightscale(tfile) :
    return HggStarHelpers.weightscale_hyystar_yearAware(tfile,theyear)

##
## Standard Variables
##
variables = [
    'HGamEventInfoAuxDyn.m_lly/1000.',
    ]

def afterburner(can) :
    import PlotFunctions as plotfunc
    import TAxisFunctions as taxisfunc
    import PyAnalysisPlotting as anaplot
    import ROOT
    import math

    HggStarHelpers.FixFbLabelOnPlotFor2015or2016(can,theyear)

    f_paramList = open('resonance_paramList.txt')
    parameters = dict()

    for i in f_paramList.readlines() :
        i = i.replace('\n','')
        parameters[i.split()[0]] = float(i.split()[1])

    f_sig = ROOT.TF1('H#rightarrow#gamma*#gamma parameterization',ROOT.dscb,105,160,7)

    # The numbering of resonance_paramList is offset by 1.
    c = category - 1
    f_sig.SetParameter(1,parameters['sigmaCBNom_SM_m125000_c%d'%(c)])
    f_sig.SetParameter(2,parameters['alphaCBLo_SM_m125000_c%d'%(c)])
    f_sig.SetParameter(3,parameters['alphaCBHi_SM_m125000_c%d'%(c)])
    f_sig.SetParameter(4,parameters['nCBLo_SM_c%d'%(c)])
    f_sig.SetParameter(5,parameters['nCBHi_SM_c%d'%(c)])
    f_sig.SetParameter(6,parameters['muCBNom_SM_m125000_c%d'%(c)])
    
    # print list(a.GetName() for a in plotfunc.GetTopPad(can).GetListOfPrimitives())
    hist = plotfunc.GetTopPad(can).GetPrimitive('pad_top_HiggsToGammaGamma')
    ratioplot = hist.Clone()
    ratioplot.GetYaxis().SetTitle('pull')
    ratioplot.GetXaxis().SetTitle('m_{ll#gamma} [GeV]')

    f_sig.SetParameter(0,1)
    integral = f_sig.Integral(115,135)
    integral_hyy = hist.Integral(1,hist.GetNbinsX())
    f_sig.SetParameter(0,integral_hyy*hist.GetBinWidth(1)/float(integral)) # bin width!!
    plotfunc.AddHistogram(can,f_sig,'l')

    # Pull!
    for i in range(ratioplot.GetNbinsX()+2) :
        bc1 = hist.GetBinContent(i)
        bc2 = f_sig.Eval(hist.GetBinCenter(i)) #ref_hist.GetBinContent(i)
        be1 = hist    .GetBinErrorLow(i) if (bc1 > bc2) else hist    .GetBinErrorUp(i)
        be2 = 0 # ref_hist.GetBinErrorLow(i) if (bc2 > bc1) else ref_hist.GetBinErrorUp(i)

        if (be1**2 + be2**2) :
            ratioplot.SetBinContent(i,(bc1-bc2)/math.sqrt(be1**2+be2**2))
        ratioplot.SetBinError(i,1)

    plotfunc.AddHistogram(can.GetPrimitive('pad_bot'),ratioplot,drawopt='pE1')

    anaplot.RatioRangeAfterBurner(can,-4,4)
    plotfunc.MakeLegend(can,0.5,0.65,0.8,0.90,totalentries=4)
    plotfunc.AddHistogram(can,hist)
    plotfunc.FormatCanvasAxes(can)

    return
