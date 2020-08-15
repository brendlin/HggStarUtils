
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
     'HGamEventInfoAuxDyn.cutFlow > 24',
     #'HGamEventInfoAuxDyn.yyStarChannel == 1',
     #'HGamEventInfoAuxDyn.isPassedEventSelection == 1',
     #'HGamPhotonsAuxDyn.pt[0]/1000>20',
     #'HGamPhotonsAuxDyn.pt[0]/1000>20',
     #'HGamEventInfoAuxDyn.pt_ll/1000>20',     
     #'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly>0',
     #'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly>0',
     #'HGamEventInfoAuxDyn.yyStarChannel == 2',
#     'HGamTruthEventInfoAuxDyn.ystar_pdg_flavor == 13',
#     'HGamTruthEventInfoAuxDyn.pT_l2_h1/1000. > 3',
#     'HGamEventInfoAuxDyn.N_mu == 2',
#      'HGamElectronsAuxDyn.pt/1000. < 15',
#     'HGamEventInfoAuxDyn.N_mu == 2',
#     'HGamEventInfoAuxDyn.N_e == 2',
#     'HGamEventInfoAuxDyn.NLoosePhotons >= 1',
#     'HGamEventInfoAuxDyn.m_ll/1000. < 83.',
#     'HGamEventInfoAuxDyn.N_e > 0', 
      #'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly>0.25',
      #'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly>0.35',
      #'HGamMuonsAuxDyn.pt[0]/1000>24',
      #'HGamElectronsAuxDyn.pt[0]/1000>23',
      #'HGamGSFTrackParticlesAuxDyn.pt[0]/1000>27',
      
    #'HGamEventInfoAuxDyn.m_ll/1000<2.5 || HGamEventInfoAuxDyn.m_ll/1000>3.5', #electron J/Psi peak
    #'HGamElectronsAuxDyn.pt[0]/1000>13',
    
    #'HGamEventInfoAuxDyn.m_ll/1000<2.9 || HGamEventInfoAuxDyn.m_ll/1000>3.3', #muon J/Psi peak
    #'HGamEventInfoAuxDyn.m_ll/1000<9.1 || HGamEventInfoAuxDyn.m_ll/1000>10.6', #muon Y peak(s)
    #'HGamMuonsAuxDyn.pt[0]/1000>11',    
    
    
    #'HGamEventInfoAuxDyn.Deta_j_j<2.5', #anti-VBF cut, if no jets in event - then value is '-99', still correctly treated
    #'HGamEventInfoAuxDyn.m_jj/1000<400', #anti-VBF cut, if no jets in event - then value is '-99', still correctly treated
    
    
    
    'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly>0.3',
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly>0.3',
    #'HGamGSFTrackParticlesAuxDyn.pt[0]/1000>27',
    
    ]

variables = [
      'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly>',
      'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly>',
      ##'HGamPhotonsAuxDyn.pt[0]/1000>',
      #'HGamElectronsAuxDyn.pt[0]/1000>',
      #'HGamElectronsAuxDyn.pt[1]/1000>',
      #'HGamMuonsAuxDyn.pt[0]/1000>',
      #'HGamMuonsAuxDyn.pt[1]/1000>',
      ##'HGamEventInfoAuxDyn.pt_ll/1000>',
      #'HGamGSFTrackParticlesAuxDyn.pt[0]/1000>',
      #'HGamGSFTrackParticlesAuxDyn.pt[1]/1000>',
#     'HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1',
#     'log(HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1)',
#     'HGamTruthEventInfoAuxDyn.pT_l1_h1/1000.',
#     'HGamTruthEventInfoAuxDyn.pT_l2_h1/1000.',
#     'HGamTruthEventInfoAuxDyn.m_yStar_undressed_h1/1000.',
#     'HGamTruthEventInfoAuxDyn.m_h1',
#     'HGamTruthEventInfoAuxDyn.m_lly/1000.',
#     'HGamTruthEventInfoAuxDyn.pT_yDirect_h1/1000.',
#     'HGamTruthPhotonsAuxDyn.pt[0]/1000.',
#     'HGamEventInfoAuxDyn.m_lly/1000.',
#     'HGamEventInfoAuxDyn.pt_ll/1000.',
#     'HGamEventInfoAuxDyn.m_lly_track4mom/1000.',
#     'HGamEventInfoAuxDyn.m_ll_track4mom/1000.',
#     'HGamEventInfoAuxDyn.m_ll_track4mom/HGamTruthEventInfoAuxDyn.m_yStar_undressed_h1',
#     'HGamPhotonsAuxDyn.pt[0]/1000.',
#     'HGamEventInfoAuxDyn.m_lly_track4mom/HGamTruthEventInfoAuxDyn.m_lly',
#     'HGamEventInfoAuxDyn.m_ll/1000.',
#     'HGamMuonsAuxDyn.pt[0]/1000.',
#     'HGamMuonsAuxDyn.pt[1]/1000.',
#     'HGamEventInfoAuxDyn.N_mu',
#     'HGamMuonsAuxDyn.pt[0]/HGamTruthEventInfoAuxDyn.pT_l1_h1',
#     'HGamMuonsAuxDyn.pt[1]/HGamTruthEventInfoAuxDyn.pT_l2_h1',
#     'HGamEventInfoAuxDyn.m_ll/HGamTruthEventInfoAuxDyn.m_yStar_undressed_h1',
#     'HGamElectronsAuxDyn.scaleFactor',
    ]

