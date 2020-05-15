
import ROOT
import os
import math

# Get base path (genericUtils)
the_path = ('/').join(os.path.abspath(__file__).split('/')[:-2])

# Add to macro path
ROOT.gROOT.SetMacroPath('%s:%s/share'%(ROOT.gROOT.GetMacroPath(),the_path))

ROOT.gROOT.LoadMacro('dscb.C')
integralTolerance = 1.E-06

##
## The bkg_paramList.txt format that this script is expecting:
##
# a1_merged_incl2015-18_mu      = -1.79138     +/-  0.407804    (limited)
# a1_muons_incl2015-18_mu      = -4.18181     +/-  0.296923    (limited)
# a1_resolved_incl2015-18_mu      = -3.60546     +/-  0.455482    (limited)
# a2_merged_incl2015-18_mu      = -0.50305     +/-  0.66434    (limited)
# a2_muons_incl2015-18_mu      = -3.06586     +/-  0.256592    (limited)
# a2_resolved_incl2015-18_mu      = 0.00528183     +/-  0.766147    (limited)
# a3_muons_incl2015-18_mu      = 4.99938     +/-  0.256178    (limited)
# lambda_merged_highptt2015-18_mu      = -0.669692     +/-  0.655263    (limited)
# lambda_muons_highptt2015-18_mu      = -1.72356     +/-  0.553476    (limited)
# lambda_resolved_highptt2015-18_mu      = -1.61853     +/-  0.927933    (limited)
# nbkg_merged_highptt2015-18_mu      = 185.876     +/-  15.135    (limited)
# nbkg_merged_incl2015-18_mu      = 6181.38     +/-  89.8828    (limited)
# nbkg_merged_vbf2015-18_mu      = 23.7833     +/-  5.51869    (limited)
# nbkg_muons_highptt2015-18_mu      = 237.115     +/-  17.1241    (limited)
# nbkg_muons_incl2015-18_mu      = 11885.6     +/-  125.181    (limited)
# nbkg_muons_vbf2015-18_mu      = 38.9121     +/-  7.01024    (limited)
# nbkg_resolved_highptt2015-18_mu      = 91.795     +/-  10.4152    (limited)
# nbkg_resolved_incl2015-18_mu      = 5334.22     +/-  83.5894    (limited)
# nbkg_resolved_vbf2015-18_mu      = 12.5735     +/-  3.98477    (limited)
# slope_merged_vbf2015-18_mu      = -0.045999     +/-  0.0153179    (limited)
# slope_muons_vbf2015-18_mu      = -0.0244015     +/-  0.0107171    (limited)
# slope_resolved_vbf2015-18_mu      = -0.0286503     +/-  0.0192116    (limited)

##
## The resonance_paramList.txt file that this script is expecting (from createSingleSignal):
##
# wt 6.89436e-05
# mResonance 5005
# functionName 0
# m_yy_m125000_c0 121.588
# m_yy_m125000_c1 126.379
# m_yy_m125000_c2 126.226
# m_yy_m125000_c7 125.459
# m_yy_m125000_c6 125.71
# m_yy_m125000_c8 125.887
# m_yy_m125000_c5 126.29
# m_yy_m125000_c3 121.264
# m_yy_m125000_c4 123.647
# muCBNom_SM_m125000_c0 124.939
# sigmaCBNom_SM_m125000_c0 1.86797
# alphaCBLo_SM_m125000_c0 1.53827
# alphaCBHi_SM_m125000_c0 1.5236
# nCBLo_SM_c0 3.92426
# nCBHi_SM_c0 100.268
# sigYield_SM_m125000_c0 68.0619
# muCBNom_SM_m125000_c1 124.943
# ...

translation = {
    'c0':'muons_incl2015-18_mu',
    'c1':'resolved_incl2015-18_mu',
    'c2':'merged_incl2015-18_mu',
    'c3':'muons_vbf2015-18_mu',
    'c4':'resolved_vbf2015-18_mu',
    'c5':'merged_vbf2015-18_mu',
    'c6':'muons_highptt2015-18_mu',
    'c7':'resolved_highptt2015-18_mu',
    'c8':'merged_highptt2015-18_mu',
    }

function = {
    'c0':'ExpPoly3',
    'c1':'ExpPoly2',
    'c2':'ExpPoly2',
    'c3':'Exponential',
    'c4':'Exponential',
    'c5':'Exponential',
    'c6':'Power Law',
    'c7':'Power Law',
    'c8':'Power Law',
    }

