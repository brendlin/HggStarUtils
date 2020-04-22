#!/usr/bin/python
import sys,os
import ROOT
from array import array
from ROOT import *
gROOT.SetBatch(1)


def Shorten(name):
    name = name.replace('HGam','')
    name = name.replace('EventInfoAuxDyn.','')
    name = name.replace('AuxDyn','')
    return name

def Simplify(name):
    name = name.replace('[','_')
    name = name.replace(']','_')
    name = name.replace('/','_over_')
    name = name.replace('(','_')
    name = name.replace(')','_')
    return name

def PlotScan(title,xtitle,ytitle,filename,var_root,var_hi,var_lo,var_steps,scan):
    points = []
    increment = (var_hi-var_lo)/float(var_steps)
    for k in range(len(scan)):
        points.append(var_lo + k*increment)
    
    c = TCanvas("c","c",800,800)
    x, y = array( 'd' ), array( 'd' )
    for point in points:
        x.append(point)
    for val in scan:
        y.append(val)
    g =  TGraph(len(scan),x,y)
    g.GetXaxis().SetTitle(xtitle)
    g.GetYaxis().SetTitle(ytitle)
    g.SetTitle(title)
    g.Draw()
    c.Print(filename)



try:
    f = open(sys.argv[1])
except:
    print "ERROR: could open file with scan. A valid file path must be specified as an argument. Exiting"
    sys.exit()
    
lines = f.readlines()
scans = []
for line in lines:
    scan = []
    try:
        exec("scan = "+line)
    except:
        print "ERROR: Could not parse line:"
        print line
        sys.exit()
    scans.append(scan)
        
vars_seen = []
iteration = 1
var_number = 1

if not os.path.isdir(os.getcwd() + "/plots"):
    print 'No \"plots\" directory found. Creating it'
    os.mkdir(os.getcwd() + "/plots")

for i,scan in enumerate(scans):
    try:
        var =       scan[0]
        var_steps = scan[1][4]
        var_lo =    scan[1][5]
        var_hi =    scan[1][6]
        var_root =  scan[1][7]
        sgnf =      scan[2]
        sig =       scan[3]
        bkg =       scan[4]
    except:
        print "ERROR: could not parse scan:"
        print scan
        sys.exit()
    
    var_simple = Simplify(Shorten(var))
    
    if var in vars_seen:
        iteration = iteration + 1
        vars_seen = []
        var_number = 1

    
    print "Plotting" + str(iteration) + "_" + str(var_number) + "_" + var_simple
    PlotScan('Cut scan: significance',var_root,"significance","plots/"+sys.argv[1].split('.')[0]+"_significance_"+str(iteration)+"_"+str(var_number)+"_"+var_simple+".png",var_root,var_hi,var_lo,var_steps,sgnf)
    PlotScan('Cut scan: signal',var_root,"signal","plots/"+sys.argv[1].split('.')[0]+"_signal_"+str(iteration)+"_"+str(var_number)+"_"+var_simple+".png",var_root,var_hi,var_lo,var_steps,sig)
    PlotScan('Cut scan: background',var_root,"background","plots/"+sys.argv[1].split('.')[0]+"_background_"+str(iteration)+"_"+str(var_number)+"_"+var_simple+".png",var_root,var_hi,var_lo,var_steps,sig)
    
    vars_seen.append(var)
    var_number = var_number + 1
    
    
    
    
    

