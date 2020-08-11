
import sys
from HggStarHelpers import StandardHistFormat as histformat
from HggStarHelpers import ChannelEnum as ChannelEnum
from HggStarHelpers import CategoryEnum as CategoryEnum
import StudyConfSnippets

###
# Change this to check out different channels / years:
# You have to run this 6 times, and then hadd. Yes, your life is so difficult. Make a bash function.
###
channel = int(sys.argv[1])
category = int(sys.argv[2])
doTruncateWeights = False
doExtraCuts = True
if doExtraCuts :
    tag = sys.argv[3]
##
# End configuration.
##

data = 'data%.root'
bkgs = 'Sherpa_228_LO_ee_10M_v7p4_smeared.root'
if channel == 1 :
    bkgs = 'Sherpa_228_LO_mumu_10M_v7p4_smeared.root'

treename = 'CollectionTree'
weight = 'HGamEventInfoAuxDyn.weight'

weight = {
    1:'HGamEventInfoAuxDyn.weight*weight_lep1Eff*weight_lep0Eff*weight_photonEff*weight_mll',
    2:'HGamEventInfoAuxDyn.weight*weight_mll*weight_lep0Eff*weight_photonEff',
    3:'HGamEventInfoAuxDyn.weight*weight_lep0Eff_mer*weight_photonEff_mer',
    }.get(channel)

if doTruncateWeights :
    weight = weight.replace('HGamEventInfoAuxDyn.weight','min(HGamEventInfoAuxDyn.weight,3)')

def weightscale(tfile) :
    return 1

variables = ['HGamEventInfoAuxDyn.m_lly/1000.']
# variables = [weight]

histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [660,105,160,histformat['HGamEventInfoAuxDyn.m_lly/1000.'][3]]
# Rebinning, just for the pdfs:
tmp_rebin = {
    1: 12,
    2: 12,
    3: 12,
    4: 12,
    5: 12,
    6: 12,
    7: 12,
    8: 12,
    9: 12,
    }.get(category)

# Applied only to data:
datacuts = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    'HGamEventInfoAuxDyn.isPassedObjSelection',
    'HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel),
    'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.3',
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.3',
    ]

if category :
    datacuts.append('HGamEventInfoAuxDyn.yyStarCategory == %d'%(category))

common = [
    'HGamEventInfoAuxDyn.m_ll < 50000',
    '(HGamEventInfoAuxDyn.m_lly > 105000 && HGamEventInfoAuxDyn.m_lly < 160000)',
    ]

if doExtraCuts :
    StudyConfSnippets.appendExtraCutByTag(common,tag)

StudyConfSnippets.appendMesonCuts(common,channel)

gencuts = [
    ]

for c in common :
    gencuts.append(c)
    datacuts.append(c)

StudyConfSnippets.appendTruthCategoryCuts(gencuts,category)
StudyConfSnippets.appendTruthElectronDeltaCuts_v1(gencuts,channel,
                                                  mergedDeltaPhiCut=0.05,
                                                  mergedFarDeltaPhiMin=0.05,
                                                  onlyFar=False,
                                                  onlyNear=False,
                                                  )
StudyConfSnippets.appendTriggerThresholds2018(gencuts,channel)
StudyConfSnippets.appendTruthLeptonAndPtllCuts(gencuts,channel)

labels ={
    '%ee%':'Sherpa LO ee#gamma',
    '%mumu%':'Sherpa LO #mu#mu#gamma',
    '%data%':'Data SB',
    }

def customnormalize(var,sig_hists=None,bkg_hists=None,data_hist=None) :
    from HggStarHelpers import customNormalizeToDataSidebands
    customNormalizeToDataSidebands(var,sig_hists,bkg_hists,data_hist)

    if not bkg_hists or not data_hist :
        return

    import ROOT
    f = ROOT.TFile('Template_c%d.root'%(category),'RECREATE')
    bkg_hists[0].Write('Template_c%d'%(category))
    data_hist.Write('Sidebands_c%d'%(category))
    f.Close()

    bkg_hists[0].Rebin(tmp_rebin)
    data_hist.Rebin(tmp_rebin)

    return

def afterburner(can) :
    import PyAnalysisPlotting as anaplot
    import PlotFunctions as plotfunc
    anaplot.RatioRangeAfterBurner(can)
    plotfunc.MakeLegend(can,0.53,0.75,0.92,0.90,totalentries=2,ncolumns=1,skip=['SM (stat)'])
    return

# How this gets put into plottrees
blindcut = datacuts
truthcuts = gencuts
