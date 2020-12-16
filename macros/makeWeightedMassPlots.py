
import PlotFunctions as plotfunc
import TAxisFunctions as taxisfunc
import ROOT
import math
import code
import numpy as np
import ctypes
import PlotText
import sys

ROOT.gROOT.SetBatch(True)

version = int(sys.argv[1])

binWidth_gev = 1
# doAll     = (version == 0)
doMuonOnly  = (version == 1)
doResOnly   = (version == 2)
doMerOnly   = (version == 3)
doEleOnly   = (version == 4)
doVBFOnly   = (version == 5)
doHipttOnly = (version == 6)
doInclusiveOnly = (version == 7)

# Weights that correspond to the data histograms
weights = []
data_hists = []

bkg = 0
bkg_plus_hyy = 0
signal = 0
hyy_bot = 0
signal_plus_hyy_bot = 0

mystyle = plotfunc.SetupStyle()

all_weights = [
    -99, # off-by-one stupidity
    math.log(1 + 61.26 / float( 1745.72 + 0.000) ),
    math.log(1 + 21.86 / float( 728.9   + 0.489) ),
    math.log(1 + 29.28 / float( 941.55  + 1.887) ),
    math.log(1 + 1.28  / float( 5.85    + 0.000) ),
    math.log(1 + 0.41  / float( 1.62    + 0.009) ),
    math.log(1 + 0.77  / float( 1.98    + 0.065) ),
    math.log(1 + 3.85  / float( 33.82   + 0.000) ),
    math.log(1 + 1.08  / float( 11.82   + 0.024) ),
    math.log(1 + 2.38  / float( 17.59   + 0.184) ),
    ]

def compute_poisson_error(n):
    """
    Part of the procedure outlined in
    Statistics of weighted Poisson events and its applications
    https://arxiv.org/pdf/1309.1287.pdf
    """

    a = ctypes.c_double()
    b = ctypes.c_double()
    if abs(n - np.round(n)) < 1E-5:
        ROOT.RooHistError.instance().getPoissonInterval(int(np.round(n)), a, b)
        a = a.value
        b = b.value
        return n - float(a), float(b) - n

    else:
        def scale_range(start, start1, start2, end1, end2):
            m = (end2 - end1) / float(start2 - start1)
            return end1 + m * (start - start1)

        yfloor = np.floor(n).astype(int)
        yceil = yfloor + 1

        ROOT.RooHistError.instance().getPoissonInterval(int(yfloor), a, b)
        floor_error = n - a.value, b.value - n
        ROOT.RooHistError.instance().getPoissonInterval(int(yceil), a, b)
        ceil_error = n - a.value, b.value - n

        lo = scale_range(n, yfloor, yceil, floor_error[0], ceil_error[0])
        hi = scale_range(n, yfloor, yceil, floor_error[1], ceil_error[1])

        return lo, hi

def compute_scaled_poisson_errorbar(nevents, _weights):
    """
    I believe this is a procedure outlined in
    Statistics of weighted Poisson events and its applications
    https://arxiv.org/pdf/1309.1287.pdf

    nevents = list of number of evets for each category
    _weights = list of _weights for each category
    return central value, error down (negative), error up
    Taken from:
    /afs/cern.ch/user/c/czhou/public/forAlex/Weighted_final_2015_2018_40_bins/plot_ttH_weighted.py
    """
    nevents = np.asarray(nevents)
    _weights = np.asarray(_weights)

    nw = float(np.sum(nevents * _weights, axis=0))
    nw2 = float(np.sum(nevents * _weights ** 2, axis=0))

    if nw == 0 or nw2 == 0 :
        return 0,0,0

    lambda_tilde = nw ** 2 / nw2
    scale = nw2 / nw

    e = compute_poisson_error(lambda_tilde)
    return nw, e[0] * scale, e[1] * scale

def ScalePdf(g1,weight) :
    if issubclass(type(g1),ROOT.TH1) :
        # For TH1-type, unfortunately asymmetric errors are not possible.
        g1.SetDirectory(0)
        g1.Scale(weight)
    else :
        for i in range(g1.GetN()) :
            g1.SetPointY(i,g1.GetPointY(i)*weight)
    return

