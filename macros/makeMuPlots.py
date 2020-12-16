
import ROOT
import PlotFunctions as plotfunc
from array import array
import math
import code
import PlotText

ROOT.gROOT.SetBatch(True)

mystyle = plotfunc.SetupStyle()

# Latest results (includes BR uncertainty)
mu_merged, mu_merged_sigma       = 7.7638e-01 ,  8.35e-01
mu_muons_3np, mu_muons_3np_sigma = 1.9336e+00 ,  6.79e-01
mu_resolved, mu_resolved_sigma   = 1.2393e+00 ,  1.10e+00
unused,mu_merged_stat            = 7.7500e-01 ,  7.95e-01
unused,mu_muons_3np_stat         = 1.9342e+00 ,  6.41e-01
unused,mu_resolved_stat          = 1.2395e+00 ,  1.05e+00

mu_highptt, mu_highptt_sigma =  3.3563e+00 ,  1.34e+00
mu_incl   , mu_incl_sigma    =  8.0635e-01 ,  5.65e-01
mu_vbf    , mu_vbf_sigma     =  2.6580e+00 ,  1.54e+00
unused    , mu_highptt_stat  =  3.3537e+00 ,  1.24e+00
unused    , mu_incl_stat     =  8.0849e-01 ,  5.45e-01
unused    , mu_vbf_stat      =  2.6593e+00 ,  1.49e+00

mu_electrons,mu_electrons_sigma =  9.4723e-01 ,  6.79e-01
mu_muons_2np,mu_muons_2np_sigma =  1.9321e+00 ,  6.79e-01
unused,mu_electrons_stat        =  9.4607e-01 ,  6.37e-01
unused,mu_muons_2np_stat        =  1.9329e+00 ,  6.41e-01

# Newer results (hacked for using HESSE)
# mu_highptt, mu_highptt_sigma =  3.3556e+00 ,  1.33e+00
# mu_incl   , mu_incl_sigma    =  8.0667e-01 ,  5.63e-01
# mu_vbf    , mu_vbf_sigma     =  2.6577e+00 ,  1.53e+00
# unused    , mu_highptt_stat  =  3.3537e+00 ,  1.24e+00
# unused    , mu_incl_stat     =  8.0850e-01 ,  5.45e-01
# unused    , mu_vbf_stat      =  2.6593e+00 ,  1.49e+00
# #
# mu_electrons,mu_electrons_sigma =   9.4746e-01 ,  6.77e-01
# mu_muons_2np,mu_muons_2np_sigma =   1.9325e+00 ,  6.70e-01
# unused,mu_electrons_stat        =   9.4598e-01 ,  6.37e-01
# unused,mu_muons_2np_stat        =   1.9330e+00 ,  6.41e-01
# #
# mu_merged, mu_merged_sigma       =   7.7662e-01 ,  8.34e-01
# mu_muons_3np, mu_muons_3np_sigma =   1.9338e+00 ,  6.70e-01
# mu_resolved, mu_resolved_sigma   =   1.2388e+00 ,  1.10e+00
# unused,mu_merged_stat            =   7.7498e-01 ,  7.95e-01
# unused,mu_muons_3np_stat         =   1.9341e+00 ,  6.41e-01
# unused,mu_resolved_stat          =   1.2394e+00 ,  1.05e+00

mu_highptt_syst   = math.sqrt(pow(mu_highptt_sigma   ,2) - pow(mu_highptt_stat  ,2))
mu_incl_syst      = math.sqrt(pow(mu_incl_sigma      ,2) - pow(mu_incl_stat     ,2))
mu_vbf_syst       = math.sqrt(pow(mu_vbf_sigma       ,2) - pow(mu_vbf_stat      ,2))
mu_electrons_syst = math.sqrt(pow(mu_electrons_sigma ,2) - pow(mu_electrons_stat,2))
mu_muons_2np_syst = math.sqrt(pow(mu_muons_2np_sigma ,2) - pow(mu_muons_2np_stat,2))
mu_merged_syst    = math.sqrt(pow(mu_merged_sigma    ,2) - pow(mu_merged_stat   ,2))
mu_muons_3np_syst = math.sqrt(pow(mu_muons_3np_sigma ,2) - pow(mu_muons_3np_stat,2))
mu_resolved_syst  = math.sqrt(pow(mu_resolved_sigma  ,2) - pow(mu_resolved_stat ,2))