histformat = {
    'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly': [55,105,160,'m_{ll#gamma} [GeV]',32,0,0.8,'p^{ll}_{T}/m_{ll#gamma}'],
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly': [55,105,160,'m_{ll#gamma} [GeV]',32,0,0.8,'p^{#gamma}_{T}/m_{ll#gamma}'],
    'HGamPhotonsAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',60,10,70,'p^{#gamma}_{T} [GeV]'],
    'HGamMuonsAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',60,11,71,'p^{#mu0}_{T} [GeV]'],
    'HGamMuonsAuxDyn.pt[1]/1000': [55,105,160,'m_{ll#gamma} [GeV]',60,3,63,'p^{#mu1}_{T} [GeV]'],
    'HGamElectronsAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',50,13,63,'p^{e0}_{T} [GeV]'],
    'HGamElectronsAuxDyn.pt[1]/1000': [55,105,160,'m_{ll#gamma} [GeV]',60,4,64,'p^{e1}_{T} [GeV]'],
    'HGamEventInfoAuxDyn.pt_ll/1000': [55,105,160,'m_{ll#gamma} [GeV]',60,0,60,'p^{ll}_{T} [GeV]'],
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',60,0,60,'p^{trk0}_{T} [GeV]'],
    'HGamGSFTrackParticlesAuxDyn.pt[1]/1000': [55,105,160,'m_{ll#gamma} [GeV]',50,0,50,'p^{trk1}_{T} [GeV]'],
    'HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1'     :[100,0,1,'Truth #Delta^{}R(lep1,lep2)'],
    'log(HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1)':[100,-14,2,'Truth log_{10}(#Delta^{}R(lep1,lep2))'],
    'HGamTruthEventInfoAuxDyn.pT_l1_h1/1000.'     :[100,0,100],
    'HGamTruthEventInfoAuxDyn.pT_l2_h1/1000.'     :[100,0,100],
    'HGamMuonsAuxDyn.pt[0]/HGamTruthEventInfoAuxDyn.pT_l1_h1':[20,0,2],
    'HGamMuonsAuxDyn.pt[1]/HGamTruthEventInfoAuxDyn.pT_l2_h1':[20,0,2],
    'HGamEventInfoAuxDyn.m_lly/1000.':[100,105,160,'m_{ll#gamma} [GeV]'],
    'HGamEventInfoAuxDyn.m_ll/HGamTruthEventInfoAuxDyn.m_yStar_undressed_h1':[100,0,2,'m_{ll}/m^{true,undressed}_{#gamma*}'],
    'HGamTruthEventInfoAuxDyn.m_lly/1000.':[100,120,130,'Truth m_{ll#gamma} (undressed) [GeV]'],
    'HGamTruthEventInfoAuxDyn.pT_yDirect_h1/1000.':[100,0,200,'Truth p^{#gamma}_{T}'],
    'HGamEventInfoAuxDyn.m_ll/1000.':[100,0,50,'m_{ll} [GeV]'],
    'HGamTruthEventInfoAuxDyn.m_yStar_undressed_h1/1000.':[100,0,20,'True m_{#gamma*} (undressed) [GeV]'],
    'HGamPhotonsAuxDyn.pt[0]/1000.':[100,0,200,'p^{#gamma}_{T}'],
    'HGamTruthPhotonsAuxDyn.pt[0]/1000.':[100,0,200,'truth p^{#gamma}_{T}'],
    'HGamEventInfoAuxDyn.m_lly_track4mom/1000.':[100,0,200,'m_{ll#gamma} (using track 4-mom) [GeV]'],
    'HGamEventInfoAuxDyn.m_ll_track4mom/1000.':[100,0,50,'m_{ll} (using track 4-mom) [GeV]'],
    'HGamEventInfoAuxDyn.m_ll_track4mom/HGamTruthEventInfoAuxDyn.m_yStar_undressed_h1':[100,0,2,'m^{trk4mom}_{ll}/m^{true,undressed}_{#gamma*}'],
    'HGamEventInfoAuxDyn.m_lly_track4mom/HGamTruthEventInfoAuxDyn.m_lly':[100,0,2,'m^{trk4mom}_{ll#gamma}/m^{true,undressed}_{ll#gamma}'],
    }

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

import HggStarHelpers
weightscale = HggStarHelpers.weightscale_hyystar
