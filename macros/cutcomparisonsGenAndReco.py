#!/usr/bin/env python

##
## This macro offers a way to compare different cut selection.
## Right now it only works for --signal MC.
## To use it, make a config file and define inside a list called "cutcomparisons", e.g. to compare
## "CutSet1" (comprised of cut1a, cut1b, cut1c) and "CutSet2" (comprised of cut2a, cut2b, cut2c) do:
## cutcomparisons = [ ['CutSet1',['cut1a','cut1b','cut1c']], ['CutSet2',['cut2a','cut2b','cut2c']] ]
##

import ROOT,sys,os
import TAxisFunctions as taxisfunc
import PyAnalysisPlotting as anaplot
import PlotFunctions as plotfunc

def DrawHistosCutComparison(variable,options,gen_hist=None,reco_hist=None,name='') :
    #
    # Clean up name
    #
    canname = anaplot.CleanUpName(variable)

    #
    # stack, before adding SUSY histograms
    #
    if options.ratio or options.pull :
        can = plotfunc.RatioCanvas(canname,canname,500,500)
    else :
        can = ROOT.TCanvas(canname,canname,500,500)

    if gen_hist :
        plotfunc.AddHistogram(can,gen_hist,drawopt='fhist')

    if reco_hist :
        if options.ratio :
            tmp1,tmp2=plotfunc.AddRatio(can,reco_hist,gen_hist,drawopt='hist')
            tmp2.SetDrawOption('pE1')
        elif options.pull :
            tmp1,tmp2=plotfunc.AddRatio(can,reco_hist,gen_hist,divide='pull',drawopt='hist')
            tmp2.SetDrawOption('pE1')
        else :
            plotfunc.AddHistogram(can,reco_hist,drawopt='hist')

    plotfunc.FormatCanvasAxes(can)
    text_lines = [plotfunc.GetSqrtsText(13)]
#     if options.fb > 0 :
#         text_lines += [plotfunc.GetLuminosityText(options.fb)]
    text_lines += [plotfunc.GetAtlasInternalText()]
    if hasattr(options,'plottext') and options.plottext :
        text_lines += options.plottext

    if options.log :
        if options.ratio :
            if taxisfunc.MinimumForLog(can.GetPrimitive('pad_top')) > 0 :
                can.GetPrimitive('pad_top').SetLogy()
        else :
            if taxisfunc.MinimumForLog(can) > 0 :
                can.SetLogy()

    if options.ratio or options.pull :
        plotfunc.DrawText(can,text_lines,0.2,0.65,0.5,0.90,totalentries=4)
        plotfunc.MakeLegend(can,0.53,0.65,0.92,0.90,totalentries=4,ncolumns=1,skip=['remove me'])
    else :
        plotfunc.DrawText(can,text_lines,0.2,0.75,0.5,0.94,totalentries=4)
        plotfunc.MakeLegend(can,0.53,0.75,0.94,0.94,totalentries=4,ncolumns=1,skip=['remove me'])
    ylabel = 'entries (normalized)' if options.normalize else 'entries'
    plotfunc.SetAxisLabels(can,options.xlabel.get(variable),ylabel,yratiolabel=('pull' if options.pull else 'ratio'))
    plotfunc.AutoFixAxes(can)

    if not options.log :
        if can.GetPrimitive('pad_top') :
            plotfunc.AutoFixYaxis(can.GetPrimitive('pad_top'),minzero=True)
        else :
            plotfunc.AutoFixYaxis(can,minzero=True)

    return can

#-------------------------------------------------------------------------
def main(options,args) :

    plotfunc.SetupStyle()

    files_g,trees_g,keys_g = anaplot.GetTreesFromFiles(options.gen   ,treename=options.treename,xAODInit=options.xAODInit)
    files_r,trees_r,keys_r = anaplot.GetTreesFromFiles(options.reco,treename=options.treename,xAODInit=options.xAODInit)

    scales_g = anaplot.GetScales(files_g,trees_g,keys_g,options)
    scales_r = anaplot.GetScales(files_r,trees_r,keys_r,options)

    weight_g = options.genweight
    if ''.join(options.gencuts) :
        weight_g = (weight_g+'*(%s)'%(' && '.join(options.gencuts).lstrip('& ').rstrip('& '))).lstrip('*')

    weight_r = options.recoweight
    if ''.join(options.recocuts) :
        weight_r = (weight_r+'*(%s)'%(' && '.join(options.recocuts).lstrip('& ').rstrip('& '))).lstrip('*')

    cans = []

    # get the histograms from the files
    for v in options.variables :
        gen_hists = []
        reco_hists = []

        # For gen-level histo var name
        vmc = options.variablemap.get(v,v)

        if options.gen :
            gen_hists = anaplot.GetVariableHistsFromTrees(trees_g,keys_g,vmc,weight_g,options,scales=scales_g,files=files_g)
            gen_hists = anaplot.MergeSamples(gen_hists,options)
            anaplot.PrepareBkgHistosForStack(gen_hists,options)
            gen_hists[0].SetLineColor(ROOT.kRed+1)

        if options.reco :
            reco_hists = anaplot.GetVariableHistsFromTrees(trees_r,keys_r,v,weight_r,options,scales=scales_r,files=files_r)
            reco_hists = anaplot.MergeSamples(reco_hists,options)
            anaplot.PrepareSignalHistos(reco_hists,options)
            reco_hists[0].SetLineColor(ROOT.kBlack)
            reco_hists[0].SetMarkerColor(ROOT.kBlack)

        if options.normalize :
            for hist in reco_hists+gen_hists :
                if not hist : continue
                hist.Scale(1/float(hist.Integral()))

        if options.rebin :
            for hist in reco_hists+gen_hists :
                if not hist : continue
                plotfunc.ConvertToDifferential(hist)

        if len(gen_hists) != 1 :
            print 'gen_hists has length != 1. exiting.'
            print gen_hists
            import sys; sys.exit()
        if len(reco_hists) != 1 :
            print 'reco_hists has length != 1. exiting.'
            import sys; sys.exit()

        ## Special canvas:
        cans.append(DrawHistosCutComparison(v,options,gen_hist=gen_hists[0],reco_hist=reco_hists[0]))

    if options.afterburner :
        for can in cans :
            options.afterburner(can)

    anaplot.UpdateCanvases(cans,options)

    if options.xAODInit :
        ROOT.xAOD.ClearTransientTrees()

    if not options.batch :
        raw_input('Press enter to exit')

    anaplot.doSaving(options,cans)

    print 'done.'
    return

if __name__ == '__main__':

    p = anaplot.TreePlottingOptParser()
    p.p.remove_option('--bkgs')
    p.p.remove_option('--signal')
    p.p.remove_option('--data')
    p.p.add_option('--gen',type='string',default='',dest='gen',help='input files for generator-level files (csv)')
    p.p.add_option('--reco',type='string',default='',dest='reco',help='input files for reco-level files (csv)')
    options,args = p.parse_args()

    options.gencuts = []
    options.recocuts = []

    for x in ['gen','reco',
              'recoweight','genweight',
              'recocuts','gencuts',
              ] :
        if hasattr(options.usermodule,x) :
            print 'setting attribute',x,'to',getattr(options.usermodule,x)
            setattr(options,x,getattr(options.usermodule,x))

    options.gen = anaplot.ExpandWildcard(options.gen)
    options.gen = anaplot.AddDotRoot(options.gen)
    options.reco = anaplot.ExpandWildcard(options.reco)
    options.reco = anaplot.AddDotRoot(options.reco)

    if not options.variables :
        print 'Error! Please specify a variable!'
        sys.exit()

    main(options,args)

