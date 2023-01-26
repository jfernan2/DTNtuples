#ifndef DTNtuple_DTNtupleConfig_h
#define DTNtuple_DTNtupleConfig_h

/** \class DTNtupleConfig DTNtupleConfig.h DTDPGAnalysis/DTNtuples/src/DTNtupleConfig.h
 *  
 * Helper class to handle :
 * - configuration parameters for edm::ParameterSet
 * - DB information from edm::EventSetup
 * - HLT configuration from dm::EventSetup and dm::Run
 *
 * \author C. Battilana (INFN BO)
 *
 *
 */

#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "CalibMuon/DTDigiSync/interface/DTTTrigBaseSync.h"

#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"

#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"

#include "DTDPGAnalysis/DTNtuples/src/DTTrigGeomUtils.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include <iostream>
#include <fstream>

#include <map>
#include <string>
#include <memory>

namespace edm {
  class ParameterSet;
  class EventSetup;
  class Run;
}  // namespace edm

class DTNtupleConfig {
public:
  enum class PhaseTag { PH1 = 0, PH2 };

  /// Constructor
  DTNtupleConfig(const edm::ParameterSet &config, edm::ConsumesCollector &&collector);

  /// Update EventSetup information
  void getES(const edm::EventSetup &environment);

  /// Update EventSetup information
  void getES(const edm::Run &run, const edm::EventSetup &environment);

  /// Map containing different input tags
  std::map<std::string, edm::InputTag> m_inputTags;

  /// Map containing different boolean parameters
  std::map<std::string, bool> m_boolParams;

  /// Map containing different boolean parameters
  std::map<std::string, std::string> m_stringParams;

  /// The class to handle DT trigger time pedestals
  std::map<PhaseTag, std::unique_ptr<DTTTrigBaseSync>> m_dtSyncs;

  /// The class to perform DT local trigger coordinate conversions
  std::unique_ptr<DTTrigGeomUtils> m_trigGeomUtils;

  /// Tracking geometry
  edm::ESGetToken<GlobalTrackingGeometry, GlobalTrackingGeometryRecord> m_trackingGeomToken;
  edm::ESHandle<GlobalTrackingGeometry> m_trackingGeometry;

  /// DT geometry
  edm::ESGetToken<DTGeometry, MuonGeometryRecord> m_dtGeomToken;
  edm::ESGetToken<DTGeometry, MuonGeometryRecord> m_dtIdealGeomToken;
  edm::ESHandle<DTGeometry> m_dtGeometry;

  /// HLT config procider
  HLTConfigProvider m_hltConfig;

  /// Name and indices of the isolated trigger used by muon filler for trigger matching
  std::string m_isoTrigName;
  std::vector<int> m_isoTrigIndices;

  /// Name and indices of the non isolated trigger used by muon filler for trigger matching
  std::string m_trigName;
  std::vector<int> m_trigIndices;
};

#endif
