
def GetWeightedCutflowHistogram(t_file) :
    import re
    for i in t_file.GetListOfKeys() :
        # get _weighted
        if not re.match('CutFlow_.*_weighted',i.GetName()) :
            continue
        if re.match('CutFlow_.*_onlyDalitz_weighted',i.GetName()) :
            continue
        return i.ReadObj()
    return 0

def GetOnlyDalitzWeightedCutflowHistogram(t_file) :
    import re
    for i in t_file.GetListOfKeys() :
        # get _noDalitz_weighted
        if not re.match('CutFlow_.*_onlyDalitz_weighted',i.GetName()) :
            continue
        return i.ReadObj()
    return 0

def weightscale_hyystar(tfile,is_h015d=False) :
    import re

    def weightscale_onefile(t_file) :

        fix_xs = 1.0

        #print 'Processing %s'%(t_file.GetName())

        weighted_histo = GetWeightedCutflowHistogram(t_file)
        tmp_xAOD  = weighted_histo.GetBinContent(1) # hopefully unskimmed MC sumw
        tmp_DxAOD = weighted_histo.GetBinContent(2) # hopefully unskimmed MC sumw

        # Multiply cross section by this ratio
        if 'Sherpa2_mumugamma_pty_15_35' in weighted_histo.GetName() :
            fix_xs = 1.8
            print 'Multiplying Sherpa2_mumugamma_pty_15_35 by %2.3f'%(fix_xs)
        
        weighted_histo_onlyDalitz = GetOnlyDalitzWeightedCutflowHistogram(t_file)
        tmp_Ntuple_DxAOD = weighted_histo_onlyDalitz.GetBinContent(3) # hopefully unskimmed MC sumw

        tmp_DxAOD = tmp_DxAOD * fix_xs
        return tmp_xAOD,tmp_DxAOD,tmp_Ntuple_DxAOD

    if type(tfile) == type([]) :
        DxAOD = 0; xAOD = 0; Ntuple_DxAOD = 0;
        for f in tfile :
            tmp1,tmp2,tmp3 = weightscale_onefile(f)
            xAOD         += tmp1
            DxAOD        += tmp2
            Ntuple_DxAOD += tmp3
            #print xAOD,DxAOD,Ntuple_DxAOD

    else :
        xAOD,DxAOD,Ntuple_DxAOD = weightscale_onefile(tfile)
        
    # add 1000. for matching our fb lumi to the MxAOD cross section.
    #print 1000. * DxAOD / float( xAOD * Ntuple_DxAOD )
    return 1000. * DxAOD / float( xAOD * Ntuple_DxAOD )

class YEAR :
    yUnspecified = 0
    y2015        = 1
    y2016        = 2
    y2017        = 3
    y2018        = 4
    y201516      = 5
    y20151617    = 6
    y2015161718  = 7

def GetFbForMCNormalization(theyear) :
    if theyear != YEAR.yUnspecified :
        # IMPORTANT NOTE: 2015/2016 MC normalization is controlled by
        # RandomRunNumber, so we need to specify the 2015+16 luminosity!
        fb = {YEAR.y2015      : 3.21956 + 32.9653,
              YEAR.y2016      : 3.21956 + 32.9653,
              YEAR.y2017      :                     44.3074,
              YEAR.y2018      :                               58.4501,
              YEAR.y201516    : 3.21956 + 32.9653,
              YEAR.y20151617  : 3.21956 + 32.9653 + 44.3074,
              YEAR.y2015161718: 3.21956 + 32.9653 + 44.3074 + 58.4501}.get(theyear)
        return fb

    return 1.0

def SherpaKfactor1p3(tfile) :
    Sherpa_NLO = ['301535','301536','301899','301900','301901','301902','301903','301904']
    checkSherpa = list(a in tfile.GetName() for a in Sherpa_NLO)
    if True in checkSherpa :
        print '%s (Sherpa) will be scaled by a factor of 1.3'%(tfile.GetName())
        return 1.3

    return 1.0

def SF_80fb(tfile) :
    mc16a = 3219.56 + 32965.3
    mc16d = 44307.4
    the_sum = float(mc16a + mc16d)

    if 'mc16a' in tfile.GetName() :
        print '%s (mc16a) will be scaled by a factor of %.2f / %.2f'%(tfile.GetName(),mc16a,the_sum)
        return mc16a / the_sum

    if 'mc16d' in tfile.GetName() :
        print '%s (mc16d) will be scaled by a factor of %.2f / %.2f'%(tfile.GetName(),mc16d,the_sum)
        return mc16d / the_sum

    return 1.0

def SF_139fb(tfile) :
    mc16a = 3219.56 + 32965.3
    mc16d = 44307.4
    mc16e = 58450.1
    the_sum = float(mc16a + mc16d + mc16e)

    if 'mc16a' in tfile.GetName() :
        print '%s (mc16a) will be scaled by a factor of %.2f / %.2f'%(tfile.GetName(),mc16a,the_sum)
        return mc16a / the_sum

    if 'mc16d' in tfile.GetName() :
        print '%s (mc16d) will be scaled by a factor of %.2f / %.2f'%(tfile.GetName(),mc16d,the_sum)
        return mc16d / the_sum

    if 'mc16e' in tfile.GetName() :
        print '%s (mc16e) will be scaled by a factor of %.2f / %.2f'%(tfile.GetName(),mc16e,the_sum)
        return mc16e / the_sum

    return 1.0

