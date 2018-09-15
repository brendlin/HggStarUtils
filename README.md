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