# These 2- or 3-POI fits are a bit older... from ARTEM.
# mu_muon,sigma_muon = 1.93435 , 0.670555
# mu_res,sigma_res = 1.23878 , 1.09606
# mu_mer,sigma_mer = 0.775386 , 0.834553
# mu_vbf,sigma_vbf =  2.65722 , 1.51767
# mu_incl,sigma_incl =  0.806072 , 0.563459
# mu_ptt,sigma_ptt =  3.35521 , 1.32896
# mu_muons,sigma_muons =  1.93314 , 0.670348
# mu_elecs,sigma_elecs =  0.946831 , 0.677204

# This was my first estimate, with rounding
#mu_global,sigma_global = 1.46 , 0.47

# Newer results from Artem
#mu_global,sigma_global,stat_global = 1.4615,0.471979,0.454714

# Newest results (includes BR uncertainty)
mu_global,sigma_global,stat_global = 1.4611,4.81e-01,4.55e-01

syst_global = math.sqrt(pow(sigma_global ,2) - pow(stat_global ,2))

#########################

# Slightly older results (stat+syst) given by Artem
# muons_incl       ,muons_incl_sigma       = 1.5508 , 0.773986
# resolved_incl    ,resolved_incl_sigma    = 0.679794 , 1.28644
# merged_incl      ,merged_incl_sigma      = -0.773745 , 1.15664
# muons_vbf        ,muons_vbf_sigma        = 1.94939 , 2.10941
# resolved_vbf     ,resolved_vbf_sigma     = 3.03229 , 3.22467
# merged_vbf       ,merged_vbf_sigma       = 3.24791 , 2.52805
# muons_highptt    ,muons_highptt_sigma    = 3.82811 , 1.79729
# resolved_highptt ,resolved_highptt_sigma = 2.93743 , 3.13016
# merged_highptt   ,merged_highptt_sigma   = 2.90995 , 2.00156

# Newer results from Artem
# merged_highptt  ,merged_highptt_sigma    = 2.90856      ,  1.99971
# merged_incl     ,merged_incl_sigma       = -0.772254    ,  1.15611
# merged_vbf      ,merged_vbf_sigma        = 3.24929      ,  2.5339
# muons_highptt   ,muons_highptt_sigma     = 3.82683      ,  1.79582
# muons_incl      ,muons_incl_sigma        = 1.5508       ,  0.773821
# muons_vbf       ,muons_vbf_sigma         = 1.94935      ,  2.11238
# resolved_highptt,resolved_highptt_sigma  = 2.94297      ,  3.13212
# resolved_incl   ,resolved_incl_sigma     = 0.680531     ,  1.2861
# resolved_vbf    ,resolved_vbf_sigma      = 3.03117      ,  3.22659

# unused,merged_highptt_stat   = 2.90928    ,  1.94657
# unused,merged_incl_stat      = -0.772175  ,  1.08723
# unused,merged_vbf_stat       = 3.25539    ,  2.47573
# unused,muons_highptt_stat    = 3.82647    ,  1.72881
# unused,muons_incl_stat       = 1.55135    ,  0.739639
# unused,muons_vbf_stat        = 1.95237    ,  2.08112
# unused,resolved_highptt_stat = 2.94334    ,  3.07789
# unused,resolved_incl_stat    = 0.679171   ,  1.22086
# unused,resolved_vbf_stat     = 3.02543    ,  3.21153

# Latest results (includes BR uncertainty)
merged_highptt  ,merged_highptt_sigma    =   2.9091e+00 ,  2.01e+00
merged_incl     ,merged_incl_sigma       =  -7.7189e-01 ,  1.16e+00
merged_vbf      ,merged_vbf_sigma        =   3.2553e+00 ,  2.54e+00
muons_highptt   ,muons_highptt_sigma     =   3.8263e+00 ,  1.81e+00
muons_incl      ,muons_incl_sigma        =   1.5514e+00 ,  7.79e-01
muons_vbf       ,muons_vbf_sigma         =   1.9524e+00 ,  2.12e+00
resolved_highptt,resolved_highptt_sigma  =   2.9433e+00 ,  3.14e+00
resolved_incl   ,resolved_incl_sigma     =   6.7906e-01 ,  1.29e+00
resolved_vbf    ,resolved_vbf_sigma      =   3.0254e+00 ,  3.23e+00

unused,merged_highptt_stat   =   2.9091e+00 ,  1.95e+00
unused,merged_incl_stat      =  -7.7190e-01 ,  1.09e+00
unused,merged_vbf_stat       =   3.2553e+00 ,  2.48e+00
unused,muons_highptt_stat    =   3.8263e+00 ,  1.73e+00
unused,muons_incl_stat       =   1.5514e+00 ,  7.40e-01
unused,muons_vbf_stat        =   1.9524e+00 ,  2.08e+00
unused,resolved_highptt_stat =   2.9433e+00 ,  3.08e+00
unused,resolved_incl_stat    =   6.7906e-01 ,  1.22e+00
unused,resolved_vbf_stat     =   3.0254e+00 ,  3.20e+00

