
treename = 'CollectionTree'

cuts = [
    'HGamEventInfoAuxDyn.yyStarChannel == 3',
#     'HGamEventInfoAuxDyn.isPassedObjPreselection == 1', # applied at skim
    'HGamEventInfoAuxDyn.isPassedEventSelection',
    ]

variables = [
    'HGamEventInfoAuxDyn.m_lly/1000.',
    'HGamElectronsAuxDyn.delta_z0_tracks',
    'HGamElectronsAuxDyn.delta_z0sinTheta_tracks',
    'HGamGSFTrackParticlesAuxDyn.z0pv[0]',
    'HGamGSFTrackParticlesAuxDyn.z0sinTheta[0]',
    'HGamGSFTrackParticlesAuxDyn.z0pv[1]',
    'HGamGSFTrackParticlesAuxDyn.z0sinTheta[1]',
    'HGamElectronsAuxDyn.EOverP0P1',
    'HGamElectronsAuxDyn.Eratio',
    'HGamElectronsAuxDyn.Reta',
    'HGamElectronsAuxDyn.RhadForPID',
    'HGamElectronsAuxDyn.Rphi',
    'HGamElectronsAuxDyn.dRExtrapTrk12',
    'HGamElectronsAuxDyn.dRExtrapTrk12_LM',
    'HGamElectronsAuxDyn.deltaEta1',
    'HGamElectronsAuxDyn.f1',
    'HGamElectronsAuxDyn.f3',
    'HGamElectronsAuxDyn.pt[0]/1000.',
    'HGamElectronsAuxDyn.weta2',
    'HGamElectronsAuxDyn.wtots1',
    'HGamGSFTrackParticlesAuxDyn.TRT_PID_trans[0]',
    'HGamGSFTrackParticlesAuxDyn.TRT_PID_trans[1]',
    'HGamGSFTrackParticlesAuxDyn.d0significance[0]',
    'HGamGSFTrackParticlesAuxDyn.d0significance[1]',
    'HGamGSFTrackParticlesAuxDyn.mergedTrackParticleIndex[0]',
    'HGamGSFTrackParticlesAuxDyn.mergedTrackParticleIndex[1]',
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.',
    'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.',
    ]

from HggStarHelpers import StandardSampleMerging, StandardPlotLabels
mergesamples = StandardSampleMerging
mergesamples['TM Higgs'] = '%gamstarTMgam%'

labels = StandardPlotLabels
labels['data'] = 'data SB'
labels['AllHiggs'] = 'Higgs'

blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]

from HggStarHelpers import StandardHistFormat
histformat = StandardHistFormat

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

from HggStarHelpers import weightscale_hyystar
weightscale = weightscale_hyystar
