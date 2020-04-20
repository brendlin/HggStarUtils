
# Command that works with ysy001 ntuples:
# plottrees.py --config plottrees_ZmumuyValidationConf.py --bkgs %Sherpa_CT10%mumugamma%r9364%.root --data ysy001.data16.%.root,ysy001.data15.p3083_p3402.root --fb 36.2 --log --signal %gamstargam%r9364%.root

from HggStarHelpers import YEAR,GetFbForMCNormalization
from HggStarHelpers import ChannelEnum,CategoryEnum
import StudyConfSnippets

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
channel = ChannelEnum.MERGED_DIELECTRON
category = None
region = REGION.SR
higgsSF = 10
theyear = YEAR.y2015161718
doMesonCuts = True
doDetailedVariables = False
##
# End configuration.
##

fb = GetFbForMCNormalization(theyear)

leptonObj = {ChannelEnum.DIMUON: 'Muons',
             ChannelEnum.RESOLVED_DIELECTRON:'Electrons',
             ChannelEnum.MERGED_DIELECTRON:  'Electrons',
             }.get(channel,None)

from HggStarHelpers import GetPlotText
plottext = GetPlotText(channel,category)
if region == REGION.SR_VBF :
    plottext = plottext.replace('channel','VBF category')

from HggStarHelpers import StandardSampleMerging as mergesamples

if region == REGION.SR_VBF :
    mergesamples = {
    'Sherpa_eegamma':'%Sherpa_CT10_eegamma%',
    'Sherpa_mmgamma':'%Sherpa_CT10_mumugamma%',
    'VBF H'         :'%345834%',
    'VH'            :['%345963%','%345964%','%345965%'],
    'ggF'           :['%345961%',],
    }

from HggStarHelpers import StandardPlotLabels as labels
labels['AllHiggs'] = 'H#rightarrow#gamma*#gamma%s'%('^{ }#times^{ }%d'%(higgsSF) if higgsSF != 1 else '')
if region == REGION.SR :
    labels['data'] = 'Data'

cuts = [
    'HGamEventInfoAuxDyn.isPassedObjSelection', # object selection
    ]

if channel :
    cuts.append('HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel))

if category :
    cuts.append('HGamEventInfoAuxDyn.yyStarCategory == %d'%(category))

if region in [REGION.CR1, REGION.CR2, REGION.SR, REGION.SR_VBF] :
    cuts += [
        '(HGamEventInfoAuxDyn.m_lly > 105000 && HGamEventInfoAuxDyn.m_lly < 160000)',
        'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.3', # new cuts
        'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.3', # new cuts
        ]

if region == REGION.CR1 :
    cuts += [
        'HGamEventInfoAuxDyn.m_ll/1000. < 83.', # FSR only
        'HGamEventInfoAuxDyn.m_ll/1000. > 45.', # Our control region
        ]

if region == REGION.CR2 :
    cuts += [
        'HGamEventInfoAuxDyn.m_ll/1000. < 45.', # our SR cut
        'HGamEventInfoAuxDyn.m_ll/1000. > 10.', # lly generator cut
        'HGamEventInfoAuxDyn.m_lly/1000. > 80.', # Closer to our SR
        ]

if region == REGION.SR or region == REGION.SR_VBF :
    cuts.append('HGamEventInfoAuxDyn.isPassedEventSelection') # our SR cut

# apply meson cuts by hand
if doMesonCuts :
    StudyConfSnippets.appendMesonCuts(cuts,channel)

blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]

##
## Standard Variables
##
variables = [
    'HGamEventInfoAuxDyn.pTt_lly/1000.',
    'HGamEventInfoAuxDyn.m_lly/1000.',
    'HGamEventInfoAuxDyn.m_ll/1000.',
    'HGamPhotonsAuxDyn.pt[0]/1000.',
    'HGam%sAuxDyn.pt[0]/1000.'%(leptonObj),
    ]

variables_detailed = []

if channel != ChannelEnum.MERGED_DIELECTRON :
    variables.append( 'HGam%sAuxDyn.pt[1]/1000.'%(leptonObj) )

if channel != ChannelEnum.DIMUON :
    variables_detailed.append( 'fabs(HGamGSFTrackParticlesAuxDyn.z0[0]-HGamGSFTrackParticlesAuxDyn.z0[1])' )
    variables_detailed.append( 'HGamEventInfoAuxDyn.deltaR_track4mom' )

