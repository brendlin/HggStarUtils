
def appendMesonCuts(cuts,channel) :
    # For applying the meson cuts by hand
    from HggStarHelpers import ChannelEnum

    if channel in [ChannelEnum.RESOLVED_DIELECTRON, ChannelEnum.MERGED_DIELECTRON] :
        cuts.append('!(HGamEventInfoAuxDyn.m_ll > 2500. && HGamEventInfoAuxDyn.m_ll <  3500.)')
        cuts.append('!(HGamEventInfoAuxDyn.m_ll > 8000. && HGamEventInfoAuxDyn.m_ll < 11000.)')

    if channel == ChannelEnum.DIMUON :
        cuts.append('!(HGamEventInfoAuxDyn.m_ll > 2900. && HGamEventInfoAuxDyn.m_ll <  3300.)')
        cuts.append('!(HGamEventInfoAuxDyn.m_ll > 9100. && HGamEventInfoAuxDyn.m_ll < 10600.)')

    return


def cutcomparisons_MllSliceStudy(truth=False) :
    # Mass cut slicing study
    from collections import OrderedDict
    cutcomparisons = OrderedDict()

    if truth :
        cutcomparisons['0 < m_{ll} < 2 GeV'] = ['HGamTruthEventInfoAuxDyn.m_ll/1000. < 2']
        cutcomparisons['2 < m_{ll} < 10 Gev'] = ['HGamTruthEventInfoAuxDyn.m_ll/1000. > 2' ,'HGamTruthEventInfoAuxDyn.m_ll/1000. < 10']
        cutcomparisons['10 < m_{ll} < 20 GeV'] = ['HGamTruthEventInfoAuxDyn.m_ll/1000. > 10','HGamTruthEventInfoAuxDyn.m_ll/1000. < 20']
        cutcomparisons['20 < m_{ll} < 30 GeV'] = ['HGamTruthEventInfoAuxDyn.m_ll/1000. > 20','HGamTruthEventInfoAuxDyn.m_ll/1000. < 30']
        cutcomparisons['30 < m_{ll} < 40 GeV'] = ['HGamTruthEventInfoAuxDyn.m_ll/1000. > 30','HGamTruthEventInfoAuxDyn.m_ll/1000. < 40']
        cutcomparisons['40 < m_{ll} < 50 GeV'] = ['HGamTruthEventInfoAuxDyn.m_ll/1000. > 40','HGamTruthEventInfoAuxDyn.m_ll/1000. < 50']

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
        cutcomparisons['p^{#gamma}_{T} > 31.5 GeV'] = ['HGamTruthPhotonsAuxDyn.pt[0]/1000. > 31.5']
        cutcomparisons['p^{#gamma}_{T} > 35 GeV'] = ['HGamTruthPhotonsAuxDyn.pt[0]/1000. > 35']
        cutcomparisons['p^{#gamma}_{T} > 40 GeV'] = ['HGamTruthPhotonsAuxDyn.pt[0]/1000. > 40']
        cutcomparisons['p^{#gamma}_{T} > 50 GeV'] = ['HGamTruthPhotonsAuxDyn.pt[0]/1000. > 50']

    # Photons (relative)
    elif variable == 'photonpt_rel' :
        cutcomparisons['p^{#gamma}_{T}/m_{ll#gamma} > 0.30'] = ['HGamTruthPhotonsAuxDyn.pt[0]/HGamTruthEventInfoAuxDyn.m_lly > 0.30']
        cutcomparisons['p^{#gamma}_{T}/m_{ll#gamma} > 0.33'] = ['HGamTruthPhotonsAuxDyn.pt[0]/HGamTruthEventInfoAuxDyn.m_lly > 0.3333']
        cutcomparisons['p^{#gamma}_{T}/m_{ll#gamma} > 0.38'] = ['HGamTruthPhotonsAuxDyn.pt[0]/HGamTruthEventInfoAuxDyn.m_lly > 0.38']
        cutcomparisons['p^{#gamma}_{T}/m_{ll#gamma} > 0.475'] = ['HGamTruthPhotonsAuxDyn.pt[0]/HGamTruthEventInfoAuxDyn.m_lly > 0.475']

    # leading muon (absolute)
    elif variable == 'leading_muon_abs' :
        cutcomparisons['p^{#mu^{}0}_{T} > 11 GeV']   = ['HGamTruthMuonsAuxDyn.pt[0]/1000. > 11']
        cutcomparisons['p^{#mu^{}0}_{T} > 20 GeV']   = ['HGamTruthMuonsAuxDyn.pt[0]/1000. > 20']
        cutcomparisons['p^{#mu^{}0}_{T} > 31.5 GeV'] = ['HGamTruthMuonsAuxDyn.pt[0]/1000. > 31.5']
        cutcomparisons['p^{#mu^{}0}_{T} > 35 GeV']   = ['HGamTruthMuonsAuxDyn.pt[0]/1000. > 35']
        cutcomparisons['p^{#mu^{}0}_{T} > 40 GeV']   = ['HGamTruthMuonsAuxDyn.pt[0]/1000. > 40']
        cutcomparisons['p^{#mu^{}0}_{T} > 50 GeV']   = ['HGamTruthMuonsAuxDyn.pt[0]/1000. > 50']

    # dimuon (relative)
    elif variable == 'leading_muon_rel' :
        cutcomparisons['p^{ll}_{T}/m_{ll#gamma} > 0.30'] = ['HGamTruthEventInfoAuxDyn.pt_ll/HGamTruthEventInfoAuxDyn.m_lly > 0.30']
        cutcomparisons['p^{ll}_{T}/m_{ll#gamma} > 0.33'] = ['HGamTruthEventInfoAuxDyn.pt_ll/HGamTruthEventInfoAuxDyn.m_lly > 0.3333']
        cutcomparisons['p^{ll}_{T}/m_{ll#gamma} > 0.38'] = ['HGamTruthEventInfoAuxDyn.pt_ll/HGamTruthEventInfoAuxDyn.m_lly > 0.38']
        cutcomparisons['p^{ll}_{T}/m_{ll#gamma} > 0.475'] = ['HGamTruthEventInfoAuxDyn.pt_ll/HGamTruthEventInfoAuxDyn.m_lly > 0.475']

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
