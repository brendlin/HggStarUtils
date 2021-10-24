
from HggStarHelpers import YEAR,GetFbForMCNormalization
from HggStarHelpers import ChannelEnum,CategoryEnum
import StudyConfSnippets
import sys

treename = 'CollectionTree'
theyear = YEAR.y2015161718

from HggStarHelpers import StandardSampleMerging as mergesamples

from HggStarHelpers import StandardHistFormat as histformat
histformat['HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1'] = [100,0,0.33,histformat['HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1'][3]]

from HggStarHelpers import StandardPlotLabels as labels
labels['AllHiggs'] = 'H#rightarrow#gamma*#gamma'

cuts = [
    'HGamTruthEventInfoAuxDyn.m_ll/1000. < 50.',
    'HGamTruthEventInfoAuxDyn.yyStarChannel > 1',

    'fabs(HGamTruthElectronsAuxDyn.eta[0]) < 2.5',
    'HGamTruthElectronsAuxDyn.pt[0]/1000. > 10',

    'fabs(HGamTruthElectronsAuxDyn.eta[1]) < 2.5',
    'HGamTruthElectronsAuxDyn.pt[1]/1000. > 10',

    'fabs(HGamTruthPhotonsAuxDyn.eta[0]) < 2.5',
    'HGamTruthPhotonsAuxDyn.pt[0]/1000. > 30',
    ]

from HggStarHelpers import weightscale_hyystar_yearAware
def weightscale(tfile) :
    return weightscale_hyystar_yearAware(tfile,theyear,1)

variables = [
    'HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1',
]
