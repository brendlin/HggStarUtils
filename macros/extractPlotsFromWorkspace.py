
# This should be stand-alone, using the WS
import ROOT
import code
import PlotFunctions as plotfunc
import TAxisFunctions as taxisfunc
import HggStarHelpers
import sys

ROOT.gROOT.SetBatch(True)

rootfile = ROOT.TFile('quick_fit_mu_float_output.root','READ')
combWS = rootfile.Get('combWS')

# Stolen from xmlAnaWSBuilder.cc
combinedPdf = combWS.pdf('CombinedPdf')
cat = combinedPdf.indexCat()
#cat_lv = ROOT.RooAbsCategoryLValue(cat)
print 'Category:',cat,type(cat)

data = combWS.data('combData')
dataList = data.split(cat,True)
print list(a.GetName() for a in dataList)

cat_i = int(sys.argv[1])
cat.setIndex(cat_i)
channelname = cat.getCurrentLabel()
pdfi = combinedPdf.getPdf(channelname)
datai = dataList.FindObject(channelname)
print 'ChannelName:', channelname, "Index: " , cat_i , ", Pdf: " , pdfi.GetName() , 
print ", Data: " , datai.GetName() , ", SumEntries: " , datai.sumEntries()

mass = pdfi.getObservables(datai).first()
mass.setRange("tmp_signalRegion",120.,130.);
frame = mass.frame()

datai.plotOn(frame,
             ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),
             ROOT.RooFit.Binning(25))
h_data = frame.getHist().Clone()

# Get rid of X-error bars
for i in range(h_data.GetN()) :
    h_data.SetPointEXhigh(i,0)
    h_data.SetPointEXlow(i,0)

signalShape = combWS.pdf('pdf__commonSig_' + channelname)
print signalShape

backgroundShape = combWS.pdf('pdf__background_%s'%(channelname))
print backgroundShape

spuriousSignalYield = combWS.function('yield__spurious_signal_' + channelname + '_' + channelname)
print spuriousSignalYield

signalYield = combWS.function('yield__signal_' + channelname + '_' + channelname)
print signalYield

backgroundYield = combWS.function('yield__background_' + channelname)
print backgroundYield

background = ROOT.RooAddPdf('background','background',ROOT.RooArgList(backgroundShape),ROOT.RooArgList(backgroundYield))
spSig = ROOT.RooAddPdf('spSig','spSig',ROOT.RooArgList(signalShape),ROOT.RooArgList(spuriousSignalYield))
signal = ROOT.RooAddPdf('signal','signal',ROOT.RooArgList(signalShape),ROOT.RooArgList(signalYield))

h_hyyOnly = ROOT.TH1F('delete','delete',1,0,1)
h_hyyPlusBkg = ROOT.TH1F('delete','delete',1,0,1)

# If it is an electron channel, then you need to include
# the hyy in the various components (total, signal peak, etc)
if cat_i in [1,2,4,5,7,8] :
    hyyShape = combWS.pdf('pdf__Hyy_background_' + channelname)
    hyyYield = combWS.function('yield__Hyy_background_' + channelname)
    hyy = ROOT.RooAddPdf('hyy','hyy',ROOT.RooArgList(hyyShape),ROOT.RooArgList(hyyYield))

    # The total pdf includes Hyy
    total = ROOT.RooAddPdf('fullResult','fullResult',ROOT.RooArgList(signal,background,spSig,hyy))

    total_expression = 'background,spSig,signal,hyy'
    sigPeak_expresssion = 'signal,hyy'

    # Hyy for the bottom plot
    total.plotOn(frame,
                 ROOT.RooFit.Components('hyy'),
                 ROOT.RooFit.LineColor(ROOT.kGreen+1),
                 ROOT.RooFit.Range('tmp_signalRegion',False))
    h_hyyOnly = frame.getCurve()

    # Background + Hyy for the top plot
    total.plotOn(frame,
                 ROOT.RooFit.Components('background,spSig,hyy'),
                 ROOT.RooFit.LineColor(ROOT.kGreen+1),
                 ROOT.RooFit.Range('tmp_signalRegion',False))
    h_hyyPlusBkg = frame.getCurve()

else :
    # The total pdf does not include Hyy
    total = ROOT.RooAddPdf('fullResult','fullResult',ROOT.RooArgList(signal,background,spSig))
    total_expression = 'background,spSig,signal'
    sigPeak_expresssion = 'signal'

# Total pdf (signal plus background) for the top pad
total.plotOn(frame,
             ROOT.RooFit.Components(total_expression),
             ROOT.RooFit.LineColor(ROOT.kRed),
             ROOT.RooFit.Range('tmp_signalRegion',False))
