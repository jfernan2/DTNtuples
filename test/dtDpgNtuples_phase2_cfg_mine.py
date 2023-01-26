import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.StandardSequences.Eras import eras

import subprocess
import sys

#process = cms.Process("DTNTUPLES",eras.Phase2C8_timing_layer_bar)
process = cms.Process("DTNTUPLES",eras.Phase2C9)

options = VarParsing.VarParsing()

options.register('globalTag',
                 '110X_mcRun4_realistic_v3', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Global Tag")

options.register('nEvents',
                 -1, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Maximum number of processed events")

options.register('inputFolder',
                 # '/eos/cms/store/group/dpg_dt/comm_dt/L1T_TDR/', #default value
                 '/eos/cms/store/group/dpg_muon/rossin/Phase2/ParticleGun_thermalNeutrons_33BX_200_PU/step2/',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "EOS folder with input files")

options.register('secondaryInputFolder',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "EOS folder with input files for secondary files")

options.register('useRPC',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True uses RPC information")

options.register('applySegmentAgeing',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True applies ageing to RECO segments")

options.register('applyTriggerAgeing',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True applies ageing to trigger emulators")

options.register('applyRpcAgeing',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True applies ageing to RPCs")

options.register('ageingInput',
                 '', #default value
                 #'MuonAgeingAndFailures_3000fbm1_DT_L1TTDR_v1_mc.db', #default value
                 #'sqlite_file:MuonAgeingAndFailures_3000fbm1_DT_L1TTDR_v1_mc.db', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Input with customised ageing, used only if non ''")

options.register('ageingTag',
                 '', #default value
                 #'MuonAgeingAndFailures_3000fbm1_DT_L1T', #default value
                 #'MuonSystemAging', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Tag for customised ageing")

options.register('applyRandomBkg',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True applies random background to phase-2 digis and emulator")

options.register('ntupleName',
                 './DTDPGNtuple_10_6_0_Phase2_Simulation.root', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Folder and name ame for output ntuple")

options.parseArguments()


process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.nEvents))

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

#process.GlobalTag.globaltag = cms.string(options.globalTag)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')



if options.ageingInput != "" :
    process.GlobalTag.toGet = cms.VPSet()
    process.GlobalTag.toGet.append(cms.PSet(record  = cms.string("MuonSystemAgingRcd"),
                                            connect = cms.string(options.ageingInput),
                                            tag     = cms.string(options.ageingTag)
                                        )
                               )

process.source = cms.Source("PoolSource",
                            
        fileNames = cms.untracked.vstring(),
        secondaryFileNames = cms.untracked.vstring(),
        skipEvents=cms.untracked.uint32(0)
)

files = subprocess.check_output(["ls", options.inputFolder])
process.source.fileNames = ["file://%s/%s" % (options.inputFolder, f.decode("utf-8")) for f in files.split()]

#print("FIXME")
#process.source.fileNames = ["/store/user/escalant/HTo2LongLivedTo4mu_MH-200_MFF-50_CTau-20mm_TuneCP5_13TeV_pythia8/MC2018_Benchmark_2mu2jets_June2019-GSR-testForL1-v2/190607_155534/0000/EXO-RunIIAutumn18DRPremix_GSR_HTo2LongLivedTo2mu2jets_MH-200_MFF-50_CTau-200mm_TuneCP5_13TeV_pythia8_1.root"]


if options.secondaryInputFolder != "" :
    files = subprocess.check_output(["ls", options.secondaryInputFolder])
    process.source.secondaryFileNames = ["file://%s/%s" % (options.secondaryInputFolder, f.decode("utf-8")) for f in files.split()]

process.TFileService = cms.Service('TFileService',
        fileName = cms.string(options.ntupleName)
    )

process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
#process.load('Configuration.Geometry.GeometryExtended2023D41Reco_cff')
#process.load('Configuration.Geometry.GeometryExtended2023D41_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")

# process.DTGeometryESModule.applyAlignment = False
# process.DTGeometryESModule.fromDDD = False

process.load("L1Trigger.DTTriggerPhase2.CalibratedDigis_cfi") 
process.load("L1Trigger.DTTriggerPhase2.dtTriggerPhase2PrimitiveDigis_cfi")

# process.CalibratedDigis.dtDigiTag = "muonDTDigis"
process.CalibratedDigis.dtDigiTag = "simMuonDTDigis"
process.CalibratedDigis.scenario = 0
process.dtTriggerPhase2PrimitiveDigis.scenario = 0
process.dtTriggerPhase2AmPrimitiveDigis = process.dtTriggerPhase2PrimitiveDigis.clone()
process.dtTriggerPhase2AmPrimitiveDigis.useRPC = options.useRPC
process.dtTriggerPhase2AmPrimitiveDigis.max_quality_to_overwrite_t0 = 9
process.dtTriggerPhase2AmPrimitiveDigis.df_extended = 2
#process.dtTriggerPhase2AmPrimitiveDigis.allow_confirmation = False 
#process.dtTriggerPhase2AmPrimitiveDigis.tanPhiTh = 1.5
#process.dtTriggerPhase2AmPrimitiveDigis.chi2Th = 0.1 / 4 
#process.dtTriggerPhase2AmPrimitiveDigis.output_confirmed = False
#process.dtTriggerPhase2AmPrimitiveDigis.cmssw_for_global = True


process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('RecoLocalMuon.Configuration.RecoLocalMuon_cff')
process.dt1DRecHits.dtDigiLabel = "simMuonDTDigis"
process.rpcRecHits.rpcDigiLabel = "simMuonRPCDigis"

#process.dt1DRecHits.dtDigiLabel = "muonDTDigis"
#process.rpcRecHits.rpcDigiLabel = "muonRPCDigis"

process.load('DTDPGAnalysis.DTNtuples.dtNtupleProducer_phase2_cfi')

process.dtNtupleProducer.useExtDataformat = cms.untracked.bool(True)
process.dtNtupleProducer.shift_coordinates = cms.untracked.bool(True)

# process.dtTriggerPhase2AmPrimitiveDigis.useBX_correlation = False
# process.dtTriggerPhase2AmPrimitiveDigis.dT0_correlate_TP = -1
# process.dtTriggerPhase2AmPrimitiveDigis.allow_confirmation = True
# process.dtTriggerPhase2AmPrimitiveDigis.max_primitives = 2

process.p = cms.Path(process.rpcRecHits
                     + process.dt1DRecHits
                     + process.dt1DRecHits
                     + process.dt4DSegments
                     + process.CalibratedDigis
                     + process.dtTriggerPhase2AmPrimitiveDigis
                     + process.dtNtupleProducer)

from DTDPGAnalysis.DTNtuples.customiseDtNtuples_cff import customiseForRandomBkg, customiseForRunningOnMC, customiseForFakePhase2Info, customiseForAgeing

customiseForRunningOnMC(process,"p")
customiseForFakePhase2Info(process)

if options.applyRandomBkg : 
    customiseForRandomBkg(process,"p")

customiseForAgeing(process,"p",options.applySegmentAgeing,options.applyTriggerAgeing,options.applyRpcAgeing)

 
