import sys, os
import time
import ROOT as r
from ROOT import gSystem
from copy import deepcopy
import CMS_lumi
#import myPlotter_input as effplot
r.gROOT.SetBatch(True)
from subprocess import call
import myPlotter_input as effplot
from markerColors import markerColors
from allLegends import legends
import itertools

import argparse
parser = argparse.ArgumentParser(description='Plotter options')
parser.add_argument('-n','--ntuples', action='store_true', default = False)
parser.add_argument('-r','--redoPlots', action='store_true', default = False)
my_namespace = parser.parse_args()

################################# CHANGE BEFORE RUNNING #######################################

categories = ['norpc', 'rpc']
files = {'norpc':[], 'rpc':[], 'DM':[]}
#files['norpc'].append('3h4h')
#files['norpc'].append('nopu_noage_norpc')
#files['norpc'].append('mu_pu200')
#files['norpc'].append('DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel_woRPC')
#files['norpc'].append('mu_PU200_noRPC_noAgeing_111X_1_0')
#files['norpc'].append('mu_PU200_noRPC_noAgeing_20210223')
#files['norpc'].append('mu_PU200_noRPC_noAgeing_20210308')
#files['norpc'].append('mu_PU200_noRPC_noAgeing_20210315')
#files['norpc'].append('mu_PU200_noRPC_noAgeing_20210315_cmssw')
#files['norpc'].append('mu_pu200_newest_analyzer')
#files['norpc'].append('mu_PU200_withRPC_noAgeing')
#files['norpc'].append('DTDPGNtuple_11_1_0_patch2_Phase2_Simulation_8muInBarrel')
#files['norpc'].append('mu_PU200_noRPC_noAgeing_3h4h')
#files['norpc'].append('mu_PU200_noRPC_noAgeing_grouping2')
#files['norpc'].append('rossin_noRPC_noAgeing_cmssw')
#files['norpc'].append('rossin_noRPC_withAgeing')
#files['norpc'].append('rossin_noRPC_noAgeing_11_2_1')
#files['norpc'].append('rossin_noRPC_noAgeing_newestlut')
#files['norpc'].append('rossin_noRPC_noAgeing_cmssw')
#files['norpc'].append('rossin_noRPC_noAgeing_alignTrue')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_alignTrue')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_confok_alignTrue')
#files['norpc'].append('rossin_noRPC_withAgeing_ext_confok_alignTrue')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v7_simple')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v9_simple')
#files['norpc'].append('rossin_noRPC_withAgeing_ext_newSLFitter_full_12_4_2_v9_simple_nocor')
#files['norpc'].append('rossin_noRPC_withAgeing_ext_newSLFitter_full_12_4_2_v9_simple')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v6_noprop')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v6_wp_1500ev')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v6_noprop_487_tdc')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v6_noprop_487')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_newSLFitter_full_12_3_0_v6_noprop')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_newSLFitter_full_12_4_2_v5')
#files['norpc'].append('rossin_noRPC_withAgeing_ext_confok_nocor_alignTrue')
#files['norpc'].append('rossin_noRPC_noAgeing_ext_confok_noprop')
#files['norpc'].append('rossin_noRPC_noAgeing_noCor_ext_alignTrue')
#files['norpc'].append('rossin_noRPC_withAgeing_alignTrue')
#files['norpc'].append('rossin_withRPC_noAgeing_alignTrue')
#files['norpc'].append('rossin_withRPC_withAgeing_alignTrue')
#files['norpc'].append('rossin_noRPC_noAgeing_alignFalse')
#files['norpc'].append('rossinQcut8_PU200')
#files['norpc'].append('rossinQcut5_PU200')
#files['norpc'].append('rossinQcut3_PU200')
files['norpc'].append('rossinQcut2_PU200')
#files['norpc'].append('rossinQcut1_PU200')
files['norpc'].append('rossinQcut0_PU200')
#files['norpc'].append('rossinQcut0_PU200_noCoincidence')
#files['norpc'].append('DYLL_M50_PU200_qcut8')
#files['norpc'].append('DYLL_M50_PU200_qcut5')
#files['norpc'].append('DYLL_M50_PU200_qcut2')
#files['norpc'].append('DYLL_M50_PU200_qcut1')
#files['norpc'].append('DYLL_M50_PU200_qcut0')
#files['norpc'].append('DTDPGNtuple_11_1_0_patch2_Phase2_Simulation')

