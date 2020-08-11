
#
# Usage: cutcomparisonsGenAndReco.py 2 0 --config CompareGenAndRecoConf.py --normalize --showflows --ratio
#

treename = 'CollectionTree'

from HggStarHelpers import StandardHistFormat as histformat
from HggStarHelpers import StandardHistRebin as rebin
from HggStarHelpers import StandardSampleMerging as mergesamples
import StudyConfSnippets
from HggStarHelpers import ChannelEnum as ChannelEnum
from HggStarHelpers import CategoryEnum as CategoryEnum
from HggStarHelpers import YEAR,GetFbForMCNormalization
from HggStarHelpers import weightscale_hyystar,SherpaKfactor1p3,SF_80fb,SF_139fb,SF_signalxN
from HggStarHelpers import GetPlotText

histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [55,105,160,'m_{ll#gamma} [GeV]']

def frange(low,high,increment) :
    return list(a*increment for a in range(int(low/increment),int(high/increment)))

def weightscale(tfile) :

    if 'Sherpa_228_LO' in tfile.GetName() :
        print tfile,'will be scaled to the Sherpa reco sample...'
        return 1
    
    weight = weightscale_hyystar(tfile)

    if theyear == YEAR.y20151617 :
        weight = weight* SF_80fb(tfile)

    if theyear == YEAR.y2015161718 :
        weight = weight* SF_139fb(tfile)

    return weight


labels ={
    '%Sh_228_mmy%':'Reco-level #mu#mu#gamma',
    '%Sh_228_eey%':'Reco-level ee#gamma',
    '%Sherpa_228_LO_mumu_10M%':'Generator-level #mu#mu#gamma',
    '%Sherpa_228_LO_ee_10M%':'Generator-level ee#gamma',
    '%data%':'Data SB',
    }

nrng = 0
rng = 0.4

histformat['HGamEventInfoAuxDyn.deltaPhi_naiveExtrap'] = [100, -rng, rng,'naive extrap. #Delta#phi^{calo}_{tracks}']

histformat['HGamEventInfoAuxDyn.m_ll/1000.'] = [30,0,30,'m_{ll} [GeV]']

histformat['HGamMuonsAuxDyn.pt[0]/1000.'] = [300,0,150,histformat['HGamMuonsAuxDyn.pt[0]/1000.'][3]]
rebin['HGamMuonsAuxDyn.pt[0]/1000.'] = frange(0,40,2) + list(range(40,80,2)) + list(range(80,100,5)) + list(range(100,150,10))

histformat['HGamMuonsAuxDyn.pt[1]/1000.'] = [120,0,60,histformat['HGamMuonsAuxDyn.pt[1]/1000.'][3]]
rebin['HGamMuonsAuxDyn.pt[1]/1000.'] = frange(0,10,0.5) + list(range(10,40)) + list(range(40,62,2))

histformat['HGamElectronsAuxDyn.pt[0]/1000.'] = [300,0,150,histformat['HGamElectronsAuxDyn.pt[0]/1000.'][3]]
rebin['HGamElectronsAuxDyn.pt[0]/1000.'] = frange(0,40,2) + list(range(40,80,2)) + list(range(80,100,5)) + list(range(100,150,10))

histformat['HGamElectronsAuxDyn.pt[1]/1000.'] = [120,0,60,histformat['HGamElectronsAuxDyn.pt[1]/1000.'][3]]
rebin['HGamElectronsAuxDyn.pt[1]/1000.'] = frange(0,10,0.5) + list(range(10,40)) + list(range(40,60,4))

histformat['HGamGSFTrackParticlesAuxDyn.pt[0]/1000.'] = [300,0,150,histformat['HGamGSFTrackParticlesAuxDyn.pt[0]/1000.'][3]]
rebin['HGamGSFTrackParticlesAuxDyn.pt[0]/1000.'] = frange(0,40,2) + list(range(40,80,2)) + list(range(80,100,5)) + list(range(100,150,10))

