
treename = 'CollectionTree'

blindcut = ['(120000 > HGamEventInfoAuxDyn.m_lly || HGamEventInfoAuxDyn.m_lly > 130000)']
peakcut = ['(122000 < HGamEventInfoAuxDyn.m_lly && HGamEventInfoAuxDyn.m_lly < 128000)']

mergesamples = {
    'Sherpa_eegamma':['mc16_13TeV.364500.Sherpa_222_NNPDF30NNLO_eegamma_pty_7_15.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364501.Sherpa_222_NNPDF30NNLO_eegamma_pty_15_35.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364502.Sherpa_222_NNPDF30NNLO_eegamma_pty_35_70.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364503.Sherpa_222_NNPDF30NNLO_eegamma_pty_70_140.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364504.Sherpa_222_NNPDF30NNLO_eegamma_pty_140_E_CMS.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      ],
    'Sherpa_mmgamma':['mc16_13TeV.364505.Sherpa_222_NNPDF30NNLO_mumugamma_pty_7_15.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364506.Sherpa_222_NNPDF30NNLO_mumugamma_pty_15_35.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364507.Sherpa_222_NNPDF30NNLO_mumugamma_pty_35_70.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364508.Sherpa_222_NNPDF30NNLO_mumugamma_pty_70_140.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364509.Sherpa_222_NNPDF30NNLO_mumugamma_pty_140_E_CMS.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      ],
    'Sherpa_ttgamma':['mc16_13TeV.364510.Sherpa_222_NNPDF30NNLO_tautaugamma_pty_7_15.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364511.Sherpa_222_NNPDF30NNLO_tautaugamma_pty_15_35.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364512.Sherpa_222_NNPDF30NNLO_tautaugamma_pty_35_70.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364513.Sherpa_222_NNPDF30NNLO_tautaugamma_pty_70_140.deriv.DAOD_HIGG1D2.e5982_e5984_s3126_r9781_r9778_p3415',
                      'mc16_13TeV.364514.Sherpa_222_NNPDF30NNLO_tautaugamma_pty_140_E_CMS.deriv.DAOD_HIGG1D2.e5928_e5984_s3126_r9781_r9778_p3415',
                      ],
    }

labels = {
    'HyyStar'           :'H^{ }#rightarrow^{ }#gamma^{ }#gamma^{ }*',
    'YstarUndressedFull':'H^{ }#rightarrow^{ }#gamma^{ }#gamma^{ }*',
    'Sherpa_eegamma':'Sherpa ee#gamma',
    'Sherpa_mmgamma':'Sherpa #mu#mu#gamma',
    'Sherpa_ttgamma':'Sherpa #tau#tau#gamma',
    'mc16_13TeV_343981_PowhegPythia8EvtGen_NNLOPS_nnlo_30_ggH125_gamgam_deriv_DAOD_HIGG1D1_e5607_e5984_s3126_r9781_r9778_p3404':'H^{ }#rightarrow^{ }#gamma^{ }#gamma^{ }*',
    'mc16_13TeV_364505_Sherpa_222_NNPDF30NNLO_mumugamma_pty_7_15_deriv_DAOD_HIGG1D2_e5928_e5984_s3126_r9781_r9778_p3415':'7<p_{T}^{#gamma}<15 GeV',
    'mc16_13TeV_364506_Sherpa_222_NNPDF30NNLO_mumugamma_pty_15_35_deriv_DAOD_HIGG1D2_e5928_e5984_s3126_r9781_r9778_p3415':'15<p_{T}^{#gamma}<35 GeV',
    'mc16_13TeV_364507_Sherpa_222_NNPDF30NNLO_mumugamma_pty_35_70_deriv_DAOD_HIGG1D2_e5928_e5984_s3126_r9781_r9778_p3415':'35<p_{T}^{#gamma}<70 GeV',
    'mc16_13TeV_364508_Sherpa_222_NNPDF30NNLO_mumugamma_pty_70_140_deriv_DAOD_HIGG1D2_e5928_e5984_s3126_r9781_r9778_p3415':'70<p_{T}^{#gamma}<140 GeV',
    'mc16_13TeV_364509_Sherpa_222_NNPDF30NNLO_mumugamma_pty_140_E_CMS_deriv_DAOD_HIGG1D2_e5928_e5984_s3126_r9781_r9778_p3415':'140<p_{T}^{#gamma} GeV',
    }

cuts = [
    'HGamEventInfoAuxDyn.isPassedEventSelection == 1',
    #cuts on top of our loose SR:
    'HGamPhotonsAuxDyn.pt[0]/1000>20',
      
    #'HGamEventInfoAuxDyn.m_ll/1000<2.5 || HGamEventInfoAuxDyn.m_ll/1000>3.5', #electron J/Psi peak
    #'HGamElectronsAuxDyn.pt[0]/1000>13',
      
    'HGamEventInfoAuxDyn.m_ll/1000<2.9 || HGamEventInfoAuxDyn.m_ll/1000>3.3', #muon J/Psi peak
    'HGamEventInfoAuxDyn.m_ll/1000<9.1 || HGamEventInfoAuxDyn.m_ll/1000>10.6', #muon Y peak(s)
    'HGamMuonsAuxDyn.pt[0]/1000>11',
    
    'HGamEventInfoAuxDyn.Deta_j_j>2.5',
    'HGamEventInfoAuxDyn.m_jj/1000>400',
      
    ]

variables = [
    'HGamEventInfoAuxDyn.Deta_j_j>',
    'abs(HGamEventInfoAuxDyn.Zepp_lly)<',
    'HGamEventInfoAuxDyn.DRmin_y_leps_2jets>',
    'HGamEventInfoAuxDyn.Dphi_lly_jj>',
    'HGamEventInfoAuxDyn.m_jj/1000>',
    'HGamEventInfoAuxDyn.pT_llyjj/1000<',
    'HGamEventInfoAuxDyn.pTt_lly/1000>',
    ]

histformat = {
    'HGamEventInfoAuxDyn.DRmin_y_leps_2jets': [55,105,160,'m_{ll#gamma} [GeV]',50,0,2,'min(#Delta^{}#R_{j-#gamma/leps})'],
    'HGamEventInfoAuxDyn.Dphi_lly_jj': [55,105,160,'m_{ll#gamma} [GeV]',50,0,4,'#Delta^{}#phi_{ll#gamma,jj}'],
    'HGamEventInfoAuxDyn.pTt_lly/1000': [55,105,160,'m_{ll#gamma} [GeV]',50,0,250,'p^{ll#gamma}_{Tt} [GeV]'],
    'HGamEventInfoAuxDyn.m_jj/1000': [55,105,160,'m_{ll#gamma} [GeV]',50,0,1000,'m_{jj} [GeV]'],
    'HGamEventInfoAuxDyn.pT_llyjj/1000': [55,105,160,'m_{ll#gamma} [GeV]',50,0,100,'p^{lljj#gamma}_{T} [GeV]'],
    'HGamEventInfoAuxDyn.Deta_j_j': [55,105,160,'m_{ll#gamma} [GeV]',8,0,4,'#Delta^{}#eta_{jj}'],
    'abs(HGamEventInfoAuxDyn.Zepp_lly)': [55,105,160,'m_{ll#gamma} [GeV]',50,0,20,'|#eta^{ll#gamma}_{Zepp}|'],
    }

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

import HggStarHelpers
weightscale = HggStarHelpers.weightscale_hyystar
