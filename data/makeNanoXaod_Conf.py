
treename = 'CollectionTree'

# Add some truth branches; turn off all cuts.
# (Usually your MxAOD runs should also have "SkimmingCut: -1" set)
doHiggsTruth = False

# Save trigger variables (TrigMatch variables may not exist anymore)
doTrigger = False

variables = [
    'HGamEventInfoAuxDyn.m_lly',
    'HGamEventInfoAuxDyn.pt_lly',
    'HGamEventInfoAuxDyn.yyStarChannel',
    'HGamEventInfoAuxDyn.isPassedObjSelection',
    'HGamEventInfoAuxDyn.isPassedEventSelection',
    'HGamEventInfoAuxDyn.m_ll',
    'HGamEventInfoAuxDyn.pt_ll',
    'HGamPhotonsAuxDyn.pt',
    'HGamMuonsAuxDyn.pt',
    'HGamElectronsAuxDyn.pt',
    'HGamEventInfoAuxDyn.deltaR_ll',
    'HGamEventInfoAuxDyn.Resolved_dRExtrapTrk12',
    'HGamElectronsAuxDyn.dRExtrapTrk12',
    'HGamEventInfoAuxDyn.crossSectionBRfilterEff',
    'HGamEventInfoAuxDyn.weight',
    'HGamGSFTrackParticlesAuxDyn.z0',
    'HGamGSFTrackParticlesAuxDyn.pt',
    ]

cuts = [
    'HGamEventInfoAuxDyn.isPassedObjSelection == 1',
    ]

if doTrigger :
    variables += [
        'EventInfoAuxDyn.RandomRunNumber',
        'EventInfoAuxDyn.passTrig_HLT_2e12_lhloose_L12EM10VH',
        'EventInfoAuxDyn.passTrig_HLT_2e17_lhvloose_nod0',
        'EventInfoAuxDyn.passTrig_HLT_2e24_lhvloose_nod0',
        'EventInfoAuxDyn.passTrig_HLT_2mu10',
        'EventInfoAuxDyn.passTrig_HLT_2mu14',
        'EventInfoAuxDyn.passTrig_HLT_e120_lhloose',
        'EventInfoAuxDyn.passTrig_HLT_e140_lhloose_nod0',
        'EventInfoAuxDyn.passTrig_HLT_e20_lhmedium_g35_loose',
        'EventInfoAuxDyn.passTrig_HLT_e20_lhmedium_nod0_g35_loose',
        'EventInfoAuxDyn.passTrig_HLT_e24_lhmedium_L1EM20VH',
        'EventInfoAuxDyn.passTrig_HLT_e25_mergedtight_g35_medium_Heg',
        'EventInfoAuxDyn.passTrig_HLT_e26_lhtight_nod0_ivarloose',
        'EventInfoAuxDyn.passTrig_HLT_e60_lhmedium',
        'EventInfoAuxDyn.passTrig_HLT_e60_lhmedium_nod0',
        'EventInfoAuxDyn.passTrig_HLT_g35_loose_L1EM24VHI_mu15_mu2noL1',
        'EventInfoAuxDyn.passTrig_HLT_g35_loose_L1EM24VHI_mu18',
        'EventInfoAuxDyn.passTrig_HLT_g35_loose_g25_loose',
        'EventInfoAuxDyn.passTrig_HLT_g35_medium_g25_medium_L12EM20VH',
        'EventInfoAuxDyn.passTrig_HLT_mu18_mu8noL1',
        'EventInfoAuxDyn.passTrig_HLT_mu20_iloose_L1MU15',
        'EventInfoAuxDyn.passTrig_HLT_mu22_mu8noL1',
        'EventInfoAuxDyn.passTrig_HLT_mu26_ivarmedium',
        'EventInfoAuxDyn.passTrig_HLT_mu40',
        'EventInfoAuxDyn.passTrig_HLT_mu50',
        'EventInfoAuxDyn.passTrigMatch_HLT_2e12_lhloose_L12EM10VH',
        'EventInfoAuxDyn.passTrigMatch_HLT_2e17_lhvloose_nod0',
        'EventInfoAuxDyn.passTrigMatch_HLT_2e24_lhvloose_nod0',
        'EventInfoAuxDyn.passTrigMatch_HLT_2mu10',
        'EventInfoAuxDyn.passTrigMatch_HLT_2mu14',
        'EventInfoAuxDyn.passTrigMatch_HLT_e120_lhloose',
        'EventInfoAuxDyn.passTrigMatch_HLT_e140_lhloose_nod0',
        'EventInfoAuxDyn.passTrigMatch_HLT_e20_lhmedium_g35_loose',
        'EventInfoAuxDyn.passTrigMatch_HLT_e20_lhmedium_nod0_g35_loose',
        'EventInfoAuxDyn.passTrigMatch_HLT_e24_lhmedium_L1EM20VH',
        'EventInfoAuxDyn.passTrigMatch_HLT_e25_mergedtight_g35_medium_Heg',
        'EventInfoAuxDyn.passTrigMatch_HLT_e26_lhtight_nod0_ivarloose',
        'EventInfoAuxDyn.passTrigMatch_HLT_e60_lhmedium',
        'EventInfoAuxDyn.passTrigMatch_HLT_e60_lhmedium_nod0',
        'EventInfoAuxDyn.passTrigMatch_HLT_g35_loose_L1EM24VHI_mu15_mu2noL1',
        'EventInfoAuxDyn.passTrigMatch_HLT_g35_loose_L1EM24VHI_mu18',
        'EventInfoAuxDyn.passTrigMatch_HLT_g35_loose_g25_loose',
        'EventInfoAuxDyn.passTrigMatch_HLT_g35_medium_g25_medium_L12EM20VH',
        'EventInfoAuxDyn.passTrigMatch_HLT_mu18_mu8noL1',
        'EventInfoAuxDyn.passTrigMatch_HLT_mu20_iloose_L1MU15',
        'EventInfoAuxDyn.passTrigMatch_HLT_mu22_mu8noL1',
        'EventInfoAuxDyn.passTrigMatch_HLT_mu26_ivarmedium',
        'EventInfoAuxDyn.passTrigMatch_HLT_mu40',
        'EventInfoAuxDyn.passTrigMatch_HLT_mu50',
        ]

if doHiggsTruth :
    variables += [
        'HGamTruthEventInfoAuxDyn.yyStarChannel',
        'HGamTruthEventInfoAuxDyn.pT_l1_h1',
        'HGamTruthEventInfoAuxDyn.pT_l2_h1',
        'HGamTruthEventInfoAuxDyn.y_h1',
        'HGamGSFTrackParticlesAuxDyn.isTrueHiggsElectron',
        ]
    cuts = []

blindcut = [
    ]
