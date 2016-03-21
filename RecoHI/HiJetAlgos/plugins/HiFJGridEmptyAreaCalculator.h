#ifndef HiJetBackground_HiFJGridEmptyAreaCalculator_h
#define HiJetBackground_HiFJGridEmptyAreaCalculator_h


// system include files
#include <memory>
#include <sstream>
#include <string>
#include <vector>

// user include files
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "TMath.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

class HiFJGridEmptyAreaCalculator : public edm::EDProducer {
   public:
      explicit HiFJGridEmptyAreaCalculator(const edm::ParameterSet&);
      ~HiFJGridEmptyAreaCalculator();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      
  /// @name setting a new event
  //\{
  //----------------------------------------------------------------

  /// tell the background estimator that it has a new event, composed
  /// of the specified particles.


private:

  /// configure the grid
  void setup_grid(double eta_min, double eta_max);
  void setup_grid_jet(const reco::Jet *jet);

  /// retrieve the grid cell index for a given PseudoJet
  int tile_index_jet(const reco::PFCandidate *pfCand);
  int tile_index_eta(const reco::PFCandidate *pfCand);
  int tile_index_eta_jet(const reco::PFCandidate *pfCand);
  int tile_index_phi(const reco::PFCandidate *pfCand);
  
  ///number of grid cells that overlap with jet constituents filling in the in between area
  int num_jet_grid_cells( std::vector<std::pair<int, int> >& indices );
  
  /// calculates the area of jets that fall within the eta 
  /// range by scaling kt areas using grid areas
  void calculate_total_jet_area(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void calculate_grid_rho(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  
  ///in a strip of eta band it calculates the median of rho over the different phi bins
  // void median_of_eta_band(std::vector<std::vector<double>>&  pt_vec);

  /// information about the grid
  const double twopi = 2*TMath::Pi(); 
  
  double _ymin, _ymax, _dy, _dphi, _tile_area, _gridWidth, _dyjet, _cell_area,
  _yminjet, _ymaxjet, _total_inbound_area, _band, _eta_min_jet, _eta_max_jet;
  int _ny, _nphi, _ntotal, _ntotaljet, _nyjet;
  
  std::vector<double> _rho_vs_eta;
  std::vector<double> _mean_rho_vs_eta;
  std::vector<double> _eta_max_grid;
  std::vector<double> _eta_min_grid;
  
  int n_tiles()  {return _ntotal;}
  double area_fraction()  {return TMath::Min(1., _total_inbound_area/((_ymax - _ymin)*twopi));}
  
  /// input tokens
  edm::EDGetTokenT<edm::View<reco::Jet>>                 jetsToken_;
  edm::EDGetTokenT<reco::PFCandidateCollection>          pfCandsToken_;
  edm::EDGetTokenT<std::vector<double>>                  mapEtaToken_;
  edm::EDGetTokenT<std::vector<double>>                  mapRhoToken_;
  edm::EDGetTokenT<std::vector<double>>                  mapRhoMToken_;
  
};

#endif

