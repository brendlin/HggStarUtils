
##
# Input: Data, fullsim ysy MC
# Output: Histograms for BackgroundReweighting.py
# Usage: something like
# plottrees.py 1 1 $tag $region --batch --config plottrees_FakesControlRegions.py --pull --outdir c01 ...
##

import HggStarHelpers
from HggStarHelpers import ChannelEnum,CategoryEnum,YEAR,REGION
import StudyConfSnippets
import sys

from HggStarHelpers import StandardSampleMerging as mergesamples
from HggStarHelpers import StandardPlotLabels as labels
from HggStarHelpers import StandardHistFormat as histformat
from HggStarHelpers import StandardHistRebin as rebin

treename = 'CollectionTree'

###
# Change this to check out different channels / years:
###
channel = int(sys.argv[1])
category = int(sys.argv[2])
doExtraCuts = True
if doExtraCuts :
    tag = sys.argv[3]
region = {'lepton_id':REGION.CR_LEPTON_INVERTID,
          'photon_id':REGION.CR_PHOTON_INVERTIDORISO,
          }.get(sys.argv[4])
higgsSF = 1
theyear = YEAR.y2015161718
doMesonCuts = True
##
# End configuration.
##

histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [55,105,160,'m_{ll#gamma} [GeV]']
if category in [4,5,6] :
    histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [33,105,160,histformat['HGamEventInfoAuxDyn.m_lly/1000.'][3]] 

fb = HggStarHelpers.GetFbForMCNormalization(theyear)

leptonObj = {ChannelEnum.DIMUON: 'Muons',
             ChannelEnum.RESOLVED_DIELECTRON:'Electrons',
             ChannelEnum.MERGED_DIELECTRON:  'Electrons',
             }.get(channel,None)

plottext = HggStarHelpers.GetPlotText(channel,category)
if region == REGION.SR_VBF :
    plottext[0].replace('channel','VBF category')

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'
## IMPORTANT NOTE: If 2015-only or 2016-only, we use RandomRunNumbers to put this
## into action for mc16a. This is because RandomRunNumbers is how triggers are turned on/of in mc16a.
## (See other important note in HggStarHelpers.GetFbForMCNormalization)
weight = HggStarHelpers.AddRandomRunNumberToWeightInCaseOf2015or2016(weight,theyear)

def weightscale(tfile) :
    return HggStarHelpers.weightscale_hyystar_yearAware(tfile,theyear,higgsSF)

blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]

if region in REGION.INVERTED_IDS :
    blindcut = []

cuts = [
    # This is assumed to be applied:
    'HGamEventInfoAuxDyn.isPassedObjPreselection',
    ]

if channel :
    cuts.append('HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel))

if category :
    if category in [4,5,6] :
        cuts.append('HGamEventInfoAuxDyn.m_jj/1000. > 400')
        cuts.append('HGamEventInfoAuxDyn.Deta_j_j > 2.5')

    else :
        cuts.append('HGamEventInfoAuxDyn.yyStarCategory == %d'%(category))

StudyConfSnippets.appendByHandSRCuts(cuts,channel)
if doExtraCuts :
    StudyConfSnippets.appendExtraCutByTag(cuts,tag)

if region == REGION.SR :
    StudyConfSnippets.appendPassLeadingLeptonID(cuts,channel)
    StudyConfSnippets.appendPassLeadingLeptonIso(cuts,channel)
    StudyConfSnippets.appendPassSubleadLeptonID(cuts,channel)
    StudyConfSnippets.appendPassSubleadLeptonIso(cuts,channel)
    StudyConfSnippets.appendPassPhotonID(cuts)
    StudyConfSnippets.appendPassPhotonIso(cuts)

elif region == REGION.CR_PHOTON_INVERTIDORISO :
    StudyConfSnippets.appendPassLeadingLeptonID(cuts,channel)
    StudyConfSnippets.appendPassLeadingLeptonIso(cuts,channel)
    StudyConfSnippets.appendPassSubleadLeptonID(cuts,channel)
    StudyConfSnippets.appendPassSubleadLeptonIso(cuts,channel)
    StudyConfSnippets.appendFailPhotonIDorIso(cuts)

elif region == REGION.CR_LEPTON_INVERTID :
    StudyConfSnippets.appendPassLeadingLeptonID(cuts,channel) # automatically skips Merged
    StudyConfSnippets.appendPassLeadingLeptonIso(cuts,channel) # automatically skips Merged
    StudyConfSnippets.appendFailSubleadLeptonID(cuts,channel) # Merged leading applied here
    StudyConfSnippets.appendPassPhotonID(cuts)
    StudyConfSnippets.appendPassPhotonIso(cuts)

else :
    print 'Do not understand region %s. Exiting.'%(region)
    sys.exit()

variables = [
    'HGamEventInfoAuxDyn.m_lly/1000.',
#     'HGamElectronsAuxDyn.topoetcone20[1]/HGamElectronsAuxDyn.pt[1]',
    'HGam%sAuxDyn.pt[1]/1000.'%(leptonObj),
    ]

def customnormalize(var,sig_hists=None,bkg_hists=None,data_hist=None) :

    if not bkg_hists or not data_hist :
        return

    if var != 'HGamEventInfoAuxDyn.m_lly/1000.' :
        return

    print 'Assuming that --bkgs is what you want to subtract (irreducible, from FullSim).'
    print 'Now I am going to subtract that from data, and save the result.'

    new_hist = data_hist.Clone()
    new_hist.SetName(new_hist.GetName()+'_irrBgkSubtracted')
    new_hist.SetTitle(new_hist.GetTitle()+' (irr bkg subtracted)')

    new_hist.Add(bkg_hists[0],-1)

    import ROOT
    rname = HggStarHelpers.GetRegionName(region)
    f = ROOT.TFile('%s_c%d.root'%(rname,category),'RECREATE')
    new_hist.Write('DataCR_%s_c%d'%(rname,category))
    f.Close()

    return
