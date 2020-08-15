
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
    #'HGamEventInfoAuxDyn.isPassedEventSelection',
            'HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000>25',
    'HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000>25',
          'HGamEventInfoAuxDyn.Deta_j_j>2.7', 
    'HGamEventInfoAuxDyn.m_jj/1000>500', 
    'min(HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000. + 999*(abs(HGamAntiKt4EMPFlowJetsAuxDyn.eta[0]) < 2.5),HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000. + 999*(abs(HGamAntiKt4EMPFlowJetsAuxDyn.eta[1]) < 2.5))>30',
        'abs(HGamEventInfoAuxDyn.Zepp_lly)<2.0',
    'HGamEventInfoAuxDyn.DRmin_y_leps_2jets>1.5',
        'HGamEventInfoAuxDyn.Dphi_lly_jj>2.8',
            'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly>0.3',
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly>0.3',
    ]

variables = [
    #'abs(HGamEventInfoAuxDyn.Zepp_lly)<',
    #'HGamEventInfoAuxDyn.DRmin_y_leps_2jets>',
    #'HGamEventInfoAuxDyn.Dphi_lly_jj>',
    #'HGamEventInfoAuxDyn.pT_llyjj/1000<',
    #'HGamEventInfoAuxDyn.pTt_lly/1000>',


    #'HGamPhotonsAuxDyn.pt[0]/1000>',
    #'HGamGSFTrackParticlesAuxDyn.pt[0]/1000>',
    #'HGamElectronsAuxDyn.pt[0]/1000>',
    #'HGamElectronsAuxDyn.pt[1]/1000>',
    #'HGamMuonsAuxDyn.pt[0]/1000>',
    #'HGamMuonsAuxDyn.pt[1]/1000>',
    #'HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000>',
    #'HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000>',
    'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly>',
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly>',
    'HGamEventInfoAuxDyn.Deta_j_j>', 
    'HGamEventInfoAuxDyn.m_jj/1000>', 
    'min(HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000. + 999*(abs(HGamAntiKt4EMPFlowJetsAuxDyn.eta[0]) < 2.5),HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000. + 999*(abs(HGamAntiKt4EMPFlowJetsAuxDyn.eta[1]) < 2.5))>',
        'abs(HGamEventInfoAuxDyn.Zepp_lly)<',
    'HGamEventInfoAuxDyn.DRmin_y_leps_2jets>',
        'HGamEventInfoAuxDyn.Dphi_lly_jj>',
    ]

histformat = {
        'min(HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000. + 999*(abs(HGamAntiKt4EMPFlowJetsAuxDyn.eta[0]) < 2.5),HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000. + 999*(abs(HGamAntiKt4EMPFlowJetsAuxDyn.eta[1]) < 2.5))': [55,105,160,'m_{ll#gamma} [GeV]',25,26,76,'p^{fwjet}_{T}'],
    'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly': [55,105,160,'m_{ll#gamma} [GeV]',32,0,0.8,'p^{ll}_{T}/m_{ll#gamma}'],
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly': [55,105,160,'m_{ll#gamma} [GeV]',32,0.0,0.8,'p^{#gamma}_{T}/m_{ll#gamma}'],
    'HGamPhotonsAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',20,20,40,'p^{#gamma}_{T} [GeV]'],
    'HGamMuonsAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',60,11,71,'p^{#mu0}_{T} [GeV]'],
    'HGamMuonsAuxDyn.pt[1]/1000': [55,105,160,'m_{ll#gamma} [GeV]',34,3,20,'p^{#mu1}_{T} [GeV]'],
    'HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',20,20,40,'p^{jet0}_{T} [GeV]'],
    'HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000': [55,105,160,'m_{ll#gamma} [GeV]',20,20,40,'p^{jet1}_{T} [GeV]'],
    'HGamElectronsAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',50,13,63,'p^{e0}_{T} [GeV]'],
    'HGamElectronsAuxDyn.pt[1]/1000': [55,105,160,'m_{ll#gamma} [GeV]',60,4.5,34.5,'p^{e1}_{T} [GeV]'],
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000': [55,105,160,'m_{ll#gamma} [GeV]',40,20,60,'p^{trk0}_{T} [GeV]'],
    
    'HGamEventInfoAuxDyn.DRmin_y_leps_2jets': [55,105,160,'m_{ll#gamma} [GeV]',30,0.5,3.5,'min(#Delta^{}R_{j-#gamma/leps})'],
    'HGamEventInfoAuxDyn.Dphi_lly_jj': [55,105,160,'m_{ll#gamma} [GeV]',30,0,3,'#Delta^{}#phi_{ll#gamma,jj}'],
    'HGamEventInfoAuxDyn.pTt_lly/1000': [55,105,160,'m_{ll#gamma} [GeV]',50,0,50,'p^{ll#gamma}_{Tt} [GeV]'],
    'HGamEventInfoAuxDyn.m_jj/1000': [55,105,160,'m_{ll#gamma} [GeV]',30,200,800,'m_{jj} [GeV]'],
    'HGamEventInfoAuxDyn.pT_llyjj/1000': [55,105,160,'m_{ll#gamma} [GeV]',50,0,100,'p^{lljj#gamma}_{T} [GeV]'],
    'HGamEventInfoAuxDyn.Deta_j_j': [55,105,160,'m_{ll#gamma} [GeV]',25,0.9,5.9,'#Delta^{}#eta_{jj}'],
    'abs(HGamEventInfoAuxDyn.Zepp_lly)': [55,105,160,'m_{ll#gamma} [GeV]',50,0,5,'|#eta^{ll#gamma}_{Zepp}|'],
    }

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

import HggStarHelpers
weightscale = HggStarHelpers.weightscale_hyystar
