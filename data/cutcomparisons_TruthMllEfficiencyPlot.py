
from HggStarHelpers import YEAR,GetFbForMCNormalization
from HggStarHelpers import ChannelEnum,CategoryEnum
import StudyConfSnippets
import HggStarHelpers
import sys

treename = 'CollectionTree'
theyear = YEAR.y2015161718
fb = GetFbForMCNormalization(theyear)

from HggStarHelpers import StandardSampleMerging as mergesamples
from HggStarHelpers import StandardHistFormat as histformat
from HggStarHelpers import StandardPlotLabels as labels

labels['AllHiggs'] = 'higgs'

m_yStar = 'HGamTruthEventInfoAuxDyn.m_yStar_born_h1/1000.'
mll_reco = 'HGamEventInfoAuxDyn.m_ll/1000.'

#histformat[m_yStar]  = [100,0.000,0.010,'True (born) m_{#gamma*} [GeV]']
#histformat[m_yStar]  = [2818283,0.001,28.18383,'True (born) m_{#gamma*} [GeV]']
histformat[m_yStar]   = [2511786,0.001,25.11886,'True (born) m_{#gamma*} [GeV]']
#histformat[m_yStar]  = [100,0,0.05,'True (born) m_{#gamma*} [GeV]']
#histformat[m_yStar]  = [100,0.18,2.5 ,'True (born) m_{#gamma*} [GeV]']
#histformat[m_yStar]  = [100,0,5. ,'True (born) m_{#gamma*} [GeV]']
#histformat[m_yStar]  = [100,0,1. ,'True (born) m_{#gamma*} [GeV]']
#histformat[m_yStar]  = [100,0,10. ,'True (born) m_{#gamma*} [GeV]']
histformat[mll_reco] = [100,0,0.005,histformat[mll_reco][3]]
dr = 'HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1'
histformat[dr] = [100,0,0.3,histformat[dr][3]]

# 45 bins between [0.001, ... 25.11886, 31.62278]
# list( float('%.5f'%(math.pow(10,x/float(10)))) for x in range(-30,16))

rebin = {
    #m_yStar: HggStarHelpers.customRebin(0,3,0.2, 30,1, 40,2, 50,5)
    #m_yStar: [0.001, 0.00112, 0.00126, 0.00141, 0.00158, 0.00178, 0.002, 0.00224, 0.00251, 0.00282, 0.00316, 0.00355, 0.00398, 0.00447, 0.00501, 0.00562, 0.00631, 0.00708, 0.00794, 0.00891, 0.01, 0.01122, 0.01259, 0.01413, 0.01585, 0.01778, 0.01995, 0.02239, 0.02512, 0.02818, 0.03162, 0.03548, 0.03981, 0.04467, 0.05012, 0.05623, 0.0631, 0.07079, 0.07943, 0.08913, 0.1, 0.1122, 0.12589, 0.14125, 0.15849, 0.17783, 0.19953, 0.22387, 0.25119, 0.28184, 0.31623, 0.35481, 0.39811, 0.44668, 0.50119, 0.56234, 0.63096, 0.70795, 0.79433, 0.89125, 1.0, 1.12202, 1.25893, 1.41254, 1.58489, 1.77828, 1.99526, 2.23872, 2.51189, 2.81838, 3.16228, 3.54813, 3.98107, 4.46684, 5.01187, 5.62341, 6.30957, 7.07946, 7.94328, 8.91251, 10.0, 11.22018, 12.58925, 14.12538, 15.84893, 17.78279, 19.95262, 22.38721, 25.11886, 28.18383],
    m_yStar: [0.001, 0.00126, 0.00158, 0.002, 0.00251, 0.00316, 0.00398, 0.00501, 0.00631, 0.00794, 0.01, 0.01259, 0.01585, 0.01995, 0.02512, 0.03162, 0.03981, 0.05012, 0.0631, 0.07943, 0.1, 0.12589, 0.15849, 0.19953, 0.25119, 0.31623, 0.39811, 0.50119, 0.63096, 0.79433, 1.0, 1.25893, 1.58489, 1.99526, 2.51189, 3.16228, 3.98107, 5.01187, 6.30957, 7.94328, 10.0, 12.58925, 15.84893, 19.95262, 25.11886],
    }

