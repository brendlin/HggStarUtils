
import ROOT
import PlotFunctions as plotfunc
from array import array
import math
import code
import PlotText

ROOT.gROOT.SetBatch(True)

mystyle = plotfunc.SetupStyle()

# Latest results (includes BR uncertainty, PS uncertainty, extra prod modes, Updated BR, using LLH scans)
# by category type, Tot unc:                                  
mu_incl, mu_incl_sigma_down, mu_incl_sigma_up                = 0.814609147537, 0.565696341629, 0.581327326584
mu_vbf, mu_vbf_sigma_down, mu_vbf_sigma_up                   = 2.70278716387, 1.44854216705, 1.77701950642
mu_highptt, mu_highptt_sigma_down, mu_highptt_sigma_up       = 3.22728439343, 1.2221320509, 1.44776277551
# Stat unc:                                                  
unused, mu_incl_stat_down, mu_incl_stat_up                   = 0.814487851677, 0.548599984856, 0.553877287788
unused, mu_vbf_stat_down, mu_vbf_stat_up                     = 2.70279877338, 1.41966860401, 1.68577192059
unused, mu_highptt_stat_down, mu_highptt_stat_up             = 3.22729594403, 1.17247588727, 1.25656469745
                                                             
# by flavor (2np), Tot unc:                                  
mu_muons_2np, mu_muons_2np_sigma_down, mu_muons_2np_sigma_up = 1.94678351407, 0.664734335358, 0.705240921478
mu_electrons, mu_electrons_sigma_down, mu_electrons_sigma_up = 0.959251513298, 0.67343324749, 0.698102936409
# Stat unc:                                                  
unused, mu_muons_2np_stat_down, mu_muons_2np_stat_up         = 1.94658141272, 0.636743323121, 0.650341061034
unused, mu_electrons_stat_down, mu_electrons_stat_up         = 0.959498129639, 0.627791973389, 0.650924260986
                                                             
# by flavor (3np), Tot unc:                                  
mu_muons_3np, mu_muons_3np_sigma_down, mu_muons_3np_sigma_up = 1.94792796113, 0.664928154121, 0.705377404839
mu_resolved, mu_resolved_sigma_down, mu_resolved_sigma_up    = 1.25245080869, 1.08275307431, 1.15320031729
mu_merged, mu_merged_sigma_down, mu_merged_sigma_up          = 0.791101033001, 0.829215017681, 0.859335232258
# Stat unc:                                                  
unused, mu_muons_3np_stat_down, mu_muons_3np_stat_up         = 1.94787740796, 0.636939267334, 0.650525592041
unused, mu_resolved_stat_down, mu_resolved_stat_up           = 1.25243853215, 1.0392726143, 1.08863295161
unused, mu_merged_stat_down, mu_merged_stat_up               = 0.79147688533, 0.776434906815, 0.817350303879

# # by category type, Tot unc:
# mu_incl, mu_incl_sigma_down, mu_incl_sigma_up                = 0.813565 , 0.564678,0.583085
# mu_vbf, mu_vbf_sigma_down, mu_vbf_sigma_up                   = 2.7032 , 1.44913,1.77877
# mu_highptt, mu_highptt_sigma_down, mu_highptt_sigma_up       = 3.22842 , 1.22375,1.44852
# # Stat unc:
# unused, mu_incl_stat_down, mu_incl_stat_up                   = 0.814485 , 0.548652,0.553936
# unused, mu_vbf_stat_down, mu_vbf_stat_up                     = 2.7028 , 1.41976,1.68582
# unused, mu_highptt_stat_down, mu_highptt_stat_up             = 3.22729 , 1.17252,1.25665

# # by flavor (2np), Tot unc:
# mu_muons_2np, mu_muons_2np_sigma_down, mu_muons_2np_sigma_up = 1.94594 , 0.663944,0.706106
# mu_electrons, mu_electrons_sigma_down, mu_electrons_sigma_up = 0.960515 , 0.675062,0.696934
# # Stat unc:
# unused, mu_muons_2np_stat_down, mu_muons_2np_stat_up         = 1.94659 , 0.636708,0.650292
# unused, mu_electrons_stat_down, mu_electrons_stat_up         = 0.959495 , 0.628169,0.651258