if region == REGION.SR :
    variables_detailed.append( 'HGamEventInfoAuxDyn.pt_lly/1000.' )
    variables_detailed.append( 'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly' )

    if channel != ChannelEnum.MERGED_DIELECTRON :
        variables_detailed.append( 'HGamEventInfoAuxDyn.deltaR_ll' )
        variables_detailed.append( 'HGamEventInfoAuxDyn.pt_ll/1000.' )
        variables_detailed.append( 'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly' )

    if channel == ChannelEnum.MERGED_DIELECTRON :
        variables_detailed.append( 'HGamElectronsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly' )
        variables_detailed.append( 'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.' )
        variables_detailed.append( 'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.' )

if (region == REGION.SR_VBF) or (category >= 4) :
    variables_detailed.append('HGamEventInfoAuxDyn.Deta_j_j'      )
    variables_detailed.append('HGamEventInfoAuxDyn.Dphi_lly_jj'   )
    variables_detailed.append('fabs(HGamEventInfoAuxDyn.Zepp_lly)')
    variables_detailed.append('HGamEventInfoAuxDyn.m_jj/1000.'    )
    variables_detailed.append('HGamEventInfoAuxDyn.pTt_lly/1000.' )
    variables_detailed.append('HGamEventInfoAuxDyn.pT_llyjj/1000.')
    variables_detailed.append('HGamEventInfoAuxDyn.DRmin_y_leps_2jets')
    variables_detailed.append('HGamEventInfoAuxDyn.DRmin_y_ystar_2jets')
    variables_detailed.append('HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000.')
    variables_detailed.append('HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000.')
    variables_detailed.append('HGamAntiKt4EMPFlowJetsAuxDyn.eta[0]')
    variables_detailed.append('HGamAntiKt4EMPFlowJetsAuxDyn.eta[1]')

if doDetailedVariables :
    variables += variables_detailed

from HggStarHelpers import StandardHistFormat as histformat
histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [100,0,200,'m_{ll#gamma} [GeV]']
from HggStarHelpers import StandardHistRebin as rebin

if region == REGION.SR :
    histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [55,105,160,'m_{ll#gamma} [GeV]']
    histformat['HGamEventInfoAuxDyn.m_ll/1000.']  = [100,0,13,'m_{ll} [GeV]']

if region == REGION.OBJ_CR :
    histformat['HGamEventInfoAuxDyn.m_ll/1000.']  = [150,0,13,'m_{ll} [GeV]']

if channel == ChannelEnum.MERGED_DIELECTRON :
    histformat['HGamElectronsAuxDyn.pt[0]/1000.'] = [100,0,200,'p^{e1+e2}_{T} (calorimeter) [GeV]']
    histformat['HGamElectronsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly'] = [100,0,1,'p^{e1+e2}_{T}/m_{ll#gamma}']

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'
## IMPORTANT NOTE: If 2015-only or 2016-only, we use RandomRunNumbers to put this
## into action for mc16a. This is because RandomRunNumbers is how triggers are turned on/of in mc16a.
## (See other important note in HggStarHelpers.GetFbForMCNormalization)
if theyear == YEAR.y2015 :
    weight += '*(EventInfoAuxDyn.RandomRunNumber < 290000)'
if theyear == YEAR.y2016 :
    weight += '*(EventInfoAuxDyn.RandomRunNumber > 290000)'

from HggStarHelpers import weightscale_hyystar,SherpaKfactor1p3,SF_80fb,SF_139fb,SF_signalxN

def weightscale(tfile) :
    weight = weightscale_hyystar(tfile)

    if theyear == YEAR.y20151617 :
        weight = weight* SF_80fb(tfile)

    if theyear == YEAR.y2015161718 :
        weight = weight* SF_139fb(tfile)

    return weight * SF_signalxN(tfile,higgsSF)

def afterburner(can) :
    import PlotFunctions as plotfunc
    import TAxisFunctions as taxisfunc
    import ROOT

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

    # Set ratio range; add dotted line at 1
    if plotfunc.GetBotPad(can) :
        taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(can),0,2)
        xmin,xmax = None,None
        for i in plotfunc.GetBotPad(can).GetListOfPrimitives() :
            if issubclass(type(i),ROOT.TH1) :
                xmin = i.GetXaxis().GetBinLowEdge(1)
                xmax = i.GetXaxis().GetBinLowEdge(i.GetNbinsX()+1)
        if xmin != None :
            line = ROOT.TLine(xmin,1,xmax,1)
            line.SetLineStyle(2)
            plotfunc.GetBotPad(can).cd()
            line.Draw()
            plotfunc.tobject_collector.append(line)

    return