histformat['HGamGSFTrackParticlesAuxDyn.pt[1]/1000.'] = [120,0,60,histformat['HGamGSFTrackParticlesAuxDyn.pt[1]/1000.'][3]]
rebin['HGamGSFTrackParticlesAuxDyn.pt[1]/1000.'] = frange(0,10,1) + list(range(10,40)) + list(range(40,60,2))

histformat['HGamPhotonsAuxDyn.pt[0]/1000.'] = [300,0,150,histformat['HGamPhotonsAuxDyn.pt[0]/1000.'][3]]
rebin['HGamPhotonsAuxDyn.pt[0]/1000.'] = frange(0,40,2) + list(range(40,80,2)) + list(range(80,100,5)) + list(range(100,150,10))

histformat['HGamEventInfoAuxDyn.pt_ll/1000.'] = [300,0,150,histformat['HGamEventInfoAuxDyn.pt_ll/1000.'][3]]
rebin['HGamEventInfoAuxDyn.pt_ll/1000.'] = frange(0,40,2) + list(range(40,80,2)) + list(range(80,100,5)) + list(range(100,150,10))

histformat['HGamEventInfoAuxDyn.pt_lly/1000.'] = [300,0,150,histformat['HGamEventInfoAuxDyn.pt_lly/1000.'][3]]
rebin['HGamEventInfoAuxDyn.pt_lly/1000.'] = frange(0,40,2) + list(range(40,60,2)) + list(range(60,100,5)) + list(range(100,150,10))

print histformat['HGamPhotonsAuxDyn.pt[0]/1000.']
# print histformat['HGamMuonsAuxDyn.pt[1]/1000.']
# print rebin['HGamMuonsAuxDyn.pt[1]/1000.']
# import sys; sys.exit()

###
# Change this to check out different channels / years:
###
import sys
channel = int(sys.argv[1])
category = int(sys.argv[2])
theyear = YEAR.y2015161718
ptthrust_cut = 100
useSmeared = True
onlyFar = False
onlyNear = False
doLowMll = False
doHighMll = False
##
# End configuration.
##

plottext = GetPlotText(channel,category)

if onlyFar :
    histformat['HGamGSFTrackParticlesAuxDyn.pt[0]/1000.'] = [300,0,150,histformat['HGamGSFTrackParticlesAuxDyn.pt[0]/1000.'][3]]
    rebin['HGamGSFTrackParticlesAuxDyn.pt[0]/1000.'] = frange(0,20,2) + list(range(20,80,2)) + list(range(80,100,5)) + list(range(100,150,10))

    histformat['HGamGSFTrackParticlesAuxDyn.pt[1]/1000.'] = [200,0,20,histformat['HGamGSFTrackParticlesAuxDyn.pt[1]/1000.'][3]]
    rebin['HGamGSFTrackParticlesAuxDyn.pt[1]/1000.'] = frange(0,10,0.2) + list(range(10,21))

fb = GetFbForMCNormalization(theyear)

reco = 'mc16%.700001.Sh_228_ysyLO_ee.p4114.ysy015_pico.root'
gen   = 'Sherpa_228_LO_ee_10M_v7p4.root'
if channel == 1 :
    reco = 'mc16%.700002.Sh_228_ysyLO_mumu.p4114.ysy015_pico.root'
    gen  = 'Sherpa_228_LO_mumu_10M_v7p4.root'

if channel != 1 :
    histformat['HGamEventInfoAuxDyn.m_ll/1000.'] = [120,0,30,'m_{ll} [GeV]']
    rebin['HGamEventInfoAuxDyn.m_ll/1000.'] = frange(0,10,0.25) + frange(10,30,1)

recoweight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'
genweight = 'HGamEventInfoAuxDyn.weight'

if useSmeared :
    gen = gen.replace('.root','_smeared.root')
    genweight = 'HGamEventInfoAuxDyn.weight*weight_lep1Eff*weight_lep0Eff*weight_photonEff*weight_mll'
    #genweight = 'HGamEventInfoAuxDyn.weight'
    if channel == 2 :
        genweight = 'HGamEventInfoAuxDyn.weight*weight_mll*weight_lep0Eff*weight_photonEff'
        #genweight = 'HGamEventInfoAuxDyn.weight'
    if channel == 3 :
        genweight = 'HGamEventInfoAuxDyn.weight*weight_lep0Eff_mer*weight_photonEff_mer'
        #genweight = 'HGamEventInfoAuxDyn.weight'