# # by flavor (3np), Tot unc:
# mu_muons_3np, mu_muons_3np_sigma_down, mu_muons_3np_sigma_up = 1.94745 , 0.664542,0.705976
# mu_resolved, mu_resolved_sigma_down, mu_resolved_sigma_up    = 1.25214 , 1.08356,1.15471
# mu_merged, mu_merged_sigma_down, mu_merged_sigma_up          = 0.792791 , 0.832293,0.85839
# # Stat unc:
# unused, mu_muons_3np_stat_down, mu_muons_3np_stat_up         = 1.94788 , 0.636928,0.650503
# unused, mu_resolved_stat_down, mu_resolved_stat_up           = 1.25244 , 1.03929,1.08865
# unused, mu_merged_stat_down, mu_merged_stat_up               = 0.791475 , 0.777038,0.817879


# Newer results (includes BR uncertainty, PS uncertainty, extra prod modes)
# mu_highptt, mu_highptt_sigma = 3.14813 , 1.26542
# mu_incl   , mu_incl_sigma    = 0.793607 , 0.55606
# mu_vbf    , mu_vbf_sigma     = 2.63643 , 1.52455

# mu_merged, mu_merged_sigma       =  0.773384 , 0.812812
# mu_muons_3np, mu_muons_3np_sigma =  1.89993 , 0.664075
# mu_resolved, mu_resolved_sigma   =  1.22155 , 1.07732

# mu_muons_2np,mu_muons_2np_sigma =  1.89848 , 0.663797
# mu_electrons,mu_electrons_sigma =  0.937051 , 0.662647

# unused    , mu_highptt_stat  = 3.1471e+00 ,  1.17e+00
# unused    , mu_incl_stat     = 7.9434e-01 ,  5.37e-01
# unused    , mu_vbf_stat      = 2.6358e+00 ,  1.48e+00

# unused,mu_merged_stat            = 7.7212e-01 ,  7.74e-01
# unused,mu_muons_3np_stat         = 1.9003e+00 ,  6.26e-01
# unused,mu_resolved_stat          = 1.2218e+00 ,  1.03e+00

# unused,mu_electrons_stat        = 9.3609e-01 ,  6.22e-01
# unused,mu_muons_2np_stat        = 1.8991e+00 ,  6.26e-01

# Newer results (includes BR uncertainty)
# mu_merged, mu_merged_sigma       = 7.7638e-01 ,  8.35e-01
# mu_muons_3np, mu_muons_3np_sigma = 1.9336e+00 ,  6.79e-01
# mu_resolved, mu_resolved_sigma   = 1.2393e+00 ,  1.10e+00
# unused,mu_merged_stat            = 7.7500e-01 ,  7.95e-01
# unused,mu_muons_3np_stat         = 1.9342e+00 ,  6.41e-01
# unused,mu_resolved_stat          = 1.2395e+00 ,  1.05e+00

# mu_highptt, mu_highptt_sigma =  3.3563e+00 ,  1.34e+00
# mu_incl   , mu_incl_sigma    =  8.0635e-01 ,  5.65e-01
# mu_vbf    , mu_vbf_sigma     =  2.6580e+00 ,  1.54e+00
# unused    , mu_highptt_stat  =  3.3537e+00 ,  1.24e+00
# unused    , mu_incl_stat     =  8.0849e-01 ,  5.45e-01
# unused    , mu_vbf_stat      =  2.6593e+00 ,  1.49e+00

# mu_electrons,mu_electrons_sigma =  9.4723e-01 ,  6.79e-01
# mu_muons_2np,mu_muons_2np_sigma =  1.9321e+00 ,  6.79e-01
# unused,mu_electrons_stat        =  9.4607e-01 ,  6.37e-01
# unused,mu_muons_2np_stat        =  1.9329e+00 ,  6.41e-01

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

