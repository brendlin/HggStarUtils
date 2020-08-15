trigger_numbers =  {
    'e24_lhmedium_L1EM20VH': '0',
    'e60_lhmedium': '1',
    'e120_lhloose': '2',
    '2e12_lhloose_L12EM10VH': '3',
    'e26_lhtight_nod0_ivarloose': '4',
    'e60_lhmedium_nod0': '5',
    'e140_lhloose_nod0': '6',
    '2e17_lhvloose_nod0': '7',
    '2e24_lhvloose_nod0': '8',
    'mu20_iloose_L1MU15': '9',
    'mu40': '10',
    '2mu10': '11',
    'mu18_mu8noL1': '12',
    'mu26_ivarmedium': '13',
    'mu50': '14',
    '2mu14': '15',
    'mu22_mu8noL1': '16',
    'e20_lhmedium_g35_loose': '17',
    'e20_lhmedium_nod0_g35_loose': '18',
    'e25_mergedtight_g35_medium_Heg': '19',
    'g35_loose_g25_loose': '20',
    'g35_medium_g25_medium_L12EM20VH': '21',
    'g25_medium_mu24': '22',
    'g35_loose_L1EM22VHI_mu18noL1': '23',
    'g35_loose_L1EM24VHI_mu18': '24',
    'g35_tight_icalotight_L1EM24VHI_mu18noL1': '25',
    'g15_loose_2mu10_msonly': '26',
    'g35_loose_L1EM22VHI_mu15noL1_mu2noL1': '27',
    'g35_loose_L1EM24VHI_mu15_mu2noL1': '28',
    'g35_tight_icalotight_L1EM24VHI_mu15noL1_mu2noL1': '29',
}


treename = 'CollectionTree'

blindcut = ['(120000 > HGamEventInfoAuxDyn.m_lly || HGamEventInfoAuxDyn.m_lly > 130000)']



labels = {
    '%345961%':'ggH H#rightarrow#gamma*#gamma',
    }

# Truth muons passed selection
cuts = [
    'HGamTruthEventInfoAuxDyn.yyStarChannel == 3',
    'HGamEventInfoAuxDyn.isPassedEventSelection'
    ]

year = '2018'
mu_triggers = {}
mu_triggers['2015'] = ['mu20_iloose_L1MU15','mu40', '2mu10', 'mu18_mu8noL1', 'g25_medium_mu24', 'g15_loose_2mu10_msonly']
mu_triggers['2016'] = ['g35_loose_L1EM22VHI_mu18noL1','g35_loose_L1EM22VHI_mu15noL1_mu2noL1','mu26_ivarmedium','mu50','2mu14','mu22_mu8noL1','g25_medium_mu24','g15_loose_2mu10_msonly']
mu_triggers['2017'] = ['g35_loose_L1EM24VHI_mu18','g35_loose_L1EM24VHI_mu15_mu2noL1','g35_tight_icalotight_L1EM24VHI_mu18noL1','g35_tight_icalotight_L1EM24VHI_mu15noL1_mu2noL1','mu26_ivarmedium','mu50','2mu14','mu22_mu8noL1','g25_medium_mu24','g15_loose_2mu10_msonly']
mu_triggers['2018'] = ['g35_loose_L1EM24VHI_mu18','g35_loose_L1EM24VHI_mu15_mu2noL1','g35_tight_icalotight_L1EM24VHI_mu18noL1','g35_tight_icalotight_L1EM24VHI_mu15noL1_mu2noL1','mu26_ivarmedium','mu50','2mu14','mu22_mu8noL1','g25_medium_mu24','g15_loose_2mu10_msonly']

import collections
cutcomparisons = collections.OrderedDict()

cutcomparisons[year + ': no trig'] = []
cutcomparisons[year + ': any trig'] = ['HGamEventInfoAuxDyn.isPassedTriggers']
#for trig in mu_triggers[year]:
    #cutcomparisons[year + ': ' + trig] = ['HGamEventInfoAuxDyn.triggerBitset & (0x1 << ' + trigger_numbers[trig] + ')']
    #cutcomparisons[year + ': only ' + trig] = ['HGamEventInfoAuxDyn.triggerBitset == (0x1 << ' + trigger_numbers[trig] + ')']
    