def AddPdfs(g1,g2) :
    if issubclass(type(g1),ROOT.TH1) :
        # For TH1-type, unfortunately asymmetric errors are not possible.
        g1.Add(g2)
    else :
        for i in range(g1.GetN()) :
            # There is some very weird binning going on here. Best to use Eval.
            g1.SetPointY(i,g1.GetPointY(i) + g2.Eval(g1.GetPointX(i)))
    return


for i in range(1,10) :
    print 'Loading file %s'%('Results_%s.root'%(i))
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
    weight = all_weights[i]

    data_hists.append(f.Get('pad_top_data').Clone())
    weights.append(weight)

    if issubclass(type(data_hists[-1]),ROOT.TH1) :
        data_hists[-1].SetDirectory(0)
    data_hists[-1].SetNameTitle('data_%d'%(i),'data_%d'%(i))

    if not bkg :
        bkg = f.Get('pad_top_bkg_function').Clone()
        ScalePdf(bkg,weight)
        bkg.SetNameTitle('background','Bkg')
        bkg.SetMarkerSize(0)
        #bkg.SetLineColor(ROOT.kBlue)
    else :
        tmp = f.Get('pad_top_bkg_function')
        ScalePdf(tmp,weight)
        AddPdfs(bkg,tmp)

    if not signal :
        signal = f.Get('pad_top_h_sig').Clone()
        ScalePdf(signal,weight)
        title = PlotText.bkg_sigMuEquals1p46 if doMuonOnly else PlotText.bkg_hyy_sigMuEquals1p46
        signal.SetNameTitle('signal',title)
    else :
        tmp = f.Get('pad_top_h_sig')
        ScalePdf(tmp,weight)
        AddPdfs(signal,tmp)


    if not signal_plus_hyy_bot :
        signal_plus_hyy_bot = f.Get('pad_bot_h_sigOnly')
        ScalePdf(signal_plus_hyy_bot,weight)
        signal_plus_hyy_bot.SetNameTitle('signal_plus_hyy_bot','signal')
        signal_plus_hyy_bot.SetLineWidth(3)
    else :
        tmp = f.Get('pad_bot_h_sigOnly')
        ScalePdf(tmp,weight)
        AddPdfs(signal_plus_hyy_bot,tmp)

    # Separately treat Hyy (top pad)
    if not bkg_plus_hyy :
        tmp = f.Get('pad_top_h_hyy')
        if tmp :
            bkg_plus_hyy = f.Get('pad_top_h_hyy').Clone()
            ScalePdf(bkg_plus_hyy,weight)
            bkg_plus_hyy.SetNameTitle('bkg_plus_hyy',PlotText.bkg_hyy)
    else :
        tmp = f.Get('pad_top_h_hyy')
        if tmp :
            ScalePdf(tmp,weight)
            AddPdfs(bkg_plus_hyy,tmp)

    # Separately treat Hyy (bottom pad)
    if not hyy_bot :
        hyy_bot = f.Get('pad_bot_h_hyyOnly')
        if hyy_bot :
            print 'In category %d and adding hyy'%(i)
            ScalePdf(hyy_bot,weight)
            hyy_bot.SetNameTitle('hyy_bot','hyy only bottom')
    else :
        tmp = f.Get('pad_bot_h_hyyOnly')
        if tmp :
            print 'In category %d and adding hyy'%(i)
            ScalePdf(tmp,weight)
            AddPdfs(hyy_bot,tmp)

data = ROOT.TGraphAsymmErrors()
data.SetMarkerSize(1)
data.SetLineWidth(2)
data.SetNameTitle('data_all','data')

if issubclass(type(data_hists[0]),ROOT.TH1) :
    for i in range(data_hists[0].GetNbinsX()) :
        nevents = list(data_hists[a].GetBinContent(i+1) for a in range(len(data_hists)))
        n,e_down,e_up = compute_scaled_poisson_errorbar(nevents,weights)
        data.SetPoint(i,data_hists[0].GetBinCenter(i+1),n)
        data.SetPointError(i,0,0,e_down,e_up)