mu_highptt_syst_up   = math.sqrt(pow(mu_highptt_sigma_up   ,2) - pow(mu_highptt_stat_up  ,2))
mu_incl_syst_up      = math.sqrt(pow(mu_incl_sigma_up      ,2) - pow(mu_incl_stat_up     ,2))
mu_vbf_syst_up       = math.sqrt(pow(mu_vbf_sigma_up       ,2) - pow(mu_vbf_stat_up      ,2))
mu_electrons_syst_up = math.sqrt(pow(mu_electrons_sigma_up ,2) - pow(mu_electrons_stat_up,2))
mu_muons_2np_syst_up = math.sqrt(pow(mu_muons_2np_sigma_up ,2) - pow(mu_muons_2np_stat_up,2))
mu_merged_syst_up    = math.sqrt(pow(mu_merged_sigma_up    ,2) - pow(mu_merged_stat_up   ,2))
mu_muons_3np_syst_up = math.sqrt(pow(mu_muons_3np_sigma_up ,2) - pow(mu_muons_3np_stat_up,2))
mu_resolved_syst_up  = math.sqrt(pow(mu_resolved_sigma_up  ,2) - pow(mu_resolved_stat_up ,2))

mu_highptt_syst_down   = math.sqrt(pow(mu_highptt_sigma_down   ,2) - pow(mu_highptt_stat_down  ,2))
mu_incl_syst_down      = math.sqrt(pow(mu_incl_sigma_down      ,2) - pow(mu_incl_stat_down     ,2))
mu_vbf_syst_down       = math.sqrt(pow(mu_vbf_sigma_down       ,2) - pow(mu_vbf_stat_down      ,2))
mu_electrons_syst_down = math.sqrt(pow(mu_electrons_sigma_down ,2) - pow(mu_electrons_stat_down,2))
mu_muons_2np_syst_down = math.sqrt(pow(mu_muons_2np_sigma_down ,2) - pow(mu_muons_2np_stat_down,2))
mu_merged_syst_down    = math.sqrt(pow(mu_merged_sigma_down    ,2) - pow(mu_merged_stat_down   ,2))
mu_muons_3np_syst_down = math.sqrt(pow(mu_muons_3np_sigma_down ,2) - pow(mu_muons_3np_stat_down,2))
mu_resolved_syst_down  = math.sqrt(pow(mu_resolved_sigma_down  ,2) - pow(mu_resolved_stat_down ,2))

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

# Newer results (includes BR uncertainty)
#mu_global,sigma_global,stat_global = 1.4611,4.81e-01,4.55e-01

# Newer results (includes BR, PS, extra prod modes)
#mu_global,sigma_global,stat_global = 1.43822,0.469997,4.44E-01

# Latest results (includes BR, PS, extra prod modes, updated BR)
mu_global,sigma_global_down,sigma_global_up =  1.47421438412, 0.469831856901, 0.499080134554
ounused,stat_global_down,stat_global_up = 1.47419969873, 0.451314557617, 0.460321460937

syst_global_down = math.sqrt(pow(sigma_global_down ,2) - pow(stat_global_down ,2))
syst_global_up = math.sqrt(pow(sigma_global_up ,2) - pow(stat_global_up ,2))

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

# Newer results (includes BR uncertainty)
# merged_highptt  ,merged_highptt_sigma    =   2.9091e+00 ,  2.01e+00
# merged_incl     ,merged_incl_sigma       =  -7.7189e-01 ,  1.16e+00
# merged_vbf      ,merged_vbf_sigma        =   3.2553e+00 ,  2.54e+00
# muons_highptt   ,muons_highptt_sigma     =   3.8263e+00 ,  1.81e+00
# muons_incl      ,muons_incl_sigma        =   1.5514e+00 ,  7.79e-01
# muons_vbf       ,muons_vbf_sigma         =   1.9524e+00 ,  2.12e+00
# resolved_highptt,resolved_highptt_sigma  =   2.9433e+00 ,  3.14e+00
# resolved_incl   ,resolved_incl_sigma     =   6.7906e-01 ,  1.29e+00
# resolved_vbf    ,resolved_vbf_sigma      =   3.0254e+00 ,  3.23e+00

