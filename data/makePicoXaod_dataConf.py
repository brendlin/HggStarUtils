
treename = 'CollectionTree'

variables = [
    'HGamEventInfoAuxDyn.m_lly',
    'HGamEventInfoAuxDyn.m_lly_gev',
    'HGamEventInfoAuxDyn.yyStarChannel',
    ]

cuts = [
    'HGamEventInfoAuxDyn.isPassedEventSelection', # PASSALL (including mll<45, mlly 105-160)
    ]

blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]
