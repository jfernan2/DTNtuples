# DTNtuples
Ntuples for the analysis of the CMS drift tubes detector performance

## Preliminary instructions
**Note**: 
In the present days this code is evolving fast, hence the installation recipe may change often. Please keep an eye on this page to check for updates.

### Installation:
```bash
cmsrel CMSSW_12_4_2
cd CMSSW_12_4_2/src/
cmsenv

git cms-init
# To be updated
# git cms-merge-topic oglez:Phase2_DTAB7Unpacker_v11.2
git cms-merge-topic jaimeleonh:AM_12_4_2_new_fitter
git clone https://github.com/jaimeleonh/DTNtuples.git DTDPGAnalysis/DTNtuples -b ntupleProduction_12_4_2 

scramv1 b -j 5
```

### Ntuple production:
```
cd DTDPGAnalysis/DTNtuples/test/
cmsRun dtDpgNtuples_phase2_cfg_mine.py nEvents=10000
```