h_sig = frame.getCurve()

# just the signal (for the bottom pad)
total.plotOn(frame,
             ROOT.RooFit.Components(sigPeak_expresssion),
             ROOT.RooFit.LineColor(ROOT.kRed),
             ROOT.RooFit.Range('tmp_signalRegion',False))
h_sigPeak = frame.getCurve()

# all bakckgrounds (for the top pad) (this is the reference for the residual histogram)
total.plotOn(frame,ROOT.RooFit.Components('background,spSig'),ROOT.RooFit.LineColor(ROOT.kBlue))
h_bkg = frame.getCurve()
h_resid = frame.residHist()

frame.Draw()

mystyle = plotfunc.SetupStyle()
mystyle.SetErrorX(0.0000)

h_data.SetLineWidth(2)
h_resid.SetLineWidth(2)
h_sig.SetLineWidth(2)
h_sigPeak.SetLineWidth(2)
h_bkg.SetLineWidth(2)
h_resid.SetMarkerSize(1)
h_data.SetMarkerSize(1)
h_hyyPlusBkg.SetLineWidth(2)
h_hyyPlusBkg.SetLineStyle(7)
h_hyyOnly.SetLineWidth(2)
h_hyyOnly.SetLineStyle(7)

function = {
    1:'ExpPoly2',
    2:'Power Law',
    3:'ExpPoly2',
    4:'Power Law',
    5:'Exponential',
    6:'Power Law',
    7:'Power Law',
    8:'Power Law',
    9:'Power Law',
}.get(cat_i + 1)

h_data.SetTitle('Data')
h_bkg.SetTitle('Bkg (%s)'%(function))
h_hyyPlusBkg.SetTitle('Bkg + H^{ }#rightarrow^{ }#gamma#gamma')
h_sig.SetTitle('Sig^{ }#times^{ }1.46 + Bkg')
if h_hyyPlusBkg.GetName() != 'delete' :
    h_sig.SetTitle('Sig^{ }#times^{ }1.46 + all Bkgs')

can = plotfunc.RatioCanvas('canvas','canvas',500,500)
plotfunc.AddHistogram(can,h_sig,drawopt='l')
plotfunc.AddHistogram(can,h_bkg,drawopt='l')
if h_hyyPlusBkg.GetName() != 'delete' :
    plotfunc.AddHistogram(can,h_hyyPlusBkg,drawopt='l')
plotfunc.AddHistogram(can,h_data,drawopt='pE')
plotfunc.AddHistogram(plotfunc.GetBotPad(can),h_sigPeak,drawopt='l')
if h_hyyOnly.GetName() != 'delete' :
    plotfunc.AddHistogram(plotfunc.GetBotPad(can),h_hyyOnly,drawopt='l')
plotfunc.AddHistogram(plotfunc.GetBotPad(can),h_resid,drawopt='pE')
plotfunc.FormatCanvasAxes(can)
taxisfunc.SetXaxisRanges(can,110,160)
plotfunc.SetAxisLabels(can,'m_{ll#gamma} [GeV]','Entries','Residual')

line = ROOT.TLine(110,0,160,0)
line.SetLineStyle(2)
plotfunc.GetBotPad(can).cd()
line.Draw()
plotfunc.tobject_collector.append(line)

text_lines = [plotfunc.GetSqrtsText(13),plotfunc.GetLuminosityText(139.0),
              plotfunc.GetAtlasInternalText(),
              HggStarHelpers.GetPlotText(999,cat_i + 1,forPaper=True)[0]]
plotfunc.DrawText(can,text_lines,0.2,0.65,0.50,0.90,totalentries=4)
plotfunc.MakeLegend(can,        0.54,0.65,0.91,0.90,totalentries=4,ncolumns=1,skip=['remove me'])

ranges = plotfunc.AutoFixYaxis(plotfunc.GetTopPad(can))
plotfunc.SetYaxisRanges(plotfunc.GetTopPad(can),0.001,ranges[1])

# Set the bottom plot ranges to something symmetric, based on the upper limit.
ranges = plotfunc.AutoFixYaxis(plotfunc.GetBotPad(can),ignoretext=True)
plotfunc.SetYaxisRanges(plotfunc.GetBotPad(can),-1.5*ranges[1],1.5*ranges[1])

can.Modified()
can.Update()

can.Print('plots/c%02d_fullFit.pdf'%(cat_i + 1))
can.Print('plots/c%02d_fullFit.png'%(cat_i + 1))

# code.interact(banner='Pausing... Press Contol-D to exit.',local=locals())
