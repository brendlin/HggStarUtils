
treename = 'CollectionTree'

variables = [
    'HGamEventInfoAuxDyn.m_lly',
    'HGamEventInfoAuxDyn.yyStarChannel',
    ]

cuts = [
    'HGamEventInfoAuxDyn.cutFlow > 21', # e.g. everything except zmass and llg mass (ysy002)
    # replace with HGamEventInfoAuxDyn.isPassedEventSelection in ysy003
    'HGamEventInfoAuxDyn.m_ll < 45000',
    '105000 < HGamEventInfoAuxDyn.m_lly && HGamEventInfoAuxDyn.m_lly < 160000',
    ]

blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]