#qualities = ['']
qualities = {'norpc':[],'rpc':[], 'DM':[]}
qualities['norpc'].append('All')
qualities['norpc'].append('Correlated')
qualities['norpc'].append('Uncorrelated')
#qualities['norpc'].append('Legacy')
#qualities['norpc'].append('4h')
#qualities['norpc'].append('3h')

#qualities['norpc'].append('Q1')
#qualities['norpc'].append('Q2')
#qualities['norpc'].append('Q3')
#qualities['norpc'].append('Q4')


##############################################################################################

# print "ATTENTION! You are using position from CMSSW"

if my_namespace.ntuples == True:
    print ("Starting ntuplizer for every sample in input")
    time.sleep(2)
    r.gInterpreter.ProcessLine(".x loadTPGSimAnalysis_Res_All.C")
    gSystem.Load(os.getcwd() + "/DTNtupleBaseAnalyzer_C.so")
    gSystem.Load(os.getcwd() + "/DTNtupleTPGSimAnalyzer_Resolution_All_C.so")
    from ROOT import DTNtupleTPGSimAnalyzer
else :
  print("Not making ntuples. If you want to make them, restart with 'yes' as first argument ")
  time.sleep(2)

path = '/eos/home-j/jfernan/L1T/'
plotsPath = "./summaryPlots/"
#outputPath = './ntuples/'
outputPath = '/eos/home-j/jfernan/L1T/ntuplesResults/'
eosPath='/eos/home-j/jfernan/L1T/resolutionsNote/'


chambTag = ["MB1", "MB2", "MB3", "MB4"]
wheelTag    = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
magnitude = ["Time", "TimeRes", "PhiRes", "PhiBRes", "TanPsiRes", "xRes"]

plottingStuff = { 'lowlimityaxis': 0,
		      'highlimityaxis': {},
		      'markersize': 1,
              'yaxistitle' : {
                  "Time": "Primitive time resolution (TDC c.)",
                  "TimeRes": "Primitive - segment time resolution (ns)",
                  "PhiRes": "Primitive - segment global Phi resolution (#murad)",
                  "PhiBRes": "#sigma of Primitive - Segment #phi_{B} (mrad)",
                  "TanPsiRes": "Primitive - segment local direction resolution (mrad)",
                  "xRes":"Primitive - segment position resolution (#mum)"
                },
		      'yaxistitleoffset': 1.5,
		      'xaxistitle': "Wheel",
		      #'legxlow' : 0.7,
              'legxlow' : 0.3075 + 1 * 0.1975,
              #'legxlow' : 0.3075 + 2 * 0.1975,
		      'legylow': 0.65,
		      'legxhigh': 0.9,
		      'legyhigh': 0.75,
		      'markertypedir':{},
		      'markercolordir':{},
              'ageingTag': "",
   		    }

plottingStuff['highlimityaxis']["Time"] = {'Q1': 10, 'Q2': 10, '3h': 10, '4h': 10, 'Q3': 10, 'Q4': 10, 'All':5, 'Correlated':10, 'Uncorrelated':10, 'Legacy':5}
plottingStuff['highlimityaxis']["TimeRes"] = {'Q1': 10, 'Q2': 10, '3h': 10, '4h': 10, 'Q3': 10, 'Q4': 10, 'All':5, 'Correlated':5, 'Uncorrelated':10, 'Legacy':5}
plottingStuff['highlimityaxis']["PhiRes"] = {'Q1': 50, 'Q2': 50, '3h': 50, '4h': 50, 'Q3': 50, 'Q4': 50, 'All':50,'Correlated':50, 'Uncorrelated':50, 'Legacy':50}
plottingStuff['highlimityaxis']["PhiBRes"] = {'Q1': 15, 'Q2': 15, '3h': 15, '4h': 10, 'Q3': 10, 'Q4': 10, 'All':1, 'Correlated':5, 'Uncorrelated':20, 'Legacy':5}
plottingStuff['highlimityaxis']["TanPsiRes"] = {'Q1': 15, 'Q2': 15, '3h': 15, '4h': 10, 'Q3': 10, 'Q4': 10, 'All':5, 'Correlated':5, 'Uncorrelated':20, 'Legacy':5}
plottingStuff['highlimityaxis']["xRes"] = {'Q1': 200, 'Q2': 200, '3h': 200, '4h': 200, 'Q3': 200, 'Q4': 200, 'All': 200, 'Correlated': 200, 'Uncorrelated':200, 'Legacy':200}

markerColors = [r.kBlue, r.kRed, r.kGreen, r.kOrange, r.kBlack, r.kMagenta]



