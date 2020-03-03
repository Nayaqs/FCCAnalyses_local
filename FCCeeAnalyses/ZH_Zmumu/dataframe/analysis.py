import sys
import ROOT

print "Load cxx analyzers ... ",
ROOT.gSystem.Load("libdatamodel")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal

_p = ROOT.fcc.ParticleData()
_s = ROOT.selectParticlesPtIso

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print " done"
    #__________________________________________________________
    def run(self):
        df2 = self.df.Define("selected_electrons", "selectParticlesPtIso(10, 0.4)(electrons, electronITags)") \
                     .Define("selected_muons", "selectParticlesPtIso(10, 0.4)(muons, muonITags)") \
                     .Define("selected_leptons", "mergeElectronsAndMuons(selected_electrons, selected_muons)") \
                     .Define("selected_leptons_pt", "get_pt(selected_leptons)") \
                     .Define("zeds", "LeptonicZBuilder(selected_leptons)") \
                     .Define("zeds_pt", "get_pt(zeds)") \
                     .Define("zeds_m", "get_mass(zeds)") \
                     .Define("jets_10_bs", "selectJets(10, true)(efjets, efbTags)") \
                     .Define("jets_10_lights", "selectJets(10, false)(efjets, efbTags)") \
                     .Define("selected_bs", "noMatchJets(0.2)(jets_10_bs, selected_leptons)") \
                     .Define("selected_lights", "noMatchJets(0.2)(jets_10_lights, selected_leptons)") \
                     .Define("nbjets", "get_njets(selected_bs)") \
                     .Define("njets", "get_njets2(selected_bs, selected_lights)") \
                     .Define("weight"," id_float(mcEventWeights)") \
                     .Define("zed_leptonic","ResonanceBuilder(23, 91)(selected_leptons)") \
                     .Define("zed_leptonic_m", "get_mass(zed_leptonic)") \
                     .Define("zed_leptonic_pt","get_pt(zed_leptonic)") \
                     .Define("zed_hadronic_light","JetResonanceBuilder(23, 91)(jets_10_lights)") \
                     .Define("zed_hadronic_light_m", "get_mass(zed_hadronic_light)") \
                     .Define("zed_hadronic_light_pt","get_pt(zed_hadronic_light)") \
                     .Define("zed_hadronic_b","JetResonanceBuilder(23, 91)(jets_10_bs)") \
                     .Define("zed_hadronic_b_m", "get_mass(zed_hadronic_b)") \
                     .Define("zed_hadronic_b_pt","get_pt(zed_hadronic_b)") \


        branchList = ROOT.vector('string')()
        for branchName in [
                "selected_leptons_pt",
                "zeds_pt",
                "zeds_m",
                "zed_leptonic_pt",
                "zed_leptonic_m",
                "zed_hadronic_light_pt",
                "zed_hadronic_light_m",
                "zed_hadronic_b_pt",
                "zed_hadronic_b_m",
                "nbjets",
                "njets",
                "weight",
        ]:
            branchList.push_back(branchName)
            df2.Snapshot("events", self.outname, branchList)