from HggStarHelpers import weightscale_hyystar_yearAware
def weightscale(tfile) :
    return weightscale_hyystar_yearAware(tfile,theyear,1)

variables = [
    m_yStar,
    #'HGamTruthEventInfoAuxDyn.deltaR_l1l2_h1',
    #'HGamEventInfoAuxDyn.m_ll/1000.',
    # 'HGamTruthEventInfoAuxDyn.yyStarChannelSimple',
    #'HGamEventInfoAuxDyn.cutFlow',
    ]

weightFinal = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'
weightInitial = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weightInitial'

cuts = [
    #'HGamTruthEventInfoAuxDyn.yyStarChannelSimple == 12',
    #'HGamTruthEventInfoAuxDyn.m_yStar_born_h1 < 0',
    #'HGamTruthEventInfoAuxDyn.m_yStar_born_h1/1000. < 0.1',
    'HGamEventInfoAuxDyn.cutFlow > 3',
    #
]

from collections import OrderedDict
cutcomparisons = OrderedDict()

selected = [
    'HGamEventInfoAuxDyn.isPassedObjSelection', # object selection
    '(HGamEventInfoAuxDyn.m_lly > 110000 && HGamEventInfoAuxDyn.m_lly < 160000)',
    'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.3', # new cuts
    'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.3', # new cuts
    ]

truthee = ['HGamTruthEventInfoAuxDyn.yyStarChannelSimple == 12']
truthmm = ['HGamTruthEventInfoAuxDyn.yyStarChannelSimple == 11']

cutcomparisons['generator-level ee'] = truthee
cutcomparisons['generator-level mm'] = truthmm
#cutcomparisons['signal-region events'] = selected
cutcomparisons['signal-region merged'] = selected + truthee + ['HGamEventInfoAuxDyn.yyStarChannel == 3']
cutcomparisons['signal-region resolved'] = selected + truthee + ['HGamEventInfoAuxDyn.yyStarChannel == 2']
cutcomparisons['signal-region elecs'] = selected + truthee + ['(HGamEventInfoAuxDyn.yyStarChannel == 2 || HGamEventInfoAuxDyn.yyStarChannel == 3)']
cutcomparisons['signal-region mm'] = selected + truthmm + ['HGamEventInfoAuxDyn.yyStarChannel == 1']