# unused,merged_highptt_stat   =   2.9091e+00 ,  1.95e+00
# unused,merged_incl_stat      =  -7.7190e-01 ,  1.09e+00
# unused,merged_vbf_stat       =   3.2553e+00 ,  2.48e+00
# unused,muons_highptt_stat    =   3.8263e+00 ,  1.73e+00
# unused,muons_incl_stat       =   1.5514e+00 ,  7.40e-01
# unused,muons_vbf_stat        =   1.9524e+00 ,  2.08e+00
# unused,resolved_highptt_stat =   2.9433e+00 ,  3.08e+00
# unused,resolved_incl_stat    =   6.7906e-01 ,  1.22e+00
# unused,resolved_vbf_stat     =   3.0254e+00 ,  3.20e+00

# Newer results (includes BR, PS, extra prod modes)
# muons_incl      ,muons_incl_sigma        =    1.52616 , 0.766502
# resolved_incl   ,resolved_incl_sigma     =   0.669175 , 1.26759
# merged_incl     ,merged_incl_sigma       =  -0.757401 , 1.13794
# muons_vbf       ,muons_vbf_sigma         =    1.93541 , 2.10079
# resolved_vbf    ,resolved_vbf_sigma      =    2.99644 , 3.21356
# merged_vbf      ,merged_vbf_sigma        =    3.23061 , 2.52998
# muons_highptt   ,muons_highptt_sigma     =    3.59053 , 1.72428
# resolved_highptt,resolved_highptt_sigma  =    2.77561 , 3.02202
# merged_highptt  ,merged_highptt_sigma    =    2.72794 , 1.89635

# unused,merged_highptt_stat   =   2.7250e+00 ,  1.84e+00
# unused,merged_incl_stat      =  -7.5853e-01 ,  1.07e+00
# unused,merged_vbf_stat       =   3.2291e+00 ,  2.46e+00
# unused,muons_highptt_stat    =   3.5897e+00 ,  1.64e+00
# unused,muons_incl_stat       =   1.5263e+00 ,  7.28e-01
# unused,muons_vbf_stat        =   1.9357e+00 ,  2.07e+00
# unused,resolved_highptt_stat =   2.7721e+00 ,  2.96e+00
# unused,resolved_incl_stat    =   6.6905e-01 ,  1.20e+00
# unused,resolved_vbf_stat     =   3.0046e+00 ,  3.19e+00

# Latest results (includes BR uncertainty, PS uncertainty, extra prod modes, Updated BR, using LLH scans)
# Tot unc:
mu_muons_incl, mu_muons_incl_sigma_down, mu_muons_incl_sigma_up                   = 1.56552984863, 0.775847192383, 0.805817270508
mu_resolved_incl, mu_resolved_incl_sigma_down, mu_resolved_incl_sigma_up          = 0.685770713867, 1.29990067773, 1.34010857129
mu_merged_incl, mu_merged_incl_sigma_down, mu_merged_incl_sigma_up                = -0.778439025635, 1.22936407397, 1.15361217529
mu_muons_vbf, mu_muons_vbf_sigma_down, mu_muons_vbf_sigma_up                      = 1.98519794482, 1.98415810205, 2.54456651318
mu_resolved_vbf, mu_resolved_vbf_sigma_down, mu_resolved_vbf_sigma_up             = 3.08174115885, 3.11411274251, 4.71951634033
mu_merged_vbf, mu_merged_vbf_sigma_down, mu_merged_vbf_sigma_up                   = 3.310951625, 2.43103580664, 3.32491501953
mu_muons_highptt, mu_muons_highptt_sigma_down, mu_muons_highptt_sigma_up          = 3.68105541687, 1.71063066864, 2.00706545532
mu_resolved_highptt, mu_resolved_highptt_sigma_down, mu_resolved_highptt_sigma_up = 2.84253326709, 3.1623634657, 3.85390086084
mu_merged_highptt, mu_merged_highptt_sigma_down, mu_merged_highptt_sigma_up       = 2.79418993457, 1.8375419021, 2.24007657471