merged_highptt_syst   = math.sqrt(pow(merged_highptt_sigma   ,2) - pow(merged_highptt_stat    ,2))
merged_incl_syst      = math.sqrt(pow(merged_incl_sigma      ,2) - pow(merged_incl_stat       ,2))
merged_vbf_syst       = math.sqrt(pow(merged_vbf_sigma       ,2) - pow(merged_vbf_stat        ,2))
muons_highptt_syst    = math.sqrt(pow(muons_highptt_sigma    ,2) - pow(muons_highptt_stat     ,2))
muons_incl_syst       = math.sqrt(pow(muons_incl_sigma       ,2) - pow(muons_incl_stat        ,2))
muons_vbf_syst        = math.sqrt(pow(muons_vbf_sigma        ,2) - pow(muons_vbf_stat         ,2))
resolved_highptt_syst = math.sqrt(pow(resolved_highptt_sigma ,2) - pow(resolved_highptt_stat  ,2))
resolved_incl_syst    = math.sqrt(pow(resolved_incl_sigma    ,2) - pow(resolved_incl_stat     ,2))
resolved_vbf_syst     = math.sqrt(pow(resolved_vbf_sigma     ,2) - pow(resolved_vbf_stat      ,2))

#########################

xmin,xmax = -5.0,7.0
dummy = ROOT.TH2F('dummy','remove',1,xmin,xmax,9,0,9)
# dummy_y = ROOT.TH2F('dummy_y','dummy_y',1,-1,5,9,0,9)
hist = ROOT.TGraphErrors(8,array('d',[mu_resolved,
                                      mu_merged,
                                      mu_muons_3np,
                                      mu_vbf,
                                      mu_highptt,
                                      mu_incl,
                                      mu_electrons,
                                      mu_muons_2np,
                                      #mu_global,
                                      ]),
                         array('d',list(a-0.5 for a in [9,8,7,6,5,4,3,2])),
                         array('d',[mu_resolved_sigma,
                                    mu_merged_sigma,
                                    mu_muons_3np_sigma,
                                    mu_vbf_sigma,
                                    mu_highptt_sigma,
                                    mu_incl_sigma,
                                    mu_electrons_sigma,
                                    mu_muons_2np_sigma,
                                    #mu_global,
                         ]),
                         array('d',[0]*8)
)
hist.SetName('hist_errors_total')
hist.SetLineWidth(2)
hist.SetMarkerSize(1.2)

hist_bestFitMu = ROOT.TGraphErrors(1,array('d',[mu_global]),array('d',[0.5]),
                                   array('d',[sigma_global]),array('d',[0]))
hist_bestFitMu.SetTitle('remove')
hist_bestFitMu.SetMarkerColor(ROOT.kRed)
hist_bestFitMu.SetMarkerSize(1.2)
hist_bestFitMu.SetLineColor(ROOT.kBlack)
hist_bestFitMu.SetLineWidth(2)

hist_syst = ROOT.TGraphErrors(9,array('d',[mu_resolved,
                                           mu_merged,
                                           mu_muons_3np,
                                           mu_vbf,
                                           mu_highptt,
                                           mu_incl,
                                           mu_electrons,
                                           mu_muons_2np,
                                           mu_global]),
                              array('d',list(a-0.5 for a in [9,8,7,6,5,4,3,2,1])),
                              array('d',[mu_resolved_syst,
                                         mu_merged_syst,
                                         mu_muons_3np_syst,
                                         mu_vbf_syst,
                                         mu_highptt_syst,
                                         mu_incl_syst,
                                         mu_electrons_syst,
                                         mu_muons_2np_syst,
                                         syst_global]),
                              array('d',[0]*9)
)
hist_syst.SetName('hist_errors_systOnly')
hist_syst.SetMarkerSize(0)

can = ROOT.TCanvas('multiMu','multiMu',800,600)
a = ROOT.TLine()
# can_trans = ROOT.TPad('asdf_trans','asdf_trans',0,0,1,1)
# can_trans.SetFillStyle(4000)

