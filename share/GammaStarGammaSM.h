//
// Try to write a stupid macro...!
// Do not use ACLIC, since there is some issue.

/* #include "TruthUtils.h" */
#include <algorithm>

bool comparePt(const xAOD::Jet *a, const xAOD::Jet *b)
{
  return a->pt() > b->pt();
}

float deltaEta( const xAOD::IParticle& p1, const xAOD::IParticle& p2 )
{
  return p1.eta() - p2.eta();
}

float deltaRapidity( const xAOD::IParticle& p1, const xAOD::IParticle& p2 )
{
  return p1.rapidity() - p2.rapidity();
}

float deltaPhi( float phiA, float phiB )
{
  return  -remainder( -phiA + phiB, 2*M_PI );
}

float deltaPhi( const xAOD::IParticle & pA, const xAOD::IParticle & pB )
{
  return deltaPhi( pA.phi(), pB.phi() );
}

float trackLoopRadius( const xAOD::IParticle & p ) {
  // Gamma m vperp  / q B
  // or pT / qB
  // (1 GeV)/((speed of light)(electron charge)*(2 tesla)) = 1.668 Meters
  return 1.668*p.p4().Pt()/1000.;
}

float phiMagnet2T( const xAOD::IParticle& p) {
  if (fabs(p.eta()) < 1.52)
    // 1.500m is the radius of the barrel calorimeter
    // 1.210m is where the magnet coil is. So this is not perfect... but close enough perhaps.
    return asin(0.750/trackLoopRadius(p));

  // 3.512m is the start of the ID endplate (in m)
  // The factor of 0.5 is what I was missing the last time....
  // Instead use 2.642, which is the z of the solenoid.
  return 0.5 * (2.642 / trackLoopRadius(p)) * (p.p4().Pt() / fabs(p.p4().Pz()) );
}

float deltaPhiMagnet2T( const xAOD::TruthParticle & pA, const xAOD::TruthParticle & pB )
{
  return deltaPhi( pA.phi() + pA.charge() * phiMagnet2T(pA) , pB.phi() + pB.charge()* phiMagnet2T(pB)  );
}

float deltaPhiMagnet2T_Rescaled( const xAOD::TruthParticle & p1, const xAOD::TruthParticle & p2 )
{

  float pt = p1.p4().Pt() > p2.p4().Pt() ? p1.p4().Pt() : p2.p4().Pt();

  TLorentzVector pA;
  pA.SetPtEtaPhiM(pt,p1.p4().Eta(),p1.p4().Phi(),0.510998);

  TLorentzVector pB;
  pB.SetPtEtaPhiM(pt,p2.p4().Eta(),p2.p4().Phi(),0.510998);

  float trackLoopRadius_A = 1.668*pA.Pt()/1000.;
  float phiMagnet2T_A = ( (fabs(pA.Eta()) < 1.52) ?
                          asin(0.750/trackLoopRadius_A) :
                          0.5 * (2.642 / trackLoopRadius_A) * (pA.Pt() / fabs(pA.Pz()) ) );

  float trackLoopRadius_B = 1.668*pB.Pt()/1000.;
  float phiMagnet2T_B = ( (fabs(pB.Eta()) < 1.52) ?
                          asin(0.750/trackLoopRadius_B) :
                          0.5 * (2.642 / trackLoopRadius_B) * (pB.Pt() / fabs(pB.Pz()) ) );

  float dphi = deltaPhi( pA.Phi() + p1.charge() * phiMagnet2T_A ,
                         pB.Phi() + p2.charge() * phiMagnet2T_B  );

  return dphi;
}

float deltaR2( const xAOD::IParticle& pA, const xAOD::IParticle& pB, bool useRapidity=true )
{
  const float dPhi = deltaPhi( pA, pB );
  const float dPhiSq = dPhi*dPhi;
  if (useRapidity) {
    const float dRapidity = deltaRapidity( pA, pB );
    return dRapidity*dRapidity + dPhiSq;
  }
  else {
    const float dEta = deltaEta( pA, pB );
    return dEta*dEta + dPhiSq;
  }
}

