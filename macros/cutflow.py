#!/usr/bin/env python

import ROOT,sys,os
import TAxisFunctions as taxisfunc
import PyAnalysisPlotting as anaplot
import PlotFunctions as plotfunc
import re

def GetDataCutflowHistograms(t_file) :
    import re
    hists = []
    for i in t_file.GetListOfKeys() :
        # get _weighted
        if not re.match('CutFlow_Run.*',i.GetName()) :
            continue
        if re.match('CutFlow_.*_.*',i.GetName()) :
            continue
        hists.append(i.ReadObj())
    return hists

def GetWeightedCutflowHistogram(t_file,channel='') :
    import re

    channel_str = ''
    if channel :
        channel_str = '_%s'%(channel)

    for i in t_file.GetListOfKeys() :
        # get _weighted
        if not re.match('CutFlow_.*_weighted',i.GetName()) :
            continue
        if not re.match('CutFlow_.*_onlyDalitz%s_weighted'%(channel_str),i.GetName()) :
            continue
        return i.ReadObj()
    return 0

def GetCrossSectionBRfilterEff(t_tree) :
    t_tree.GetEntry(0)
    crossSectionBRfilterEff = getattr(t_tree,"HGamEventInfoAuxDyn.crossSectionBRfilterEff")
    return crossSectionBRfilterEff

#-------------------------------------------------------------------------
def main(options,args) :

    plotfunc.SetupStyle()

    files_b,trees_b,keys_b = anaplot.GetTreesFromFiles(options.bkgs  ,treename=options.treename,xAODInit=options.xAODInit)
    files_s,trees_s,keys_s = anaplot.GetTreesFromFiles(options.signal,treename=options.treename,xAODInit=options.xAODInit)
    files_d,trees_d,keys_d = anaplot.GetTreesFromFiles(options.data  ,treename=options.treename,xAODInit=options.xAODInit)

    scales_b = anaplot.GetScales(files_b,trees_b,keys_b,options)
    scales_s = anaplot.GetScales(files_s,trees_s,keys_s,options)

    hist = None

    if options.signal :

        sig_hists = []

        print 'Including the following histograms:'

        for k in sorted(keys_s) :

            sig_hists.append(GetWeightedCutflowHistogram(files_s[k],options.channel))

            tags = ['mc16a','mc16d','mc16e']
            print ' -',''.join(list(a if a in k else '' for a in tags)),sig_hists[-1].GetName()
            sig_hists[-1].SetTitle(k)

            # Global scale
            if scales_s and (scales_s[k] != 1) :
                sig_hists[-1].Scale(scales_s[k])

            # XS Br Feff from one of the branches
            sig_hists[-1].Scale(GetCrossSectionBRfilterEff(trees_s[k]))

        class tmp_options :
            mergesamples = {'All Higgs':'%gamstargam%',
                            'HtoGammaGamma':'%343981%',
                            }

        sig_hists = anaplot.MergeSamples(sig_hists,tmp_options)
        if len(sig_hists) > 1 :
            print 'Error - merging did not work correctly. Correct above.'
            import sys; sys.exit()

        print ' ^ ignore this number above ^'

        hist = sig_hists[0]

    if options.data :

        data_hists = []

        print 'Including the following histograms:'

        for k in sorted(keys_d) :

            for h in GetDataCutflowHistograms(files_d[k]) :
                data_hists.append(h)

                tags = ['data15','data16','data17','data18']
                print ' -',''.join(list(a if a in k else '' for a in tags)),data_hists[-1].GetName()
                data_hists[-1].SetTitle(k+data_hists[-1].GetTitle())

        class tmp_options :
            mergesamples = {'Data':'data%'}

        data_hist = anaplot.MergeSamples(data_hists,tmp_options,requireFullyMerged=True)[0]
        print ' ^ ignore this number above ^'

        hist = data_hist

    if not hist :
        return

    # Make sure this is matched up with what is determined in weightscale !
    norm_bin = 4

    text = ''
    header_str = '{:<40} & {:<17} & {:<16} & {:<16} \\\\\n'
    text += header_str.format('Cut','Surviving events','Cut efficiency','Total efficiency')
    for bin in range(norm_bin,hist.GetNbinsX()+1) :
        text += ('%s:'%(hist.GetXaxis().GetBinLabel(bin))).ljust(40)
        text += ' & '
        if options.signal :
            text += ('%2.2f \\pm %2.2f'%(hist.GetBinContent(bin),hist.GetBinError(bin))).rjust(17)
        else :
            text += ('%d'%(hist.GetBinContent(bin))).rjust(17)
        text += ' & '
        prev_bin_content = hist.GetBinContent(max(bin-1,0))
        text += ('%2.1f'%(100*hist.GetBinContent(bin)/float(prev_bin_content))).rjust(16)
        text += ' & '
        text += ('%2.1f'%(100*hist.GetBinContent(bin)/float(hist.GetBinContent(3)))).rjust(16)
        text += ' \\\\\n'

    print text

    print 'done.'
    return

#-------------------------------------------------------------------------
if __name__ == '__main__':

    p = anaplot.TreePlottingOptParser()
    p.p.add_option('--channel',type='string',default='',dest='channel',help='Truth channel')
    options,args = p.parse_args()

    if not options.variables :
        print 'Error! Please specify a variable!'
        sys.exit()

    channels = ['','Dimuon','ResolvedDielectron','MergedDielectron','AmbiguousDielectron',
                'DimuonFullPhaseSpace','DielectronFullPhaseSpace','DielectronFullPhaseSpace_RecoResolved','DielectronFullPhaseSpace_RecoMerged']
    if options.channel not in channels :
        print 'Wrong channel! Pick from:',', '.join(channels)
        sys.exit()

    main(options,args)