channels_text = [
    '#font[52]{ee} resolved channels',
    '#font[52]{ee} merged channels',
    '#font[152]{mm} channels',
    'VBF-enriched channels',
    'High-#font[52]{p}_{T#font[52]{t}} channels',
    'Low-#font[52]{p}_{T#font[52]{t}} channels',
    '#font[52]{ee} channels',
    '#font[152]{mm} channels',
    '%s global fit'%(PlotText.hysyllg),
    ]

text_lines = [plotfunc.GetAtlasInternalText('Internal'),
              plotfunc.GetSqrtsText(13)+', '+plotfunc.GetLuminosityText(139.0),
              ]

for i in range(9) :
    dummy.GetYaxis().SetBinLabel(i+1,' ')
band = ROOT.TH1F('band','remove',1,mu_global-sigma_global,mu_global+sigma_global)
band.SetLineWidth(0)
band.SetBinContent(1,9)
band.SetFillColor(ROOT.kGray)

plotfunc.AddHistogram(can,dummy,drawopt='colz')
plotfunc.AddHistogram(can,band,drawopt='hist')
a.SetLineStyle(1)
a.SetLineColor(ROOT.kRed)
a.DrawLine(mu_global,0,mu_global,9)

hist.SetTitle('Total unc.')
hist.SetLineColor(ROOT.kBlack)
plotfunc.AddHistogram(can,hist)

hist_syst.SetTitle('Syst. only')
hist_syst.SetFillColor(ROOT.kBlack)
hist_syst.SetLineColor(ROOT.kAzure-8)
ROOT.gStyle.SetEndErrorSize(0)
hist_syst.SetLineWidth(7)

plotfunc.AddHistogram(can,hist_syst,drawopt='E')

plotfunc.DrawText(can,channels_text,0.07,0.135,0.5,0.95,textsize=28)
leg = plotfunc.DrawText(can,text_lines,0.63,0.80,0.93,0.92,textsize=28)
leg.SetTextAlign(32)
plotfunc.MakeLegend(can,         0.74,0.68,0.94,0.80,option=['pL','L'],textsize=28,totalentries=2)
can.GetPrimitive('multiMu_hist_errors_total').Draw('pE')
plotfunc.AddHistogram(can,hist_bestFitMu)

plotfunc.FormatCanvasAxes800600(can)
plotfunc.SetAxisLabels(can,PlotText.mu_xsbr,'')
for i in can.GetListOfPrimitives() :
    if hasattr(i,'GetYaxis') :
        i.GetYaxis().SetTickLength(0)
can.SetLeftMargin(0.05)

a.SetLineStyle(1)
a.SetLineColor(ROOT.kBlack)
a.DrawLine(xmin,1,xmax,1)
a.DrawLine(xmin,3,xmax,3)
a.DrawLine(xmin,6,xmax,6)

a.SetLineStyle(7)
a.DrawLine(1,0,1,9)

can.RedrawAxis()
can.Modified()
can.Update()

can.Print('mu_plots.pdf')
can.Print('mu_plots.png')

##############################################################
##############################################################

x_limits = [-9.0,10.0]

dummy2 = ROOT.TH2F('dummy2','remove',1,x_limits[0],x_limits[1],10,0,10)
hist_indiv_ch = ROOT.TGraphErrors(9,array('d',[resolved_vbf    ,
                                               merged_vbf      ,
                                               muons_vbf       ,
                                               resolved_highptt,
                                               merged_highptt  ,
                                               muons_highptt   ,
                                               resolved_incl   ,
                                               merged_incl     ,
                                               muons_incl      ,
                                               #mu_global,
                                               ]),
                                  array('d',list(a-0.5 for a in [10,9,8,7,6,5,4,3,2])),
                                  array('d',[resolved_vbf_sigma    ,
                                             merged_vbf_sigma      ,
                                             muons_vbf_sigma       ,
                                             resolved_highptt_sigma,
                                             merged_highptt_sigma  ,
                                             muons_highptt_sigma   ,
                                             resolved_incl_sigma   ,
                                             merged_incl_sigma     ,
                                             muons_incl_sigma      ,
                                             #sigma_global,
                                             ]),
                                  array('d',[0]*9)
)
hist_indiv_ch.SetName('hist_indiv_ch_errors_total')
hist_indiv_ch.SetLineWidth(2)
hist_indiv_ch.SetMarkerSize(1.2)