# Stat unc:
unused, mu_muons_incl_stat_down, mu_muons_incl_stat_up             = 1.56552908936, 0.744701425171, 0.754186593628
unused, mu_resolved_incl_stat_down, mu_resolved_incl_stat_up       = 0.685771782227, 1.23090166162, 1.26083749951
unused, mu_merged_incl_stat_down, mu_merged_incl_stat_up           = -0.778437057129, 1.09609588123, 1.11507203088
unused, mu_muons_vbf_stat_down, mu_muons_vbf_stat_up               = 1.98519781641, 1.94999183301, 2.4700291825
unused, mu_resolved_vbf_stat_down, mu_resolved_vbf_stat_up         = 3.0817410848, 3.08967023468, 4.60866994629
unused, mu_merged_vbf_stat_down, mu_merged_vbf_stat_up             = 3.31095300146, 2.36710979553, 3.17733999036
unused, mu_muons_highptt_stat_down, mu_muons_highptt_stat_up       = 3.68105344336, 1.68120928564, 1.83597756641
unused, mu_resolved_highptt_stat_down, mu_resolved_highptt_stat_up = 2.8425322373, 3.09914484436, 3.68323817522
unused, mu_merged_highptt_stat_down, mu_merged_highptt_stat_up     = 2.79418809277, 1.82508258643, 2.08157833594

mu_merged_highptt_syst_up   = math.sqrt(pow(mu_merged_highptt_sigma_up   ,2) - pow(mu_merged_highptt_stat_up    ,2))
mu_merged_incl_syst_up      = math.sqrt(pow(mu_merged_incl_sigma_up      ,2) - pow(mu_merged_incl_stat_up       ,2))
mu_merged_vbf_syst_up       = math.sqrt(pow(mu_merged_vbf_sigma_up       ,2) - pow(mu_merged_vbf_stat_up        ,2))
mu_muons_highptt_syst_up    = math.sqrt(pow(mu_muons_highptt_sigma_up    ,2) - pow(mu_muons_highptt_stat_up     ,2))
mu_muons_incl_syst_up       = math.sqrt(pow(mu_muons_incl_sigma_up       ,2) - pow(mu_muons_incl_stat_up        ,2))
mu_muons_vbf_syst_up        = math.sqrt(pow(mu_muons_vbf_sigma_up        ,2) - pow(mu_muons_vbf_stat_up         ,2))
mu_resolved_highptt_syst_up = math.sqrt(pow(mu_resolved_highptt_sigma_up ,2) - pow(mu_resolved_highptt_stat_up  ,2))
mu_resolved_incl_syst_up    = math.sqrt(pow(mu_resolved_incl_sigma_up    ,2) - pow(mu_resolved_incl_stat_up     ,2))
mu_resolved_vbf_syst_up     = math.sqrt(pow(mu_resolved_vbf_sigma_up     ,2) - pow(mu_resolved_vbf_stat_up      ,2))

