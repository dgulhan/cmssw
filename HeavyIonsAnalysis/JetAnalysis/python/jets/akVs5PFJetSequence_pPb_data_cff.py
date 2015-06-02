

import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.patHeavyIonSequences_cff import *
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *

akVs5PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVs5PFJets"),
    matched = cms.InputTag("ak5HiGenJetsCleaned"),
    maxDeltaR = 0.5
    )

akVs5PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVs5PFJets"),
                                                        matched = cms.InputTag("hiGenParticles")
                                                        )

akVs5PFcorr = patJetCorrFactors.clone(
    useNPV = False,
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),                                                                
    src = cms.InputTag("akVs5PFJets"),
    payload = "AKVs5PF_generalTracks"
    )

akVs5PFpatJets = patJets.clone(jetSource = cms.InputTag("akVs5PFJets"),
                                               jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVs5PFcorr")),
                                               genJetMatch = cms.InputTag("akVs5PFmatch"),
                                               genPartonMatch = cms.InputTag("akVs5PFparton"),
                                               jetIDMap = cms.InputTag("akVs5PFJetID"),
                                               addBTagInfo         = False,
                                               addTagInfos         = False,
                                               addDiscriminators   = False,
                                               addAssociatedTracks = False,
                                               addJetCharge        = False,
                                               addJetID            = False,
                                               getJetMCFlavour     = False,
                                               addGenPartonMatch   = False,
                                               addGenJetMatch      = False,
                                               embedGenJetMatch    = False,
                                               embedGenPartonMatch = False,
                                               # embedCaloTowers     = False,
                                               # embedPFCandidates = False
				            )

akVs5PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVs5PFpatJets"),
                                                             genjetTag = 'ak5HiGenJetsCleaned',
                                                             rParam = 0.5,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJets',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlow'),
                                                             trackTag = cms.InputTag("generalTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
                                                             genParticles = cms.untracked.InputTag("hiGenParticles"),
							     eventInfoTag = cms.InputTag("generator")
                                                             )

akVs5PFJetSequence_mc = cms.Sequence(
						  akVs5PFmatch
                                                  *
                                                  akVs5PFparton
                                                  *
                                                  akVs5PFcorr
                                                  *
                                                  akVs5PFpatJets
                                                  *
                                                  akVs5PFJetAnalyzer
                                                  )

akVs5PFJetSequence_data = cms.Sequence(akVs5PFcorr
                                                    *
                                                    akVs5PFpatJets
                                                    *
                                                    akVs5PFJetAnalyzer
                                                    )

akVs5PFJetSequence_jec = cms.Sequence(akVs5PFJetSequence_mc)
akVs5PFJetSequence_mix = cms.Sequence(akVs5PFJetSequence_mc)

akVs5PFJetSequence = cms.Sequence(akVs5PFJetSequence_data)
