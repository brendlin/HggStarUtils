#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TColor.h"
#include "TStyle.h"
#include <string>
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include "TBrowser.h"
#include "TTree.h"
#include "TChain.h"
#include "TFile.h"
#include "TDirectory.h"

#include "TPRegexp.h"

#include "TEntryList.h"
#include <string.h>

TEntryList* GetTEntryListFromSelection(TTree* tree,const char* name,const char* cuts) {
  // Apply the selection defined in "cuts"

  tree->SetBranchStatus("*",1);
  std::cout << Form("tree.Draw(\">>%s\",\"%s\",\"entrylist\")",name,cuts) << std::endl;
  tree->Draw(Form(">>%s",name),cuts,"entrylist");
  TEntryList* entryList = (TEntryList*)gDirectory->Get(name);
  std::cout << "number in TEntryList: " << entryList->GetN() << std::endl;

  return entryList;
}

void SetSelectedBranchStatusesOn(TTree* tree,char* branches) {
  // Set only a subset of branches to status 1
  // Iterate over branches and set branch status of particular ones.
  // branch names should be separated by ","

  tree->SetBranchStatus("*",0);

  char* token;
  token = strtok(branches,",");
  while (token != NULL) {
    tree->SetBranchStatus(token,1);
    token = strtok(NULL,",");
  }

  return;
}

// Copy all the base-directory histograms
//
void CopyHistogramsFromBaseDirectory(TFile* old_file,TFile* new_file) {
  // Copy any 0th-level histograms to the file too
  TIter next(old_file->GetListOfKeys());
  TKey *key;
  while ( (key = (TKey*)next()) ) {
    TClass *key_class = gROOT->GetClass(key->GetClassName());
    if (!key_class->InheritsFrom("TH1")) continue;
    TH1 *hist = (TH1*)key->ReadObj();
    new_file->cd();
    hist->Write();
  }

  return;
}

//
// To add a pTthrust category (the cut is hard-coded below)
//
void makePicoXaod_NewCategories(TFile* oldfile,TTree* oldtree,const char* name,const char* cuts,char* branches,const char* outdir,const char* filename_nodotroot) {

  // Apply the "cuts" selection
  TEntryList* elist = GetTEntryListFromSelection(oldtree,name,cuts);

  // Copy only the specified subset of branches
  SetSelectedBranchStatusesOn(oldtree,branches);


  // Grab the old variables that you need to derive the new variables
  int yyStarCategoryOld;
  oldtree->SetBranchStatus ("HGamEventInfoAuxDyn.yyStarCategory",1);
  oldtree->SetBranchAddress("HGamEventInfoAuxDyn.yyStarCategory",&yyStarCategoryOld);

  float pTt_lly;
  oldtree->SetBranchStatus ("HGamEventInfoAuxDyn.pTt_lly",1);
  oldtree->SetBranchAddress("HGamEventInfoAuxDyn.pTt_lly",&pTt_lly);


  //Create a new file + a clone of old tree in new file
  TFile *newfile = new TFile(Form("%s/%s.root",outdir,filename_nodotroot),"recreate");
  TTree* newtree = oldtree->CloneTree(0);

  // Create the new, derived branch
  int yyStarCategoryNew = 0;
  newtree->Branch("HGamEventInfoAuxDyn.yyStarCategoryNew", &yyStarCategoryNew, "HGamEventInfoAuxDyn.yyStarCategoryNew/I");

  for (Long64_t el = 0; el < elist->GetN(); el++) {
    Long64_t entryNumber = elist->GetEntry(el);

    oldtree->GetEntry(entryNumber);

    // Define the new branch
    yyStarCategoryNew = yyStarCategoryOld;
    float pTt_cutval = 50;
    if (yyStarCategoryNew == 1 && pTt_lly/1000. > pTt_cutval) yyStarCategoryNew = 7;
    if (yyStarCategoryNew == 2 && pTt_lly/1000. > pTt_cutval) yyStarCategoryNew = 8;
    if (yyStarCategoryNew == 3 && pTt_lly/1000. > pTt_cutval) yyStarCategoryNew = 9;

    newtree->Fill();
  }

  // Copy any 0th-level histograms to the file too
  CopyHistogramsFromBaseDirectory(oldfile,newfile);

  newfile->cd();
  newtree->AutoSave();

  newfile->Close();
  delete elist;
  delete newfile;
}
