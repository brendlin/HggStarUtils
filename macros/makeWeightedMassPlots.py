
import PlotFunctions as plotfunc
import TAxisFunctions as taxisfunc
import ROOT
import math

doMuonOnly = False
doResOnly = False
doMerOnly = False
doEleOnly = False
doVBFOnly = False
doHipttOnly = False
doInclusiveOnly = False

data = 0
bkg = 0
bkg_plus_hyy = 0
signal = 0
hyy_bot = 0

weights = [
    -99, # off-by-one stupidity
    math.log(1 + 61.25 / float( 1750.6 + 0.000) ),
    math.log(1 + 21.85 / float( 731.28 + 0.489) ),
    math.log(1 + 29.28 / float( 943.39 + 1.887) ),
    math.log(1 +  1.28 / float(   5.86 + 0.000) ),
    math.log(1 +  0.41 / float(   1.62 + 0.009) ),
    math.log(1 +  0.77 / float(   1.98 + 0.065) ),
    math.log(1 +  3.85 / float(  33.81 + 0.000) ),
    math.log(1 +  1.08 / float(  11.77 + 0.024) ),
    math.log(1 +  2.38 / float(  17.59 + 0.184) ),
    ]


for i in range(1,10) :
    f = ROOT.TFile('Results_%s.root'%(i),'READ')

    if doMuonOnly and i in [2,3,5,6,8,9] :
        continue
    if doResOnly and i in [1,3,4,6,7,9] :
        continue
    if doMerOnly and i in [1,2,4,5,7,8] :
        continue
    if doEleOnly and i in [1,4,7] :
        continue
    if doVBFOnly and i in [1,2,3,7,8,9] :
        continue
    if doHipttOnly and i in [1,2,3,4,5,6] :
        continue
    if doInclusiveOnly and i in [4,5,6,7,8,9] :
        continue

    print 'Adding category %d'%(i)

    if not data :
        data = f.Get('pad_top_data').Clone()
        data.SetDirectory(0)
        data.Scale(weights[i])
        data.SetNameTitle('data','data')

        bkg = f.Get('pad_top_bkg_function').Clone()
        bkg.SetDirectory(0)
        bkg.Scale(weights[i])
        bkg.SetNameTitle('background','Bkg')
        bkg.SetMarkerSize(0)
        bkg.SetLineColor(ROOT.kBlue)

        bkg_plus_hyy = f.Get('pad_top_h_hyy').Clone()
        bkg_plus_hyy.SetDirectory(0)
        bkg_plus_hyy.Scale(weights[i])
        bkg_plus_hyy.SetNameTitle('bkg_plus_hyy','Bkg + H#rightarrow#gamma#gamma')

        signal = f.Get('pad_top_h_sig').Clone()
        signal.SetDirectory(0)
        signal.Scale(weights[i])
        signal.SetNameTitle('signal','Bkg + H#rightarrow#gamma#gamma + Sig (#sigma_{SM}^{ }#times^{ }1.46)')

        signal_plus_hyy_bot = f.Get('pad_bot_h_sigOnly')
        signal_plus_hyy_bot.SetDirectory(0)
        signal_plus_hyy_bot.Scale(weights[i])
        signal_plus_hyy_bot.SetNameTitle('signal_plus_hyy_bot','signal')

    else :
        tmp = f.Get('pad_top_data')
        tmp.Scale(weights[i])
        data.Add(tmp)

        tmp = f.Get('pad_top_bkg_function')
        tmp.Scale(weights[i])
        bkg.Add(tmp)

        tmp = f.Get('pad_top_h_hyy')
        tmp.Scale(weights[i])
        bkg_plus_hyy.Add(tmp)

        tmp = f.Get('pad_top_h_sig')
        tmp.Scale(weights[i])
        signal.Add(tmp)

        tmp = f.Get('pad_bot_h_sigOnly')
        tmp.Scale(weights[i])
        signal_plus_hyy_bot.Add(tmp)


    if not hyy_bot :
        hyy_bot = f.Get('pad_bot_h_hyyOnly')
        if not hyy_bot :
            continue
        print 'In category %d and adding hyy'%(i)
        hyy_bot.SetDirectory(0)
        hyy_bot.Scale(weights[i])
        hyy_bot.SetNameTitle('hyy_bot','hyy only bottom')

    else :
        tmp = f.Get('pad_bot_h_hyyOnly')
        if not tmp :
            continue
        print 'In category %d and adding hyy'%(i)
        tmp.Scale(weights[i])
        hyy_bot.Add(tmp)

