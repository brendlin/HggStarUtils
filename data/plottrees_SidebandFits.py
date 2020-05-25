
# Usage: plottrees.py 1 1 --config plottrees_SidebandFits.py --data data%.root --ratio --poisson --batch --outdir c01_sbFit

from HggStarHelpers import YEAR,GetFbForMCNormalization
from HggStarHelpers import ChannelEnum,CategoryEnum
import StudyConfSnippets
from HggStarHelpers import StandardSampleMerging as mergesamples
from HggStarHelpers import StandardHistFormat as histformat
histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [55,105,160,'m_{ll#gamma} [GeV]']

treename = 'CollectionTree'

class REGION :
    CR1 = 0
    CR2 = 1
    SR = 2
    SR_VBF = 3
    OBJ_CR = 4

###
# Change this to check out different channels / years:
###
import sys
channel = int(sys.argv[1])
category = int(sys.argv[2])
region = REGION.SR
higgsSF = 100
theyear = YEAR.y2015161718
doMesonCuts = True
doDetailedVariables = False
##
# End configuration.
##

fb = GetFbForMCNormalization(theyear)

leptonObj = {ChannelEnum.DIMUON: 'Muons',
             ChannelEnum.RESOLVED_DIELECTRON:'Electrons',
             ChannelEnum.MERGED_DIELECTRON:  'Electrons',
             }.get(channel,None)

from HggStarHelpers import GetPlotText
plottext = GetPlotText(channel,category)
if region == REGION.SR_VBF :
    plottext = plottext.replace('channel','VBF category')

from HggStarHelpers import StandardPlotLabels as labels
labels['AllHiggs'] = 'H#rightarrow#gamma*#gamma%s'%('^{ }#times^{ }%d'%(higgsSF) if higgsSF != 1 else '')
if region == REGION.SR :
    labels['data'] = 'Data Sideband'

cuts = [
    'HGamEventInfoAuxDyn.isPassedObjSelection', # object selection
    'HGamEventInfoAuxDyn.isPassedEventSelection', # object selection
#     'HGamElectronsAuxDyn.pt[0] < 40000.',
    ]

if channel :
    cuts.append('HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel))

if category :
    cuts.append('HGamEventInfoAuxDyn.yyStarCategory == %d'%(category))

if region in [REGION.CR1, REGION.CR2, REGION.SR, REGION.SR_VBF] :
    cuts += [
        '(HGamEventInfoAuxDyn.m_lly > 105000 && HGamEventInfoAuxDyn.m_lly < 160000)',
        'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly > 0.3', # new cuts
        'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly > 0.3', # new cuts
        ]

blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]

##
## Standard Variables
##
variables = [
    'HGamEventInfoAuxDyn.m_lly/1000.',
    ]

