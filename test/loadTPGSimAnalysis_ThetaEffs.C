#include "TROOT.h"

void loadTPGSimAnalysis_ThetaEffs()
{
  gROOT->ProcessLine(".L DTNtupleBaseAnalyzer.C++");
  gROOT->ProcessLine(".L DTNtupleTPGSimAnalyzer_ThetaEfficiency.C++");
}
