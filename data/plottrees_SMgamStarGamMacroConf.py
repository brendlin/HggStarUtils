
treename = 'CollectionTree'

##
## CONFIGURATION
##
doMuons = False
##
## END CONFIGURATION
##

doElectrons = not doMuons

variables = [
    'LeadingTruth%sPt'%('Muon' if doMuons else 'Electron'),
    'SubleadTruth%sPt'%('Muon' if doMuons else 'Electron'),
    'LeadingTruthPhotonPt',
    'TruthMll',
    'TruthPtll',
    'TruthMlly',
    'TruthPtlly',
    'TruthDeltaRll',
    'LeadingTruthJetPt',
    'SubleadTruthJetPt',
    'LeadingTruthJetEta',
    'SubleadTruthJetEta',
    'TruthNJets',
    'TruthDeta_jj',
    'TruthM_jj',
    ]

plottext = ['Born leptons']

labels = {
    '%DAOD%':'Sherpa ll#gamma',
    'TRUTH5_Sherpa_228_NLO_mumu_mll05_core1%':'NLO ll#gamma',
    'TRUTH5_Sherpa_228_LO_mumu_mll05%':'LO ll#gamma',
    # 'TRUTH5_Sherpa_228_LO_mumu_mll05%':'m_{ll}>0.5',
    'TRUTH5_Sherpa_228_LO_mumu_mll02%':'m_{ll}>0.2',
    '%Sherpa_228_LO_ee%':'LO ee#gamma',
    '%DAOD_TRUTH5.mumugamma_LO_2M%':'LO #mu#mu#gamma',
    }

histformat = {
    'LeadingTruthPhotonPt':[None,None,None,'Leading truth p^{#gamma}_{T} [GeV]'],
    'LeadingTruthElectronPt':[None,None,None,'Leading truth p^{e}_{T} [GeV]'],
    'SubleadTruthElectronPt':[None,None,None,'Subleading truth p^{e}_{T} [GeV]'],
    'LeadingTruthMuonPt':[None,None,None,'Leading truth p^{#mu}_{T} [GeV]'],
    'SubleadTruthMuonPt':[None,None,None,'Subleading truth p^{#mu}_{T} [GeV]'],
    'LeadingTruthJetPt':[None,None,None,'Leading truth p^{jet}_{T} [GeV]'],
    'SubleadTruthJetPt':[None,None,None,'Subleading truth p^{jet}_{T} [GeV]'],
    'LeadingTruthJetEta':[None,None,None,'Leading truth #eta^{jet}'],
    'SubleadTruthJetEta':[None,None,None,'Subleading truth #eta^{jet}'],
    'TruthMll':[None,None,None,'truth m_{%s} [GeV]'%('#mu#mu' if doMuons else 'ee')],
    'TruthDeltaRll':[None,None,None,'truth #Delta^{}R_{ll} [GeV]'],
    'TruthPtll':[None,None,None,'truth p_{T}^{%s} [GeV]'%('#mu#mu' if doMuons else 'ee')],
    'TruthPtlly':[None,None,None,'truth p_{T}^{%s} [GeV]'%('#mu#mu#gamma' if doMuons else 'ee#gamma')],
    'TruthMlly':[None,None,None,'truth m_{%s#gamma} [GeV]'%('#mu#mu' if doMuons else 'ee')],
    'TruthNJets':[None,None,None,'truth N_{jet}'],
    'TruthDeta_jj':[None,None,None,'truth #Delta#eta_{jj}'],
    'TruthM_jj':[None,None,None,'truth m_{jj} [GeV]'],
    }

def afterburner(can) :
    import PlotFunctions as plotfunc
    import TAxisFunctions as taxisfunc
    import ROOT

    # Set ratio range; add dotted line at 1
    if plotfunc.GetBotPad(can) :
        taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(can),0,2)
        xmin,xmax = None,None
        for i in plotfunc.GetBotPad(can).GetListOfPrimitives() :
            if issubclass(type(i),ROOT.TH1) :
                xmin = i.GetXaxis().GetBinLowEdge(1)
                xmax = i.GetXaxis().GetBinLowEdge(i.GetNbinsX()+1)
        if xmin != None :
            line = ROOT.TLine(xmin,1,xmax,1)
            line.SetLineStyle(2)
            plotfunc.GetBotPad(can).cd()
            line.Draw()
            plotfunc.tobject_collector.append(line)

    return
