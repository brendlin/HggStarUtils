from HggStarHelpers import ChannelEnum

def appendTruthCategoryCuts(truthcuts,category,ptthrust_cut=100) :

    if not category :
        return

    if category in [4,5,6] :
        truthcuts.append('HGamEventInfoAuxDyn.passVBF')
    elif category in [7,8,9] :
        truthcuts.append('HGamEventInfoAuxDyn.passVBF == 0 && HGamEventInfoAuxDyn.pTt_lly/1000. > %d'%(ptthrust_cut))
    else :
        truthcuts.append('HGamEventInfoAuxDyn.passVBF == 0 && HGamEventInfoAuxDyn.pTt_lly/1000. < %d'%(ptthrust_cut))

    return

def appendTruthLeptonAndPtllCuts(truthcuts,channel) :
    if channel == ChannelEnum.DIMUON :
        truthcuts.append('HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.3')

    if channel == ChannelEnum.RESOLVED_DIELECTRON :
        truthcuts.append('HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.3')
        truthcuts.append('HGamElectronsAuxDyn.pt0/1000. > 13.0')
        truthcuts.append('HGamElectronsAuxDyn.pt1/1000. > 4.5')

    elif channel == ChannelEnum.MERGED_DIELECTRON :
        truthcuts.append('abs(HGamElectronsAuxDyn.eta0) < 2.37')
        truthcuts.append('abs(HGamElectronsAuxDyn.eta1) < 2.37')
        truthcuts.append('-HGamEventInfoAuxDyn.deltaPhi_ll > -0.02')
        # truthcuts.append('-HGamEventInfoAuxDyn.deltaPhi_ll <  0.01')
        truthcuts.append('-HGamEventInfoAuxDyn.deltaPhi_ll < 0.01*TMath::E()^(-0.374538*(HGamElectronsAuxDyn.pt1/1000.-0.5)) + 0.001')

    return

def appendVBFCuts_v1(cuts,truth=False) :
    # two-variable VBF cuts:

    if truth :
        cuts.append('HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000. > 25')
        cuts.append('HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000. > 25')
        cuts.append('HGamEventInfoAuxDyn.m_jj/1000. > 400')
        cuts.append('HGamEventInfoAuxDyn.Deta_j_j > 2.5')

    else :
        cuts.append('HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000. > 25')
        cuts.append('HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000. > 25')
        cuts.append('HGamEventInfoAuxDyn.m_jj/1000. > 400')
        cuts.append('HGamEventInfoAuxDyn.Deta_j_j > 2.5')

    return

def appendVBFCuts_v2(cuts,truth=False) :
    # new cuts developed by Artem

    # These should work for truth and reco
    cuts.append('HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000. > 25')
    cuts.append('HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000. > 25')
    cuts.append('HGamEventInfoAuxDyn.m_jj/1000. > 500')
    cuts.append('HGamEventInfoAuxDyn.Zepp_lly < 2.0')
    cuts.append('HGamEventInfoAuxDyn.DRmin_y_leps_2jets > 1.5')
    cuts.append('HGamEventInfoAuxDyn.Dphi_lly_jj > 2.8')
    cuts.append('HGamEventInfoAuxDyn.Deta_j_j > 2.7')

    return

def appendTruthElectronDeltaCuts_v1(truthcuts,channel,
                                    mergedDeltaPhiCut=0.05,mergedDeltaEtaCut=0.05,
                                    mergedFarDeltaPhiMin=0.05,
                                    onlyNear=False,
                                    onlyFar=False,
                                    ) :

    if channel == ChannelEnum.RESOLVED_DIELECTRON :

        truthcuts.append('(abs(HGamEventInfoAuxDyn.deltaPhiMagnet_ll) > %.2f || abs(HGamEventInfoAuxDyn.deltaEta_ll) > %.2f)'%(mergedDeltaPhiCut,mergedDeltaEtaCut))
        #truthcuts.append('sqrt(HGamEventInfoAuxDyn.deltaPhiMagnet_ll*HGamEventInfoAuxDyn.deltaPhiMagnet_ll + HGamEventInfoAuxDyn.deltaEta_ll*HGamEventInfoAuxDyn.deltaEta_ll) > %.2f'%(mergedDeltaPhiCut))
        return

    elif channel == ChannelEnum.MERGED_DIELECTRON :

        # DeltaEta cut
        truthcuts.append('abs(HGamEventInfoAuxDyn.deltaEta_ll) < %.2f'%(mergedDeltaEtaCut))

        # DeltaPhi cut (far and near sources)

        merged_nominal = 'abs(HGamEventInfoAuxDyn.deltaPhiMagnet_ll) < %.2f'%(mergedDeltaPhiCut)
        merged_nominalRelPtVar = 'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly'

        merged_farele  = 'abs(HGamEventInfoAuxDyn.deltaPhiMagnet_ll) > %.2f && abs(HGamEventInfoAuxDyn.deltaPhiMagnetRescaled_ll) < %.2f'%(mergedFarDeltaPhiMin,mergedDeltaPhiCut)
        #merged_fareleRelPtVar = 'HGamElectronsAuxDyn.pt0/HGamEventInfoAuxDyn.m_ly'
        merged_fareleRelPtVar = 'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly'

        req_nominal = '(%s && %s > 0.30)'%(merged_nominal,merged_nominalRelPtVar)
        req_farele  = '(%s && %s > 0.30)'%(merged_farele,merged_fareleRelPtVar)

        if onlyNear :
            truthcuts.append(req_nominal)

        elif onlyFar :
            truthcuts.append(req_farele)

        else :
            truthcuts.append('(%s || %s)'%(req_nominal,req_farele))

        return

    return