else :
    for i in range(data_hists[0].GetN()) :
        nevents = list(data_hists[a].GetPointY(i) for a in range(len(data_hists)))
        n,e_down,e_up = compute_scaled_poisson_errorbar(nevents,weights)
        data.SetPoint(i,data_hists[0].GetPointX(i),n)
        data.SetPointError(i,0,0,e_down,e_up)

c = plotfunc.RatioCanvas('weighted','weighted',500,500)
drawopt_pdfs = 'L hist' if issubclass(type(bkg),ROOT.TH1) else 'L'
#code.interact(banner='Pausing... Press Contol-D to exit.',local=locals())

ROOT.gStyle.SetLineStyleString(5,"12 8 12 8") # 5 = h_hyy
ROOT.gStyle.SetLineStyleString(11,"16 20 4 0") # 7 = h_bkg
if not doMuonOnly :
    plotfunc.AddHistogram(c,bkg_plus_hyy,drawopt_pdfs)
plotfunc.AddHistogram(c,bkg,drawopt_pdfs)
plotfunc.AddHistogram(c,signal,drawopt_pdfs)
plotfunc.AddHistogram(c,data)
ranges = plotfunc.AutoFixYaxis(plotfunc.GetTopPad(c),minzero=True)
plotfunc.SetYaxisRanges(plotfunc.GetTopPad(c),ranges[0],int(ranges[1]*1.05))

ratioplot = ROOT.TGraphAsymmErrors() # hist.Clone()
ratioplot.SetMarkerSize(1)
ratioplot.SetLineWidth(2)

if True :
    for i in range(data.GetN()) :
        bc1 = data.GetPointY(i)
        #ratio WRT background-only
        bcenter = data.GetPointX(i)
        if issubclass(type(bkg),ROOT.TGraph) :
            i_bkg = i
            bc2 = bkg.Eval(bcenter)
        else :
            print 'Warning: this is not working correctly because the bin width is too coarse.'
            i_bkg = bkg.FindBin(bcenter)
            #print bkg.GetBinCenter(i_bkg)
            bc2 = bkg.GetBinContent(i_bkg)
        #print bcenter,bc2

        be1 = data    .GetErrorYlow(i) if (bc1 > bc2) else data    .GetErrorYhigh(i)
        be2 = 0 # ref_data.GetBinErrorLow(i) if (bc2 > bc1) else ref_data.GetBinErrorUp(i)

        if bc1 < 0.00001 :
            bc1 = -99

        ratioplot.SetPoint(i,
                           bcenter,
                           (bc1-bc2))

        ratioplot.SetPointError(i,
                                0,0,
                                # (0.5)*data.GetBinWidth(1),
                                # (0.5)*data.GetBinWidth(1),
                                data.GetErrorYlow(i),
                                data.GetErrorYhigh(i))


plotfunc.AddHistogram(plotfunc.GetBotPad(c),ratioplot)
plotfunc.FormatCanvasAxes500500(c)
line = ROOT.TLine(110.45,0,160,0)
line.SetLineWidth(2)
line.SetLineStyle(7)
if not doMuonOnly :
    plotfunc.AddHistogram(plotfunc.GetBotPad(c),hyy_bot,drawopt_pdfs)
plotfunc.GetBotPad(c).cd(); line.Draw()
plotfunc.AddHistogram(plotfunc.GetBotPad(c),signal_plus_hyy_bot,drawopt_pdfs)
plotfunc.AddHistogram(plotfunc.GetBotPad(c),ratioplot)
perGeV = '^{ }/^{ }GeV' if (binWidth_gev == 1) else '^{ }/^{ }%d GeV'%(binWidth_gev)
plotfunc.SetAxisLabels(c,'m_{%s} [GeV]'%(PlotText.llg_subscript),
                       '#scale[1.5]{#Sigma}^{ }weights%s'%(perGeV),
                       '#scale[1.5]{#Sigma}^{ }w #minus Bkg')

