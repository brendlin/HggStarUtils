
def GetWeightedCutflowHistogram(t_file) :
    import re
    for i in t_file.GetListOfKeys() :
        # get _weighted
        if not re.match('CutFlow_.*_weighted',i.GetName()) :
            continue
        if re.match('CutFlow_.*_onlyDalitz_weighted',i.GetName()) :
            continue
        return i.ReadObj()
    return 0

def GetOnlyDalitzWeightedCutflowHistogram(t_file) :
    import re
    for i in t_file.GetListOfKeys() :
        # get _noDalitz_weighted
        if not re.match('CutFlow_.*_onlyDalitz_weighted',i.GetName()) :
            continue
        return i.ReadObj()
    return 0

def weightscale_hyystar(tfile,is_h015d=False) :
    import re

    def weightscale_onefile(t_file) :

        fix_xs = 1.0

        #print 'Processing %s'%(t_file.GetName())

        weighted_histo = GetWeightedCutflowHistogram(t_file)
        tmp_xAOD  = weighted_histo.GetBinContent(1) # hopefully unskimmed MC sumw
        tmp_DxAOD = weighted_histo.GetBinContent(2) # hopefully unskimmed MC sumw

        # Multiply cross section by this ratio
        if 'Sherpa2_mumugamma_pty_15_35' in weighted_histo.GetName() :
            fix_xs = 1.8
            print 'Multiplying Sherpa2_mumugamma_pty_15_35 by %2.3f'%(fix_xs)
        
        weighted_histo_onlyDalitz = GetOnlyDalitzWeightedCutflowHistogram(t_file)
        tmp_Ntuple_DxAOD = weighted_histo_onlyDalitz.GetBinContent(3) # hopefully unskimmed MC sumw

        tmp_DxAOD = tmp_DxAOD * fix_xs
        return tmp_xAOD,tmp_DxAOD,tmp_Ntuple_DxAOD

    if type(tfile) == type([]) :
        DxAOD = 0; xAOD = 0; Ntuple_DxAOD = 0;
        for f in tfile :
            tmp1,tmp2,tmp3 = weightscale_onefile(f)
            xAOD         += tmp1
            DxAOD        += tmp2
            Ntuple_DxAOD += tmp3
            #print xAOD,DxAOD,Ntuple_DxAOD

    else :
        xAOD,DxAOD,Ntuple_DxAOD = weightscale_onefile(tfile)
        
    # add 1000. for matching our fb lumi to the MxAOD cross section.
    #print 1000. * DxAOD / float( xAOD * Ntuple_DxAOD )
    return 1000. * DxAOD / float( xAOD * Ntuple_DxAOD )

def SherpaKfactor1p3(tfile) :
    Sherpa_NLO = ['301535','301536','301899','301900','301901','301902','301903','301904']
    checkSherpa = list(a in tfile.GetName() for a in Sherpa_NLO)
    if True in checkSherpa :
        print '%s (Sherpa) will be scaled by a factor of 1.3'%(tfile.GetName())
        return 1.3

    return 1

def SF_80fb(tfile) :
    mc16a = 3219.56 + 32965.3
    mc16d = 44307.4

    if 'mc16a' in tfile.GetName() :
        print '%s (mc16a) will be scaled by a factor of %.2f / %.2f'%(tfile.GetName(),mc16a,mc16a+mc16d)
        return mc16a / (mc16a + mc16d)

    if 'mc16d' in tfile.GetName() :
        print '%s (mc16d) will be scaled by a factor of %.2f / %.2f'%(tfile.GetName(),mc16d,mc16a+mc16d)
        return mc16d / (mc16a + mc16d)

    return 1

StandardPlotLabels = {
    # Now possible via regular expressions (use % instead of .*)
    '%Sherpa_CT10_eegammaPt10_35%'   :'p_{T}^{#gamma}#in[10,35]',
    '%Sherpa_CT10_eegammaPt35_70%'   :'p_{T}^{#gamma}#in[35,70]',
    '%Sherpa_CT10_eegammaPt70_140%'  :'p_{T}^{#gamma}#in[70,140]',
    '%Sherpa_CT10_eegammaPt140%'     :'p_{T}^{#gamma}>140 GeV',
    '%Sherpa_CT10_mumugammaPt10_35%' :'p_{T}^{#gamma}#in[10,35]',
    '%Sherpa_CT10_mumugammaPt35_70%' :'p_{T}^{#gamma}#in[35,70]',
    '%Sherpa_CT10_mumugammaPt70_140%':'p_{T}^{#gamma}#in[70,140]',
    '%Sherpa_CT10_mumugammaPt140%'   :'p_{T}^{#gamma}>140 GeV',
    'Sherpa_eegamma'                 :'ee#gamma',
    'Sherpa_mmgamma'                 :'#mu#mu#gamma',
    '%345961%'                       :'ggH H#rightarrow#gamma*#gamma',
    '%345962%'                       :'VBF H#rightarrow#gamma*#gamma',
    '%345963%'                       :'WmH H#rightarrow#gamma*#gamma',
    '%345964%'                       :'WpH H#rightarrow#gamma*#gamma',
    '%345965%'                       :'ZH H#rightarrow#gamma*#gamma',
    }

StandardSampleMerging = {
    # Now possible via regular expressions (use % instead of .*)
    'Sherpa_eegamma':'%Sherpa_CT10_eegamma%',
    'Sherpa_mmgamma':'%Sherpa_CT10_mumugamma%',
    'AllHiggs':'%gamstargam%',
    }
