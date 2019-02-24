
treename = 'CollectionTree'

class CHANNEL :
    CHANNELUNKNOWN = 0
    DIMUON = 1
    RESOLVED_DIELECTRON = 2
    MERGED_DIELECTRON = 3
    AMBIGUOUS_DIELECTRON = 4
    FAILEDTRKELECTRON = 5
    OTHER = 6
    OUT_OF_ACCEPTANCE = 7

totalEvents = 206.946096372 # See "afterburner" for how to use
doRequireTrueHiggsElectron = False
doRequireInsideWindow = False
doRequireOutsideWindow = False
doSR = False
MllyWindow = [120,130]

cuts = []

if doSR :
    cuts.append( 'HGamEventInfoAuxDyn.isPassedEventSelection' )

if doRequireTrueHiggsElectron :
    cuts += [
        'HGamEventInfoAuxDyn.yyStarChannel > 1',
        'HGamGSFTrackParticlesAuxDyn.isTrueHiggsElectron[0] == 1 && HGamGSFTrackParticlesAuxDyn.isTrueHiggsElectron[1] == 1',
        ]

if doRequireInsideWindow or doRequireOutsideWindow :
    isOutside = '!' if doRequireOutsideWindow else ''
    cuts += [
        '%s(%.0f < HGamEventInfoAuxDyn.m_lly && HGamEventInfoAuxDyn.m_lly < %.0f)'%(isOutside,MllyWindow[0]*1000,MllyWindow[1]*1000),
        ]

variables = [
    'HGamEventInfoAuxDyn.yyStarChannel',
    'HGamTruthEventInfoAuxDyn.yyStarChannel',
    ]

histformat = {
    'HGamEventInfoAuxDyn.yyStarChannel'     :[8,0,8,'Reco channel'],
    'HGamTruthEventInfoAuxDyn.yyStarChannel':[8,0,8,'Truth channel'],
    'HGamEventInfoAuxDyn.m_lly/1000.':[100,105,160,'m_{ll#gamma} [GeV]'],
    }

binlabels = {
    'HGamEventInfoAuxDyn.yyStarChannel'     :['None','2#mu','2e Res','2e merged','2e ambi','#minus','#minus','#minus'],
    'HGamTruthEventInfoAuxDyn.yyStarChannel':['None','2#mu','2e Res','2e merged','2e ambi','truth-trk fail','other','out-of-acc'],
}

weight = 'HGamEventInfoAuxDyn.crossSectionBRfilterEff*HGamEventInfoAuxDyn.weight'

import HggStarHelpers
weightscale = HggStarHelpers.weightscale_hyystar

def afterburner(can) :
    import ROOT
    style = ROOT.gROOT.GetStyle('mystyle')
    style.SetPaintTextFormat('4.1f%%')
    style.SetTextFont(42)

    can.SetRightMargin(0.13)
    can.SetBottomMargin(0.16)
    can.SetLeftMargin(0.24)

    for i in can.GetListOfPrimitives() :
        if issubclass(type(i),ROOT.TH2) :
            i.SetDrawOption('colztext')
            i.SetMarkerSize(1.5)

            ## In order for the fraction to be correct, first run on NON-SKIMMED
            ## sample and get the total number of events. THEN scale by this number.
            print i.Integral()
            i.Scale(100/float(totalEvents))
            
            for j,label in enumerate(binlabels['HGamEventInfoAuxDyn.yyStarChannel']) :
                i.GetXaxis().SetBinLabel(j+1,label)
            for j,label in enumerate(binlabels['HGamTruthEventInfoAuxDyn.yyStarChannel']) :
                i.GetYaxis().SetBinLabel(j+1,label)

            i.GetXaxis().SetTitleOffset(1.7)
            i.GetYaxis().SetTitleOffset(3.0)
            i.GetXaxis().SetLabelOffset(0.01)
            i.GetZaxis().SetTitle('Fraction of events')

            i.SetDrawOption('colztext')
            
    return