if year == '2015':
    cuts.append('EventInfoAuxDyn.RandomRunNumber<=284484')
elif year == '2016':
    cuts.append('EventInfoAuxDyn.RandomRunNumber>284484')
    


variables = [
        #'HGamMuonsAuxDyn.pt[0]/1000.',
        #'HGamElectronsAuxDyn.pt[0]/1000.',
        #'HGamMuonsAuxDyn.pt[1]/1000.',
                #'HGamElectronsAuxDyn.pt[1]/1000.',
        'HGamPhotonsAuxDyn.pt[0]/1000.',
        'HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1',
        #'HGamMuonsAuxDyn.eta[0]',
        #'HGamMuonsAuxDyn.eta[1]',
        'HGamGSFTrackParticlesAuxDyn.pt[0]/1000'
    ]
    


histformat = {
    'HGamGSFTrackParticlesAuxDyn.pt[0]/1000': [25,0,100,'p^{trk0}_{T} [GeV]'],
    'HGamElectronsAuxDyn.topoetcone20/1000' :[60,-5,10, 'e topoetcone20/1000'],
    'HGamPhotonsAuxDyn.topoetcone20/1000' :[60,-5,10, '#gamma topoetcone20/1000'],
    'HGamElectronsAuxDyn.pt[0]/1000.':[25,0,100,'p^{e lead}_{T}'],
    'HGamElectronsAuxDyn.pt[1]/1000.':[25,0,100,'p^{e sublead}_{T}'],
        'HGamMuonsAuxDyn.pt[0]/1000.':[25,0,100,'p^{#mu lead}_{T}'],
        'HGamMuonsAuxDyn.pt[1]/1000.':[25,0,100,'p^{#mu sublead}_{T}'],
        'HGamMuonsAuxDyn.eta[0]':[50,-4,4,'#eta^{#mu lead}'],
        'HGamMuonsAuxDyn.eta[1]':[50,-4,4,'#eta^{#mu sublead}'],
    'HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1'     :[25,0,0.25,'Truth #Delta^{}R(lep1,lep2)'],
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
    'HGamPhotonsAuxDyn.pt[0]/1000.':[25,0,150,'p^{#gamma}_{T}'],
    'HGamTruthPhotonsAuxDyn.pt[0]/1000.':[100,0,200,'truth p^{#gamma}_{T}'],
    'HGamEventInfoAuxDyn.m_lly_track4mom/1000.':[100,0,200,'m_{ll#gamma} (using track 4-mom) [GeV]'],
    'HGamEventInfoAuxDyn.m_ll_track4mom/1000.':[100,0,50,'m_{ll} (using track 4-mom) [GeV]'],
    'HGamEventInfoAuxDyn.m_ll_track4mom/HGamTruthEventInfoAuxDyn.m_yStar_undressed_h1':[100,0,2,'m^{trk4mom}_{ll}/m^{true,undressed}_{#gamma*}'],
    'HGamEventInfoAuxDyn.m_lly_track4mom/HGamTruthEventInfoAuxDyn.m_lly':[100,0,2,'m^{trk4mom}_{ll#gamma}/m^{true,undressed}_{ll#gamma}'],
    }

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

import HggStarHelpers
from HggStarHelpers import StandardSampleMerging as mergesamples
from HggStarHelpers import StandardPlotLabels as labels
weightscale = HggStarHelpers.weightscale_hyystar
#from HggStarHelpers import weightscale_hyystar,SF_139fb


#def weightscale(tfile) :
    #weight = weightscale_hyystar(tfile)


    #weight = weight* SF_139fb(tfile)

    #return weight


def afterburner(can) :
    import TAxisFunctions

    if can.GetPrimitive('pad_bot') :
        TAxisFunctions.SetYaxisRanges(can.GetPrimitive('pad_bot'),0.9,1.1)

    return