text = 'ln(1^{ }+^{ }S#scale[0.5]{#lower[0.4]{90}}^{ }/^{ }B#scale[0.5]{#lower[0.4]{90}}) weighted sum'
outname = 'weighted'

taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-3,5 if binWidth_gev == 1 else 8)
if doMuonOnly :
    outname += '_muonOnly'
    text += ', #font[152]{mm} categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-3,5)
if doResOnly :
    outname += '_resOnly'
    text += ', #font[52]{ee} resolved categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.999,2)
if doMerOnly :
    outname += '_mergedOnly'
    text += ', #font[52]{ee} merged categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.999,3)
    taxisfunc.SetYaxisRanges(plotfunc.GetTopPad(c),0,15)
if doEleOnly :
    outname += '_eleOnly'
    text += ', #font[52]{ee} categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.999,4)
if doVBFOnly :
    outname += '_vbfOnly'
    text += ', VBF categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-0.999,2.6)
if doHipttOnly :
    outname += '_hipttOnly'
    text += ', high-#font[52]{p}_{T#font[52]{t}} categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.5,2.0)
if doInclusiveOnly :
    outname += '_inclusiveOnly'
    text += ', low-#font[52]{p}_{T#font[52]{t}} categories'
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(c),-1.999,4.0)

taxisfunc.SetXaxisRanges(c,110,160)
taxisfunc.SetXaxisRanges(plotfunc.GetBotPad(c),110,160)

order = [0,1,2] if doMuonOnly else [1,0,2,3]

if (version == 0) :
    plotfunc.MakeLegend(c,0.46,0.64,0.82,0.89,totalentries=4,textsize=17,order=order)
    plotfunc.DrawText(c,[plotfunc.GetAtlasInternalText(),
                         '%s, %s'%(plotfunc.GetSqrtsText(13),plotfunc.GetLuminosityText(139.0)),
                         text,
                         ],0.20,0.08,0.5,0.29,totalentries=3,textsize=17)
    ranges = taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(c),
                                    minzero=True,ignoretext=True,ignorelegend=True)
    taxisfunc.SetYaxisRanges(plotfunc.GetTopPad(c),0.001,55 if binWidth_gev == 2 else 30)
elif doVBFOnly or doResOnly :
    plotfunc.MakeLegend(c,0.54,0.64,0.95,0.89,totalentries=4,textsize=17,order=order)
    plotfunc.DrawText(c,[plotfunc.GetAtlasInternalText(),
                         '%s, %s'%(plotfunc.GetSqrtsText(13),plotfunc.GetLuminosityText(139.0)),
                         ' ',' ',
                         text],
                      0.19,0.58,0.5,0.89,totalentries=5,textsize=17)
    ranges = taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(c),minzero=True)
    taxisfunc.SetYaxisRanges(plotfunc.GetTopPad(c),0.001,ranges[1])
else :
    plotfunc.MakeLegend(c,0.54,0.64,0.95,0.89,totalentries=4,textsize=17,order=order)
    plotfunc.DrawText(c,[plotfunc.GetAtlasInternalText(),
                         '%s, %s'%(plotfunc.GetSqrtsText(13),plotfunc.GetLuminosityText(139.0))],
                      0.19,0.765,0.5,0.89,totalentries=2,textsize=17)
    ranges = taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(c),minzero=True,ignorelegend=True)
    taxisfunc.SetYaxisRanges(plotfunc.GetTopPad(c),0.001,ranges[1])
    plotfunc.DrawText(c,[text],0.19,0.08,0.5,0.15,totalentries=1,textsize=17)

plotfunc.GetTopPad(c).RedrawAxis()
plotfunc.GetBotPad(c).RedrawAxis()

c.Modified()
c.Update()

#code.interact(banner='Pausing... Press Contol-D to exit.',local=locals())

c.Print('%s.pdf'%(outname))
