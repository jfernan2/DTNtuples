legends = {
      #'All'                                                          : '',
  'All'                                                          : 'Every quality',
  'correlated'                                                   : 'Correlated Only',
  'confirmed'                                                    : 'Correlated + Confirmed',
  'Q8'                                                           : 'Q8 only',
  'legacy'                                                       : 'Quality > 2',
  'index0'                                                       : 'Only Index 0',
  'index01'                                                      : 'Only Index 01',
  'index012'                                                     : 'Only Index 012',
  'index0123'                                                    : 'Only Index 0123',
  'nothreehits'                                                  : 'Quality > 1',
  'withmatchedthreehits'                                         : 'Quality > 2 + RPC-matched Quality<=2',
  'qualityORSegs'                                                : 'Every DT quality + RPC segments',
  'qualityORSegsClus'                                            : 'Every DT quality + RPC segments and clusters',
  'qualityMatchedORSegs'                                         : 'Quality > 2 + RPC-matched Quality<=2 + RPC segments',
  'qualityMatchedORSegsClus'                                     : 'Quality > 2 + RPC-matched Quality<=2 + RPC segments and clusters',
  'AM'                                                           : 'AM',
  'HB'                                                           : 'HB',
  'nu_pu250_noage_norpc'                                         : 'Nu gun PU250 + no bkg',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_debug'                        : 'Old emulator',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_debugGoodBX'                  : 'AllQ, Old emulator',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_debugGoodBX+qu>=3'            : 'Q>=3, Old emulator',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_newestAnalyzer'               : 'Nu gun PU250 + bkg (New fit)',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_newestAnalyzerGoodBX'         : 'Nu gun PU250 + bkg AllQ (New fit)',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_newestAnalyzerGoodBX+qu>=3'   : 'Nu gun PU250 + bkg Q>=3 (New fit)',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_20210223'                     : 'New emulator',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_20210303'                     : 'New emulator',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_20210223GoodBX'               : 'AllQ, New emulator',  
  'nu_PU250_noRPC_noAgeing_bkg9E34_20210223GoodBX+qu>=3'         : 'Q>=3, New emulator',  
  'nu_pu250_noage_norpcGoodBX'                                   : 'No random AllQ',  
  'nu_pu250_noage_norpcGoodBX+qu>=3'                             : 'No random Q>=3',  
  'nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000'             : 'w/Aging No RPC',
  'nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000GoodBX'       : 'No random w/Aging AllQ',
  'nu_pu250_age_norpc_youngseg_muonage_norpcage_fail_3000GoodBX+qu>=3' : 'No random w/Aging Q>=3',
  'nu_pu250_noage_withrpc'                                       : 'No Aging w/RPC',  
  'nu_pu250_age_withrpc_youngseg_muonage_norpcage_fail_3000'     : 'w/Aging w/RPC',  
  'PU0_bkgHits'                                                  : 'PU0 + bkg',  
  'PU200_bkgHits'                                                : 'PU200 + bkg',  
  'PU200_nu_bkg7p5'                                              : 'Nu gun PU200 + bkg7.5',  
  'PU250_nu_bkg9'                                                : 'Nu gun PU250 + bkg9',  
  'PU250_nu_bkg9GoodBX'                                          : 'Random 9E34 AllQ',  
  'PU250_nu_bkg9GoodBX+qu>=3'                                    : 'Random 9E34 Q>=3',  
  'nopu_noage_norpc'                                             : 'PU0 NoAging',  
  'pu200_noage_norpc'                                            : 'PU200 No Aging',
  'pu200_noage_withrpc'                                          : 'PU200 w/RPC',
  'mu_PU200_noRPC_noAgeing_111X_1_0'                             : 'PU 200 Old Emulator',
  'mu_PU200_noRPC_noAgeing_111Xdev'                              : 'PU 200 11XDev', 
  'mu_PU200_noRPC_noAgeing_newAnalyzer'                          : 'PU 200 new analyzer',
  'mu_PU200_noRPC_noAgeing_20210223'                             : 'PU 200 New Emulator', 
  'mu_PU200_noRPC_noAgeing_20210303'                             : 'PU 200 New Emulator', 
  'mu_PU200_noRPC_noAgeing_20210308'                             : 'New Emul. (CMSSW)', 
  'mu_PU200_noRPC_noAgeing_20210315'                             : 'New Emul. (LUT)', 
  'mu_PU200_noRPC_noAgeing_20210315_cmssw'                       : 'New Emul. (CMSSW Flag)',
  'mu_PU200_noRPC_noAgeing_newAnalyzer260521'                    : 'PU 200 no aging, no RPC',
  'mu_PU200_noRPC_noAgeing_ext_dataformat'                       : 'PU 200 no aging, no RPC, ext. df.',
  'mu_PU200_noRPC_withAgeing_ext'                                : 'PU 200 with aging, no RPC, ext. df.',
  'mu_PU200_withRPC_noAgeing_newAnalyzer260521'                  : 'PU 200 no aging, with RPC',
  'mu_PU200_noRPC_withAgeing_newAnalyzer260521'                  : 'PU 200 with aging, no RPC',
  'mu_PU200_withRPC_withAgeing_newAnalyzer260521'                : 'PU 200 with aging, with RPC',
  'DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel'      : 'PU 200 + real bkg w/RPC',
  'DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrelGoodBX': 'PU 200 + real bkg w/RPC AllQ',
  'DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrelGoodBX+qu>=3': 'PU 200 + real bkg w/RPC Q>=3',
  'DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPC'      : 'PU 200 + real bkg',
  'DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPCGoodBX': 'PU 200 + real bkg AllQ',
  'DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPCGoodBX+qu>=3': 'PU 200 + real bkg Q>=3',
  'rossin_noRPC_noAgeing'                                        : 'Rossin No RPC, No Ageing',
  'rossin_noRPC_noAgeing_cmssw'                                  : 'Rossin No RPC, No Ageing',
  'rossin_noRPC_noAgeing_newestlut'                              : 'Rossin No RPC, No Ageing',
  'rossin_noRPC_noAgeing_11_2_1'                              : 'Rossin No RPC, No Ageing',
  'rossin_noRPC_noAgeing_alignTrue'                              : 'DT AM w/o ageing',
  'rossin_withRPC_noAgeing_alignTrue'                            : 'DT+RPC AM w/o ageing',
  'rossin_noRPC_noAgeing_alignFalse'                             : 'Rossin No RPC, No Ageing',
  'rossin_noRPC_withAgeing'                                      : 'Rossin No RPC, 3000fb^{-1} Ageing',
  'rossin_noRPC_withAgeing_alignTrue'                            : 'DT AM w/ 3000 fb^{-1} ageing',
  'rossin_withRPC_withAgeing_alignTrue'                          : 'DT+RPC AM w/ ageing',
  'rossin_noRPC_noAgeing_noCor_alignTrue'                        : 'DT AM w/o correlation',
  'rossin_noRPC_noAgeing_noCor_ext_alignTrue'                    : 'DT AM w/o correlation',
  'rossin_noRPC_noAgeing_ext_alignTrue'                          : 'DT AM No Ageing',
  'rossin_noRPC_noAgeing_ext_confok_alignTrue'                   : 'DT AM w/o ageing',
  'rossin_noRPC_withAgeing_ext_confok_alignTrue'                 : 'DT AM w/ 3000 fb^{-1} ageing',
  'rossin_noRPC_noAgeing_ext_confok_nocor_alignTrue'             : 'DT AM w/o correlation',
  'rossin_noRPC_withAgeing_ext_confok_nocor_alignTrue'           : 'DT AM w/o correlation',
  'rossin_noRPC_noAgeing_ext_confok_noprop'                      : 'DT AM w/o ageing',
  'rossin_noRPC_noAgeing_ext_newSLFitter'                        : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_noTol'                  : 'DT AM w/o ageing (New fitter, 0 Tol)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full'                   : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_raw_v8'            : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2'            : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v5'         : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v6_noprop'  : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_3_0_v6_noprop'  : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v6_noprop_487'  : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v6_noprop_487_tdc'  : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v6_wp_1500ev'  : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v7'         : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v7_simple'         : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_withAgeing_ext_newSLFitter_full_12_4_2_v9_simple'         : 'DT AM w/ ageing (New fitter)',
  'rossin_noRPC_withAgeing_ext_newSLFitter_full_12_4_2_v9_simple_nocor'         : 'DT AM w/ ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v9_simple'         : 'DT AM w/o ageing (New fitter)',
  'rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v9_simple_nocor'         : 'DT AM w/o ageing (New fitter)',
  'rossinQcut8_PU200' : 'Matching for any q',
  'rossinQcut5_PU200' : 'Matching for q<6',
  'rossinQcut3_PU200' : 'Matching for q<4',
  'rossinQcut2_PU200' : 'Matching for q<3',
  'rossinQcut2_PU200_exceptionAll' : 'Matching for q<3 exception All',
  'rossinQcut2_PU200_exception' : 'Matching for q<3 exception in Wh2MB1/2',
  'rossinQcut2_PU200_exception_t0phi' : 'Matching for q<3 exception in Wh2MB1/2 t0phi',
  'rossinQcut2_PU200_prime' : 'Matching for q<3 new',
  'rossinQcut1_PU200' : 'Matching for q<2',
  'rossinQcut0_PU200' : 'No matching',
  'rossinQcut8_PU200GoodBX' : 'Matching for any q',
  'rossinQcut5_PU200GoodBX' : 'Matching for q<6',
  'rossinQcut3_PU200GoodBX' : 'Matching for q<4',
  'rossinQcut2_PU200GoodBX' : 'Matching for q<3',
  'rossinQcut1_PU200GoodBX' : 'Matching for q<2',
  'rossinQcut0_PU200GoodBX' : 'No matching',
  'rossinQcut0_PU200_noCoincidence' : 'Without filter in Theta matching and coincidence',
  'DTDPGNtuple_mu_PU140_qcut2_noRPC_noAgeing' : 'Matching for q<3',
  'DTDPGNtuple_mu_PU140_qcut0_noRPC_noAgeing' : 'Matching',
  'mb_PU200_qcut8_1_noRPC_noAgeing_12_3_X' : 'Matching for any q',
  'mb_PU200_qcut2_1_noRPC_noAgeing_12_3_X' : 'Matching for q<3',
  'mb_PU200_qcut0_1_noRPC_noAgeing_12_3_X' : 'No matching',
  'mb_PU200_qcut0_1_noRPC_noAgeing_12_3_XGoodBX' : 'No matching',
  'mb_PU200_qcut2_1_noRPC_noAgeing_12_3_XGoodBX' : 'Matching for q<3',
  'mb_PU200_qcut8_1_noRPC_noAgeing_12_3_XGoodBX' : 'Matching for any q',
  'jpsimumu_qcut8' : 'Matching for any q',
  'jpsimumu_qcut2' : 'Matching for q<3',
  'jpsimumu_qcut0' : 'No matching',
  'DYLL_M50_PU200_qcut8' : 'Matching for any q',
  'DYLL_M50_PU200_qcut5' : 'Matching for q<6',
  'DYLL_M50_PU200_qcut2' : 'Matching for q<3',
  'DYLL_M50_PU200_qcut2_prime' : 'Matching for q<3',
  'DYLL_M50_PU200_qcut2_exception' : 'Matching for q<3 exception in Wh2MB1/2',
  'DYLL_M50_PU200_qcut2_exceptionAll' : 'Matching for q<3 exception All',
  'DYLL_M50_PU200_qcut2_exceptionAll_t0phi' : 'Matching for q<3 exception All t0phi',
  'DYLL_M50_PU200_qcut2_exception_t0phi' : 'Matching for q<3 exception in Wh2MB1/2 t0phi',
  'DYLL_M50_PU200_qcut0' : 'No matching',
  'DTDPGNtuple_11_1_0_patch2_Phase2_Simulation' : 'test',
}