variables = [
    'HGamPhotonsAuxDyn.pt[0]/1000.',
    'HGamMuonsAuxDyn.pt[0]/1000.',
    'HGamMuonsAuxDyn.pt[1]/1000.',
    'HGamElectronsAuxDyn.pt[0]/1000.',
    'HGamElectronsAuxDyn.pt[1]/1000.',
    'HGamEventInfoAuxDyn.m_ll/1000.',
    'HGamEventInfoAuxDyn.m_lly/1000.',
    'HGamEventInfoAuxDyn.pt_lly/1000.',
    'HGamEventInfoAuxDyn.pt_ll/1000.',
    'HGamEventInfoAuxDyn.deltaPhi_naiveExtrap',
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.',
    'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.',
    ]

variablemap = {
    'HGamPhotonsAuxDyn.pt[0]/1000.':'HGamPhotonsAuxDyn.pt0/1000.',
    'HGamMuonsAuxDyn.pt[0]/1000.'  :'HGamMuonsAuxDyn.pt0/1000.',
    'HGamMuonsAuxDyn.pt[1]/1000.'  :'HGamMuonsAuxDyn.pt1/1000.',
    'HGamElectronsAuxDyn.pt[0]/1000.'  :'HGamElectronsAuxDyn.pt0/1000.',
    'HGamElectronsAuxDyn.pt[1]/1000.'  :'HGamElectronsAuxDyn.pt1/1000.',
    'HGamEventInfoAuxDyn.deltaPhi_naiveExtrap':'-HGamEventInfoAuxDyn.deltaPhiMagnet_ll',
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.':'HGamGSFTrackParticlesAuxDyn.pt0/1000.',
    'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.':'HGamGSFTrackParticlesAuxDyn.pt1/1000.',
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.':'HGamElectronsAuxDyn.pt0/1000.',
    'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.':'HGamElectronsAuxDyn.pt1/1000.',
    }

print variables

if channel != 1 :
    for var in range(len(variables)-1,-1,-1) :
        if 'Muon' in variables[var] :
            variables.pop(variables.index(variables[var]))
else :
    for var in range(len(variables)-1,-1,-1) :
        if 'Electron' in variables[var] :
            variables.pop(variables.index(variables[var]))
        if 'GSFTrack' in variables[var] :
            variables.pop(variables.index(variables[var]))

if channel != 2 :
    var = 'HGamElectronsAuxDyn.pt[1]/1000.'
    if var in variables :
        variables.pop(variables.index(var))
    # This is not calibrated correctly !!! Use pt_ll for the converted photon calibration!
    var = 'HGamElectronsAuxDyn.pt[0]/1000.'
    if var in variables :
        variables.pop(variables.index(var))

if channel == 3 :
    histformat['HGamEventInfoAuxDyn.pt_ll/1000.'][3] = 'Merged electron p_{T} [GeV]'

recocuts = [
    '105000 < HGamEventInfoAuxDyn.m_lly && HGamEventInfoAuxDyn.m_lly < 160000',
    'HGamEventInfoAuxDyn.isPassedEventSelection',
    'HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel),
    ]

if category :
    recocuts.append('HGamEventInfoAuxDyn.yyStarCategory == %d'%(category))

gencuts = [
    'HGamEventInfoAuxDyn.m_ll < 30000',
    ]

common = []
if doLowMll :
    common.append('HGamEventInfoAuxDyn.m_ll < 3000')
if doHighMll :
    common.append('HGamEventInfoAuxDyn.m_ll > 3000')

for c in common :
    gencuts.append(c)
    recocuts.append(c)

if onlyFar :
    recocuts.append('HGamEventInfoAuxDyn.deltaPhi_naiveExtrap < -0.05')

if onlyNear :
    recocuts.append('HGamEventInfoAuxDyn.deltaPhi_naiveExtrap > -0.05')

