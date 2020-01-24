#include("Sherpa_i/2.2.8_NNPDF30NNLO.py")
include("Sherpa_i/Base_Fragment.py")
include("Sherpa_i/NNPDF30NNLO.py")

evgenConfig.description = "Sherpa eegamma + 0,1,2,3j@LO with yy* cuts, no Higgs"
evgenConfig.keywords = ["SM", "2electron", "photon", "LO" ]
evgenConfig.contact  = [ "atlas-generators-sherpa@cern.ch", "frank.siegert@cern.ch" ]
evgenConfig.minevents = 1000

genSeq.Sherpa_i.RunCard = """
(run){
  % tags for process setup
  NJET:=3; QCUT:=20;

  % me generator settings
  ME_SIGNAL_GENERATOR Comix;

  MASS[25]=1e10


}(run)

(processes){
  Process 93 93 -> 22 11 -11 93{NJET}
  Order (*,3); CKKW sqr(QCUT/E_CMS)
  PSI_ItMin 20000 {4}
  Integration_Error 0.99 {4}
  PSI_ItMin 50000 {5,6}
  Integration_Error 0.99 {5,6}
  End process
}(processes)

(selector){

# mll > 2*ml
#Mass 11 -11 0.001022 55
Mass 11 -11 0.5 55

# pT dilepton > 28
"PT" 90,90  28,E_CMS

# pt lepton
 MinSelector {
   "PT" 90 19.5,E_CMS:0.5,E_CMS [PT_UP]
   "PT" 90 13.0,E_CMS:4.5,E_CMS [PT_UP]
  }

# pT photon > 28
"PT" 22 28,E_CMS [PT_UP]

# three-body mass
"Calc(Mass(p[0]+p[1]+p[2])>95.0)" 11,-11,22 1,1

#photon isolation cuts
  IsolationCut  22  0.1  2  0.10
  DeltaR  22  90  0.1 1000.0


}(selector)
"""

genSeq.Sherpa_i.Parameters += [ "OL_PARAMETERS=redlib1=5=redlib2=5=write_parameters=1" ]
genSeq.Sherpa_i.NCores = 24 #was 96, 24 might not be enough
#genSeq.Sherpa_i.CleanupGeneratedFiles = 1
evgenConfig.nEventsPerJob = 2000