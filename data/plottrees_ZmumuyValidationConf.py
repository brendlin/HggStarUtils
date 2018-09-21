
# Command that works with ysy001 ntuples:
# plottrees.py --config plottrees_ZmumuyValidationConf.py --bkgs %Sherpa_CT10%mumugamma%r9364%.root --data ysy001.data16.%.root,ysy001.data15.p3083_p3402.root --fb 36.2 --log --signal %gamstargam%r9364%.root

treename = 'CollectionTree'

mergesamples = {
    # Now possible via regular expressions (use % instead of .*)
    # 'Sherpa_eegamma':'%Sherpa_CT10_eegamma%',
    # 'Sherpa_mmgamma':'%Sherpa_CT10_mumugamma%',
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
    '%345961%'                       :'ggH H#rightarrow#gamma*#gamma',
    }

cuts = [
    'HGamEventInfoAuxDyn.yyStarChannel == 1', # 1 = dimuon
    'HGamEventInfoAuxDyn.cutFlow > 18' # >19 = ZMASSCUT, so 18 is right before that (a good validation point)
    ]

variables = [
    'HGamEventInfoAuxDyn.m_ll/1000.',
    'HGamPhotonsAuxDyn.pt[0]/1000.',
    ]

histformat = {
    'HGamEventInfoAuxDyn.m_ll/1000.':[100,0,120,'m_{ll} [GeV]'],
    'HGamPhotonsAuxDyn.pt[0]/1000.':[100,0,200,'p^{#gamma}_{T} [GeV]'],
    }

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

import HggStarHelpers
weightscale = HggStarHelpers.weightscale_hyystar
