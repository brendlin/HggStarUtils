
#include "PicoXaodSkimAlgos_helpers.h"
#include "dscb.C"
//#include "turnon.C"

//
// To add a pTthrust category (the cut is hard-coded below)
//
void skim(TFile* oldfile,TTree* oldtree,const char* name,const char* cuts,char* branches,const char* outdir,const char* filename_nodotroot) {

  // Apply the "cuts" selection
  TEntryList* elist = GetTEntryListFromSelection(oldtree,name,cuts);

  // Copy only the specified subset of branches
  SetSelectedBranchStatusesOn(oldtree,branches);

  //TRandom3 rand(1);

  bool doTrackSmearing = oldtree->FindBranch("HGamElectronsAuxDyn.pt0");
  bool doMuonEff       = oldtree->FindBranch("HGamMuonsAuxDyn.pt0");

  float HGamMuonsAuxDyn_pt0;
  float HGamMuonsAuxDyn_pt1;
  float HGamMuonsAuxDyn_eta0;
  float HGamMuonsAuxDyn_eta1;
  float HGamElectronsAuxDyn_pt0;
  float HGamElectronsAuxDyn_pt1;
  float HGamElectronsAuxDyn_eta0;
  float HGamElectronsAuxDyn_eta1;
  float HGamPhotonsAuxDyn_pt0;
  float HGamEventInfoAuxDyn_mll;
  float HGamEventInfoAuxDyn_deltaEta_ll;
  float HGamEventInfoAuxDyn_deltaPhiMagnet_ll;
  float HGamEventInfoAuxDyn_deltaPhiMagnetRescaled_ll;
  float HGamEventInfoAuxDyn_pt_ll;
  
  if (doMuonEff) {
    oldtree->SetBranchStatus ("HGamMuonsAuxDyn.pt0",1);
    oldtree->SetBranchAddress("HGamMuonsAuxDyn.pt0",&HGamMuonsAuxDyn_pt0);
    oldtree->SetBranchStatus ("HGamMuonsAuxDyn.pt1",1);
    oldtree->SetBranchAddress("HGamMuonsAuxDyn.pt1",&HGamMuonsAuxDyn_pt1);
    oldtree->SetBranchStatus ("HGamMuonsAuxDyn.eta0",1);
    oldtree->SetBranchAddress("HGamMuonsAuxDyn.eta0",&HGamMuonsAuxDyn_eta0);
    oldtree->SetBranchStatus ("HGamMuonsAuxDyn.eta1",1);
    oldtree->SetBranchAddress("HGamMuonsAuxDyn.eta1",&HGamMuonsAuxDyn_eta1);
  }

  if (doTrackSmearing) {
    oldtree->SetBranchStatus ("HGamElectronsAuxDyn.pt0",1);
    oldtree->SetBranchAddress("HGamElectronsAuxDyn.pt0",&HGamElectronsAuxDyn_pt0);
    oldtree->SetBranchStatus ("HGamElectronsAuxDyn.pt1",1);
    oldtree->SetBranchAddress("HGamElectronsAuxDyn.pt1",&HGamElectronsAuxDyn_pt1);
    oldtree->SetBranchStatus ("HGamElectronsAuxDyn.eta0",1);
    oldtree->SetBranchAddress("HGamElectronsAuxDyn.eta0",&HGamElectronsAuxDyn_eta0);
    oldtree->SetBranchStatus ("HGamElectronsAuxDyn.eta1",1);
    oldtree->SetBranchAddress("HGamElectronsAuxDyn.eta1",&HGamElectronsAuxDyn_eta1);

    oldtree->SetBranchStatus ("HGamEventInfoAuxDyn.pt_ll",1);
    oldtree->SetBranchAddress("HGamEventInfoAuxDyn.pt_ll",&HGamEventInfoAuxDyn_pt_ll);
    oldtree->SetBranchStatus ("HGamEventInfoAuxDyn.deltaEta_ll",1);
    oldtree->SetBranchAddress("HGamEventInfoAuxDyn.deltaEta_ll",&HGamEventInfoAuxDyn_deltaEta_ll);
    oldtree->SetBranchStatus ("HGamEventInfoAuxDyn.deltaPhiMagnet_ll",1);
    oldtree->SetBranchAddress("HGamEventInfoAuxDyn.deltaPhiMagnet_ll",&HGamEventInfoAuxDyn_deltaPhiMagnet_ll);
    oldtree->SetBranchStatus ("HGamEventInfoAuxDyn.deltaPhiMagnetRescaled_ll",1);
    oldtree->SetBranchAddress("HGamEventInfoAuxDyn.deltaPhiMagnetRescaled_ll",&HGamEventInfoAuxDyn_deltaPhiMagnetRescaled_ll);
  }

  oldtree->SetBranchStatus ("HGamPhotonsAuxDyn.pt0",1);
  oldtree->SetBranchAddress("HGamPhotonsAuxDyn.pt0",&HGamPhotonsAuxDyn_pt0);

  oldtree->SetBranchStatus ("HGamEventInfoAuxDyn.m_ll",1);
  oldtree->SetBranchAddress("HGamEventInfoAuxDyn.m_ll",&HGamEventInfoAuxDyn_mll);

  //Create a new file + a clone of old tree in new file
  TFile *newfile = new TFile(Form("%s/%s.root",outdir,filename_nodotroot),"recreate");
  TTree* newtree = oldtree->CloneTree(0);

  // Leading
  TF1 f_leading("Fit to DSCB (leading)",dscb,0,2,7);

  f_leading.SetParameters(9.01979e-02,
                          3.45270e-02,
                          2.97359e-01,
                          7.13949e-01,
                          6.64047e+00,
                          3.20115e+00,
                          1.01520e+00
                          );

  // Subleading
  TF1 f_sublead("Fit to DSCB (subleading)",dscb,0,2,7);
  f_sublead.SetParameters(
                          1.33010e-01,
                          1.75356e-02,
                          2.53431e-01,
                          7.41292e-01,
                          2.94694e+00,
                          2.30235e+00,
                          1.01444e+00
                          );

  /*   // Create the new, derived branch */
  float HGamGSFTrackParticlesAuxDyn_pt0 = -99;
  float HGamGSFTrackParticlesAuxDyn_pt1 = -99;
  if (doTrackSmearing) {
    newtree->Branch("HGamGSFTrackParticlesAuxDyn.pt0", &HGamGSFTrackParticlesAuxDyn_pt0, "HGamGSFTrackParticlesAuxDyn.pt0/F");
    newtree->Branch("HGamGSFTrackParticlesAuxDyn.pt1", &HGamGSFTrackParticlesAuxDyn_pt1, "HGamGSFTrackParticlesAuxDyn.pt1/F");
  }

/*   TF1 turnon_func_photon("turnon_func_photon",turnon_f_photon,0,1000,3); */
/*   turnon_func_photon.SetParameters(14,5.1,0.94); */


  //
  // Muons
  //
  TF1 turnon_func_mu1("turnon_func_mu1","pol3",0,1000);
  turnon_func_mu1.SetParameters(
                                -3.2648,
                                1.88641,
                                -0.271893,
                                0.0129066
                                );

  TF1 turnon_func_mu0("turnon_func_mu0","pol5",0,1000);
  turnon_func_mu0.SetParameters(
                                -0.26766,
                                0.0914452,
                                -0.00249145,
                                3.3925e-05,
                                -2.36858e-07,
                                6.62371e-10
                                );

  TF1 turnon_func_photon("turnon_func_photon","pol4",0,1000);
  if (doMuonEff)
    turnon_func_photon.SetParameters(
                                     -2.50535,
                                     0.170072,
                                     -0.00284204,
                                     1.95342e-05,
                                     -4.69755e-08
                                     );

  TF1 turnon_func_mll("turnon_func_mll","pol4",0,1000);
  if (doMuonEff)
    turnon_func_mll.SetParameters(
                                  0.841353,
                                  0.0811987,
                                  -0.00796218,
                                  0.00032288,
                                  -4.54581e-06
                                  );

  //
  // Resolved electrons
  //
  if (doTrackSmearing)
    turnon_func_mll.SetParameters(
                                  0.742694,
                                  -0.519795,
                                  0.238731,
                                  -0.025846,
                                  0.000697929
                                  );

  TF1 turnon_func_el1_res("turnon_func_el1_res","pol4",0,1000);
  turnon_func_el1_res.SetParameters(
                                    1,
                                    1,
                                    1,
                                    1,
                                    1
                                    );

  TF1 turnon_func_el0_res("turnon_func_el0_res","pol6",0,1000);
  turnon_func_el0_res.SetParameters(
                                    -99.6145,
                                    12.8877,
                                    -0.67328,
                                    0.0183852,
                                    -0.000277048,
                                    2.18667e-06,
                                    -7.07097e-09
                                    );

  if (doTrackSmearing)
    turnon_func_photon.SetParameters(
                                     -1.82682,
                                     0.139528,
                                     -0.00246115,
                                     1.88536e-05,
                                     -5.37007e-08
                                     );

  //
  // Merged electrons - near
  //
  TF1 turnon_func_ptll_mer_near("turnon_func_ptll_mer_near","pol4",0,1000);
  turnon_func_ptll_mer_near.SetParameters(
                                          -2.38212,
                                          0.102836,
                                          -0.000815131,
                                          4.50449e-08,
                                          1.38934e-08
                                          );

  TF1 turnon_func_photon_mer_near("turnon_func_photon_mer_near","pol4",0,1000);
  turnon_func_photon_mer_near.SetParameters(
                                            -0.965731,
                                            0.0788701,
                                            -0.000981151,
                                            3.99854e-06,
                                            -1.97246e-09
                                            );

  // Merged electrons - far
  TF1 turnon_func_ptll_mer_far("turnon_func_ptll_mer_far","pol4",0,1000);
  turnon_func_ptll_mer_far.SetParameters(
                                         -1.01422,
                                         0.042362,
                                         0.00023864,
                                         -7.42715e-06,
                                         3.1999e-08
                                         );

  TF1 turnon_func_photon_mer_far("turnon_func_photon_mer_far","pol4",0,1000);
  turnon_func_photon_mer_far.SetParameters(
                                           -0.752726,
                                           0.0767325,
                                           -0.00106891,
                                           5.14588e-06,
                                           -4.96807e-09
                                           );

  //
  // Merged electrons - near
  //
  TF1 turnon_func_ptll_mer_all("turnon_func_ptll_mer_all","pol4",0,1000);
  turnon_func_ptll_mer_all.SetParameters(
                                         -1.02797,
                                         0.0397508,
                                         0.000304619,
                                         -8.43448e-06,
                                         3.69105e-08
                                         );

  TF1 turnon_func_photon_mer_all("turnon_func_photon_mer_all","pol4",0,1000);
  turnon_func_photon_mer_all.SetParameters(
                                           -0.788976,
                                           0.0734317,
                                           -0.000932459,
                                           3.81923e-06,
                                           -1.46756e-09
                                           );

/*   TF1 turnon_func_mu0_eta0p0("turnon_func_mu0_eta0p0",turnon_f_muons,0,1000,4); */
/*   TF1 turnon_func_mu0_eta0p1("turnon_func_mu0_eta0p1",turnon_f_muons,0,1000,4); */
/*   TF1 turnon_func_mu0_eta2p5("turnon_func_mu0_eta2p5",turnon_f_muons,0,1000,4); */

/*   TF1 turnon_func_mu1_eta0p0("turnon_func_mu0_eta0p0",turnon_f_muons,0,1000,4); */
/*   TF1 turnon_func_mu1_eta0p1("turnon_func_mu0_eta0p1",turnon_f_muons,0,1000,4); */
/*   TF1 turnon_func_mu1_eta2p5("turnon_func_mu0_eta2p5",turnon_f_muons,0,1000,4); */

/*   turnon_func_mu0_eta0p0.SetParameters(1.6,3.97,446,353); */
/*   turnon_func_mu0_eta0p1.SetParameters(2.824,10.1987,89629,10477); */
/*   turnon_func_mu0_eta2p5.SetParameters(2.99,12.2,51024,2322); */

/*   turnon_func_mu1_eta0p0.SetParameters(1.9,-1.32,418,262); */
/*   turnon_func_mu1_eta0p1.SetParameters(3.57,2.88,4175680,60842); */
/*   turnon_func_mu1_eta2p5.SetParameters(0.943,-6.89,70.88,62.13); */

  float weight_photonEff;
  newtree->Branch("weight_photonEff", &weight_photonEff, "weight_photonEff/F");
  float weight_photonEff_mer;

  float weight_lep0Eff = 1;
  float weight_lep1Eff = 1;
  float weight_lep0Eff_mer = 1;
  float weight_lep1Eff_mer = 1;
  if (doMuonEff || doTrackSmearing) {
    newtree->Branch("weight_lep0Eff", &weight_lep0Eff, "weight_lep0Eff/F");
    newtree->Branch("weight_lep1Eff", &weight_lep1Eff, "weight_lep1Eff/F");
  }
  if (doTrackSmearing) {
    newtree->Branch("weight_lep0Eff_mer", &weight_lep0Eff_mer, "weight_lep0Eff_mer/F");
    newtree->Branch("weight_lep1Eff_mer", &weight_lep1Eff_mer, "weight_lep1Eff_mer/F");    
    newtree->Branch("weight_photonEff_mer", &weight_photonEff_mer, "weight_photonEff_mer/F");    
  }

  float weight_mll = 1;
  newtree->Branch("weight_mll", &weight_mll, "weight_mll/F");

  for (Long64_t el = 0; el < elist->GetN(); el++) {
    Long64_t entryNumber = elist->GetEntry(el);

    oldtree->GetEntry(entryNumber);

    if (doTrackSmearing) {
      // Resolved
      weight_lep0Eff = turnon_func_el0_res.Eval(std::min(HGamElectronsAuxDyn_pt0/1000.,40.));
      weight_lep1Eff = turnon_func_el1_res.Eval(std::min(HGamElectronsAuxDyn_pt1/1000.,14.));
      weight_photonEff = turnon_func_photon.Eval(std::min(HGamPhotonsAuxDyn_pt0/1000.,140.));
      weight_mll = turnon_func_mll.Eval(std::min(HGamEventInfoAuxDyn_mll/1000.,7.));

      // Merged
      HGamGSFTrackParticlesAuxDyn_pt0 = f_leading.GetRandom(0,2)*HGamElectronsAuxDyn_pt0;
      HGamGSFTrackParticlesAuxDyn_pt1 = f_sublead.GetRandom(0,2)*HGamElectronsAuxDyn_pt1;

      bool separateNearAndFar = false;
      if (separateNearAndFar) {
        bool isNearEle = (abs(HGamEventInfoAuxDyn_deltaEta_ll) < 0.05 && 
                          abs(HGamEventInfoAuxDyn_deltaPhiMagnet_ll) < 0.05);

        bool isFarEle = (abs(HGamEventInfoAuxDyn_deltaEta_ll) < 0.05 && 
                         abs(HGamEventInfoAuxDyn_deltaPhiMagnet_ll) > 0.05 &&
                         abs(HGamEventInfoAuxDyn_deltaPhiMagnetRescaled_ll) < 0.05);

        if (isNearEle) {
          // ptll
          weight_lep0Eff_mer = turnon_func_ptll_mer_near.Eval(std::min(HGamEventInfoAuxDyn_pt_ll/1000.,100.));
          weight_photonEff_mer = turnon_func_photon_mer_near.Eval(std::min(HGamPhotonsAuxDyn_pt0/1000.,80.));
        }
        else if (isFarEle) {
          weight_lep0Eff_mer = turnon_func_ptll_mer_far.Eval(std::min(HGamEventInfoAuxDyn_pt_ll/1000.,80.));
          weight_photonEff_mer = turnon_func_photon_mer_far.Eval(std::min(HGamPhotonsAuxDyn_pt0/1000.,80.));
        }
      }
      else { // treat near and far together..
        weight_lep0Eff_mer = turnon_func_ptll_mer_all.Eval(std::min(HGamEventInfoAuxDyn_pt_ll/1000.,80.));
        weight_photonEff_mer = turnon_func_photon_mer_all.Eval(std::min(HGamPhotonsAuxDyn_pt0/1000.,100.));
      }
    }

    if (doMuonEff) {
      weight_photonEff = turnon_func_photon.Eval(std::min(HGamPhotonsAuxDyn_pt0/1000.,120.));
      weight_lep0Eff = turnon_func_mu0.Eval(std::min(HGamMuonsAuxDyn_pt0/1000.,120.));
      weight_lep1Eff = turnon_func_mu1.Eval(std::min(HGamMuonsAuxDyn_pt1/1000.,6.));
      weight_mll = turnon_func_mll.Eval(std::min(HGamEventInfoAuxDyn_mll/1000.,30.));
    }


/*     if (doMuonEff) { */
/*       float abseta = fabs(HGamMuonsAuxDyn_eta0); */
/*       if      (0.0 <= abseta && abseta < 0.1)  weight_lep0Eff = turnon_func_mu0_eta0p0.Eval(HGamMuonsAuxDyn_eta0/1000.); */
/*       else if (0.1 <= abseta && abseta < 2.5)  weight_lep0Eff = turnon_func_mu0_eta0p1.Eval(HGamMuonsAuxDyn_eta0/1000.); */
/*       else /\*(2.5 <= abseta && abseta < 2.7)*\/ weight_lep0Eff = turnon_func_mu0_eta2p5.Eval(HGamMuonsAuxDyn_eta0/1000.); */

/*       abseta = fabs(HGamMuonsAuxDyn_eta1); */
/*       if      (0.0 <= abseta && abseta < 0.1)  weight_lep1Eff = turnon_func_mu1_eta0p0.Eval(HGamMuonsAuxDyn_eta1/1000.); */
/*       else if (0.1 <= abseta && abseta < 2.5)  weight_lep1Eff = turnon_func_mu1_eta0p1.Eval(HGamMuonsAuxDyn_eta1/1000.); */
/*       else /\*(2.5 <= abseta && abseta < 2.7)*\/ weight_lep1Eff = turnon_func_mu1_eta2p5.Eval(HGamMuonsAuxDyn_eta1/1000.); */
/*     } */

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
