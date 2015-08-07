import FWCore.ParameterSet.Config as cms

################################################################################### 
# pp iterative tracking modified for hiOffline reco (the vertex is the one reconstructed in HI)
################################### 5th step: large impact parameter tracking using TIB/TID/TEC stereo layer seeding

from RecoHI.HiTracking.HITrackingRegionProducer_cfi import *

###################################
from RecoTracker.IterativeTracking.PixelLessStep_cff import *

# NEW CLUSTERS (remove previously used clusters)
hiRegitPixelLessStepClusters = cms.EDProducer("HITrackClusterRemover",
                                                clusterLessSolution= cms.bool(True),
                                                oldClusterRemovalInfo = cms.InputTag("hiRegitMixedTripletStepClusters"),
                                                trajectories = cms.InputTag("hiRegitMixedTripletStepTracks"),
                                                overrideTrkQuals = cms.InputTag('hiRegitMixedTripletStepSelector','hiRegitMixedTripletStep'),
                                                TrackQuality = cms.string('highPurity'),
                                                pixelClusters = cms.InputTag("siPixelClusters"),
                                                stripClusters = cms.InputTag("siStripClusters"),
                                                Common = cms.PSet(
    maxChi2 = cms.double(9.0),
    ),
                                                Strip = cms.PSet(
    maxChi2 = cms.double(9.0),
    #Yen-Jie's mod to preserve merged clusters
    maxSize = cms.uint32(2)
    )
                                                )

# SEEDING LAYERS
hiRegitPixelLessStepSeedLayers =  RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepSeedLayers.clone()
hiRegitPixelLessStepSeedLayers.TIB.skipClusters = cms.InputTag('hiRegitPixelLessStepClusters')
hiRegitPixelLessStepSeedLayers.TID.skipClusters = cms.InputTag('hiRegitPixelLessStepClusters')
hiRegitPixelLessStepSeedLayers.TEC.skipClusters  = cms.InputTag('hiRegitPixelLessStepClusters')
hiRegitPixelLessStepSeedLayers.layerList = cms.vstring('TIB1+TIB2',
        'TID1_pos+TID2_pos','TID2_pos+TID3_pos',
        'TEC1_pos+TEC2_pos','TEC2_pos+TEC3_pos','TEC3_pos+TEC4_pos','TEC3_pos+TEC5_pos','TEC4_pos+TEC5_pos',
        'TID1_neg+TID2_neg','TID2_neg+TID3_neg',
        'TEC1_neg+TEC2_neg','TEC2_neg+TEC3_neg','TEC3_neg+TEC4_neg','TEC3_neg+TEC5_neg','TEC4_neg+TEC5_neg')

hiRegitPixelLessStepSeeds = RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepSeeds.clone()
hiRegitPixelLessStepSeeds.RegionFactoryPSet                                           = HiTrackingRegionFactoryFromJetsBlock.clone()
hiRegitPixelLessStepSeeds.ClusterCheckPSet.doClusterCheck                             = False # do not check for max number of clusters pixel or strips
hiRegitPixelLessStepSeeds.OrderedHitsFactoryPSet.SeedingLayers = 'hiRegitPixelLessStepSeedLayers'
hiRegitPixelLessStepSeeds.RegionFactoryPSet.RegionPSet.ptMin = 0.5


# building: feed the new-named seeds
hiRegitPixelLessStepTrajectoryFilter = RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepTrajectoryFilter.clone()

hiRegitPixelLessStepTrajectoryBuilder = RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepTrajectoryBuilder.clone(
    trajectoryFilter     = cms.PSet(refToPSet_ = cms.string('hiRegitPixelLessStepTrajectoryFilter')),
    clustersToSkip       = cms.InputTag('hiRegitPixelLessStepClusters')
)

hiRegitPixelLessStepTrackCandidates        =  RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepTrackCandidates.clone(
    src               = cms.InputTag('hiRegitPixelLessStepSeeds'),
    TrajectoryBuilderPSet = cms.PSet(refToPSet_ = cms.string('hiRegitPixelLessStepTrajectoryBuilder')),
    maxNSeeds=100000
    )

# fitting: feed new-names
hiRegitPixelLessStepTracks                 = RecoTracker.IterativeTracking.PixelLessStep_cff.pixelLessStepTracks.clone(
    src                 = 'hiRegitPixelLessStepTrackCandidates',
    AlgorithmName = cms.string('pixelLessStep')
    )


# Track selection
import RecoHI.HiTracking.hiMultiTrackSelector_cfi
hiRegitPixelLessStepSelector = RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiMultiTrackSelector.clone(
    src='hiRegitPixelLessStepTracks',
    trackSelectors= cms.VPSet(
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiLooseMTS.clone(
    name = 'hiRegitPixelLessStepLoose',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ), #end of pset
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiTightMTS.clone(
    name = 'hiRegitPixelLessStepTight',
    preFilterName = 'hiRegitPixelLessStepLoose',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ),
    RecoHI.HiTracking.hiMultiTrackSelector_cfi.hiHighpurityMTS.clone(
    name = 'hiRegitPixelLessStep',
    preFilterName = 'hiRegitPixelLessStepTight',
    d0_par2 = [9999.0, 0.0],
    dz_par2 = [9999.0, 0.0],
    applyAdaptedPVCuts = False
    ),
    ) #end of vpset
    ) #end of clone  

hiRegitPixelLessStep = cms.Sequence(
                             hiRegitPixelLessStepClusters *
                             hiRegitPixelLessStepSeedLayers *
                             hiRegitPixelLessStepSeeds *
                             hiRegitPixelLessStepTrackCandidates *
                             hiRegitPixelLessStepTracks *
                             hiRegitPixelLessStepSelector)
