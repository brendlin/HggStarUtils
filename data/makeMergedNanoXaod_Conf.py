
treename = 'CollectionTree'

# Require the selected tracks to be matched to the Higgs
requireTruthMatchedHiggsTracks = True

variables = [
    # Most useful variables
    'HGamEventInfoAuxDyn.m_lly',
    'HGamEventInfoAuxDyn.pt_lly',
    'HGamEventInfoAuxDyn.yyStarChannel',
    'HGamEventInfoAuxDyn.isPassedObjSelection',
    'HGamEventInfoAuxDyn.isPassedEventSelection',
    'HGamEventInfoAuxDyn.m_ll',
    'HGamEventInfoAuxDyn.pt_ll',
    'HGamPhotonsAuxDyn.pt',
    'HGamElectronsAuxDyn.pt',
    'HGamEventInfoAuxDyn.deltaR_ll',
    'HGamEventInfoAuxDyn.crossSectionBRfilterEff',
    'HGamEventInfoAuxDyn.weight',

    # GSF-track decorators
    'HGamGSFTrackParticlesAuxDyn.z0pv',
    'HGamGSFTrackParticlesAuxDyn.z0sinTheta',
    'HGamGSFTrackParticlesAuxDyn.pt',
    'HGamGSFTrackParticlesAuxDyn.d0',
    'HGamGSFTrackParticlesAuxDyn.d0significance',
    'HGamGSFTrackParticlesAuxDyn.TRT_PID_trans',
    'HGamGSFTrackParticlesAuxDyn.mergedTrackParticleIndex',
    'HGamGSFTrackParticlesAuxDyn.isTrueHiggsElectron',

    # Electron decorators
    'HGamElectronsAuxDyn.EOverP0P1',
    'HGamElectronsAuxDyn.RhadForPID',
    'HGamElectronsAuxDyn.deltaEta1',
    'HGamElectronsAuxDyn.f1',
    'HGamElectronsAuxDyn.Eratio',
    'HGamElectronsAuxDyn.wtots1',
    'HGamElectronsAuxDyn.Reta',
    'HGamElectronsAuxDyn.Rphi',
    'HGamElectronsAuxDyn.weta2',
    'HGamElectronsAuxDyn.f3',
    'HGamElectronsAuxDyn.EOverP0P1',
    'HGamElectronsAuxDyn.dRExtrapTrk12',
    'HGamElectronsAuxDyn.dRExtrapTrk12_LM',
    'HGamElectronsAuxDyn.delta_z0_tracks',
    'HGamElectronsAuxDyn.delta_z0sinTheta_tracks',
    ]

cuts = [
    'HGamEventInfoAuxDyn.isPassedObjPreselection == 1',
    'HGamEventInfoAuxDyn.yyStarChannel == 3',
    'HGamEventInfoAuxDyn.m_lly > 105000.',
    'HGamEventInfoAuxDyn.m_lly < 160000.',
    ]

truthcuts = []
if requireTruthMatchedHiggsTracks :
    truthcuts = [
        'HGamGSFTrackParticlesAuxDyn.isTrueHiggsElectron[0] == 1 && HGamGSFTrackParticlesAuxDyn.isTrueHiggsElectron[1] == 1',
        ]

blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]
