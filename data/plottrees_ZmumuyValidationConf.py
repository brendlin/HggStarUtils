
# Command that works with ysy001 ntuples:
# plottrees.py --config plottrees_ZmumuyValidationConf.py --bkgs %Sherpa_CT10%mumugamma%r9364%.root --data ysy001.data16.%.root,ysy001.data15.p3083_p3402.root --fb 36.2 --log --signal %gamstargam%r9364%.root

treename = 'CollectionTree'

class ChannelEnum :
    CHANNELUNKNOWN=0
    DIMUON=1
    RESOLVED_DIELECTRON=2
    MERGED_DIELECTRON=3

###
# Change this to check out different channels:
###
channel = ChannelEnum.MERGED_DIELECTRON


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
    'AllHiggs'                       :' H#rightarrow#gamma*#gamma',
    }

cuts = [
    'HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel),
    'HGamEventInfoAuxDyn.isPassedObjSelection == 1', # object selection
    ]
if channel != ChannelEnum.MERGED_DIELECTRON :
    cuts += [
        'HGamEventInfoAuxDyn.m_ll/1000. < 83.', # FSR only
        'HGamEventInfoAuxDyn.m_ll/1000. > 45.', # Our control region
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
    variables += [
        'HGam%sAuxDyn.pt[1]/1000.'%(leptonObj),
        ]

histformat = {
    'HGamEventInfoAuxDyn.m_ll/1000.':[100,0,120,'m_{ll} [GeV]'],
    'HGamEventInfoAuxDyn.m_lly/1000.':[100,0,200,'m_{ll#gamma} [GeV]'],
    'HGamPhotonsAuxDyn.pt[0]/1000.':[100,0,200,'p^{#gamma}_{T} [GeV]'],
    'HGamMuonsAuxDyn.pt[0]/1000.'  :[100,0,200,'p^{#mu1}_{T} [GeV]'],
    'HGamMuonsAuxDyn.pt[1]/1000.'  :[100,0,60,'p^{#mu2}_{T} [GeV]'],
    'HGamElectronsAuxDyn.pt[0]/1000.'  :[100,0,200,'p^{e1}_{T} [GeV]'],
    'HGamElectronsAuxDyn.pt[1]/1000.'  :[100,0,60,'p^{e2}_{T} [GeV]'],
    }

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

import HggStarHelpers
def weightscale_SherpaKfactor(tfile) :

    weight = HggStarHelpers.weightscale_hyystar(tfile)

    fix_xs = 1.

    Sherpa_NLO = ['301535','301536','301899','301900','301901','301902','301903','301904']
    checkSherpa = list(a in tfile.GetName() for a in Sherpa_NLO)
    if True in checkSherpa :
        print '%s (Sherpa) will be scaled by a factor of 1.3'%(tfile.GetName())
        fix_xs = 1.3

    return weight * fix_xs

weightscale = weightscale_SherpaKfactor
