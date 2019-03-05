
# Command that works with ysy001 ntuples:
# plottrees.py --config plottrees_ZmumuyValidationConf.py --bkgs %Sherpa_CT10%mumugamma%r9364%.root --data ysy001.data16.%.root,ysy001.data15.p3083_p3402.root --fb 36.2 --log --signal %gamstargam%r9364%.root

treename = 'CollectionTree'

class ChannelEnum :
    CHANNELUNKNOWN=0
    DIMUON=1
    RESOLVED_DIELECTRON=2
    MERGED_DIELECTRON=3

class REGION :
    CR1 = 0
    CR2 = 1
    SR = 2

class YEAR :
    yUnspecified = 0
    y2015        = 1
    y2016        = 2
    y2017        = 3
    y2018        = 4
    y201516      = 5
    y20151617    = 6

###
# Change this to check out different channels / years:
###
channel = ChannelEnum.MERGED_DIELECTRON
region = REGION.SR
higgsSF = 10
theyear = YEAR.y20151617
##
# End configuration.
##

if theyear != YEAR.yUnspecified :
    # IMPORTANT NOTE: 2015/2016 MC normalization is controlled by
    # RandomRunNumber, so we need to specify the 2015+16 luminosity!
    fb = {YEAR.y2015    :3.21956 + 32.9653, YEAR.y2016: 3.21956 + 32.9653, YEAR.y2017:44.3074, YEAR.y2018:9999,
          YEAR.y201516  :3.21956 + 32.9653,
          YEAR.y20151617:3.21956 + 32.9653 + 44.3074}.get(theyear)

leptonObj = 'Muons' if channel == ChannelEnum.DIMUON else 'Electrons'
plottext = {ChannelEnum.DIMUON             : ['Dimuon channel'],
            ChannelEnum.RESOLVED_DIELECTRON: ['Resolved e channel'],
            ChannelEnum.MERGED_DIELECTRON  : ['Merged e channel']
            }.get(channel,[])


from HggStarHelpers import StandardPlotLabels,StandardSampleMerging

mergesamples = StandardSampleMerging

labels = StandardPlotLabels
labels['AllHiggs'] = 'H#rightarrow#gamma*#gamma%s'%('^{ }#times^{ }%d'%(higgsSF) if higgsSF != 1 else '')

if region == REGION.SR :
    labels['data'] = 'Data'


cuts = [
    'HGamEventInfoAuxDyn.yyStarChannel == %d'%(channel),
    'HGamEventInfoAuxDyn.isPassedObjSelection == 1', # object selection
    ]

if region == REGION.CR1 :
    cuts += [
        'HGamEventInfoAuxDyn.m_ll/1000. < 83.', # FSR only
        'HGamEventInfoAuxDyn.m_ll/1000. > 45.', # Our control region
        ]

if region == REGION.CR2 :
    cuts += [
        'HGamEventInfoAuxDyn.m_ll/1000. < 45.', # our SR cut
        'HGamEventInfoAuxDyn.m_ll/1000. > 10.', # lly generator cut
        'HGamEventInfoAuxDyn.m_lly/1000. > 80.', # Closer to our SR
        ]

if region == REGION.SR :
    cuts += [
        'HGamEventInfoAuxDyn.isPassedEventSelection', # our SR cut
        ]


blindcut = [
    '(HGamEventInfoAuxDyn.m_lly < 120000 || 130000 < HGamEventInfoAuxDyn.m_lly)',
    ]

variables = [
    'HGamEventInfoAuxDyn.m_ll/1000.',
    'HGamEventInfoAuxDyn.m_lly/1000.',
    'HGamPhotonsAuxDyn.pt[0]/1000.',
    'HGam%sAuxDyn.pt[0]/1000.'%(leptonObj),
    ]

if channel != ChannelEnum.MERGED_DIELECTRON :
    variables.append( 'HGam%sAuxDyn.pt[1]/1000.'%(leptonObj) )