mu_merged_highptt_syst_down   = math.sqrt(pow(mu_merged_highptt_sigma_down   ,2) - pow(mu_merged_highptt_stat_down    ,2))
mu_merged_incl_syst_down      = math.sqrt(pow(mu_merged_incl_sigma_down      ,2) - pow(mu_merged_incl_stat_down       ,2))
mu_merged_vbf_syst_down       = math.sqrt(pow(mu_merged_vbf_sigma_down       ,2) - pow(mu_merged_vbf_stat_down        ,2))
mu_muons_highptt_syst_down    = math.sqrt(pow(mu_muons_highptt_sigma_down    ,2) - pow(mu_muons_highptt_stat_down     ,2))
mu_muons_incl_syst_down       = math.sqrt(pow(mu_muons_incl_sigma_down       ,2) - pow(mu_muons_incl_stat_down        ,2))
mu_muons_vbf_syst_down        = math.sqrt(pow(mu_muons_vbf_sigma_down        ,2) - pow(mu_muons_vbf_stat_down         ,2))
mu_resolved_highptt_syst_down = math.sqrt(pow(mu_resolved_highptt_sigma_down ,2) - pow(mu_resolved_highptt_stat_down  ,2))
mu_resolved_incl_syst_down    = math.sqrt(pow(mu_resolved_incl_sigma_down    ,2) - pow(mu_resolved_incl_stat_down     ,2))
mu_resolved_vbf_syst_down     = math.sqrt(pow(mu_resolved_vbf_sigma_down     ,2) - pow(mu_resolved_vbf_stat_down      ,2))

mu_resolved_vbf_label     = '\\vbfee            '
mu_merged_vbf_label       = '\\vbfeemerged      '
mu_muons_vbf_label        = '\\vbfmumu          '
mu_resolved_highptt_label = '\highpttee        '
mu_merged_highptt_label   = '\highptteemerged  '
mu_muons_highptt_label    = '\highpttmumu      '
mu_resolved_incl_label    = '\lowpttee         '
mu_merged_incl_label      = '\lowptteemerged   '
mu_muons_incl_label       = '\lowpttmumu       '
mu_global_label           = 'global fit        '

cats = [
    'mu_resolved_vbf',
    'mu_merged_vbf',
    'mu_muons_vbf',
    'mu_resolved_highptt',
    'mu_merged_highptt',
    'mu_muons_highptt',
    'mu_resolved_incl',
    'mu_merged_incl',
    'mu_muons_incl',
]

groups = [
    'mu_resolved',
    'mu_merged',
    'mu_muons_3np',
    'mu_vbf',
    'mu_highptt',
    'mu_incl',
    'mu_electrons',
    'mu_muons_2np',
]

for c in cats :
    exec('val = {}'.format(c))
    exec('label = {}_label'.format(c))
    exec('tot_up = {}_sigma_up'.format(c))
    exec('tot_dn = {}_sigma_down'.format(c))
    exec('syst_up = {}_syst_up'.format(c))
    exec('syst_dn = {}_syst_down'.format(c))
    exec('stat_up = {}_stat_up'.format(c))
    exec('stat_dn = {}_stat_down'.format(c))
    print '{} & {:.1f} & $^{{+{:.1f}}}_{{-{:.1f}}}$ & $^{{+{:.1f}}}_{{-{:.1f}}}$ & $^{{+{:.1f}}}_{{-{:.1f}}}$ \\\\'.format(label,val,tot_up,tot_dn,stat_up,stat_dn,syst_up,syst_dn)

tot_stuff = '{} & {:.1f} & $^{{+{:.1f}}}_{{-{:.1f}}}$ & $^{{+{:.1f}}}_{{-{:.1f}}}$ & $^{{+{:.1f}}}_{{-{:.1f}}}$ \\\\'.format('global fit        ',mu_global,sigma_global_up,sigma_global_down,stat_global_up,stat_global_down,syst_global_up,syst_global_down)
print tot_stuff

print
print

mu_resolved_label  = '$ee$ resolved categories'
mu_merged_label    = '$ee$ merged categories  '
mu_muons_3np_label = '$\mu\mu$ categories     '
mu_vbf_label       = 'VBF-enriched categories '
mu_highptt_label   = '\highpttcat categories  '
mu_incl_label      = '\lowpttcat categories   '
mu_electrons_label = '$ee$ categories         '
mu_muons_2np_label = '$\mu\mu$ categories     '

