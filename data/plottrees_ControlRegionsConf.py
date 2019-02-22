
# Command that works with ysy001 ntuples:
# plottrees.py --config plottrees_ZmumuyValidationConf.py --bkgs %Sherpa_CT10%mumugamma%r9364%.root --data ysy001.data16.%.root,ysy001.data15.p3083_p3402.root --fb 36.2 --log --signal %gamstargam%r9364%.root

treename = 'CollectionTree'

class ChannelEnum :
    CHANNELUNKNOWN=0
    DIMUON=1
    RESOLVED_DIELECTRON=2
    MERGED_DIELECTRON=3

class REGION :
    CR1 = 0
    CR2 = 1
    SR = 2

###
# Change this to check out different channels:
###
channel = ChannelEnum.MERGED_DIELECTRON
region = REGION.SR
higgsSF = 10

leptonObj = 'Muons' if channel == ChannelEnum.DIMUON else 'Electrons'
plottext = {ChannelEnum.DIMUON             : ['Dimuon channel'],
            ChannelEnum.RESOLVED_DIELECTRON: ['Resolved e channel'],
            ChannelEnum.MERGED_DIELECTRON  : ['Merged e channel']
            }.get(channel,[])

mergesamples = {
    # Now possible via regular expressions (use % instead of .*)
    'Sherpa_eegamma':'%Sherpa_CT10_eegamma%',
    'Sherpa_mmgamma':'%Sherpa_CT10_mumugamma%',
    'AllHiggs':'%gamstargam%',
    }

labels = {
    # Now possible via regular expressions (use % instead of .*)
    # 'Sherpa_eegamma':'Sherpa ee#gamma',
    # 'Sherpa_mmgamma':'Sherpa #mu#mu#gamma',
    '%Sherpa_CT10_eegammaPt10_35%'   :'p_{T}^{#gamma}#in[10,35]',
    '%Sherpa_CT10_eegammaPt35_70%'   :'p_{T}^{#gamma}#in[35,70]',
    '%Sherpa_CT10_eegammaPt70_140%'  :'p_{T}^{#gamma}#in[70,140]',
    '%Sherpa_CT10_eegammaPt140%'     :'p_{T}^{#gamma}>140 GeV',
    '%Sherpa_CT10_mumugammaPt10_35%' :'p_{T}^{#gamma}#in[10,35]',
    '%Sherpa_CT10_mumugammaPt35_70%' :'p_{T}^{#gamma}#in[35,70]',
    '%Sherpa_CT10_mumugammaPt70_140%':'p_{T}^{#gamma}#in[70,140]',
    '%Sherpa_CT10_mumugammaPt140%'   :'p_{T}^{#gamma}>140 GeV',
    'Sherpa_eegamma'                 :'ee#gamma',
    'Sherpa_mmgamma'                 :'#mu#mu#gamma',
    '%345961%'                       :'ggH H#rightarrow#gamma*#gamma',
    '%345962%'                       :'VBF H#rightarrow#gamma*#gamma',
    '%345963%'                       :'WmH H#rightarrow#gamma*#gamma',
    '%345964%'                       :'WpH H#rightarrow#gamma*#gamma',
    '%345965%'                       :'ZH H#rightarrow#gamma*#gamma',
    'AllHiggs'                       :'H#rightarrow#gamma*#gamma%s'%('^{ }#times^{ }%d'%(higgsSF) if higgsSF != 1 else ''),
    }

if region == REGION.SR :
    labels['data'] = 'Data'


cuts = [
    'HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel),
    'HGamEventInfoAuxDyn.isPassedObjSelection == 1', # object selection
    ]


if channel != ChannelEnum.MERGED_DIELECTRON :
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

if region == REGION.SR :
    cuts += [
        'HGamEventInfoAuxDyn.isPassedEventSelection', # our SR cut
        ]


blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]

variables = [
    'HGamEventInfoAuxDyn.m_ll/1000.',
    'HGamEventInfoAuxDyn.m_lly/1000.',
    'HGamPhotonsAuxDyn.pt[0]/1000.',
    'HGam%sAuxDyn.pt[0]/1000.'%(leptonObj),
    ]