c = plotfunc.RatioCanvas('weighted','weighted',600,500)
plotfunc.AddHistogram(c,bkg,'L hist')
plotfunc.AddHistogram(c,bkg_plus_hyy,'L hist')
plotfunc.AddHistogram(c,signal,'L hist')
plotfunc.AddHistogram(c,data)
plotfunc.AutoFixYaxis(plotfunc.GetTopPad(c),minzero=True)


ratioplot = ROOT.TGraphAsymmErrors() # hist.Clone()
ratioplot.SetMarkerSize(1)
ratioplot.SetLineWidth(2)

# ratio
#for i in range(ratioplot.GetNbinsX()+2) :
for i in range(1,data.GetNbinsX()+1) :
    bc1 = data.GetBinContent(i)
    #ratio WRT background-only
    bcenter = data.GetBinCenter(i)
    i_bkg = bkg.FindBin(bcenter)
    bc2 = bkg.GetBinContent(i_bkg)

    be1 = data    .GetBinErrorLow(i) if (bc1 > bc2) else data    .GetBinErrorUp(i)
    be2 = 0 # ref_data.GetBinErrorLow(i) if (bc2 > bc1) else ref_data.GetBinErrorUp(i)

    if (be1**2 + be2**2) :
        ratioplot.SetPoint(i-1,
                           bcenter,
                           (bc1-bc2))

    ratioplot.SetPointError(i-1,
                            0,0,
                            # (0.5)*data.GetBinWidth(1),
                            # (0.5)*data.GetBinWidth(1),
                            data.GetBinErrorLow(i),
                            data.GetBinErrorUp(i))

plotfunc.AddHistogram(plotfunc.GetBotPad(c),ratioplot)
plotfunc.AddHistogram(plotfunc.GetBotPad(c),signal_plus_hyy_bot,'L hist')
if not doMuonOnly :
    plotfunc.AddHistogram(plotfunc.GetBotPad(c),hyy_bot,'L hist')
plotfunc.AddHistogram(plotfunc.GetBotPad(c),ratioplot)
plotfunc.SetAxisLabels(c,'m_{ll#gamma} [GeV]','#scale[1.5]{#Sigma}^{ }weights / 2 GeV','#scale[1.5]{#Sigma}^{ }w #minus Bkg')

text = 'ln(1 + S_{90}^{ }/^{ }B_{90}) weighted sum'
outname = 'weighted'

taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-3,8)
if doMuonOnly :
    outname += '_muonOnly'
    text += ', Muon Categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-3,5)
if doResOnly :
    outname += '_resOnly'
    text += ', Resolved Electron Categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.999,2)
if doMerOnly :
    outname += '_mergedOnly'
    text += ', Merged Electron Categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.999,3)
    taxisfunc.SetYaxisRanges(plotfunc.GetTopPad(c),0,15)
if doEleOnly :
    outname += '_eleOnly'
    text += ', Electron Categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.999,4)
if doVBFOnly :
    outname += '_vbfOnly'
    text += ', VBF Categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-0.999,2.5)
if doHipttOnly :
    outname += '_hipttOnly'
    text += ', high-p_{TThrust} Categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.5,2.0)
if doInclusiveOnly :
    outname += '_inclusiveOnly'
    text += ', Inclusive (rest) Categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.999,4.0)

taxisfunc.SetXaxisRanges(plotfunc.GetBotPad(c),110,160)
plotfunc.MakeLegend(c,0.50,0.65,0.82,0.90,totalentries=4)

if doVBFOnly or doHipttOnly :
    plotfunc.DrawText(c,[plotfunc.GetSqrtsText(13),
                         plotfunc.GetLuminosityText(139.0),
                         plotfunc.GetAtlasInternalText(),
                         ' ',
                         text,
                         ],0.2,0.58,0.5,0.90,totalentries=5)
    taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(c),minzero=True)
else :
    plotfunc.DrawText(c,[plotfunc.GetSqrtsText(13),
                         plotfunc.GetLuminosityText(139.0),
                         plotfunc.GetAtlasInternalText(),
                         text,
                         ],0.2,0.10,0.5,0.37,totalentries=4)

    

line = ROOT.TLine(110,0,160,0)
line.SetLineStyle(2)
plotfunc.GetBotPad(c).cd()
line.Draw()

plotfunc.FormatCanvasAxes(c)
c.Modified()
c.Update()
c.Print('%s.pdf'%(outname))