StandardPlotLabels = {
    # Now possible via regular expressions (use % instead of .*)
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
    }

StandardSampleMerging = {
    # Now possible via regular expressions (use % instead of .*)
    'Sherpa_eegamma':'%Sherpa_CT10_eegamma%',
    'Sherpa_mmgamma':'%Sherpa_CT10_mumugamma%',
    'AllHiggs':'%gamstargam%',
    }

StandardHistFormat = {
    'HGamEventInfoAuxDyn.m_ll/1000.'                      :[100,  0,120,'m_{ll} [GeV]'                ],
    'HGamEventInfoAuxDyn.m_lly/1000.'                     :[100,105,160,'m_{ll#gamma} [GeV]'          ],
    'HGamEventInfoAuxDyn.pt_lly/1000.'                    :[100,  0,200,'p_{Tll#gamma} [GeV]'         ],
    'HGamPhotonsAuxDyn.pt[0]/1000.'                       :[100,  0,200,'p^{#gamma}_{T} [GeV]'        ],
    'HGamMuonsAuxDyn.pt[0]/1000.'                         :[100,  0,200,'p^{#mu1}_{T} [GeV]'          ],
    'HGamMuonsAuxDyn.pt[1]/1000.'                         :[100,  0, 60,'p^{#mu2}_{T} [GeV]'          ],
    'HGamElectronsAuxDyn.pt[0]/1000.'                     :[100,  0,200,'p^{e1}_{T} [GeV]'            ],
    'HGamElectronsAuxDyn.pt[1]/1000.'                     :[100,  0, 60,'p^{e2}_{T} [GeV]'            ],
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly'   :[100,  0,  1,'p^{#gamma}_{T}/m_{ll#gamma}' ],
    'HGamEventInfoAuxDyn.deltaR_ll'                       :[100,  0,  2,'#Delta^{}R_{ll}'             ],
    'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly' :[100,  0,  1,'p^{ll}_{T}/m_{ll#gamma}'     ],
    'HGamEventInfoAuxDyn.pt_ll/1000.'                     :[100,  0,200,'p^{ll}_{T} [GeV]'            ],
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.'             :[100,  0,100,'p^{trk0}_{T} [GeV]'          ],
    'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.'             :[100,  0, 30,'p^{trk1}_{T} [GeV]'          ],
    # VBF variables
    'HGamEventInfoAuxDyn.Deta_j_j'       :[ 30,  2,    8,'#Delta#eta_{jj}'           ],
    'HGamEventInfoAuxDyn.Dphi_lly_jj'    :[ 12,1.75, 3.15,'#Delta#phi_{ll#gamma-jj}' ],
    'HGamEventInfoAuxDyn.Dy_j_j'         :[ 30,  2,    8,'#Delta^{}y_{jj}'           ],
    'fabs(HGamEventInfoAuxDyn.Zepp_lly)' :[ 20,  0,    5,'|#eta_{Zepp}|'             ],
    'HGamEventInfoAuxDyn.m_jj/1000.'     :[ 21, 80,  500,'m_{jj} [GeV]'              ],
    'HGamEventInfoAuxDyn.pTt_lly/1000.'  :[ 40,  0,  200,'p^{Tt} [GeV]'              ],
    'HGamEventInfoAuxDyn.pT_llyjj/1000.' :[ 25,  0,  120,'p_{Tll#gamma^{}jj} [GeV]'  ],
    'HGamEventInfoAuxDyn.DRmin_y_leps_2jets'  :[ 40,  0.0,  4,'#Delta^{}R^{min}_{j,e/#mu/#gamma}'  ],
    'HGamEventInfoAuxDyn.DRmin_y_ystar_2jets' :[ 40,  0.0,  4,'#Delta^{}R^{min}_{j,#gamma/#gamma*}'  ],
    # Track variables
    'HGamGSFTrackParticlesAuxDyn.z0pv[0]'           :[100,-10,10,'z_{0}^{PV} (lead)'             ],
    'HGamGSFTrackParticlesAuxDyn.z0pv[1]'           :[100,-10,10,'z_{0}^{PV} (sublead)'          ],
    'HGamGSFTrackParticlesAuxDyn.z0sinTheta[0]'     :[100,-10,10,'z_{0}^{PV}sin#theta (lead)'    ],
    'HGamGSFTrackParticlesAuxDyn.z0sinTheta[1]'     :[100,-10,10,'z_{0}^{PV}sin#theta (sublead)' ],
    'HGamGSFTrackParticlesAuxDyn.d0significance[0]' :[100,  0,10,'d_{0}Significance (lead)'      ],
    'HGamGSFTrackParticlesAuxDyn.d0significance[1]' :[100,  0,10,'d_{0}Significance (sublead)'   ],
    'HGamGSFTrackParticlesAuxDyn.TRT_PID_trans[0]'  :[100, -1, 1,'Transformed TRT PID (lead)'    ],
    'HGamGSFTrackParticlesAuxDyn.TRT_PID_trans[1]'  :[100, -1, 1,'Transformed TRT PID (sublead)' ],
    # Standard electron variables
    'HGamElectronsAuxDyn.Reta'       :[100,  0.8,1.05,'R_{#eta}'       ],
    'HGamElectronsAuxDyn.Eratio'     :[100,  0.3,1.05,'E_{Ratio}'      ],
    'HGamElectronsAuxDyn.RhadForPID' :[100,-0.05,0.12,'R_{Had}'        ],
    'HGamElectronsAuxDyn.Rphi'       :[100,  0.5,1.05,'R_{#phi}'       ],
    'HGamElectronsAuxDyn.deltaEta1'  :[100,-0.02,0.02,'#Delta#eta_{1}' ],
    'HGamElectronsAuxDyn.f1'         :[100,    0, 0.6,'f_{1}'          ],
    'HGamElectronsAuxDyn.f3'         :[100,    0,0.03,'f_{3}'          ],
    'HGamElectronsAuxDyn.weta2'      :[100,0.005,0.02,'w_{#eta2}'      ],
    'HGamElectronsAuxDyn.wtots1'     :[100,    0,   6,'w_{s,tot}'      ],
    # Merged ID variables
    'HGamElectronsAuxDyn.delta_z0_tracks'                     :[100,-10, 10,'#Delta^{}z_{0}^{PV}'             ],
    'HGamElectronsAuxDyn.delta_z0sinTheta_tracks'             :[100,-10, 10,'#Delta^{}z_{0}^{PV}sin#theta'    ],
    'HGamElectronsAuxDyn.EOverP0P1'                           :[100,  0, 10,'E/(p_{trk0}+p_{trk1})'           ],
    'HGamGSFTrackParticlesAuxDyn.mergedTrackParticleIndex[0]' :[  5,  0,  5,'Track particle index (lead)'     ],
    'HGamGSFTrackParticlesAuxDyn.mergedTrackParticleIndex[1]' :[  5,  0,  5,'Track particle index (sublead)'  ],
    'HGamElectronsAuxDyn.ambiguityType'                       :[  6,  0,  6,'Ambiguity type'                  ],
    'HGamElectronsAuxDyn.ambiConvRadius'                      :[ 50,-20,100,'Ambiguous photon conversion radius [mm]'],
    #
    'HGamElectronsAuxDyn.dEtaExtrapTrk12'   :[100,-0.11,0.11,'#Delta#eta_{local} P'],
    'HGamElectronsAuxDyn.dPhiExtrapTrk12'   :[100,-0.21,0.21,'#Delta#phi_{local} P'],
    'HGamElectronsAuxDyn.dEtaExtrapTrk12_LM':[100,-0.11,0.11,'#Delta#eta_{local} LM'],
    'HGamElectronsAuxDyn.dPhiExtrapTrk12_LM':[100,-0.21,0.21,'#Delta#phi_{local} LM'],
    'HGamElectronsAuxDyn.dRExtrapTrk12'     :[100,-0.21,0.21,'#Delta^{}R_{local} P' ],
    'HGamElectronsAuxDyn.dRExtrapTrk12_LM'  :[100,-0.21,0.21,'#Delta^{}R_{local} LM'],
    #
    'HGamElectronsAuxDyn.dR1betweenTracks_LM'  :[100,-0.21,0.21,'#Delta^{}R_{1} LM'],
    'HGamElectronsAuxDyn.dR2betweenTracks_LM'  :[100,-0.21,0.21,'#Delta^{}R_{2} LM'],
    'HGamElectronsAuxDyn.dR1betweenTracks_P'   :[100,-0.21,0.21,'#Delta^{}R_{1} P' ],
    'HGamElectronsAuxDyn.dR2betweenTracks_P'   :[100,-0.21,0.21,'#Delta^{}R_{2} P' ],
    'HGamElectronsAuxDyn.dEta1betweenTracks_LM':[100,-0.11,0.11,'#Delta#eta_{1} LM'],
    'HGamElectronsAuxDyn.dEta1betweenTracks_P' :[100,-0.11,0.11,'#Delta#eta_{1} P' ],
    'HGamElectronsAuxDyn.dEta2betweenTracks_LM':[100,-0.11,0.11,'#Delta#eta_{2} LM'],
    'HGamElectronsAuxDyn.dEta2betweenTracks_P' :[100,-0.11,0.11,'#Delta#eta_{2} P' ],
    'HGamElectronsAuxDyn.dPhi1betweenTracks_LM':[100,-0.21,0.21,'#Delta#phi_{1} LM'],
    'HGamElectronsAuxDyn.dPhi1betweenTracks_P' :[100,-0.21,0.21,'#Delta#phi_{1} P' ],
    'HGamElectronsAuxDyn.dPhi2betweenTracks_LM':[100,-0.21,0.21,'#Delta#phi_{2} LM'],
    'HGamElectronsAuxDyn.dPhi2betweenTracks_P' :[100,-0.21,0.21,'#Delta#phi_{2} P' ],
    }