StudyConfSnippets.appendTruthCategoryCuts(gencuts,category)
StudyConfSnippets.appendTruthElectronDeltaCuts_v1(gencuts,channel,
                                                  mergedDeltaPhiCut=0.05,
                                                  mergedFarDeltaPhiMin=0.05,
                                                  onlyFar=onlyFar,
                                                  onlyNear=onlyNear,
                                                  )
StudyConfSnippets.appendTriggerThresholds2018(gencuts,channel)
StudyConfSnippets.appendTruthLeptonAndPtllCuts(gencuts,channel)

for v in variablemap.keys() :
    histformat[variablemap[v]] = histformat[v]
for v in variablemap.keys() :
    if v in rebin.keys() :
        rebin[variablemap[v]] = rebin[v]

def afterburner(can) :
    import PyAnalysisPlotting as anaplot
    import PlotFunctions as plotfunc
    import ROOT

    print can.GetName()

    anaplot.RatioRangeAfterBurner(can)

    if 'HGamEventInfoAuxDyn_m_lly_over_1000' in can.GetName() :
        anaplot.RatioRangeAfterBurner(can,ymin=0.5,ymax=1.5)

    xmin,xmax = 0,0

    if 'HGamPhotonsAuxDyn_pt_0_over_1000' in can.GetName() :
        xmin,xmax = 30,140
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol4',xmin,xmax)
    elif 'HGamMuonsAuxDyn_pt_0_over_1000' in can.GetName() :
        xmin,xmax = 16,120
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol5',xmin,xmax)
    elif 'HGamMuonsAuxDyn_pt_1_over_1000' in can.GetName() :
        xmin,xmax = 3,8
#         f = ROOT.TF1('func_%s'%(can.GetName()),'[0] - [1]*TMath::Exp(-[2]*(x-[3]))',xmin,xmax)
#         f.SetParameter(0,1.1)
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol3',xmin,xmax)
    elif 'HGamEventInfoAuxDyn_m_ll_over_1000' in can.GetName() :
        xmin,xmax = 0,30
        if channel == 2 :
            xmin,xmax = 0,8
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol4',xmin,xmax)
    elif 'HGamEventInfoAuxDyn_m_lly_over_1000' in can.GetName() :
        xmin,xmax = 105,160
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol1',xmin,xmax)
    elif 'HGamEventInfoAuxDyn_pt_lly_over_1000' in can.GetName() :
        xmin,xmax = 0,150
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol4',xmin,xmax)
    elif 'HGamElectronsAuxDyn_pt_1_over_1000' in can.GetName() :
        xmin,xmax = 4.5,25
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol7',xmin,xmax)
    elif 'HGamElectronsAuxDyn_pt_0_over_1000' in can.GetName() :
        xmin,xmax = 24,70
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol6',xmin,xmax)
    elif 'HGamGSFTrackParticlesAuxDyn_pt_1_over_1000' in can.GetName() :
        xmin,xmax = 0,20
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol7',xmin,xmax)
    elif 'HGamEventInfoAuxDyn_pt_ll_over_1000' in can.GetName() :
        xmin,xmax = 32,140
        f = ROOT.TF1('func_%s'%(can.GetName()),'pol4',xmin,xmax)

    else :
        return

    hist = None
    for i in list(plotfunc.GetBotPad(can).GetListOfPrimitives()) :
        if issubclass(type(i),ROOT.TH1) :
            hist = i
            
    if not hist :
        return

    f.SetLineColor(ROOT.kBlue)
    hist.SetMarkerColor(ROOT.kGray+2)
    hist.SetLineColor(ROOT.kGray+2)
    hist.Fit(f,"","goff",xmin,xmax)

    can.GetPrimitive('pad_bot').cd()
    leg = ROOT.TLegend(0.18,0.74,0.34,0.86)
    leg.AddEntry(f,'^{ }'+f.GetTitle(),'l') # plef
    plotfunc.tobject_collector.append(leg)
    leg.SetTextFont(43)
    leg.SetTextSize(18)
    leg.SetTextFont(43)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.Draw()

    return