for cat in files :
  for fil in files[cat] :
    if my_namespace.ntuples == True:
      print ('Obtaining resolution ntuples for ' + fil )
      time.sleep(2)
      analysis = DTNtupleTPGSimAnalyzer(path + fil + '.root', outputPath + 'results_resols_' +fil + '_.root')
      analysis.Loop()

    ageingTag = ("" if "withAgeing" not in fil else "3000 fb^{-1}")
    ageingLegend = ("No ageing" if "withAgeing" not in fil else "3000 fb^{-1} ageing")

    if my_namespace.ntuples == True or my_namespace.redoPlots == True:
      rc = call ('./runPlots.sh ' + fil + " " + ageingLegend, shell=True)


    for mag in magnitude :
      for qual in qualities[cat] :
        listofplots = []
        plotscaffold = "h" + mag + "_{al}_" + qual + "_{wh}"
        savescaffold = "h" + mag + "_{al}_" + qual

        plottingStuff['markertypedir']["h_" + "AM" + "_" + fil+qual] = 20
        plottingStuff['markercolordir']["h_" + "AM" + "_" + fil+qual] = markerColors[0]
        effplot.makeResolPlot(listofplots, "AM", fil+qual, plotsPath + fil + '/' +  'outPlots.root', plotscaffold)
        #if "withAgeing" in fil:
        #    plottingStuff['ageingTag'] = "3000 fb^{-1}"
        #else:
        #    plottingStuff['ageingTag'] = ""
        print "\nCombining and saving\n"
        effplot.combineResolPlots(listofplots, mag, qual, [], plottingStuff, plotsPath + fil + '/' + qual  + '/', savescaffold.format(al='AM') )

   # rc = call('cp -r ' + plotsPath + fil + ' ' + eosPath , shell=True)
   # rc = call('cp -r /eos/home-j/jfernan/backup/index_resol_php ' + eosPath + fil + "/index.php" , shell=True)
   # for qual in qualities[cat] : rc = call('cp -r /eos/home-j/jfernan/backup/index_resol_php ' + eosPath + fil + "/" + qual + "/index.php" , shell=True)

for cat in files :
  if not files[cat] or not qualities[cat] : continue
  for mag in magnitude :
    for fil in files[cat] :
      listofplots = []
      num = 0
      for qual in qualities[cat] :
        plotscaffold = "h" + mag + "_{al}_" + qual + "_{wh}"
        savescaffold = "h" + mag + "_{al}"

        plottingStuff['markertypedir']["h_" + "AM" + "_" + fil+qual] = 20
        plottingStuff['markercolordir']["h_" + "AM" + "_" + fil+qual] = markerColors[num]
        num+=1
        effplot.makeResolPlot(listofplots, "AM", fil+qual, plotsPath + fil + '/' +  'outPlots.root', plotscaffold)

      print "\nCombining and saving\n"
      if not os.path.isdir(plotsPath + fil + '/mixed/') : os.mkdir(plotsPath + fil + '/mixed/')
      effplot.combineResolPlots(listofplots, mag, qual, qualities[cat], plottingStuff, plotsPath + fil + '/mixed/', savescaffold.format(al='AM') )


for cat in files:
    if not files[cat]: continue
    dirname = "{}/{}/".format(plotsPath, cat)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    for mag in magnitude:
        for qual in qualities[cat] :
            listofplots = []
            mylegends = []
            num = 0
            plottingStuff['ageingTag'] = ""
            for fil in files[cat]:
                plotscaffold = "h" + mag + "_{al}_" + qual + "_{wh}"
                savescaffold = "h" + mag + "_{al}_" + qual

                plottingStuff['markertypedir']["h_" + "AM" + "_" + fil+qual] = 20
                plottingStuff['markercolordir']["h_" + "AM" + "_" + fil+qual] = markerColors[num]
                #if "withAgeing" in fil:
                    #plottingStuff['ageingTag'] = "3000 fb^{-1}"
                num+=1
                effplot.makeResolPlot(listofplots, "AM", fil+qual, plotsPath + fil + '/' +  'outPlots.root', plotscaffold)
                print legends[fil]
                mylegends.append(legends[fil])
            print listofplots
            print [plot.Integral() for plot in listofplots]
            print "\nCombining and saving\n"
            effplot.combineResolPlots(listofplots, mag, qual, mylegends, plottingStuff, dirname, savescaffold.format(al='AM') )