float deltaR( const xAOD::IParticle& pA, const xAOD::IParticle& pB, bool useRapidity=true )
{ 
  return std::sqrt( deltaR2( pA, pB, useRapidity ) );
}

float Mt( const xAOD::MissingET_v1& met, const xAOD::IParticle& p )
{
  return sqrt(2*p.pt()*met.met()*(1-cos(deltaPhi(met.phi(),p.phi()))));
}

float Deta_j_j(const xAOD::Jet& j1, const xAOD::Jet& j2){
  return fabs(j1.eta() - j2.eta());
}

float Phi_0_2pi(float Phi_mpi_pi)
{
  float ret = Phi_mpi_pi;
  while (ret >= 2*M_PI) ret -= 2*M_PI;
  while (ret <      0.) ret += 2*M_PI;
  return ret;
}

void GammaStarGammaSM(TFile* file,std::string key) {

  /* CONFIGURATION */
  TString LeptonContainer = "BornLeptons"; // TruthElectrons or BornLeptons
  // dont forget to change the conf.py file!
  bool doDressed = false;
  bool doAnalysisSelection = true;
  int leptonChannel = 1; // 1: muons; 2: resolved electrons; 3: merged electrons
  // dont forget to change the conf.py file!
  bool doVBF = false;
  bool doNonVBF = false;
  bool doOverlapRemoval = true; // need to consider photons overlapping with jets
  bool doNtuple = true;
  /* END CONFIGURATION */

  bool doMuons = (leptonChannel == 1);
  bool doElectrons = !doMuons;
  bool doAllChannels = !doVBF && !doNonVBF;
  float GeV = 1000.;

  TFile* outFile = NULL;
  TTree* outTree = NULL;
  float EventInfoAuxDyn_mcEventWeight;
  float HGamTruthEventInfoAuxDyn_m_lly;
  float HGamTruthEventInfoAuxDyn_m_ly; // leading lepton plus photon
  float HGamTruthEventInfoAuxDyn_m_ll;
  float HGamTruthEventInfoAuxDyn_pt_ll;
  float HGamTruthEventInfoAuxDyn_pt_lly;
  float HGamTruthEventInfoAuxDyn_pTt_lly;
  float HGamTruthEventInfoAuxDyn_deltaR_ll;
  float HGamTruthEventInfoAuxDyn_deltaEta_ll;
  float HGamTruthEventInfoAuxDyn_deltaPhi_ll;
  float HGamTruthEventInfoAuxDyn_deltaPhiMagnet_ll;
  float HGamTruthEventInfoAuxDyn_deltaPhiMagnetRescaled_ll;
  float HGamTruthEventInfoAuxDyn_Deta_j_j;
  float HGamTruthEventInfoAuxDyn_m_jj;
  float HGamTruthEventInfoAuxDyn_Zepp_lly;
  float HGamTruthEventInfoAuxDyn_Dphi_lly_jj;
  float HGamTruthEventInfoAuxDyn_DRmin_y_leps_2jets;

  std::vector<float> HGamTruthPhotonsAuxDyn_pt;
  std::vector<float> HGamTruthPhotonsAuxDyn_eta;
  std::vector<float> HGamTruthLeptonsAuxDyn_pt;
  std::vector<float> HGamTruthLeptonsAuxDyn_eta;
  std::vector<float> HGamAntiKt4TruthWZJetsAuxDyn_pt;
  std::vector<float> HGamAntiKt4TruthWZJetsAuxDyn_eta;

  if (doNtuple) {
    outFile = new TFile(Form("%s_nano.root",key.c_str()), "RECREATE");
    outTree = new TTree("CollectionTree","evgen_tree");
    outTree->Branch("EventInfoAuxDyn.mcEventWeight",&EventInfoAuxDyn_mcEventWeight);
    outTree->Branch("HGamTruthEventInfoAuxDyn.m_lly",&HGamTruthEventInfoAuxDyn_m_lly);
    outTree->Branch("HGamTruthEventInfoAuxDyn.m_ly",&HGamTruthEventInfoAuxDyn_m_ly);
    outTree->Branch("HGamTruthEventInfoAuxDyn.m_ll",&HGamTruthEventInfoAuxDyn_m_ll);
    outTree->Branch("HGamTruthEventInfoAuxDyn.pt_ll",&HGamTruthEventInfoAuxDyn_pt_ll);
    outTree->Branch("HGamTruthEventInfoAuxDyn.pt_lly",&HGamTruthEventInfoAuxDyn_pt_lly);
    outTree->Branch("HGamTruthEventInfoAuxDyn.pTt_lly",&HGamTruthEventInfoAuxDyn_pTt_lly);
    outTree->Branch("HGamTruthEventInfoAuxDyn.deltaR_ll",&HGamTruthEventInfoAuxDyn_deltaR_ll);
    outTree->Branch("HGamTruthEventInfoAuxDyn.deltaEta_ll",&HGamTruthEventInfoAuxDyn_deltaEta_ll);
    outTree->Branch("HGamTruthEventInfoAuxDyn.deltaPhi_ll",&HGamTruthEventInfoAuxDyn_deltaPhi_ll);
    outTree->Branch("HGamTruthEventInfoAuxDyn.deltaPhiMagnet_ll",&HGamTruthEventInfoAuxDyn_deltaPhiMagnet_ll);
    outTree->Branch("HGamTruthEventInfoAuxDyn.deltaPhiMagnetRescaled_ll",&HGamTruthEventInfoAuxDyn_deltaPhiMagnetRescaled_ll);
    outTree->Branch("HGamTruthEventInfoAuxDyn.Deta_j_j",&HGamTruthEventInfoAuxDyn_Deta_j_j);
    outTree->Branch("HGamTruthEventInfoAuxDyn.m_jj",&HGamTruthEventInfoAuxDyn_m_jj);
    outTree->Branch("HGamTruthEventInfoAuxDyn.Zepp_lly",&HGamTruthEventInfoAuxDyn_Zepp_lly);
    outTree->Branch("HGamTruthEventInfoAuxDyn.Dphi_lly_jj",&HGamTruthEventInfoAuxDyn_Dphi_lly_jj);
    outTree->Branch("HGamTruthEventInfoAuxDyn.DRmin_y_leps_2jets",&HGamTruthEventInfoAuxDyn_DRmin_y_leps_2jets);

    outTree->Branch("HGamTruthPhotonsAuxDyn.pt",&HGamTruthPhotonsAuxDyn_pt);
    outTree->Branch("HGamTruthPhotonsAuxDyn.eta",&HGamTruthPhotonsAuxDyn_eta);
    outTree->Branch(Form("HGamTruth%sAuxDyn.pt",(doMuons ? "Muons":"Electrons")),&HGamTruthLeptonsAuxDyn_pt);
    outTree->Branch(Form("HGamTruth%sAuxDyn.eta",(doMuons ? "Muons":"Electrons")),&HGamTruthLeptonsAuxDyn_eta);
    outTree->Branch("HGamAntiKt4TruthWZJetsAuxDyn.pt",&HGamAntiKt4TruthWZJetsAuxDyn_pt);
    outTree->Branch("HGamAntiKt4TruthWZJetsAuxDyn.eta",&HGamAntiKt4TruthWZJetsAuxDyn_eta);
  }

  gROOT->cd();
  TH1F* h_PhotonPt   = new TH1F(Form("LeadingTruthPhotonPt_%s"  ,key.c_str()),"tmp_title",100,0,200);
  TH1F* h_LeptonPt   = new TH1F(Form("LeadingTruth%sPt_%s",(doMuons ? "Muon":"Electron"),key.c_str()),"tmp_title",120,0,120);
  TH1F* h_Lepton2Pt  = new TH1F(Form("SubleadTruth%sPt_%s",(doMuons ? "Muon":"Electron"),key.c_str()),"tmp_titl",120,0,60);
  TH2F* h_LeptonPts  = new TH2F(Form("LeadingTruth%sPt_SubleadTruth%sPt_%s",(doMuons ? "Muon":"Electron"),(doMuons ? "Muon":"Electron"),key.c_str()),"tmp_title",100,0,120,100,0,60);
  TH1F* h_DeltaRll   = new TH1F(Form("TruthDeltaRll_%s",key.c_str()),"tmp_titl",100,0,4);
  TH1F* h_mll        = new TH1F(Form("TruthMll_%s" ,key.c_str()),"tmp_titl",110,0,55);
  TH1F* h_ptll       = new TH1F(Form("TruthPtll_%s",key.c_str()),"tmp_titl",100,0,200);
  TH1F* h_mlly       = new TH1F(Form("TruthMlly_%s",key.c_str()),"tmp_titl",90, 90,180);
  TH1F* h_ptlly      = new TH1F(Form("TruthPtlly_%s",key.c_str()),"tmp_titl",100, 0,100);
  TH2F* h_ptll_mlly  = new TH2F(Form("TruthPtll_TruthMlly_%s",key.c_str()),"tmp_titl",100,0,100,100,70,200);

  TH2F* h_PhotonPt_LeptonPt   = new TH2F(Form("LeadingTruth%sPt_LeadingTruth%sPt_%s","Photon",(doMuons ? "Muon":"Electron"),key.c_str()),"tmp_title",100,0,200,100,0,120);
  TH2F* h_PhotonPt_Lepton2Pt  = new TH2F(Form("LeadingTruth%sPt_SubleadTruth%sPt_%s","Photon",(doMuons ? "Muon":"Electron"),key.c_str()),"tmp_title",100,0,200,100,0,60);

  TH1F* h_Jet0Pt   = new TH1F(Form("LeadingTruthJetPt_%s"  ,key.c_str()),"tmp_title",100,0,150);
  TH1F* h_Jet1Pt   = new TH1F(Form("SubleadTruthJetPt_%s"  ,key.c_str()),"tmp_title",100,0,150);
  TH1F* h_Jet0Eta  = new TH1F(Form("LeadingTruthJetEta_%s" ,key.c_str()),"tmp_title",100,-5,5);
  TH1F* h_Jet1Eta  = new TH1F(Form("SubleadTruthJetEta_%s" ,key.c_str()),"tmp_title",100,-5,5);
  TH1F* h_nJets    = new TH1F(Form("TruthNJets_%s"         ,key.c_str()),"tmp_title",5,-0.5,4.5);
  TH1F* h_deta_jj  = new TH1F(Form("TruthDeta_jj_%s"            ,key.c_str()),"tmp_title",30,2,8);
  TH1F* h_m_jj     = new TH1F(Form("TruthM_jj_%s"               ,key.c_str()),"tmp_title",46,80,1000);

  xAOD::Init();
  xAOD::TEvent* event = new xAOD::TEvent (xAOD::TEvent::kClassAccess);
  TTree* tree = (TTree*)file->Get("CollectionTree");
  if (!event->readFrom(file).isSuccess()) {
    std::cout << "Read failed." << std::endl;
    return;
  }

  for (Long64_t entry=0;entry<tree->GetEntries();++entry) {

    if (!(entry % 10000)) std::cout << Form("Processed %.3fM events",entry/1000000.) << std::endl;

    event->getEntry(entry);
    //if (entry > 5000) break;

    const xAOD::EventInfo* ei = 0;
    if (event->retrieve(ei,"EventInfo") == xAOD::TReturnCode::kFailure) {
      std::cout << "Error - could not find EventInfo." << std::endl;
      break;
    }
    float weight = ei->mcEventWeight();

    const xAOD::JetContainer* jets = 0;
    if (event->retrieve(jets,"AntiKt4TruthDressedWZJets") == xAOD::TReturnCode::kFailure) {
      std::cout << "Error - could not find jets." << std::endl;
      break;
    }

    const xAOD::TruthParticleContainer* photons = 0;
    if (event->retrieve(photons,"TruthPhotons") == xAOD::TReturnCode::kFailure) {
      std::cout << "Error - could not find photons." << std::endl;
      break;
    }

    const xAOD::TruthParticleContainer* leptons = 0;
    if (event->retrieve(leptons,LeptonContainer.Data()) == xAOD::TReturnCode::kFailure) {
      std::cout << Form("Error - could not find %s container.",LeptonContainer.Data()) << std::endl;
      break;
    }

    const xAOD::TruthParticle* selPhoton = NULL;

    for (auto ph : *photons) {
      unsigned int ph_type = ph->auxdata<unsigned int>("classifierParticleType");
      if (ph_type == 16) continue; // Allow Unk, Iso or NonIso photon (not Bkg (16))

      if (doAnalysisSelection) {
        if (ph->pt() < 20*GeV) continue;
        if (fabs(ph->eta()) > 2.37) continue;
        if (fabs(ph->eta()) > 1.37 && fabs(ph->eta()) < 1.52) continue;
      }

      if (!selPhoton) selPhoton = ph;
      if (ph->pt() > selPhoton->pt()) selPhoton = ph;
    }

    const xAOD::TruthParticle* selLepton0 = NULL;
    const xAOD::TruthParticle* selLepton1 = NULL;

    TLorentzVector tlv_lep0;
    TLorentzVector tlv_lep1;

    for (auto lep : *leptons) {
      /* std::cout << fabs(lep->pdgId()) << std::endl; */
      if (doElectrons && fabs(lep->pdgId()) != 11) continue;
      if (doMuons     && fabs(lep->pdgId()) != 13) continue;

      if (doAnalysisSelection) {
        if (doMuons && lep->pt() < 3.0*GeV) continue;
        if (doMuons && fabs(lep->eta()) > 2.7) continue;

        if (doElectrons && lep->pt() < 0.500*GeV) continue;
        if (doElectrons && fabs(lep->eta()) > 2.47) continue;
        if (doElectrons && fabs(lep->eta()) > 1.37 && fabs(lep->eta()) < 1.52) continue;
      }

      // Make the TLorentzVector
      TLorentzVector tmp_tlv_lep;
      if (doDressed)
        tmp_tlv_lep.SetPtEtaPhiE(lep->auxdata<float>("pt_dressed"),
                                 lep->auxdata<float>("eta_dressed"),
                                 lep->auxdata<float>("phi_dressed"),
                                 lep->auxdata<float>("e_dressed")
                                 );
      else
        tmp_tlv_lep = lep->p4();


      if (!selLepton0)
      {
        selLepton0 = lep;
        tlv_lep0 = tmp_tlv_lep;
      }
      else if (tmp_tlv_lep.Pt() > tlv_lep0.Pt()) {
        selLepton1 = selLepton0;
        tlv_lep1 = tlv_lep0;
        selLepton0 = lep;
        tlv_lep0 = tmp_tlv_lep;
      }
      else if (!selLepton1)
      {
        selLepton1 = lep;
        tlv_lep1 = tmp_tlv_lep;
      }
      else if (tmp_tlv_lep.Pt() > tlv_lep1.Pt())
      {
        selLepton1 = lep;
        tlv_lep1 = tmp_tlv_lep;
      }
    }

    // Overlap removal
    if (doOverlapRemoval) {
      if (selPhoton && selLepton0 && deltaR(*selPhoton,*selLepton0) < 0.4) selLepton0 = NULL;
      if (selPhoton && selLepton1 && deltaR(*selPhoton,*selLepton1) < 0.4) selLepton1 = NULL;
    }

    xAOD::JetContainer* goodJets = new xAOD::JetContainer();
    xAOD::AuxContainerBase* goodJetsAux = new xAOD::AuxContainerBase();
    goodJets->setStore( goodJetsAux ); //< Connect the two

    for (auto j : *jets) {
      /* if (selPhoton && deltaR(*selPhoton,*j) < 0.4) continue; */
      if (j->pt() < 20*GeV) continue;
      if (fabs(j->rapidity()) > 4.4) continue;

      // Overlap removal
      if (doOverlapRemoval) {
        if (selPhoton && deltaR(*j,*selPhoton) < 0.4) continue;
        if (doElectrons) {
          if (selLepton0 && deltaR(*j,*selLepton0) < 0.2) continue;
          if (selLepton1 && deltaR(*j,*selLepton1) < 0.2) continue;
          if (selLepton0 && deltaR(*j,*selLepton0) < 0.4) selLepton0 = NULL;
          if (selLepton1 && deltaR(*j,*selLepton1) < 0.4) selLepton1 = NULL;
        }
        if (doMuons) {
          if (selLepton0 && deltaR(*j,*selLepton0) < 0.4) continue;
          if (selLepton1 && deltaR(*j,*selLepton1) < 0.4) continue;
        }
      }

      //selJets.push_back( j );
      xAOD::Jet* jet = new xAOD::Jet();
      goodJets->push_back( jet ); // jet acquires the goodJets auxstore
      *jet= *j; // copies auxdata from one auxstore to the other

    }

    goodJets->sort(comparePt);

    if (false) {
      std::cout << goodJets->size() << std::endl;
      for (auto j : *goodJets) std::cout << " - " << j->pt() << std::endl;
    }

    // Cuts
    if (!selLepton0) {delete goodJetsAux; delete goodJets; continue;}
    if (!selLepton1) {delete goodJetsAux; delete goodJets; continue;}
    if (!selPhoton) {delete goodJetsAux; delete goodJets; continue;}

    float m_ll  = (tlv_lep0 + tlv_lep1).M();
    float pt_ll = (tlv_lep0 + tlv_lep1).Pt();
    float m_lly = (tlv_lep0 + tlv_lep1 + selPhoton->p4()).M();
    float m_ly = (tlv_lep0 + selPhoton->p4()).M();
    float pt_lly = (tlv_lep0 + tlv_lep1 + selPhoton->p4()).Pt();
    float deltaRll = deltaR(*selLepton0,*selLepton1,/*useRapidity*/false);

    TLorentzVector g1 = selPhoton->p4();
    TLorentzVector g2 = tlv_lep0 + tlv_lep1;
    float pTt_lly = fabs(g1.Px() * g2.Py() - g2.Px() * g1.Py()) / (g1 - g2).Pt() * 2.0;

    bool passAnalysisSelection = true;

    if (doAnalysisSelection) {
      //==== CUT 22 : Z Mass window cut ====
      if ( m_ll > 50.*GeV ) passAnalysisSelection = false;

      //==== CUT 23 : lly window cut ====
      if ( 105.*GeV > m_lly || m_lly > 160.*GeV ) passAnalysisSelection = false;

      //==== CUT 24 : mll window (veto J/Psi and Y) cut ====
      if(leptonChannel == 1){
        if ( (m_ll > 2.9*GeV && m_ll < 3.3*GeV) || (m_ll > 9.1*GeV && m_ll < 10.6*GeV) )
          passAnalysisSelection = false;
      }
      else{
        if ( (m_ll > 2.5*GeV && m_ll < 3.5*GeV) || (m_ll > 8.0*GeV && m_ll < 11.0*GeV) )
          passAnalysisSelection = false;
      }

      //==== CUT 25 : pt_ll fraction ggF cut ====
      //if (pt_ll/m_lly < 0.3) passAnalysisSelection = false;

      //==== CUT 26 : pt_y fraction ggF cut ====
      if (selPhoton->pt()/m_lly < 0.3) passAnalysisSelection = false;

      // Additional lepton pt cuts - probably need to improve this one:
      if (doMuons && selLepton1->pt() < 3.0*GeV) passAnalysisSelection = false;
      if (doElectrons && selLepton1->pt() < 0.500*GeV) passAnalysisSelection = false;

    }

    if (!passAnalysisSelection) {delete goodJetsAux; delete goodJets; continue;}

    float vbf_m = -1;
    float deta_jj = -99;
    float Zepp_lly = -99;
    float DRmin_y_leps_2jets = 99999;
    float Dphi_lly_jj = -99;

    // VBF cuts
    bool passVBF = false;
    if (goodJets->size() > 1){ //we have two or more jets - prerequisite to pass VBF
      passVBF = true;
      vbf_m = (goodJets->at(0)->p4() + goodJets->at(1)->p4()).M();
      deta_jj = Deta_j_j(*(goodJets->at(0)),*(goodJets->at(1)));

      Zepp_lly = (( tlv_lep0 + tlv_lep1 + selPhoton->p4()).Eta() -
                  (goodJets->at(0)->p4().Eta() + goodJets->at(1)->p4().Eta()) / 2.0 );

      Dphi_lly_jj = fabs(( tlv_lep0 + tlv_lep1 + selPhoton->p4()).DeltaPhi(goodJets->at(0)->p4() + goodJets->at(0)->p4()));

      DRmin_y_leps_2jets = std::min(DRmin_y_leps_2jets,deltaR(*(goodJets->at(0)),*selPhoton ,false));
      DRmin_y_leps_2jets = std::min(DRmin_y_leps_2jets,deltaR(*(goodJets->at(1)),*selPhoton ,false));
      DRmin_y_leps_2jets = std::min(DRmin_y_leps_2jets,deltaR(*(goodJets->at(0)),*selLepton0,false));
      DRmin_y_leps_2jets = std::min(DRmin_y_leps_2jets,deltaR(*(goodJets->at(1)),*selLepton0,false));
      DRmin_y_leps_2jets = std::min(DRmin_y_leps_2jets,deltaR(*(goodJets->at(0)),*selLepton1,false));
      DRmin_y_leps_2jets = std::min(DRmin_y_leps_2jets,deltaR(*(goodJets->at(1)),*selLepton1,false));

      passVBF = passVBF && vbf_m > 400*GeV;
      passVBF = passVBF && deta_jj > 2.5;
      passVBF = passVBF && goodJets->at(0)->pt() > 25 * GeV;
      passVBF = passVBF && goodJets->at(1)->pt() > 25 * GeV;
    }

    // apply these VBF cuts
    if (doVBF && !passVBF) {delete goodJetsAux; delete goodJets; continue;}
    if (doNonVBF && passVBF) {delete goodJetsAux; delete goodJets; continue;}

    // Cut to understand the effect of the low-mll range:
    //if (m_ll > 1*GeV) continue;

    /* if (selLepton0 && selLepton1) */
    /*   std::cout << "Electrons: " << selLepton0->pt() << " " << selLepton1->pt() << std::endl; */

    // quick pty reweighting
    //weight = weight* ( 0.356077 + 0.0119177*selPhoton->pt()*0.001 );

    // Fill histograms
    h_PhotonPt->Fill(selPhoton ? selPhoton->pt()*0.001 : 0,weight);
    h_LeptonPt ->Fill(selLepton0 ? tlv_lep0.Pt()*0.001 : 0,weight);
    h_Lepton2Pt->Fill(selLepton1 ? tlv_lep1.Pt()*0.001 : 0,weight);
    h_LeptonPts->Fill(tlv_lep0.Pt()*0.001, tlv_lep1.Pt()*0.001,weight);
    h_DeltaRll->Fill(selLepton0 && selLepton1 ? deltaRll : 999, weight);
    h_mll->Fill(selLepton0 && selLepton1 ? m_ll*0.001 : 0,weight);
    h_ptll->Fill(selLepton0 && selLepton1 ? pt_ll*0.001 : 0,weight);
    h_mlly->Fill(selLepton0 && selLepton1 && selPhoton ? m_lly*0.001 : 0,weight);
    h_ptlly->Fill(selLepton0 && selLepton1 && selPhoton ? pt_lly*0.001 : 0,weight);
    h_ptll_mlly->Fill(pt_ll*0.001, m_lly*0.001, weight);

    h_PhotonPt_LeptonPt->Fill(selPhoton->pt()*0.001, tlv_lep0.Pt()*0.001,weight);
    h_PhotonPt_Lepton2Pt->Fill(selPhoton->pt()*0.001, tlv_lep1.Pt()*0.001,weight);

    h_nJets->Fill(goodJets->size(), weight);
    if (goodJets->size() > 0) {
      h_Jet0Pt->Fill(goodJets->at(0)->pt()*0.001, weight);
      h_Jet0Eta->Fill(goodJets->at(0)->eta(), weight);
    }
    if (goodJets->size() > 1) {
      h_Jet1Pt->Fill(goodJets->at(1)->pt()*0.001, weight);
      h_Jet1Eta->Fill(goodJets->at(1)->eta(), weight);
      h_deta_jj->Fill(deta_jj, weight);
      h_m_jj->Fill(vbf_m*0.001, weight);
    }

    // Fill ntuples
    if (doNtuple) {
      HGamTruthPhotonsAuxDyn_pt .clear();
      HGamTruthPhotonsAuxDyn_eta.clear();
      HGamTruthLeptonsAuxDyn_pt .clear();
      HGamTruthLeptonsAuxDyn_eta.clear();
      HGamAntiKt4TruthWZJetsAuxDyn_pt .clear();
      HGamAntiKt4TruthWZJetsAuxDyn_eta.clear();

      EventInfoAuxDyn_mcEventWeight = weight;
      HGamTruthEventInfoAuxDyn_m_lly = m_lly;
      HGamTruthEventInfoAuxDyn_m_ly = m_ly;
      HGamTruthEventInfoAuxDyn_m_ll = m_ll;
      HGamTruthEventInfoAuxDyn_pt_ll = pt_ll;
      HGamTruthEventInfoAuxDyn_pt_lly = pt_lly;
      HGamTruthEventInfoAuxDyn_pTt_lly = pTt_lly;
      HGamTruthEventInfoAuxDyn_deltaR_ll = deltaRll;
      HGamTruthEventInfoAuxDyn_deltaEta_ll = deltaEta(*selLepton0,*selLepton1);
      HGamTruthEventInfoAuxDyn_deltaPhi_ll = selLepton0->charge() * deltaPhi(*selLepton0,*selLepton1);
      HGamTruthEventInfoAuxDyn_deltaPhiMagnet_ll = selLepton0->charge() * deltaPhiMagnet2T(*selLepton0,*selLepton1);
      HGamTruthEventInfoAuxDyn_deltaPhiMagnetRescaled_ll = selLepton0->charge() * deltaPhiMagnet2T_Rescaled(*selLepton0,*selLepton1);
      HGamTruthEventInfoAuxDyn_Deta_j_j = deta_jj;
      HGamTruthEventInfoAuxDyn_m_jj = vbf_m;
      HGamTruthEventInfoAuxDyn_Zepp_lly = Zepp_lly;
      HGamTruthEventInfoAuxDyn_Dphi_lly_jj = Dphi_lly_jj;
      HGamTruthEventInfoAuxDyn_DRmin_y_leps_2jets = DRmin_y_leps_2jets;

      if (selPhoton) {
        HGamTruthPhotonsAuxDyn_pt .push_back(selPhoton->pt() );
        HGamTruthPhotonsAuxDyn_eta.push_back(selPhoton->eta());
      }
      if (selLepton0) {
        HGamTruthLeptonsAuxDyn_pt .push_back(selLepton0->pt() );
        HGamTruthLeptonsAuxDyn_eta.push_back(selLepton0->eta());
      }
      if (selLepton1) {
        HGamTruthLeptonsAuxDyn_pt .push_back(selLepton1->pt() );
        HGamTruthLeptonsAuxDyn_eta.push_back(selLepton1->eta());
      }
      for (int jet_i=0; jet_i<goodJets->size(); jet_i++) {
        HGamAntiKt4TruthWZJetsAuxDyn_pt .push_back(goodJets->at(jet_i)->pt() );
        HGamAntiKt4TruthWZJetsAuxDyn_eta.push_back(goodJets->at(jet_i)->eta());
      }

      outTree->Fill();
    } // if doNtuple

    delete goodJetsAux;
    delete goodJets;

  }

  if (doNtuple) {
    outFile->Write();
    //outFile->Close();
  }

  //std::cout << "Finished." << std::endl;

  return;
}