if channel != ChannelEnum.MERGED_DIELECTRON :
    variables.append( 'HGam%sAuxDyn.pt[1]/1000.'%(leptonObj) )

if channel != ChannelEnum.DIMUON :
    variables.append( 'fabs(HGamGSFTrackParticlesAuxDyn.z0[0]-HGamGSFTrackParticlesAuxDyn.z0[1])' )

if region == REGION.SR :
    variables.append( 'HGamEventInfoAuxDyn.pt_lly/1000.' )
    variables.append( 'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly' )

    if channel != ChannelEnum.MERGED_DIELECTRON :
        variables.append( 'HGamEventInfoAuxDyn.deltaR_ll' )
        variables.append( 'HGamEventInfoAuxDyn.pt_ll/1000.' )
        variables.append( 'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly' )
        variables.append( 'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.' )
        variables.append( 'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.' )

    if channel == ChannelEnum.MERGED_DIELECTRON :
        variables.append( 'HGamElectronsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly' )

histformat = {
    'HGamEventInfoAuxDyn.m_ll/1000.':[100,0,120,'m_{ll} [GeV]'],
    'HGamEventInfoAuxDyn.m_lly/1000.':[100,0,200,'m_{ll#gamma} [GeV]'],
    'HGamEventInfoAuxDyn.pt_lly/1000.':[100,0,200,'p_{Tll#gamma} [GeV]'],
    'HGamPhotonsAuxDyn.pt[0]/1000.':[100,0,200,'p^{#gamma}_{T} [GeV]'],
    'HGamMuonsAuxDyn.pt[0]/1000.'  :[100,0,200,'p^{#mu1}_{T} [GeV]'],
    'HGamMuonsAuxDyn.pt[1]/1000.'  :[100,0,60,'p^{#mu2}_{T} [GeV]'],
    'HGamElectronsAuxDyn.pt[0]/1000.'  :[100,0,200,'p^{e1}_{T} [GeV]'],
    'HGamElectronsAuxDyn.pt[1]/1000.'  :[100,0,60,'p^{e2}_{T} [GeV]'],
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly':[100,0,1,'p^{#gamma}_{T}/m_{ll#gamma}'],
    'HGamEventInfoAuxDyn.deltaR_ll':[100,0,2,'#Delta^{}R_{ll}'],
    'fabs(HGamGSFTrackParticlesAuxDyn.z0[0]-HGamGSFTrackParticlesAuxDyn.z0[1])':[100,0,3,'|#Delta^{}Z_{0}| [mm]'],
    'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly':[100,0,1,'p^{ll}_{T}/m_{ll#gamma}'],
    'HGamEventInfoAuxDyn.pt_ll/1000.':[100,0,200,'p^{ll}_{T} [GeV]'],
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.':[100,0,100,'p^{trk0}_{T} [GeV]'],
    'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.':[100,0,30,'p^{trk1}_{T} [GeV]'],
    }

if region == REGION.SR :
    histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [55,105,160,'m_{ll#gamma} [GeV]']
    histformat['HGamEventInfoAuxDyn.m_ll/1000.']  = [100,0,13,'m_{ll} [GeV]']

if channel == ChannelEnum.MERGED_DIELECTRON :
    histformat['HGamElectronsAuxDyn.pt[0]/1000.'] = [100,0,200,'p^{e1+e2}_{T} (calorimeter) [GeV]']
    histformat['HGamElectronsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly'] = [100,0,1,'p^{e1+e2}_{T}/m_{ll#gamma}']

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

from HggStarHelpers import weightscale_hyystar,SherpaKfactor1p3,SF_80fb

def SF_signalxN(tfile) :
    higgs = ['345961','345962','345963','345964','345965']
    checkHiggs = list(a in tfile.GetName() for a in higgs)
    if True in checkHiggs :
        print '%s (Higgs) will be scaled by a factor of 100'%(tfile.GetName())
        return higgsSF

    return 1

def weightscale(tfile) :
    weight = weightscale_hyystar(tfile)
    return weight * SF_signalxN(tfile) * SherpaKfactor1p3(tfile) * SF_80fb(tfile)