CategoryNames = {
    'c0':'Inclusive Dimuon',
    'c1':'Inclusive Resolved Electron',
    'c2':'Inclusive Merged Electron',
    'c3':'VBF Dimuon',
    'c4':'VBF Resolved Electron',
    'c5':'VBF Merged Electron',
    'c6':'High-$p_{TThrust}$ Dimuon',
    'c7':'High-$p_{TThrust}$ Resolved Electron',
    'c8':'High-$p_{TThrust}$ Merged Electron',
    }

expr = {
    'ExpPoly3':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100) + [3]*(x - 100)/100*(x - 100)/100)',
    'ExpPoly2':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100))',
    'ExpPoly2':'[0]*exp((x - 100)/100*([1] + [2]*(x - 100)/100))',
    'Exponential':'[0]*exp(x*[1])',
    'Power Law':'[0]*TMath::Power((x*1),[1])',
    }

#ROOT.Math.IntegratorOneDimOptions.SetDefaultIntegrator("Gauss")

#-------------------------------------------------------------------------
def findSmallestWindow(f,total,containing=0.9,lim_lo=110,lim_hi=140,epsilon=1.0) :
    # Strategy: keep finding smaller windows that contain >90% of events, iteratively.

    verbose = False

    if verbose : print '%.6f,%.6f'%(lim_lo,lim_hi),
    current_frac = f.IntegralOneDim(lim_lo,lim_hi,integralTolerance,integralTolerance,ROOT.Double())/total

    # First check if shifting the current window will result in a larger yield:
    check = f.IntegralOneDim(lim_lo + epsilon, lim_hi + epsilon,integralTolerance,integralTolerance,ROOT.Double())/total
    if check > current_frac :
        if verbose : print 'shifting window up improves from %.6f to %.6f'%(current_frac,check)
        return findSmallestWindow(f,total,containing,lim_lo+epsilon,lim_hi+epsilon,epsilon)

    check = f.IntegralOneDim(lim_lo - epsilon, lim_hi - epsilon,integralTolerance,integralTolerance,ROOT.Double())/total
    if check > current_frac :
        if verbose : print 'shifting window dn improves from %.6f to %.6f'%(current_frac,check)
        return findSmallestWindow(f,total,containing,lim_lo-epsilon,lim_hi-epsilon,epsilon)

    # before reducing epsilon, check for the break-out:
    if epsilon < 0.000001 :
        if verbose : print 'calculated window:',lim_lo,lim_hi,current_frac
        return lim_lo,lim_hi,current_frac

    # Next check if squeezing the limit by epsilon still results in a result >90%
    check = f.IntegralOneDim(lim_lo + epsilon, lim_hi - epsilon,integralTolerance,integralTolerance,ROOT.Double())/total
    if check < containing :
        if verbose : print 'need to lower epsilon (Integral goes to %.6f), epsilon -> %.6f'%(check,epsilon/2.0)
        return findSmallestWindow(f,total,containing,lim_lo,lim_hi,epsilon/2.0)
    if check > containing :
        if verbose : print 'Squeezing by epsilon finds a smaller window containing >90%% (%.6f), moving to that one (epsilon = %.6f).'%(check,epsilon)
        return findSmallestWindow(f,total,containing,lim_lo + epsilon,lim_hi - epsilon,epsilon)

    return -99,-99,-99