def afterburner(can) :
    import ROOT
    import PlotFunctions as plotfunc
    import PlotText

    # outfile = ROOT.TFile('truthmll.root','RECREATE')
    for i in can.GetListOfPrimitives() :
        if issubclass(type(i),ROOT.TH1) :
            i.SetName(i.GetTitle().split(',')[1].replace('-','_').replace(' ','_').lstrip('_'))

    for i in can.GetListOfPrimitives() :
         if issubclass(type(i),ROOT.TH1) :
             print i.GetName()

    hists = dict()
    hists['generator_level_ee']     = can.GetPrimitive('generator_level_ee'    ).Clone()
    hists['generator_level_mm']     = can.GetPrimitive('generator_level_mm'    ).Clone()
    hists['signal_region_merged']   = can.GetPrimitive('signal_region_merged'  ).Clone()
    hists['signal_region_resolved'] = can.GetPrimitive('signal_region_resolved').Clone()
    hists['signal_region_elecs']    = can.GetPrimitive('signal_region_elecs'   ).Clone()
    hists['signal_region_mm']       = can.GetPrimitive('signal_region_mm'      ).Clone()

    can.GetPrimitive('generator_level_ee'    ).Delete()
    can.GetPrimitive('generator_level_mm'    ).Delete()
    can.GetPrimitive('signal_region_merged'  ).Delete()
    can.GetPrimitive('signal_region_resolved').Delete()
    can.GetPrimitive('signal_region_elecs'   ).Delete()
    can.GetPrimitive('signal_region_mm'      ).Delete()

    # gen_ee_name = 'Total #font[12]{#scale[1.10]{ee}}#font[152]{#scale[1.0]{g}} yield'
    # gen_mm_name = 'Total #font[152]{#scale[1.0]{mmg}} yield'
    hysyeey = '#font[12]{H}#kern[0.15]{#rightarrow}#kern[0.1]{#font[152]{#scale[1.0]{g}}}#kern[-0.2]{*}#font[152]{#scale[1.0]{g}}#rightarrow#kern[0.1]{#font[12]{#scale[1.10]{ee}}}#font[152]{#scale[1.0]{g}} yield'
    hysymmy = '#font[12]{H}#kern[0.15]{#rightarrow}#kern[0.1]{#font[152]{#scale[1.0]{g}}}#kern[-0.2]{*}#font[152]{#scale[1.0]{g}}#rightarrow#font[152]{#scale[1.0]{mmg}} yield'
    gen_ee_name = '%s'%(hysyeey)
    gen_mm_name = '%s'%(hysymmy)

    hists['generator_level_ee'].SetTitle(gen_ee_name)
    hists['generator_level_mm'].SetTitle(gen_mm_name)
    hists['signal_region_merged'].SetTitle(' #font[12]{#scale[1.10]{ee}} merged')
    hists['signal_region_resolved'].SetTitle(' #font[12]{#scale[1.10]{ee}} resolved')
    hists['signal_region_elecs'].SetTitle('#font[12]{#scale[1.10]{ee}}#font[152]{#scale[1.0]{g}}:')
    hists['signal_region_mm'].SetTitle('#font[152]{#scale[1.0]{mmg}}')

    hists['generator_level_ee'].SetMarkerSize(1.2)
    hists['generator_level_mm'].SetMarkerSize(1.2)
    hists['signal_region_merged'].SetMarkerSize(1.2)
    hists['signal_region_resolved'].SetMarkerSize(1.2)
    hists['signal_region_elecs'].SetMarkerSize(1.2)
    hists['signal_region_mm'].SetMarkerSize(1.2)

    leftmax = 0.58
    rightmax = 17 # was 17 #1.1*hists['generator_level_ee'].GetMaximum();

    hists['signal_region_merged']  .Divide(hists['signal_region_merged']  ,hists['generator_level_ee'],1,1,'B')
    hists['signal_region_resolved'].Divide(hists['signal_region_resolved'],hists['generator_level_ee'],1,1,'B')
    hists['signal_region_elecs']   .Divide(hists['signal_region_elecs']   ,hists['generator_level_ee'],1,1,'B')
    hists['signal_region_mm']      .Divide(hists['signal_region_mm']      ,hists['generator_level_mm'],1,1,'B')

    # // scale hint1 to the pad coordinates
    scale = leftmax/rightmax;
    hists['generator_level_ee'].Scale(scale);
    hists['generator_level_mm'].Scale(scale);
    hists['generator_level_mm'].SetLineColor(ROOT.kBlue-9)
    hists['generator_level_ee'].SetLineColor(ROOT.kGray+1)
    hists['generator_level_ee'].SetFillStyle(3001)
    plotfunc.AddHistogram(can,hists['generator_level_ee'],drawopt='hist')
    plotfunc.AddHistogram(can,hists['generator_level_mm'],drawopt='hist')

    text = [plotfunc.GetAtlasInternalText(status='Simulation'),
            plotfunc.GetSqrtsText(13)]
    text[-1] += ', ' + plotfunc.GetLuminosityText(139.0)            
    plotfunc.DrawText(can,text,0.14,0.8,0.44,0.92,textsize=28)
    leg = plotfunc.MakeLegend(can,0.51,0.80,0.75,0.92,textsize=28,totalentries=2)
    leg.SetName('leg1')
    leg.SetTextColor(ROOT.kGray+2)

    hists['signal_region_merged'].SetLineColor(ROOT.kMagenta+3)
    hists['signal_region_merged'].SetMarkerColor(ROOT.kMagenta+3)
    hists['signal_region_merged'].SetMarkerStyle(24)
    hists['signal_region_resolved'].SetLineColor(ROOT.kRed+1)
    hists['signal_region_resolved'].SetMarkerColor(ROOT.kRed+1)
    hists['signal_region_resolved'].SetMarkerStyle(25)
    hists['signal_region_elecs'].SetLineColor(ROOT.kBlack)
    hists['signal_region_elecs'].SetMarkerColor(ROOT.kBlack)
    hists['signal_region_mm'].SetLineColor(ROOT.kBlue)
    hists['signal_region_mm'].SetMarkerColor(ROOT.kBlue)
    hists['signal_region_mm'].SetMarkerStyle(22)

    plotfunc.AddHistogram(can,hists['signal_region_merged'])
    plotfunc.AddHistogram(can,hists['signal_region_resolved'])
    plotfunc.AddHistogram(can,hists['signal_region_elecs'])
    plotfunc.AddHistogram(can,hists['signal_region_mm'])

    plotfunc.DrawText(can,'Signal efficiencies:',0.22,0.63,0.42,0.67,textsize=28)
    leg2 = plotfunc.MakeLegend(can,0.22,0.42,0.42,0.63,
                               textsize=28,
                               skip=[gen_ee_name,gen_mm_name],order=[3,2,0,1])

    plotfunc.SetYaxisRanges(can,0,leftmax)

    plotfunc.SetAxisLabels(can,'Born-level m_{%s} [GeV]'%(PlotText.ll),'Acceptance #times efficiency')
    can.SetLogx()
    plotfunc.FormatCanvasAxes800600(can,YTitleOffset=1.0,XTitleOffset=1.25)
    can.SetLeftMargin(0.11)
    can.SetRightMargin(0.11)
    can.SetBottomMargin(0.15)

    # // draw an axis on the right side
    axis = ROOT.TGaxis(25.11886,0,25.11886,leftmax,0,rightmax,510,'+L')
    # can.GetUxmax(),can.GetUymin(),
    #                    can.GetUxmax(),can.GetUymax(),0,rightmax,510,"+L")
    axis.SetLineColor(ROOT.kGray+2)
    axis.SetTextColor(ROOT.kGray+2)
    axis.SetLabelColor(ROOT.kGray+2)
    axis.SetLabelFont(43)
    axis.SetLabelSize(32)
    axis.SetTitleFont(43)
    axis.SetTitleSize(32)
    axis.SetTitleOffset(1.0)
    axis.SetTitle('Events^{ }/^{ }bin')
    can.cd()
    axis.Draw()
    plotfunc.tobject_collector.append(axis)

    can.RedrawAxis();
    can.Modified(); can.Update();
    can.Modified(); can.Update();
    

    if plotfunc.GetTopPad(can) :
        plotfunc.SetXaxisRanges(plotfunc.GetTopPad(can),0.001,25)
        plotfunc.GetTopPad(can).SetLogx()

    if plotfunc.GetBotPad(can) :
        plotfunc.SetXaxisRanges(plotfunc.GetBotPad(can),0.001,25)
        plotfunc.GetBotPad(can).SetLogx()

    return


weight = {
    'generator-level ee' : weightInitial,
    'generator-level mm' : weightInitial,
    'signal-region merged'  : weightFinal,
    'signal-region resolved': weightFinal,
    'signal-region elecs'   : weightFinal,
    'signal-region mm'      : weightFinal,
}
