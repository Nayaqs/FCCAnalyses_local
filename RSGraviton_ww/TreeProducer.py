from __future__ import division
from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
from heppy.particles.tlv.resonance import Resonance2 as Resonance

import ROOT
from ROOT import *

ROOT.gROOT.ProcessLine(".L /afs/cern.ch/work/i/iarts/FCCSW/heppy/FCChhAnalyses/RSGraviton_ww/BDT_QCD.class.C+")

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        
	self.tree.var('weight', float)
	self.tree.var('nelectrons', float)
	self.tree.var('nmuons', float)

	bookParticle(self.tree, 'electron')
	bookParticle(self.tree, 'muon')
        bookMet(self.tree, 'met') 

	self.tree.var('Jet1_tau1', float)	
	self.tree.var('Jet1_tau2', float)
        self.tree.var('Jet1_tau3', float)
        self.tree.var('Jet2_tau1', float)
        self.tree.var('Jet2_tau2', float)
        self.tree.var('Jet2_tau3', float)
	self.tree.var('Jet1_tau32', float)
        self.tree.var('Jet1_tau31', float)
        self.tree.var('Jet1_tau21', float)
        self.tree.var('Jet2_tau32', float)
        self.tree.var('Jet2_tau31', float)
        self.tree.var('Jet2_tau21', float)

        bookParticle(self.tree, 'Jet1')
        bookParticle(self.tree, 'Jet2')

	bookParticle(self.tree, 'softDroppedJet1')
	bookParticle(self.tree, 'softDroppedJet2')
        
	bookParticle(self.tree, 'trimmedJet1')
        bookParticle(self.tree, 'trimmedJet2')

	bookParticle(self.tree, 'prunedJet1')
        bookParticle(self.tree, 'prunedJet2')

	self.tree.var('RSGravitonReconstructedMass', float)
	self.tree.var('RSGravitonReconstructedMass_trimmed', float)
	self.tree.var('RSGravitonReconstructedMass_softDropped', float)
	self.tree.var('RSGravitonReconstructedMass_pruned', float)

	self.tree.var('Jet1_Flow15',float)
	self.tree.var('Jet1_Flow25',float)
	self.tree.var('Jet1_Flow35',float)
	self.tree.var('Jet1_Flow45',float)
	self.tree.var('Jet1_Flow55',float)
	self.tree.var('Jet2_Flow15',float)
	self.tree.var('Jet2_Flow25',float)
	self.tree.var('Jet2_Flow35',float)
	self.tree.var('Jet2_Flow45',float)
	self.tree.var('Jet2_Flow55',float)
	
	self.tree.var('BDTvariable_qcd', float)

    def process(self, event):
        self.tree.reset()
	jets = getattr(event, self.cfg_ana.fatjets)
	muons = getattr(event, self.cfg_ana.muons)
	electrons = getattr(event, self.cfg_ana.electrons)

	if (len(jets)>1 and jets[0].pt() > 2000.):
		self.tree.fill('weight' , event.weight )

		self.tree.fill('Jet1_tau1' , jets[0].tau1 )
		self.tree.fill('Jet1_tau2' , jets[0].tau2 )
		self.tree.fill('Jet1_tau3' , jets[0].tau3 )
		self.tree.fill('Jet2_tau1' , jets[1].tau1 )
		self.tree.fill('Jet2_tau2' , jets[1].tau2 )
		self.tree.fill('Jet2_tau3' , jets[1].tau3 )
		self.tree.fill('nelectrons' , len(electrons) )
                self.tree.fill('nmuons' , len(muons) )
                fillMet(self.tree, 'met', event.met)
		if (len(electrons) >= 1):
			fillParticle(self.tree, 'electron', electrons[0])
		if (len(muons) >= 1):
			fillParticle(self.tree, 'muon', muons[0])


		if (jets[0].tau1 != 0.0):
			Jet1_tau21 = jets[0].tau2/jets[0].tau1
			self.tree.fill('Jet1_tau31' , jets[0].tau3/jets[0].tau1 )
		else:
			Jet1_tau21 = -99
			self.tree.fill('Jet1_tau31' , -99)

		self.tree.fill('Jet1_tau21' , Jet1_tau21)

		if (jets[0].tau2 != 0.0):
			Jet1_tau32 = jets[0].tau3/jets[0].tau2
		else:
			Jet1_tau32 = -99

		self.tree.fill('Jet1_tau32', Jet1_tau32)

		if (jets[1].tau1 != 0.0):
			self.tree.fill('Jet2_tau31' , jets[1].tau3/jets[1].tau1 )
			self.tree.fill('Jet2_tau21' , jets[1].tau2/jets[1].tau1 )
		else:
			self.tree.fill('Jet2_tau31' , -99)
			self.tree.fill('Jet2_tau21' , -99)

		if (jets[1].tau2 != 0.0):
			self.tree.fill('Jet2_tau32', jets[1].tau3/jets[1].tau2)
		else:
			self.tree.fill('Jet2_tau32', -99)

		fillParticle(self.tree, 'Jet1', jets[0])
		fillParticle(self.tree, 'Jet2', jets[1])

		fillParticle(self.tree, 'softDroppedJet1', jets[0].subjetsSoftDrop[0])
		fillParticle(self.tree, 'softDroppedJet2', jets[1].subjetsSoftDrop[0])

		fillParticle(self.tree, 'trimmedJet1', jets[0].subjetsTrimming[0])
		fillParticle(self.tree, 'trimmedJet2', jets[1].subjetsTrimming[0])

		fillParticle(self.tree, 'prunedJet1', jets[0].subjetsPruning[0])
		fillParticle(self.tree, 'prunedJet2', jets[1].subjetsPruning[0])

		jet1_ungroomed = ROOT.TLorentzVector(); jet2_ungroomed = ROOT.TLorentzVector()
		jet1_ungroomed.SetPtEtaPhiE(jets[0].pt(), jets[0].eta(), jets[0].phi(), jets[0].e())
		jet2_ungroomed.SetPtEtaPhiE(jets[1].pt(), jets[1].eta(), jets[1].phi(), jets[1].e())
		self.tree.fill('RSGravitonReconstructedMass', (jet1_ungroomed+jet2_ungroomed).M())            

		jet1_trimmed = ROOT.TLorentzVector(); jet2_trimmed = ROOT.TLorentzVector()
		jet1_trimmed.SetPtEtaPhiE(jets[0].subjetsTrimming[0].pt(),jets[0].subjetsTrimming[0].eta(),jets[0].subjetsTrimming[0].phi(),jets[0].subjetsTrimming[0].e())
		jet2_trimmed.SetPtEtaPhiE(jets[1].subjetsTrimming[0].pt(),jets[1].subjetsTrimming[0].eta(),jets[1].subjetsTrimming[0].phi(),jets[1].subjetsTrimming[0].e())
		self.tree.fill('RSGravitonReconstructedMass_trimmed', (jet1_trimmed+jet2_trimmed).M())

		jet1_pruned = ROOT.TLorentzVector(); jet2_pruned = ROOT.TLorentzVector()
		jet1_pruned.SetPtEtaPhiE(jets[0].subjetsPruning[0].pt(),jets[0].subjetsPruning[0].eta(),jets[0].subjetsPruning[0].phi(),jets[0].subjetsPruning[0].e())
		jet2_pruned.SetPtEtaPhiE(jets[1].subjetsPruning[0].pt(),jets[1].subjetsPruning[0].eta(),jets[1].subjetsPruning[0].phi(),jets[1].subjetsPruning[0].e())
		self.tree.fill('RSGravitonReconstructedMass_pruned', (jet1_pruned+jet2_pruned).M())

		jet1_softDropped = ROOT.TLorentzVector(); jet2_softDropped = ROOT.TLorentzVector()
		jet1_softDropped.SetPtEtaPhiE(jets[0].subjetsSoftDrop[0].pt(),
                                              jets[0].subjetsSoftDrop[0].eta(),
                                              jets[0].subjetsSoftDrop[0].phi(),
                                              jets[0].subjetsSoftDrop[0].e())
		jet2_softDropped.SetPtEtaPhiE(jets[1].subjetsSoftDrop[0].pt(),
				              jets[1].subjetsSoftDrop[0].eta(),
				              jets[1].subjetsSoftDrop[0].phi(),
				              jets[1].subjetsSoftDrop[0].e())
		self.tree.fill('RSGravitonReconstructedMass_softDropped', (jet1_softDropped+jet2_softDropped).M())
		
		#Flow n,5
		#############################################################################
                #REQIRES THE FOLLOWING IN heppy/analyzers/fcc/Reader.py AFTER LINE 151:
		
		#	particle_relations = defaultdict(list)
        	#       for tjet in store.get(self.cfg_ana.fatjets):
                #		for i in range(tjet.particles_size()):
                #     			particle_relations[Jet(tjet)].append(Particle(tjet.particles(i)))
            	#	for fatjet, particles in particle_relations.items():
                # 		fatjets[fatjet].jetConstituents = particles 

		#############################################################################

		R = 0.8

		flow_Jet1 = [0]*5
		flow_Jet2 = [0]*5

		constituent_vector = ROOT.TLorentzVector()
		for n in range(1,5+1):		
			for constituent in jets[0].jetConstituents[1:]:
				constituent_vector.SetPtEtaPhiE(constituent.pt(),constituent.eta(),constituent.phi(),constituent.e())
				dR = jet1_ungroomed.DeltaR(constituent_vector)
				if ((dR >= (n-1)/5*R) and (dR < n/5*R)):
					flow_Jet1[n-1] += abs(constituent.pt())/abs(jets[0].pt())
			for constituent in jets[1].jetConstituents[1:]:
                                constituent_vector.SetPtEtaPhiE(constituent.pt(),constituent.eta(),constituent.phi(),constituent.e())
                                dR = jet2_ungroomed.DeltaR(constituent_vector)
                                if ((dR >= (n-1)/5*R) and (dR < n/5*R)):
					flow_Jet2[n-1] += abs(constituent.pt())/abs(jets[1].pt())

		self.tree.fill('Jet1_Flow15', flow_Jet1[0]); self.tree.fill('Jet2_Flow15', flow_Jet2[0])
		self.tree.fill('Jet1_Flow25', flow_Jet1[1]); self.tree.fill('Jet2_Flow25', flow_Jet2[1])
		self.tree.fill('Jet1_Flow35', flow_Jet1[2]); self.tree.fill('Jet2_Flow35', flow_Jet2[2])
		self.tree.fill('Jet1_Flow45', flow_Jet1[3]); self.tree.fill('Jet2_Flow45', flow_Jet2[3])
		self.tree.fill('Jet1_Flow55', flow_Jet1[4]); self.tree.fill('Jet2_Flow55', flow_Jet2[4])
		
		varlist = [ 
				"Jet1_pt",
				"Jet1_tau21",
				"Jet1_tau32",
				"Jet1_Flow15",
				"Jet1_Flow25",
				"Jet1_Flow35",
				"Jet1_Flow45",
				"Jet1_Flow55",
				"softDroppedJet1_m",
		]

		inputs = ROOT.vector('string')()
		for v in varlist:
			inputs.push_back(v)

		mva = ROOT.ReadQCD(inputs)
		values = ROOT.vector('double')()

		values.push_back(jets[0].pt())
		values.push_back(Jet1_tau21)
		values.push_back(Jet1_tau32)
		values.push_back(flow_Jet1[0]) 
		values.push_back(flow_Jet1[1])
		values.push_back(flow_Jet1[2])
		values.push_back(flow_Jet1[3])
		values.push_back(flow_Jet1[4])        
		values.push_back(jets[0].subjetsSoftDrop[0].m())
         
   
		mva_value=mva.GetMvaValue(values)
		self.tree.fill('BDTvariable_qcd', mva_value)

                self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

