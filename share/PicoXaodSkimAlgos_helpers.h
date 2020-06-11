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
