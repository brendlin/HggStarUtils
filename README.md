HggStarUtils - An Introduction to the Package
================

This package contains the following scripts:

 - **plottrees.py** (part of the genericUtils package)
   - A generic script for making stacked histograms comparing MC and data.
 - **makePicoXaod.py** (part of the genericUtils package)
   - This script allows you to make a smaller version of an existing flat ntuple.

Initial setup
==================

To get started, simply check out the package from git, and run the following commands
(or put them in your `.bash_profile` script):

     export PYTHONPATH=$PYTHONPATH:/path/to/HggStarUtils/python
     export PYTHONPATH=$PYTHONPATH:/path/to/HggStarUtils/genericUtils/python
     export PATH=$PATH:/path/to/HggStarUtils/genericUtils/macros

(This appends the python directories to PYTHONPATH, and makes the genericUtils/macros executable from
any directory.) Now you can run these scripts in any directory:

    cd testarea
    plottrees.py ...

And that's it - you're ready to go!

**makePicoXaod.py** (genericUtils) - Description and Instructions
==================

### What is it

This script, which lives inside genericUtils,
allows you to skim the existing ntuples (in our case HggStar MxAODs)
into much smaller ntuples that can e.g. be saved on your computer. Special configuration files are
included in this package to help run this package on photon-specific samples:
 - makePicoXaod_yyStarConf.py

The output will be a much smaller ntuple saved in an output directory of your choice.
For more information on the script, see the README from the genericUtils package.

### How to run it

You can run the script using the following commands:

    cd testarea
    ln -s /path/to/HggStarUtils/data/makePicoXaod_yyStarConf.py .
    makePicoXaod.py --config makePicoXaod_yyStarConf.py --bkgs Sherpa_CT10_mumugammaPt10_35.root,mc16d.Sherpa_CT10_mumugammaPt140.root --outdir yystar_output
    
Note that `--bkgs` is a comma-separated list of files that you want to run over. The output
files will have the same name as the input files, with "_pico.root" at the end, and stored
in the "yystar_output" directory in this case.

There is a data conf file set up for very small picoXaods, for e.g. running workspaces - to run it, do:

      cd testarea
      ln -s /path/to/HggStarUtils/data/makePicoXaod_dataConf.py .
      makePicoXaod.py --config makePicoXaod_dataConf.py --data data%.root --outdir yystar_output

**plottrees.py** (genericUtils) - Description and Instructions
==================

An example of how to use this script, using a conf file for Zmumu validation as an example (data15+16 vs mc16a), is below:

    plottrees.py --config plottrees_ZmumuyValidationConf.py --bkgs %Sherpa_CT10%mumugamma%r9364%.root --data ysy001.data16.%.root,ysy001.data15.p3083_p3402.root --fb 36.2 --log --signal %gamstargam%r9364%.root

**cutcomparisons.py** (genericUtils) - Description and Instructions
==================

This macro offers a way to compare different cut selection. Right now it only works for --signal MC.
To use it, make a config file and define inside a list called "cutcomparisons", e.g. to compare
different channels:

    cutcomparisons = [
        ['#mu#mu#gamma'      ,'HGamEventInfoAuxDyn.yyStarChannel == 1']
        ['ee#gamma resolved' ,'HGamEventInfoAuxDyn.yyStarChannel == 2']
        ['ee#gamma merged'   ,'HGamEventInfoAuxDyn.yyStarChannel == 3']
        ['ee#gamma ambiguous','HGamEventInfoAuxDyn.yyStarChannel == 4']
        ]

Note that the first element of the list corresponds to the name of the selection, and the subsequent
cuts are applied as usual.
Then run e.g. the following:

    cutcomparisons.py --signal %gamstargam%r9364%.root --config cutcomparisons_Channels.py

The cuts defined in the "cuts" option can/will still be applied on top, as a preselection to the
cuts specified in "cutcomparisons".