def afterburner(can) :
    import PlotFunctions as plotfunc
    import TAxisFunctions as taxisfunc
    import ROOT
    import math

    # Fix fb label for 2015-only and 2016-only (see important notes above)
    if theyear in [YEAR.y2015,YEAR.y2016] :
        fb = {YEAR.y2015:3.2,YEAR.y2016:33.0}.get(theyear)
        text_can = can
        if plotfunc.GetTopPad(can) :
            text_can = plotfunc.GetTopPad(can)
        for prim in text_can.GetListOfPrimitives() :
            if '_text' in prim.GetName() :
                for entry in prim.GetListOfPrimitives() :
                    if '36.2' in entry.GetLabel() :
                        entry.SetLabel(entry.GetLabel().replace('36.2','%.1f'%(fb)))
        text_can.Modified()


    # print list(plotfunc.GetTopPad(can).GetListOfPrimitives())
    hist = plotfunc.GetTopPad(can).GetPrimitive('pad_top_data')
    ratioplot = hist.Clone()
    ratioplot.GetYaxis().SetTitle('pull')
    ratioplot.GetXaxis().SetTitle('m_{ll#gamma} [GeV]')

    bkg_parameters_block = '''
nbkg_muons_incl2015-18_mu      = 11878.2     +/-  120.399    (limited)
a1_muons_incl2015-18_mu      = -4.53852     +/-  0.179633    (limited)
a2_muons_incl2015-18_mu      = 3.30439     +/-  0.165049    (limited)
a3_muons_incl2015-18_mu      = -1.47459     +/-  0.508958    (limited)

nbkg_resolved_incl2015-18_mu      = 5334.09     +/-  83.7904    (limited)
a1_resolved_incl2015-18_mu      = -3.60607     +/-  0.455044    (limited)
a2_resolved_incl2015-18_mu      = 0.00628578     +/-  0.762606    (limited)

nbkg_merged_incl2015-18_mu      = 6180.67     +/-  90.8015    (limited)
a1_merged_incl2015-18_mu      = -1.79265     +/-  0.393113    (limited)
a2_merged_incl2015-18_mu      = -0.500681     +/-  0.648747    (limited)

nbkg_muons_vbf2015-18_mu      = 38.9094     +/-  6.96168    (limited)
slope_muons_vbf2015-18_mu      = -0.0243778     +/-  0.0107391    (limited)

nbkg_resolved_vbf2015-18_mu      = 12.5782     +/-  3.9915    (limited)
slope_resolved_vbf2015-18_mu      = -0.0286611     +/-  0.0190401    (limited)

nbkg_merged_vbf2015-18_mu      = 23.7751     +/-  5.48928    (limited)
slope_merged_vbf2015-18_mu      = -0.0459791     +/-  0.0148474    (limited)

nbkg_muons_highptt2015-18_mu      = 237.156     +/-  17.191    (limited)
lambda_muons_highptt2015-18_mu      = -1.72409     +/-  0.546747    (limited)

nbkg_resolved_highptt2015-18_mu      = 91.8353     +/-  10.7243    (limited)
lambda_resolved_highptt2015-18_mu      = -1.61933     +/-  0.931285    (limited)

nbkg_merged_highptt2015-18_mu      = 185.889     +/-  15.1875    (limited)
lambda_merged_highptt2015-18_mu      = -0.67296     +/-  0.618264    (limited)
'''

    tmp_name = {
        1 : 'muons_incl2015-18_mu',
        2 : 'resolved_incl2015-18_mu',
        3 : 'merged_incl2015-18_mu',
        4 : 'muons_vbf2015-18_mu',
        5 : 'resolved_vbf2015-18_mu',
        6 : 'merged_vbf2015-18_mu',
        7 : 'muons_highptt2015-18_mu',
        8 : 'resolved_highptt2015-18_mu',
        9 : 'merged_highptt2015-18_mu',
        }.get(category)

    function = {
        1:'ExpPoly3',
        2:'ExpPoly2',
        3:'ExpPoly2',
        4:'Exponential',
        5:'Exponential',
        6:'Exponential',
        7:'Power Law',
        8:'Power Law',
        9:'Power Law',
        }.get(category)

    expr = {
        'ExpPoly3':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100 + [3]*(x - 100)/100*(x - 100)/100))',
        'ExpPoly2':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100))',
        'ExpPoly2':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100))',
        'Exponential':'[0]*exp(x*[1])',
        'Power Law':'[0]*TMath::Power((x*1),[1])',
        }.get(function)

    f_bkg = ROOT.TF1(function,expr,105,160)
    f_bkg.SetTitle(function)

    translation = {
        'c1':'muons_incl2015-18_mu',
        'c2':'resolved_incl2015-18_mu',
        'c3':'merged_incl2015-18_mu',
        'c4':'muons_vbf2015-18_mu',
        'c5':'resolved_vbf2015-18_mu',
        'c6':'merged_vbf2015-18_mu',
        'c7':'muons_highptt2015-18_mu',
        'c8':'resolved_highptt2015-18_mu',
        'c9':'merged_highptt2015-18_mu',
        }

    parameters = dict()
    for i in bkg_parameters_block.split('\n') :
        if not i : continue
        key = i.split()[0]
        for t in translation.keys() :
            key = key.replace(translation[t],t)
        parameters[key] = float(i.split()[2])

    cstr = 'c%d'%(category)
    if function in ['ExpPoly3','ExpPoly2'] :
        par = parameters['a1_%s'%(cstr)]
        f_bkg.SetParameter(1,par)
    if function in ['ExpPoly3','ExpPoly2'] :
        par = parameters['a2_%s'%(cstr)]
        f_bkg.SetParameter(2,par)
    if function in ['ExpPoly3'] :
        par = parameters['a3_%s'%(cstr)]
        f_bkg.SetParameter(3,par)
    if function in ['Power Law'] :
        par = parameters['lambda_%s'%(cstr)]
        f_bkg.SetParameter(1,par)
    if function in ['Exponential'] :
        par = parameters['slope_%s'%(cstr)]
        f_bkg.SetParameter(1,par)

    f_bkg.SetParameter(0,1)
    integral = f_bkg.Integral(105,160)
    f_bkg.SetParameter(0,parameters['nbkg_%s'%(cstr)]/float(integral))
    f_bkg.SetLineColor(ROOT.kBlue)
    plotfunc.AddHistogram(can,f_bkg,'l')
    ranges = plotfunc.AutoFixYaxis(plotfunc.GetTopPad(can))
    plotfunc.SetYaxisRanges(plotfunc.GetTopPad(can),0.001,ranges[1])

    # Pull!
    for i in range(ratioplot.GetNbinsX()+2) :
        bc1 = hist.GetBinContent(i)
        bc2 = f_bkg.Eval(hist.GetBinCenter(i)) #ref_hist.GetBinContent(i)
        be1 = hist    .GetBinErrorLow(i) if (bc1 > bc2) else hist    .GetBinErrorUp(i)
        be2 = 0 # ref_hist.GetBinErrorLow(i) if (bc2 > bc1) else ref_hist.GetBinErrorUp(i)

        if (be1**2 + be2**2) :
            ratioplot.SetBinContent(i,(bc1-bc2)/math.sqrt(be1**2+be2**2))
        ratioplot.SetBinError(i,1)

        if 120 < hist.GetBinCenter(i) and hist.GetBinCenter(i) < 130 :
            ratioplot.SetBinContent(i,-99)

    plotfunc.AddHistogram(can.GetPrimitive('pad_bot'),ratioplot,drawopt='pE1')

    # Set ratio range; add dotted line at 1
    if plotfunc.GetBotPad(can) :
        taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(can),-4,4)
        xmin,xmax = None,None
        for i in plotfunc.GetBotPad(can).GetListOfPrimitives() :
            if issubclass(type(i),ROOT.TH1) :
                xmin = i.GetXaxis().GetBinLowEdge(1)
                xmax = i.GetXaxis().GetBinLowEdge(i.GetNbinsX()+1)
        if xmin != None :
            line = ROOT.TLine(xmin,0,xmax,0)
            line.SetLineStyle(2)
            plotfunc.GetBotPad(can).cd()
            line.Draw()
            plotfunc.tobject_collector.append(line)

    plotfunc.MakeLegend(can,totalentries=2)
    plotfunc.AddHistogram(can,hist)
    plotfunc.FormatCanvasAxes(can)

    return
