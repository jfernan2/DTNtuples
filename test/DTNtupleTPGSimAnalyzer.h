#ifndef DTTnPBaseAnalysis_h
#define DTTnPBaseAnalysis_h

#include "DTNtupleBaseAnalyzer.h"

#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TEfficiency.h"
#include "TProfile.h"
#include "TMath.h"

#include <string>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <map>

// DT AM Emulator constants
#include "L1Trigger/DTTriggerPhase2/interface/constants.h"

using namespace cmsdt;

class DTNtupleTPGSimAnalyzer : public DTNtupleBaseAnalyzer 
{
  
public:
  
  DTNtupleTPGSimAnalyzer(const TString & inFileName,
			 const TString & outFileName);
  DTNtupleTPGSimAnalyzer(const TString & inFileName,
                         const TString & outFileName,
                         const TString & quality);
  DTNtupleTPGSimAnalyzer(const TString & inFileName,
                         const TString & outFileName,
                         const TString & quality,
                         const bool & DM);
  ~DTNtupleTPGSimAnalyzer();

  void virtual Loop() override;

protected:
  
  void book();
  void fill();
  void endJob();

private:
  
  Double_t trigPhiInRad(Double_t trigPhi, Int_t sector)
  {
   return trigPhi / PHIRES_CONV + TMath::Pi() / 6 * (sector - 1);
  }
  Double_t trigPhiInRadPh1(Double_t trigPhi, Int_t sector)
  {
   return trigPhi / 4096. + TMath::Pi() / 6 * (sector - 1);
  }
  void printMPs(int);
  void printSeg(int);
  void printHits();
  int getPh1Hits(int wh, int se, int st);
  int getPh2Hits(int wh, int se, int st);
  void printPh2Hits();
 
  TString quality_; 
  bool DM_; 
  TFile m_outFile;
  
  std::map<std::string, TH1*> m_plots;
  std::map<std::string, TH2*> m_plots2;
  std::map<std::string, TEfficiency*> m_effs;
  
  TH1F* makeHistoPer( std::string, std::string, vector<std::string>, std::string);  
  TH1F* makeHistoPerCorrelated( std::string, std::string, vector<std::string>, std::string);  
  Double_t m_minMuPt;
  Double_t m_maxMuPt;
  
  Double_t m_maxMuSegDPhi;
  Double_t m_maxMuSegDEta;
  
  Int_t m_minSegHits;
  Int_t m_minZSegHits;

  Double_t m_maxSegTrigDPhi;
  Double_t m_maxMuTrigDPhi;

  Double_t m_maxSegTrigDEta;
  Double_t MBRadius[3] = {402.0,488.5,597.5};

  Int_t thisEntry; 
  Int_t numberOfEntries; 
  Int_t m_maxSegT0;

  bool unique; 
  


};

#endif