# Uncorrelated - correlated task
#files_to_use = ["rossin_noRPC_withAgeing_ext_confok_alignTrue", "rossin_noRPC_withAgeing_ext_confok_nocor_alignTrue"]
#files_to_use = ["rossin_noRPC_withAgeing_ext_newSLFitter_full_12_4_2_v9_simple", "rossin_noRPC_withAgeing_ext_newSLFitter_full_12_4_2_v9_simple_nocor"]
#files_to_use = ["DYLL_M50_PU200_qcut2","DYLL_M50_PU200_qcut0"]
files_to_use = ["rossinQcut2_PU200","rossinQcut0_PU200"]
qualities_to_use = ["Correlated", "Uncorrelated"]

for mag in magnitude:
    listofplots = []
    num = 0
    for fil, qual in zip(files_to_use, qualities_to_use):
        plotscaffold = "h" + mag + "_{al}_" + qual + "_{wh}"
        savescaffold = "h" + mag + "_{al}"

        plottingStuff['markertypedir']["h_" + "AM" + "_" + fil+qual] = 20 + num
        plottingStuff['markercolordir']["h_" + "AM" + "_" + fil+qual] = markerColors[num]
        num+=1
        effplot.makeResolPlot(listofplots, "AM", fil+qual, plotsPath + fil + '/' +  'outPlots.root', plotscaffold)

    print "\nCombining and saving\n"
    if not os.path.isdir(plotsPath + '/coruncor/'):
        os.mkdir(plotsPath + '/coruncor/')
    effplot.combineResolPlots(listofplots, mag, qual, qualities_to_use, plottingStuff, plotsPath + '/coruncor/', savescaffold.format(al='AM') )


files_to_use = ["rossinQcut2_PU200"]
qualities_to_use = ["3h", "4h"]
legends = ["Q1 + Q2", "Q3 + Q4"]

plottingStuff['highlimityaxis']["Time"] = {'Q1': 10, 'Q2': 10, '3h': 10, '4h': 10, 'Q3': 10, 'Q4': 10, 'All':5, 'Correlated':5, 'Uncorrelated':10, 'Legacy':5}
plottingStuff['highlimityaxis']["TimeRes"] = {'Q1': 10, 'Q2': 10, '3h': 10, '4h': 10, 'Q3': 10, 'Q4': 10, 'All':5, 'Correlated':5, 'Uncorrelated':10, 'Legacy':5}
plottingStuff['highlimityaxis']["PhiRes"] = {'Q1': 50, 'Q2': 50, '3h': 50, '4h': 50, 'Q3': 50, 'Q4': 50, 'All':50,'Correlated':50, 'Uncorrelated':50, 'Legacy':50}
plottingStuff['highlimityaxis']["PhiBRes"] = {'Q1': 15, 'Q2': 15, '3h': 15, '4h': 10, 'Q3': 10, 'Q4': 10, 'All':1, 'Correlated':5, 'Uncorrelated':20, 'Legacy':5}
plottingStuff['highlimityaxis']["TanPsiRes"] = {'Q1': 15, 'Q2': 15, '3h': 100, '4h': 100, 'Q3': 10, 'Q4': 10, 'All':5, 'Correlated':5, 'Uncorrelated':20, 'Legacy':5}
plottingStuff['highlimityaxis']["xRes"] = {'Q1': 200, 'Q2': 200, '3h': 200, '4h': 200, 'Q3': 200, 'Q4': 200, 'All': 200, 'Correlated': 200, 'Uncorrelated':200, 'Legacy':200}

for mag in magnitude:
    listofplots = []
    num = 0
    for fil, qual in itertools.product(files_to_use, qualities_to_use):
        plotscaffold = "h" + mag + "_{al}_" + qual + "_{wh}"
        savescaffold = "h" + mag + "_{al}"

        plottingStuff['markertypedir']["h_" + "AM" + "_" + fil+qual] = 20 + num
        plottingStuff['markercolordir']["h_" + "AM" + "_" + fil+qual] = markerColors[num]
        num+=1
        effplot.makeResolPlot(listofplots, "AM", fil + qual, plotsPath + fil + '/' +  'outPlots.root', plotscaffold)

    print "\nCombining and saving\n"
    if not os.path.isdir(plotsPath + '/uncor_comparison/'):
        os.mkdir(plotsPath + '/uncor_comparison/')
    effplot.combineResolPlots(listofplots, mag, qual, legends, plottingStuff, plotsPath + '/uncor_comparison/', savescaffold.format(al='AM') )

###############################################################################################
#######################################     END     ###########################################
###############################################################################################
