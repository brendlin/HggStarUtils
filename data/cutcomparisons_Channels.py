
treename = 'CollectionTree'

blindcut = ['(120000 > HGamEventInfoAuxDyn.m_lly || HGamEventInfoAuxDyn.m_lly > 130000)']

class CHANNEL :
    CHANNELUNKNOWN = 0
    DIMUON = 1
    RESOLVED_DIELECTRON = 2
    MERGED_DIELECTRON = 3

from HggStarHelpers import StandardPlotLabels,StandardSampleMerging
mergesamples = StandardSampleMerging
labels = StandardPlotLabels

# These are the preselection cuts
cuts = [
    'HGamEventInfoAuxDyn.isPassedEventSelection',
    ]

cutcomparisons = {
    '#mu#mu#gamma'      :['HGamEventInfoAuxDyn.yyStarChannel == %d'%(CHANNEL.DIMUON              )],
    'ee#gamma resolved' :['HGamEventInfoAuxDyn.yyStarChannel == %d'%(CHANNEL.RESOLVED_DIELECTRON )],
    'ee#gamma merged'   :['HGamEventInfoAuxDyn.yyStarChannel == %d'%(CHANNEL.MERGED_DIELECTRON   )],
    }

variables = [
    'HGamEventInfoAuxDyn.m_lly/1000.',
    'HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1',
    ]

histformat = {
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
    'HGamEventInfoAuxDyn.pt_ll/1000.':[100,0,150,'p_{T,ll}'],
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