def appendMesonCuts(cuts,channel) :
    # For applying the meson cuts by hand

    if channel in [ChannelEnum.RESOLVED_DIELECTRON, ChannelEnum.MERGED_DIELECTRON] :
        cuts.append('!(HGamEventInfoAuxDyn.m_ll > 2500. && HGamEventInfoAuxDyn.m_ll <  3500.)')
        cuts.append('!(HGamEventInfoAuxDyn.m_ll > 8000. && HGamEventInfoAuxDyn.m_ll < 11000.)')

    if channel == ChannelEnum.DIMUON :
        cuts.append('!(HGamEventInfoAuxDyn.m_ll > 2900. && HGamEventInfoAuxDyn.m_ll <  3300.)')
        cuts.append('!(HGamEventInfoAuxDyn.m_ll > 9100. && HGamEventInfoAuxDyn.m_ll < 10600.)')

    return

def appendTriggerThresholds2018(cuts,channel) :

    if channel in [ChannelEnum.RESOLVED_DIELECTRON] :
        resolved_trig_thresh_2018  = '('
        resolved_trig_thresh_2018 += 'HGamElectronsAuxDyn.pt0 > 27000'
        resolved_trig_thresh_2018 += ' || (HGamElectronsAuxDyn.pt0 > 25000 && HGamElectronsAuxDyn.pt1 > 25000)'
        resolved_trig_thresh_2018 += ' || (HGamElectronsAuxDyn.pt0 > 35000 && HGamPhotonsAuxDyn.pt0 > 25000)'
        resolved_trig_thresh_2018 += ' || (HGamElectronsAuxDyn.pt0 > 25000 && HGamPhotonsAuxDyn.pt0 > 35000)'
        resolved_trig_thresh_2018 += ')'

        cuts.append(resolved_trig_thresh_2018)

    if channel in [ChannelEnum.MERGED_DIELECTRON] :
        merged_trig_thresh_2018  = '('
        merged_trig_thresh_2018 += 'HGamEventInfoAuxDyn.pt_ll > 27000'
        merged_trig_thresh_2018 += ' || (HGamEventInfoAuxDyn.pt_ll > 25000 && HGamPhotonsAuxDyn.pt0 > 35000)'
        merged_trig_thresh_2018 += ' || (HGamEventInfoAuxDyn.pt_ll > 35000 && HGamPhotonsAuxDyn.pt0 > 25000)'
        merged_trig_thresh_2018 += ')'

        cuts.append(merged_trig_thresh_2018)

    return