if channel != ChannelEnum.DIMUON :
    variables.append( 'fabs(HGamGSFTrackParticlesAuxDyn.z0[0]-HGamGSFTrackParticlesAuxDyn.z0[1])' )

if region == REGION.SR :
    variables.append( 'HGamEventInfoAuxDyn.pt_lly/1000.' )
    variables.append( 'HGamPhotonsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly' )

    if channel != ChannelEnum.MERGED_DIELECTRON :
        variables.append( 'HGamEventInfoAuxDyn.deltaR_ll' )
        variables.append( 'HGamEventInfoAuxDyn.pt_ll/1000.' )
        variables.append( 'HGamEventInfoAuxDyn.pt_ll/HGamEventInfoAuxDyn.m_lly' )

    if channel == ChannelEnum.MERGED_DIELECTRON :
        variables.append( 'HGamElectronsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly' )
        variables.append( 'HGamGSFTrackParticlesAuxDyn.pt[0]/1000.' )
        variables.append( 'HGamGSFTrackParticlesAuxDyn.pt[1]/1000.' )

from HggStarHelpers import StandardHistFormat
histformat = StandardHistFormat
histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [100,0,200,'m_{ll#gamma} [GeV]']

if region == REGION.SR :
    histformat['HGamEventInfoAuxDyn.m_lly/1000.'] = [55,105,160,'m_{ll#gamma} [GeV]']
    histformat['HGamEventInfoAuxDyn.m_ll/1000.']  = [100,0,13,'m_{ll} [GeV]']

if channel == ChannelEnum.MERGED_DIELECTRON :
    histformat['HGamElectronsAuxDyn.pt[0]/1000.'] = [100,0,200,'p^{e1+e2}_{T} (calorimeter) [GeV]']
    histformat['HGamElectronsAuxDyn.pt[0]/HGamEventInfoAuxDyn.m_lly'] = [100,0,1,'p^{e1+e2}_{T}/m_{ll#gamma}']

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'
## IMPORTANT NOTE: If 2015-only or 2016-only, we use RandomRunNumbers to put this
## into action for mc16a. This is because RandomRunNumbers is how triggers are turned on/of in mc16a.
## (See other important note above)
if theyear == YEAR.y2015 :
    weight += '*(EventInfoAuxDyn.RandomRunNumber < 290000)'
if theyear == YEAR.y2016 :
    weight += '*(EventInfoAuxDyn.RandomRunNumber > 290000)'

from HggStarHelpers import weightscale_hyystar,SherpaKfactor1p3,SF_80fb

def SF_signalxN(tfile) :
    higgs = ['345961','345962','345963','345964','345965']
    checkHiggs = list(a in tfile.GetName() for a in higgs)
    if True in checkHiggs :
        print '%s (Higgs) will be scaled by a factor of 100'%(tfile.GetName())
        return higgsSF

    return 1

def weightscale(tfile) :
    weight = weightscale_hyystar(tfile)

    if theyear == YEAR.y20151617 :
        weight = weight* SF_80fb(tfile)

    return weight * SF_signalxN(tfile)

def afterburner(can) :
    import PlotFunctions as plotfunc
    import TAxisFunctions as taxisfunc
    import ROOT

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

    # Set ratio range; add dotted line at 1
    if plotfunc.GetBotPad(can) :
        taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(can),0,2)
        xmin,xmax = None,None
        for i in plotfunc.GetBotPad(can).GetListOfPrimitives() :
            if issubclass(type(i),ROOT.TH1) :
                xmin = i.GetXaxis().GetBinLowEdge(1)
                xmax = i.GetXaxis().GetBinLowEdge(i.GetNbinsX()+1)
        if xmin != None :
            line = ROOT.TLine(xmin,1,xmax,1)
            line.SetLineStyle(2)
            plotfunc.GetBotPad(can).cd()
            line.Draw()
            plotfunc.tobject_collector.append(line)

    return