#-------------------------------------------------------------------------
def main(options,args) :

    f_paramList = open('resonance_paramList.txt')
    f_bkgList   = open('bkg_paramList.txt')

    parameters = dict()
    
    for i in f_paramList.readlines() :
        i = i.replace('\n','')
        parameters[i.split()[0]] = float(i.split()[1])

    for i in f_bkgList.readlines() :
        i = i.replace('\n','')
        key = i.split()[0]
        for t in translation.keys() :
            key = key.replace(translation[t],t)
        parameters[key] = float(i.split()[2])

    parameters_table = []
    res_table = []

    # print parameters
    strformat = '{:<40} & {:>19} & {:>8} & {:>8} & {:>15} & {:>8} \\\\ \hline'
    print strformat.format('Category','$S_{90}$ mass range','$S_{90}$','$B_{90}$','$f_{90}$ [\%]','$Z_{90}$')

    for c in range(9) :

        parameters_table.append([])
        res_table.append([])
        cstr = 'c%d'%(c)

        f_sig = ROOT.TF1('Fit to DSCB',ROOT.dscb,105,160,7)
        
        #f_sig.SetParameter(0,parameters['sigYield_SM_m125000_c%d'%(c)])
        f_sig.SetParameter(1,parameters['sigmaCBNom_SM_m125000_c%d'%(c)])
        f_sig.SetParameter(2,parameters['alphaCBLo_SM_m125000_c%d'%(c)])
        f_sig.SetParameter(3,parameters['alphaCBHi_SM_m125000_c%d'%(c)])
        f_sig.SetParameter(4,parameters['nCBLo_SM_c%d'%(c)])
        f_sig.SetParameter(5,parameters['nCBHi_SM_c%d'%(c)])
        f_sig.SetParameter(6,parameters['muCBNom_SM_m125000_c%d'%(c)])

        f_sig.SetParameter(0,1)
        integral = f_sig.IntegralOneDim(80,180,integralTolerance,integralTolerance,ROOT.Double())
        f_sig.SetParameter(0,parameters['sigYield_SM_m125000_c%d'%(c)]/integral)

        lim_lo_68,lim_hi_68,f68 = findSmallestWindow(f_sig,parameters['sigYield_SM_m125000_c%d'%(c)],containing=0.68)
        res_table[-1].append(0.5*(lim_hi_68-lim_lo_68))

        lim_lo_90,lim_hi_90,f90 = findSmallestWindow(f_sig,parameters['sigYield_SM_m125000_c%d'%(c)])
        res_table[-1].append(0.5*(lim_hi_90-lim_lo_90))

        parameters_table[-1].append(function[cstr])
        parameters_table[-1].append(str(parameters['nbkg_%s'%(cstr)]))

        f_bkg = ROOT.TF1(function[cstr],expr[function[cstr]],105,160)
        f_bkg.SetTitle(function[cstr])
        if function[cstr] in ['ExpPoly3','ExpPoly2'] :
            par = parameters['a1_%s'%(cstr)]
            parameters_table[-1].append(str(par))
            f_bkg.SetParameter(1,par)
        if function[cstr] in ['ExpPoly3','ExpPoly2'] :
            par = parameters['a2_%s'%(cstr)]
            parameters_table[-1].append(str(par))
            f_bkg.SetParameter(2,par)
        if function[cstr] in ['ExpPoly3'] :
            par = parameters['a3_%s'%(cstr)]
            parameters_table[-1].append(str(par))
            f_bkg.SetParameter(3,par)
        if function[cstr] in ['Power Law'] :
            par = parameters['lambda_%s'%(cstr)]
            parameters_table[-1].append(str(par))
            f_bkg.SetParameter(3,par)
        if function[cstr] in ['Exponential'] :            
            par = parameters['slope_%s'%(cstr)]
            parameters_table[-1].append(str(par))
            f_bkg.SetParameter(3,par)

        while len(parameters_table[-1]) < 5 :
            parameters_table[-1].append('')

        f_bkg.SetParameter(0,1)
        integral = f_bkg.Integral(105,160)
        f_bkg.SetParameter(0,parameters['nbkg_%s'%(cstr)]/float(integral))

        s90 = parameters['sigYield_SM_m125000_c%d'%(c)]*0.9
        b90 = f_bkg.Integral(lim_lo_90,lim_hi_90)
        z90 = math.sqrt( 2*( (s90+b90)*math.log(1+s90/b90) - s90) )

        #f_bkg.Draw()
        #raw_input('pause')

        str_range = '[%.2f, %.2f]'%(lim_lo_90,lim_hi_90)
        str_b90 = '%.3g'%(b90) if b90 < 1000 else '%.0f'%(b90)
        strformat = '{:<40} & {:<19} & {:8.3g} & {:>8} & {:15.1f} & {:8.2f} \\\\'
        print strformat.format(CategoryNames[cstr],str_range,s90,str_b90,s90*100/(s90+b90),z90)


    print ''
    ##
    ## Print the effective resolution s68 and s90
    ##
    strformat = '{:<40} & {:>21} & {:>21} \\\\ \hline \midrule'
    print strformat.format('Category','$\sigma_{68}$ [GeV]','$\sigma_{90}$ [GeV]')
    for c,res in enumerate(res_table) :
        cstr = 'c%d'%(c)
        strformat = '{:<40} & {:>21.2f} & {:>21.2f} \\\\'
        print strformat.format(CategoryNames[cstr],res[0],res[1])

    print ''
    ##
    ## Print the parameters of the bkg fits.
    ##
    strformat = '{:<40} & {:>11} & {:>11} & {:>11} & {:>11} & {:>11} \\\\ \hline \midrule'
    print strformat.format('Category','Form','Bkg Yield','p0','p1','p2')

    for c,cat in enumerate(parameters_table) :
        cstr = 'c%d'%(c)
        strformat = '{:<40} & {:>11} & {:>11} & {:>11} & {:>11} & {:>11} \\\\'
        print strformat.format(CategoryNames[cstr],cat[0],cat[1],cat[2],cat[3],cat[4])

    return

if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    options,args = p.parse_args()

    main(options,args)