def cutcomparisons_MllSliceStudy(truth=False) :
    # Mass cut slicing study
    from collections import OrderedDict
    cutcomparisons = OrderedDict()

    if truth :
        cutcomparisons['0 < m_{ll} < 2 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. < 2']
        cutcomparisons['2 < m_{ll} < 10 Gev'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 2' ,'HGamEventInfoAuxDyn.m_ll/1000. < 10']
        cutcomparisons['10 < m_{ll} < 20 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 10','HGamEventInfoAuxDyn.m_ll/1000. < 20']
        cutcomparisons['20 < m_{ll} < 30 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 20','HGamEventInfoAuxDyn.m_ll/1000. < 30']
        cutcomparisons['30 < m_{ll} < 40 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 30','HGamEventInfoAuxDyn.m_ll/1000. < 40']
        cutcomparisons['40 < m_{ll} < 50 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 40','HGamEventInfoAuxDyn.m_ll/1000. < 50']

    else :
        cutcomparisons['0 < m_{ll} < 2 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. < 2']
        cutcomparisons['2 < m_{ll} < 10 Gev'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 2' ,'HGamEventInfoAuxDyn.m_ll/1000. < 10']
        cutcomparisons['10 < m_{ll} < 20 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 10','HGamEventInfoAuxDyn.m_ll/1000. < 20']
        cutcomparisons['20 < m_{ll} < 30 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 20','HGamEventInfoAuxDyn.m_ll/1000. < 30']
        cutcomparisons['30 < m_{ll} < 40 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 30','HGamEventInfoAuxDyn.m_ll/1000. < 40']
        cutcomparisons['40 < m_{ll} < 50 GeV'] = ['HGamEventInfoAuxDyn.m_ll/1000. > 40','HGamEventInfoAuxDyn.m_ll/1000. < 50']

    return cutcomparisons

def cutcomparisons_SculptingStudy(variable='photonpt') :

    from collections import OrderedDict
    cutcomparisons = OrderedDict()

    # Photons (absolute)
    if variable == 'photonpt_abs' :
        cutcomparisons['p^{#gamma}_{T} > 31.5 GeV'] = ['HGamPhotonsAuxDyn.pt[0]/1000. > 31.5']
        cutcomparisons['p^{#gamma}_{T} > 35 GeV'] = ['HGamPhotonsAuxDyn.pt[0]/1000. > 35']
        cutcomparisons['p^{#gamma}_{T} > 40 GeV'] = ['HGamPhotonsAuxDyn.pt[0]/1000. > 40']
        cutcomparisons['p^{#gamma}_{T} > 50 GeV'] = ['HGamPhotonsAuxDyn.pt[0]/1000. > 50']

    # Photons (relative)
    elif variable == 'photonpt_rel' :
        cutcomparisons['p^{#gamma}_{T}/m_{ll#gamma} > 0.30'] = ['HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.30']
        cutcomparisons['p^{#gamma}_{T}/m_{ll#gamma} > 0.33'] = ['HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.3333']
        cutcomparisons['p^{#gamma}_{T}/m_{ll#gamma} > 0.38'] = ['HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.38']
        cutcomparisons['p^{#gamma}_{T}/m_{ll#gamma} > 0.475'] = ['HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.475']

    # leading muon (absolute)
    elif variable == 'leading_muon_abs' :
        cutcomparisons['p^{#mu^{}0}_{T} > 11 GeV']   = ['HGamMuonsAuxDyn.pt[0]/1000. > 11']
        cutcomparisons['p^{#mu^{}0}_{T} > 20 GeV']   = ['HGamMuonsAuxDyn.pt[0]/1000. > 20']
        cutcomparisons['p^{#mu^{}0}_{T} > 31.5 GeV'] = ['HGamMuonsAuxDyn.pt[0]/1000. > 31.5']
        cutcomparisons['p^{#mu^{}0}_{T} > 35 GeV']   = ['HGamMuonsAuxDyn.pt[0]/1000. > 35']
        cutcomparisons['p^{#mu^{}0}_{T} > 40 GeV']   = ['HGamMuonsAuxDyn.pt[0]/1000. > 40']
        cutcomparisons['p^{#mu^{}0}_{T} > 50 GeV']   = ['HGamMuonsAuxDyn.pt[0]/1000. > 50']

    # dimuon (relative)
    elif variable == 'leading_muon_rel' :
        cutcomparisons['p^{ll}_{T}/m_{ll#gamma} > 0.30'] = ['HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.30']
        cutcomparisons['p^{ll}_{T}/m_{ll#gamma} > 0.33'] = ['HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.3333']
        cutcomparisons['p^{ll}_{T}/m_{ll#gamma} > 0.38'] = ['HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.38']
        cutcomparisons['p^{ll}_{T}/m_{ll#gamma} > 0.475'] = ['HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.475']

    else :
        print 'cutcomparisons_SculptingStudy: Do not understand variable %s. Doing nothing.'%(variable)

    return cutcomparisons


def forwardJetStudyModifications(cuts,mergesamples,labels,
                                 requireCentralCentral=False,
                                 requireAtLeastOneFwd=True,
                                 fwdjetcut=35) :
    # Add snippets to perform the forward jet study.
    # Everything is applied to the reference objects; no new objects are made.

    # The pt cuts on the forward jet
    cuts.append('(HGamAntiKt4EMPFlowJetsAuxDyn.pt[0]/1000. > %d || abs(HGamAntiKt4EMPFlowJetsAuxDyn[0].eta) < 2.5)'%(fwdjetcut))
    cuts.append('(HGamAntiKt4EMPFlowJetsAuxDyn.pt[1]/1000. > %d || abs(HGamAntiKt4EMPFlowJetsAuxDyn[1].eta) < 2.5)'%(fwdjetcut))

    if requireCentralCentral :
        cuts.append('abs(HGamAntiKt4EMPFlowJetsAuxDyn[0].eta) < 2.5 && abs(HGamAntiKt4EMPFlowJetsAuxDyn[1].eta) < 2.5')

    if requireAtLeastOneFwd :
        cuts.append('abs(HGamAntiKt4EMPFlowJetsAuxDyn[0].eta) > 2.5 || abs(HGamAntiKt4EMPFlowJetsAuxDyn[1].eta) > 2.5')

    # Split the samples into "VBF" and "others"
    mergesamples['AllHiggs'] = '%34596%'
    mergesamples['VBF'] = '%345834%'
    labels['AllHiggs'] = 'ggF+others%s'%('^{ }#times^{ }%d'%(higgsSF) if higgsSF != 1 else '')
    labels['VBF'] = 'VBF%s'%('^{ }#times^{ }%d'%(higgsSF) if higgsSF != 1 else '')

    return
