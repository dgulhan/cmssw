

import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.patHeavyIonSequences_cff import *
from HeavyIonsAnalysis.JetAnalysis.inclusiveJetAnalyzer_cff import *

akVs1PFmatch = patJetGenJetMatch.clone(
    src = cms.InputTag("akVs1PFJets"),
    matched = cms.InputTag("ak1HiGenJetsCleaned"),
    maxDeltaR = 0.1
    )

akVs1PFparton = patJetPartonMatch.clone(src = cms.InputTag("akVs1PFJets"),
                                                        matched = cms.InputTag("genParticles")
                                                        )

akVs1PFcorr = patJetCorrFactors.clone(
    useNPV = False,
#    primaryVertices = cms.InputTag("hiSelectedVertex"),
    levels   = cms.vstring('L2Relative','L3Absolute'),                                                                
    src = cms.InputTag("akVs1PFJets"),
    payload = "AKVs1PF_hiIterativeTracks"
    )

akVs1PFpatJets = patJets.clone(jetSource = cms.InputTag("akVs1PFJets"),
                                               jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akVs1PFcorr")),
                                               genJetMatch = cms.InputTag("akVs1PFmatch"),
                                               genPartonMatch = cms.InputTag("akVs1PFparton"),
                                               jetIDMap = cms.InputTag("akVs1PFJetID"),
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

akVs1PFJetAnalyzer = inclusiveJetAnalyzer.clone(jetTag = cms.InputTag("akVs1PFpatJets"),
                                                             genjetTag = 'ak1HiGenJetsCleaned',
                                                             rParam = 0.1,
                                                             matchJets = cms.untracked.bool(False),
                                                             matchTag = 'patJets',
                                                             pfCandidateLabel = cms.untracked.InputTag('particleFlowTmp'),
                                                             trackTag = cms.InputTag("hiGeneralTracks"),
                                                             fillGenJets = False,
                                                             isMC = False,
                                                             genParticles = cms.untracked.InputTag("genParticles"),
							     eventInfoTag = cms.InputTag("generator")
                                                             )

akVs1PFJetSequence_mc = cms.Sequence(
						  akVs1PFmatch
                                                  *
                                                  akVs1PFparton
                                                  *
                                                  akVs1PFcorr
                                                  *
                                                  akVs1PFpatJets
                                                  *
                                                  akVs1PFJetAnalyzer
                                                  )

akVs1PFJetSequence_data = cms.Sequence(akVs1PFcorr
                                                    *
                                                    akVs1PFpatJets
                                                    *
                                                    akVs1PFJetAnalyzer
                                                    )

akVs1PFJetSequence_jec = cms.Sequence(akVs1PFJetSequence_mc)
akVs1PFJetSequence_mix = cms.Sequence(akVs1PFJetSequence_mc)

akVs1PFJetSequence = cms.Sequence(akVs1PFJetSequence_data)