for c in groups :
    exec('val = {}'.format(c))
    exec('label = {}_label'.format(c))
    exec('tot_up = {}_sigma_up'.format(c))
    exec('tot_dn = {}_sigma_down'.format(c))
    exec('syst_up = {}_syst_up'.format(c))
    exec('syst_dn = {}_syst_down'.format(c))
    exec('stat_up = {}_stat_up'.format(c))
    exec('stat_dn = {}_stat_down'.format(c))
    print '{} & {:.1f} & $^{{+{:.1f}}}_{{-{:.1f}}}$ & $^{{+{:.1f}}}_{{-{:.1f}}}$ & $^{{+{:.1f}}}_{{-{:.1f}}}$ \\\\'.format(label,val,tot_up,tot_dn,stat_up,stat_dn,syst_up,syst_dn)
print tot_stuff

#########################

xmin,xmax = -5.0,7.0
dummy = ROOT.TH2F('dummy','remove',1,xmin,xmax,9,0,9)
# dummy_y = ROOT.TH2F('dummy_y','dummy_y',1,-1,5,9,0,9)
hist = ROOT.TGraphAsymmErrors(8,array('d',[mu_resolved,
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
                              array('d',[mu_resolved_sigma_down,
                                         mu_merged_sigma_down,
                                         mu_muons_3np_sigma_down,
                                         mu_vbf_sigma_down,
                                         mu_highptt_sigma_down,
                                         mu_incl_sigma_down,
                                         mu_electrons_sigma_down,
                                         mu_muons_2np_sigma_down,
                                         #mu_global,
                                         ]),
                              array('d',[mu_resolved_sigma_up,
                                         mu_merged_sigma_up,
                                         mu_muons_3np_sigma_up,
                                         mu_vbf_sigma_up,
                                         mu_highptt_sigma_up,
                                         mu_incl_sigma_up,
                                         mu_electrons_sigma_up,
                                         mu_muons_2np_sigma_up,
                                         #mu_global,
                                         ]),
                              array('d',[0]*8),
                              array('d',[0]*8)
)
hist.SetName('hist_errors_total')
hist.SetLineWidth(2)
hist.SetMarkerSize(1.4)

hist_bestFitMu = ROOT.TGraphAsymmErrors(1,array('d',[mu_global]),
                                        array('d',[0.5]),
                                        array('d',[sigma_global_down]),
                                        array('d',[sigma_global_up]),
                                        array('d',[0]),
                                        array('d',[0])
                                        )
hist_bestFitMu.SetTitle('remove')
hist_bestFitMu.SetMarkerColor(ROOT.kRed)
hist_bestFitMu.SetMarkerSize(1.4)
hist_bestFitMu.SetLineColor(ROOT.kBlack)
hist_bestFitMu.SetLineWidth(2)

hist_syst = ROOT.TGraphAsymmErrors(9,array('d',[mu_resolved,
                                                mu_merged,
                                                mu_muons_3np,
                                                mu_vbf,
                                                mu_highptt,
                                                mu_incl,
                                                mu_electrons,
                                                mu_muons_2np,
                                                mu_global]),
                                   array('d',list(a-0.5 for a in [9,8,7,6,5,4,3,2,1])),
                                   array('d',[mu_resolved_syst_down,
                                              mu_merged_syst_down,
                                              mu_muons_3np_syst_down,
                                              mu_vbf_syst_down,
                                              mu_highptt_syst_down,
                                              mu_incl_syst_down,
                                              mu_electrons_syst_down,
                                              mu_muons_2np_syst_down,
                                              syst_global_down]),
                                   array('d',[mu_resolved_syst_up,
                                              mu_merged_syst_up,
                                              mu_muons_3np_syst_up,
                                              mu_vbf_syst_up,
                                              mu_highptt_syst_up,
                                              mu_incl_syst_up,
                                              mu_electrons_syst_up,
                                              mu_muons_2np_syst_up,
                                              syst_global_up]),
                                   array('d',[0]*9),
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

text_lines = [plotfunc.GetAtlasInternalText(''),
              plotfunc.GetSqrtsText(13)+', '+plotfunc.GetLuminosityText(139.0),
              ]

for i in range(9) :
    dummy.GetYaxis().SetBinLabel(i+1,' ')
band = ROOT.TH1F('band','remove',1,mu_global-sigma_global_down,mu_global+sigma_global_up)
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
hist_syst.SetLineWidth(11)

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
hist_indiv_ch = ROOT.TGraphAsymmErrors(9,array('d',[mu_resolved_vbf    ,
                                                    mu_merged_vbf      ,
                                                    mu_muons_vbf       ,
                                                    mu_resolved_highptt,
                                                    mu_merged_highptt  ,
                                                    mu_muons_highptt   ,
                                                    mu_resolved_incl   ,
                                                    mu_merged_incl     ,
                                                    mu_muons_incl      ,
                                                    #mu_global,
                                                    ]),
                                       array('d',list(a-0.5 for a in [10,9,8,7,6,5,4,3,2])),
                                       array('d',[mu_resolved_vbf_sigma_down    ,
                                                  mu_merged_vbf_sigma_down      ,
                                                  mu_muons_vbf_sigma_down       ,
                                                  mu_resolved_highptt_sigma_down,
                                                  mu_merged_highptt_sigma_down  ,
                                                  mu_muons_highptt_sigma_down   ,
                                                  mu_resolved_incl_sigma_down   ,
                                                  mu_merged_incl_sigma_down     ,
                                                  mu_muons_incl_sigma_down      ,
                                                  #sigma_global,
                                                  ]),
                                       array('d',[mu_resolved_vbf_sigma_up    ,
                                                  mu_merged_vbf_sigma_up      ,
                                                  mu_muons_vbf_sigma_up       ,
                                                  mu_resolved_highptt_sigma_up,
                                                  mu_merged_highptt_sigma_up  ,
                                                  mu_muons_highptt_sigma_up   ,
                                                  mu_resolved_incl_sigma_up   ,
                                                  mu_merged_incl_sigma_up     ,
                                                  mu_muons_incl_sigma_up      ,
                                                  #sigma_global,
                                                  ]),
                                       array('d',[0]*9),
                                       array('d',[0]*9)
)
hist_indiv_ch.SetName('hist_indiv_ch_errors_total')
hist_indiv_ch.SetLineWidth(2)
hist_indiv_ch.SetMarkerSize(1.4)

hist_indiv_ch_syst = ROOT.TGraphAsymmErrors(10,array('d',[mu_resolved_vbf    ,
                                                          mu_merged_vbf      ,
                                                          mu_muons_vbf       ,
                                                          mu_resolved_highptt,
                                                          mu_merged_highptt  ,
                                                          mu_muons_highptt   ,
                                                          mu_resolved_incl   ,
                                                          mu_merged_incl     ,
                                                          mu_muons_incl      ,
                                                          mu_global]),
                                            array('d',list(a-0.5 for a in [10,9,8,7,6,5,4,3,2,1])),
                                            array('d',[mu_resolved_vbf_syst_down    ,
                                                       mu_merged_vbf_syst_down      ,
                                                       mu_muons_vbf_syst_down       ,
                                                       mu_resolved_highptt_syst_down,
                                                       mu_merged_highptt_syst_down  ,
                                                       mu_muons_highptt_syst_down   ,
                                                       mu_resolved_incl_syst_down   ,
                                                       mu_merged_incl_syst_down     ,
                                                       mu_muons_incl_syst_down      ,
                                                       syst_global_down]),
                                            array('d',[mu_resolved_vbf_syst_up    ,
                                                       mu_merged_vbf_syst_up      ,
                                                       mu_muons_vbf_syst_up       ,
                                                       mu_resolved_highptt_syst_up,
                                                       mu_merged_highptt_syst_up  ,
                                                       mu_muons_highptt_syst_up   ,
                                                       mu_resolved_incl_syst_up   ,
                                                       mu_merged_incl_syst_up     ,
                                                       mu_muons_incl_syst_up      ,
                                                       syst_global_up]),
                                            array('d',[0]*10),
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
band2 = ROOT.TH1F('band2','remove',1,mu_global-sigma_global_down,mu_global+sigma_global_up)
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
hist_indiv_ch_syst.SetLineWidth(11)

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
