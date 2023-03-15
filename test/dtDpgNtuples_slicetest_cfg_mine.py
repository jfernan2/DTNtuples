import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.StandardSequences.Eras import eras

import lxml.etree as etree
import subprocess
import sys
import os

XML_FOLDER = "./cmsrun_xml/"
HAS_AUTOCOND = os.path.isfile("./slice_test_autocond.py")

if HAS_AUTOCOND:
    import slice_test_autocond as autocond

def appendToGlobalTag(process, rcd, tag, fileName, label) :

    if  not fileName :
        return process

    if not hasattr(process.GlobalTag,"toGet") :
        process.GlobalTag.toGet = cms.VPSet()

    process.GlobalTag.toGet.append(
        cms.PSet(tag = cms.string(tag),
                 record = cms.string(rcd),
                 connect = cms.string("sqlite_file:" + fileName),
                 label = cms.untracked.string(label)
             )
    )

    return process

options = VarParsing.VarParsing()

options.register('globalTag',
                 '123X_dataRun3_Prompt_v6', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Global Tag")

options.register('nEvents',
                 -1, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Maximum number of processed events")

options.register('runNumber',
                 '347683', #default value
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,
                 "Run number to be looked for in either 'inputFolderCentral' or 'inputFolderDT' folders")

options.register('inputFile',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "The input file to be processed, if non null overrides runNumber based input file selection")

options.register('inputFolderCentral',
                 '/eos/cms/store/data/Commissioning2022/MiniDaq/RAW/v1/', #default value
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                 "Base EOS folder with input files from MiniDAQ/Global runs with central tier0 transfer")

options.register('inputFolderDT',
                 '/eos/cms/store/group/dpg_dt/comm_dt/commissioning_2022_data/root/', #default value
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                 "Base EOS folder with input files from MiniDAQ runs with DT 'private' tier0 transfer")

options.register('tTrigFile',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "File with customised DT legacy tTrigs, used only if non ''")

options.register('t0File',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "File with customised DT legacy t0is, used only if non ''")

options.register('tTrigFilePh2',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "File with customised DT phase-2 tTrigs, used only if non ''")

options.register('t0FilePh2',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "File with customised DT phase-2 t0is, used only if non ''")

options.register('vDriftFile',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "File with customised DT vDrifts, used only if non ''")

options.register('runOnDat',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If set to True switches source from 'PoolSource' to 'NewEventStreamFileReader'")

options.register('runOnTestPulse',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If set to True switches off the filling of all collections but digis")

options.register('ntupleName',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Folder and name ame for output ntuple, if non null overrides 'standard' naming based on runNumber option")

if HAS_AUTOCOND:
    options.register('autocond',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Autocond label: valid ones are {}".format(autocond.labels()))

options.parseArguments()

process = cms.Process("DTNTUPLES",eras.Run3)

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.nEvents))

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.GlobalTag.globaltag = cms.string(options.globalTag)

goodAutocond = HAS_AUTOCOND and options.autocond

tTrigFile = autocond.get_ttrig("phase1",options.autocond) \
            if (goodAutocond and not options.tTrigFile) else options.tTrigFile
tTrigFilePh2 = autocond.get_ttrig("phase2",options.autocond) \
               if (goodAutocond and not options.tTrigFilePh2) else options.tTrigFilePh2
t0File = autocond.get_t0i("phase1") if (goodAutocond and not options.t0File) else options.t0File
t0FilePh2 = autocond.get_t0i("phase2") if (goodAutocond and not options.t0FilePh2) else options.t0FilePh2
    
process = appendToGlobalTag(process, "DTTtrigRcd", "ttrig", tTrigFile, "cosmics")
process = appendToGlobalTag(process, "DTT0Rcd", "t0", t0File, "")

process = appendToGlobalTag(process, "DTTtrigRcd", "ttrig", tTrigFilePh2, "cosmics_ph2")
process = appendToGlobalTag(process, "DTT0Rcd", "t0", t0FilePh2, "ph2")

process = appendToGlobalTag(process, "DTMtimeRcd", "vDrift", options.vDriftFile, "")

process.source = cms.Source("NewEventStreamFileReader" if options.runOnDat else "PoolSource",
                            
        fileNames = cms.untracked.vstring()
)

if options.inputFile :

    print('[dtDpgNtuples_slicetest_cfg.py]: inputFile parameter is non-null running on file:\n\t\t\t{}'.format(options.inputFile))
    # process.source.fileNames = cms.untracked.vstring(options.inputFile)
    process.source.fileNames = cms.untracked.vstring(
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/d3ef6b97-e4de-4aaf-afd0-b6150ac49ee4.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/9c22a028-4795-4264-9da5-1c92c82b72fc.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/cb0af0ca-fc7c-47d2-ba80-e8b937ac18af.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/da18da25-d431-4e5e-af21-b8bcc5cfcc2c.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/3051f177-f23c-4a84-8fb9-d5e8ae8d5d4e.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/7d0629fc-94fa-46a7-99d4-8e3b39207552.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/55ae9714-22fe-4a42-a1f4-d8865d22cb99.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/b5c820ac-c2bf-4039-ae1f-1e49534d3e3a.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/ac14ea0c-1800-4380-9f8e-09c544e53dd2.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/869c7a79-c53d-4a90-be67-ec7797886b9a.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/d83ec456-133c-498b-8041-dc7f2f480c77.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/6b4cf93b-b06d-495b-9919-e7e111dad4c7.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/160b1068-1528-46d2-be42-84e58217b8ec.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/7d525e43-7c4a-43e4-bca4-9e27a94a82ae.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/5c3b09bc-c4d2-489e-9250-ad2e214bceea.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/beb80af1-d2d5-437a-b76e-ccbf55216784.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/f07b4f66-351d-4875-8e05-2cbccd1b0507.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/55f0512d-e200-4a78-af29-0f6bbf6a8401.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/fe67b562-e962-4c9d-a645-423698c635b8.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/0e6d2b15-e5e1-4726-9643-89a450d50ed8.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/853e66fc-be96-4ef7-a6f9-a68ab347c3a6.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/4de9ca94-556b-48a5-90d5-3bff57f848e5.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/0e1bd2f5-6aaf-47da-abe1-00f35d02cfcb.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/ca1f3a40-6819-4ea9-930d-e92166743c78.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/c7ebf26a-341d-4a02-ba2e-4b3eb5ffade8.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/d30d3fdc-ee40-47d2-b3a9-cf6c3c93113a.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/707b05d2-ddbf-420e-9523-f16a40b9b386.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/ef20add4-4e19-411e-bfcb-2c9d219ddca5.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/39a85880-ea87-453b-b51c-669205c58059.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/9b5917a3-fd21-4ea5-ac4b-e98b0ceed765.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/fa107366-6d91-408d-9646-60af9fc43d29.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/0da315fa-129d-4662-98c7-9b25eef3e9a2.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/cb206ddb-93e2-41d8-9073-04578c133c0e.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/c5605fb9-d97a-4436-add7-583907bf2e1b.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/cf15efc3-dfd1-4077-85d3-dc42a9e72804.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/a349775f-832d-43ce-a372-3656e6b63beb.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/0bb45f35-7d29-4ac5-a71e-df4f606f160c.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/c450cf40-78b0-4cc3-baee-4830e0a35670.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/1b391398-1081-4d5e-905d-0a14442e71b8.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/701b1c6a-c84b-4220-a5a0-9765bf03cc14.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/31d8f227-4318-4ed0-a303-6d8ffe266a1e.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/489a88e9-9497-4511-8c4d-abe1975ad254.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/31ae3271-398e-435f-8992-0833eedfa158.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/87f8fb3d-874b-440b-9cd9-2d1f225e45ce.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/b5ad1e67-fee6-455d-8d6b-9c97404a4148.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/76bc53b2-f01f-446c-8f55-d4086488444c.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/721dcaf1-a94e-49d5-a186-e39c77f027d8.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/ececcdfd-b1e3-4f9e-8da3-ced0838952dc.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/163310e5-9e54-4132-be13-79e19a6fa100.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/b293d2c9-a326-40c2-ab6a-59322a640710.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/64b9bbc6-1695-4043-8d73-641d9abc5ca4.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/203d414d-8dfd-4353-839e-2c487f852cbe.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/11c4a03b-78eb-4fa6-aac8-f99477a3f29d.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/b3a3b372-3d8e-4810-aeff-cc83b77b3330.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/36b167b5-c5e0-4ba2-a131-8fa1f9d3c9f8.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/636434f3-dd98-4cd1-942a-a8e0b4ea03b5.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/eb895ad3-6b87-4444-9fbc-846e0cbea6ff.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/e348a321-2b16-45fa-8ad8-8ae28fb11c17.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/ebb73221-9125-4bc8-a99d-529c3f5d77a9.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/b2c93faa-825c-45ef-9707-25ba99bdd242.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/8d750227-ce15-4cef-8e16-5602639ab85d.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/1ba16abe-1404-4da0-9d79-78e2a9d8b0fb.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/63ca21be-757b-4988-aed2-5e408ac2a29c.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/08135afe-5443-4bec-b532-40bbc9f38b06.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/18f072c2-fbd8-4c79-aad2-f763b3a02f8c.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/1efcc080-5e57-4d5f-9d05-4423b147e520.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/c4dc9234-cda4-4e1d-992b-4f96e74a14dc.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/e65517de-9c2f-4e82-af08-430bf39dc5df.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/0092ec38-72a1-4423-99e1-c2fb26b826a0.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/ca7451f9-7bcb-449f-9a04-aea03a569277.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/014d5b9f-7e85-49b5-abde-85e343ecad02.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/f2b481e0-6aa0-467c-838b-004e7d725702.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/a3c2b400-d413-4321-a79b-d584697d2560.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/007600b6-0842-4d7c-b114-0e0ce0f0b384.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/12a070ba-cf2f-4c2d-90fb-72ce7e1f4185.root",
                 # "/store/data/Run2022C/Commissioning/RAW/v1/000/357/080/00000/b4b7e946-b4c4-49c4-b322-637720623100.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/7f598df6-ba6e-4ea4-972e-29e5a23f07ca.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/85f8939f-66bc-4a46-8d25-495c7d8c00ec.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/2185b169-9603-4cb7-8a74-9e9d59336da9.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/ebcdcc34-0836-4066-992d-bb1bf3fa18b2.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/b9e12904-f4fe-4c54-a107-eb90a874f8ac.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/c952294a-b1ed-49c3-898c-d7d0f77cf91f.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/bbeb217f-35e3-41a7-972c-78817c504f0e.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/3dac7345-4177-401e-a92e-38edf318d357.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/86f64502-88bd-487c-8698-dd73600f0688.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/bc8d0d0e-798b-4ecf-b1bf-2ff154b9e833.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/b801b74b-138a-46e5-b631-f07e2534fe56.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/c6407e71-0580-483a-b83d-b594d1bb24af.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/560d67e8-ea62-4adf-ac4c-13ca07840282.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/fe571981-14e8-42ea-b8d8-82125c61124f.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/237e171a-660c-4b54-88a2-b61332de86e4.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/ea9e1532-1701-4163-856d-16c02931722e.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/6063b790-243c-4c69-aa31-4b7ceb050421.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/5397a3b0-47db-497c-a954-3992a7cf9de2.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/a9d371c6-7083-41df-bd9c-1054abefaaa0.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/8e7bb6e3-f649-4cdd-9304-60ab08a881f6.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/cee1acd9-6cac-408d-b763-12d0738f0e3d.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/1ba3b9fe-96ae-4c38-8b7a-060664350327.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/57ecdee7-69f2-4361-aa07-c429cd7ed242.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/ca052687-c443-4391-ab58-567ec797d7ae.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/5a9e5857-4d64-4bfe-b0e9-c9c7466f2a85.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/c5a0e97a-9c9c-46a2-8dc6-ead954cec57c.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/68e4cfbc-c2d9-467b-aee9-d5e0fb634128.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/af5f0dad-5b62-4622-91f6-82d3737ff84d.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/a24694ff-8b2c-4ca6-8108-482569d27e86.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/69f2da23-fd21-46ce-b5a7-8f673d912fd4.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/db7fecb7-7d22-405e-a1ff-cf956976fd1f.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/d7317f21-ec98-4299-bf2b-8d6d90af1735.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/de1d160f-a606-472e-a804-051483343780.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/3d8b0574-9043-42d5-94da-48d16f300294.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/d51d31f3-22c2-44ee-88be-0318310de482.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/45187187-b6f0-4901-b3de-8202842b0b1c.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/4997c1ac-364a-4c77-89f9-2cd6446213ef.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/d17ff21d-aad0-4667-9f3e-2480696a33b1.root",
                 "/store/data/Run2022C/Commissioning/RAW/v1/000/357/081/00000/c899d498-56a3-4160-aadf-a4f947e97aff.root"
    )
    #process.source.fileNames = cms.untracked.vstring("file://" + options.inputFile)

else :

    runStr = str(options.runNumber).zfill(9)
    runFolder = options.inputFolderCentral + "/" + runStr[0:3] + "/" + runStr[3:6] + "/" + runStr[6:] 
    if not options.runOnDat:
        runFolder = runFolder + "/00000"
    
    print('[dtDpgNtuples_slicetest_cfg.py]: looking for files under:\n\t\t\t{}'.format(runFolder))
    
    if os.path.exists(runFolder) :
        files = subprocess.check_output(["ls", runFolder])
        process.source.fileNames = ["file://" + runFolder + "/" + f.decode("utf-8") for f in files.split()]

    else :
        print('[dtDpgNtuples_slicetest_cfg.py]: files not found there, looking under:\n\t\t\t{}'.format(options.inputFolderDT))

        files = subprocess.check_output(["ls", options.inputFolderDT])
        filesFromRun = [f.decode("utf-8") for f in files.split() if f.find(runStr[3:]) > -1]

        if len(filesFromRun) == 1 :
            process.source.fileNames.append("file://" + options.inputFolderDT + "/" + filesFromRun[0])

        else :
            print('[dtDpgNtuples_slicetest_cfg.py]: {} files found, can\'t run!'.format(len(filesFromRun)))
            sys.exit(999)

print(process.source.fileNames)

ntupleName = options.ntupleName if options.ntupleName else "./DTDPGNtuple_run" + str(options.runNumber) + ".root"  

process.TFileService = cms.Service('TFileService',
        fileName = cms.string(ntupleName)
    )

process.load('Configuration/StandardSequences/GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")

process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('EventFilter.DTRawToDigi.dtab7unpacker_cfi')

process.load('DTDPGAnalysis.DTNtuples.dtUpgradeFedL1AProducer_cfi')

process.load('RecoLocalMuon.Configuration.RecoLocalMuonCosmics_cff')

process.load('DTDPGAnalysis.DTNtuples.dtNtupleProducer_slicetest_cfi')

process.dtNtupleProducer.useExtDataformat = cms.untracked.bool(True)
process.dtNtupleProducer.shift_coordinates = cms.untracked.bool(True)
process.dtNtupleProducer.maxdrift_filename = cms.untracked.string('L1Trigger/DTTriggerPhase2/data/simple_vdrift.txt')

process.p = cms.Path(process.muonDTDigis
                     + process.dtAB7unpacker
                     + process.dtUpgradeFedL1AProducer
                     + process.twinMuxStage2Digis
                     + process.bmtfDigis
                     + process.dtlocalrecoT0Seg
                     + process.dtNtupleProducer)

if tTrigFilePh2 and t0FilePh2 :
    from DTDPGAnalysis.DTNtuples.customiseDtPhase2Reco_cff import customiseForPhase2Reco
    process = customiseForPhase2Reco(process,"p", tTrigFilePh2, t0FilePh2)

    from DTDPGAnalysis.DTNtuples.customiseDtPhase2Emulator_cff import customiseForPhase2Emulator
    process = customiseForPhase2Emulator(process,"p")

if options.runOnTestPulse :
    from DTDPGAnalysis.DTNtuples.customiseDtNtuples_cff import customiseForTestPulseRun
    process = customiseForTestPulseRun(process)

xml_base = etree.Element("options") 

for var, val in options._singletons.items():
    if var == "ntupleName":
        etree.SubElement(xml_base, var).text = os.path.abspath(ntupleName)
    elif var == "vDriftFile" and val != "":
        etree.SubElement(xml_base, var).text = os.path.abspath(val)
    elif "File" in var:
        continue
    else:
        etree.SubElement(xml_base, var).text = str(val)
        
if t0File != "":
    etree.SubElement(xml_base, "t0File").text = os.path.abspath(t0File)
if t0FilePh2 != "":
    etree.SubElement(xml_base, "t0FilePh2").text = os.path.abspath(t0FilePh2)
if tTrigFile != "":
    etree.SubElement(xml_base, "tTrigFile").text = os.path.abspath(tTrigFile)
if tTrigFilePh2 != "":
    etree.SubElement(xml_base, "tTrigFilePh2").text = os.path.abspath(tTrigFilePh2)

if not os.path.exists(XML_FOLDER):
    os.makedirs(XML_FOLDER)

xml_string = etree.tostring(xml_base, pretty_print=True)

out_file_name = "ntuple_cfg_run" + str(options.runNumber) + ".xml"
out_file_path = os.path.join(XML_FOLDER, out_file_name)

with open(out_file_path, 'w') as file: file.write(xml_string.decode("utf-8"))