hist_indiv_ch_syst = ROOT.TGraphErrors(10,array('d',[resolved_vbf    ,
                                                     merged_vbf      ,
                                                     muons_vbf       ,
                                                     resolved_highptt,
                                                     merged_highptt  ,
                                                     muons_highptt   ,
                                                     resolved_incl   ,
                                                     merged_incl     ,
                                                     muons_incl      ,
                                                     mu_global]),
                                       array('d',list(a-0.5 for a in [10,9,8,7,6,5,4,3,2,1])),
                                       array('d',[resolved_vbf_syst    ,
                                                  merged_vbf_syst      ,
                                                  muons_vbf_syst       ,
                                                  resolved_highptt_syst,
                                                  merged_highptt_syst  ,
                                                  muons_highptt_syst   ,
                                                  resolved_incl_syst   ,
                                                  merged_incl_syst     ,
                                                  muons_incl_syst      ,
                                                  syst_global]),
                                       array('d',[0]*10)
)
hist_indiv_ch_syst.SetName('hist_indiv_ch_systOnly')
hist_indiv_ch_syst.SetMarkerSize(0)

can2 = ROOT.TCanvas('multiMu9','multiMu9',700,500)

channels_text = [
    '#font[52]{ee} resolved VBF-enriched',
    '#font[52]{ee} merged VBF-enriched',
    '#font[152]{mm} VBF-enriched',
    '#font[52]{ee} resolved high-#font[52]{p}_{T#font[52]{t}}',
    '#font[52]{ee} merged high-#font[52]{p}_{T#font[52]{t}}',
    '#font[152]{mm} high-#font[52]{p}_{T#font[52]{t}}',
    '#font[52]{ee} resolved low-#font[52]{p}_{T#font[52]{t}}',
    '#font[52]{ee} merged low-#font[52]{p}_{T#font[52]{t}}',
    '#font[152]{mm} low-#font[52]{p}_{T#font[52]{t}}',
    '%s global fit'%(PlotText.hysyllg),
    ]

for i in range(10) :
    dummy2.GetYaxis().SetBinLabel(i+1,' ')
band2 = ROOT.TH1F('band2','remove',1,mu_global-sigma_global,mu_global+sigma_global)
band2.SetLineWidth(0)
band2.SetBinContent(1,10)
band2.SetFillColor(ROOT.kGray)

plotfunc.AddHistogram(can2,dummy2,drawopt='colz')
plotfunc.AddHistogram(can2,band2,drawopt='hist')
a.SetLineStyle(1)
a.SetLineColor(ROOT.kRed)
a.DrawLine(mu_global,0,mu_global,10)

hist_indiv_ch.SetTitle('Total unc.')
hist_indiv_ch.SetLineColor(ROOT.kBlack)
plotfunc.AddHistogram(can2,hist_indiv_ch)
plotfunc.AddHistogram(can2,hist_bestFitMu)

hist_indiv_ch_syst.SetTitle('Syst. only')
hist_indiv_ch_syst.SetFillColor(ROOT.kBlack)
hist_indiv_ch_syst.SetLineColor(ROOT.kAzure-8)
ROOT.gStyle.SetEndErrorSize(0)
hist_indiv_ch_syst.SetLineWidth(7)

plotfunc.AddHistogram(can2,hist_indiv_ch_syst,drawopt='E')

plotfunc.DrawText(can2,channels_text,0.07,0.135,0.5,0.95,textsize=28)
leg = plotfunc.DrawText(can2,text_lines,0.63,0.34,0.93,0.46,textsize=28)
leg.SetTextAlign(32)
plotfunc.MakeLegend(can2,         0.74,0.22,0.94,0.34,option=['pL','L'],textsize=28,totalentries=2)
can2.GetPrimitive('multiMu9_hist_indiv_ch_errors_total').Draw('pE')
plotfunc.AddHistogram(can2,hist_bestFitMu)

plotfunc.FormatCanvasAxes800600(can2)
for i in can2.GetListOfPrimitives() :
    if hasattr(i,'GetYaxis') :
        i.GetYaxis().SetTickLength(0)

a.SetLineStyle(1)
a.SetLineColor(ROOT.kBlack)
a.DrawLine(x_limits[0],1,x_limits[1],1)
#a.DrawLine(x_limits[0],4,x_limits[1],4)
#a.DrawLine(x_limits[0],7,x_limits[1],7)
a.SetLineStyle(7)
a.DrawLine(1,0,1,10)

plotfunc.SetAxisLabels(can2,PlotText.mu_xsbr,'')
can2.SetLeftMargin(0.05)

can2.RedrawAxis()
can2.Modified()
can2.Update()

if not ROOT.gROOT.IsBatch() :
    code.interact(banner='Pausing... Press Contol-D to exit.',local=locals())

can2.Print('mu_plots_9channels.pdf')
can2.Print('mu_plots_9channels.png')
