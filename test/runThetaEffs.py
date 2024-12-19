import sys, os
import time
import ROOT as r
r.gROOT.SetBatch(True)
from copy import deepcopy
import CMS_lumi
import myPlotter_input as effplot
from allLegends import legends
from subprocess import call
from bcolors import bcolors
from markerColors import markerColors


import argparse
parser = argparse.ArgumentParser(description='Plotter options')
parser.add_argument('-n','--ntuples', action='store_true', default = False)
my_namespace = parser.parse_args()
################################# CHANGE BEFORE RUNNING #######################################

categories = ['norpc']#, 'rpc']

files = {'norpc':[], 'rpc':[], 'DM':[]}
#files['norpc'].append('DTDPGNtuple_Parallel')
#files['norpc'].append('DTDPGNtuple_Bayes')
#files['norpc'].append('DTDPGNtuple_AM')
#files['norpc'].append('rossinQcut8_PU200')
#files['norpc'].append('rossinQcut5_PU200')
#files['norpc'].append('rossinQcut3_PU200')
#files['norpc'].append('rossinQcut2_PU200_exceptionAll')
files['norpc'].append('rossinQcut2_PU200_exception')
files['norpc'].append('rossinQcut2_PU200_exception_t0phi')
#files['norpc'].append('rossinQcut2_PU200_prime')
files['norpc'].append('rossinQcut2_PU200')
#files['norpc'].append('rossinQcut1_PU200')
files['norpc'].append('rossinQcut0_PU200')
#files['norpc'].append('rossinQcut0_PU200_noCoincidence')
#files['norpc'].append('DTDPGNtuple_mu_PU140_qcut2_noRPC_noAgeing')
#files['norpc'].append('DTDPGNtuple_mu_PU140_qcut0_noRPC_noAgeing')
#files['norpc'].append('mb_PU200_qcut8_1_noRPC_noAgeing_12_3_X')
#files['norpc'].append('mb_PU200_qcut2_1_noRPC_noAgeing_12_3_X')
#files['norpc'].append('mb_PU200_qcut0_1_noRPC_noAgeing_12_3_X')
#files['norpc'].append('DYLL_M50_PU200_qcut8')
#files['norpc'].append('DYLL_M50_PU200_qcut2')
#files['norpc'].append('DYLL_M50_PU200_qcut2_exceptionAll')
#files['norpc'].append('DYLL_M50_PU200_qcut2_exception')
#files['norpc'].append('DYLL_M50_PU200_qcut2_exceptionAll_t0phi')
#files['norpc'].append('DYLL_M50_PU200_qcut2_exception_t0phi')
#files['norpc'].append('DYLL_M50_PU200_qcut2_prime')
#files['norpc'].append('DYLL_M50_PU200_qcut0')
#files['norpc'].append('jpsimumu_PU200_qcut8')
#files['norpc'].append('jpsimumu_PU200_qcut2')
#files['norpc'].append('jpsimumu_PU200_qcut0')

algos = ["AM"]#, "Ph1"]


'''
Possible efficiency categories:
    - 'All' -> Every quality
    - 'correlated' -> Qualities 6, 7 and 6
    - '8' -> Quality 8 only
    - 'legacy' -> Qualities 3, 4, 6, 7 and 8
    - 'nothreehits -> Quality > 1
        - 'index0' -> Only index 0
        - 'index01' -> Only indexes 0 and 1
    - 'index012' -> Only indexes 0, 1 and 2
    - 'index0123' -> Only indexes 0, 1, 2 and 3

    With useRPC = True :
    - 'withmatchedthreehits' -> Quality > 1 + quality <= 1 matched with an RPC cluster or segment
    - 'qualityORSegs' -> Every DT quality + RPC segments
    - 'qualityORSegsClus' -> Every DT quality + RPC segments and clusters
    - 'qualityMatchedORSegs' -> Quality > 1 + quality <= 1 matched with an RPC cluster or segment + RPC segments
    - 'qualityMatchedORSegsClus' -> Quality > 1 + quality <= 1 matched with an RPC cluster or segment + RPC segments and clusters
'''

possibleQualities = ['All','correlated', 'Q8', 'legacy', 'index0', 'index01', 'index012', 'index0123', 'nothreehits']#, 'withmatchedthreehits' ,'qualityORSegs','qualityORSegsClus','qualityMatchedORSegs','qualityMatchedORSegsClus']




#qualities = ['']
qualities = {'norpc':[],'rpc':[], 'DM':[]}
#qualities['norpc'] = ['All', 'correlated']
#qualities['norpc'] = ['index0', 'index01', 'index012', 'index0123', 'All']
#qualities['norpc'] = ['All','nothreehits','legacy', 'correlated']
#qualities['norpc'] = ['All']
#qualities['norpc'] = ['All','correlated', 'Q8', 'nothreehits']
#qualities['norpc'] = ['Q8', 'nothreehits']
#qualities['norpc'] = ['All','nothreehits']
#qualities['norpc'] = ['legacy']
#qualities['rpc'] = ['qualityMatchedORSegs','qualityMatchedORSegsClus']
#qualities['rpc'] = ['All','nothreehits', 'withmatchedthreehits' ,'qualityORSegs','qualityORSegsClus','qualityMatchedORSegs','qualityMatchedORSegsClus']
#qualities['DM'] = ['All','nothreehits']
#qualities['DM'] = ['All']
#qualities['norpc'] = ['All','nothreehits','legacy','correlated']#, 'Q8', 'nothreehits']#, 'confirmed']
#qualities['norpc'] = ['All','nothreehits','legacy']
#qualities['norpc'] = ['legacy','correlated']
#qualities['norpc'] = ['correlated']
qualities['norpc'] = ['All','nothreehits']
#qualities['norpc'] = ['nothreehits']

##############################################################################################

if my_namespace.ntuples == True :
  print ("Starting ntuplizer for every sample in input")
  time.sleep(2)
  r.gInterpreter.ProcessLine(".x loadTPGSimAnalysis_ThetaEffs.C")
if my_namespace.ntuples == True :
  r.gSystem.Load(os.getcwd() + "/DTNtupleBaseAnalyzer_C.so")
  r.gSystem.Load(os.getcwd() + "/DTNtupleTPGSimAnalyzer_ThetaEfficiency_C.so")
  from ROOT import DTNtupleTPGSimAnalyzer
else :
  print("Not making ntuples. If you want to make them, restart with 'yes' as first argument ")
  time.sleep(2)

path = '/afs/cern.ch/work/j/jfernan/public/L1T/comp/CMSSW_14_1_0/src/DTDPGAnalysis/DTNtuples/test/'
path = '/eos/home-j/jfernan/L1T/'
effPath = "./plotsEffTheta/"
outputPath = './ntuplesTheta/'

if not os.path.isdir(effPath) : rc = call('mkdir ' + effPath, shell=True)

for cat in files :
  if cat == 'DM' : DM = True
  else : DM = False

  if DM == True :
    print bcolors.green +  "Warning!: If you run over DM samples, you may consider matching with seg_dirGlb instead of seg_posGlb avoiding eta matching" + bcolors.reset



  for fil in files[cat] :
      if my_namespace.ntuples == True :
          for quality in qualities[cat] :
              print ('Obtaining efficiency ntuples for ' + fil + ' with quality type ' + quality )
              if quality not in possibleQualities :
                  print (  bcolors.red + 'ERROR: quality category does not exist. It will not get considered in the ntuple production' + bcolors.reset)
                  continue
              time.sleep(2)
              analysis = DTNtupleTPGSimAnalyzer(path + fil + '.root', outputPath + 'results_effis_' +fil + '_' + quality + '.root', quality, DM)
              analysis.Loop()
  for algo in algos:
      for plot in ["Eff", "EffNoBX"]:
        plottingStuff = {
              'lowlimityaxis': 0.0,
              'highlimityaxis': 1.01,
              'markersize': 1,
              'yaxistitle' : 'DT Local Trigger Efficiency',
              'yaxistitleoffset': 1.5,
              'xaxistitle': "Wheel",
              #'legxlow' : 0.5,
              'legxlow' : 0.3075 + 2 * 0.1975,
              #'legylow': 0.2,
              'legylow': 0.3,
              'legxhigh': 0.9,
              #'legyhigh': 0.5,
              'legyhigh': 0.55,
              'markertypedir':[],
              'markercolordir':[],
              # 'markertypedir':{},
              # 'markercolordir':{},
              'printPU':True,
              'ageingTag': "",
              'ageingLegend': "",
            }
        if plot == "SegEff": 
            plottingStuff["lowlimityaxis"] = 0
            plottingStuff['legylow'] = 0.7
            
        all_plots = []
        all_legends = []
        all_ageingTag = ""
        for fil in files[cat]:
          plotscaffold = "h" + plot + "_{st}_{al}_{ty}"
          savescaffold = "h%s_%s_%s" % (plot, algo, fil)

          listofplots = []
          myLegends = []
          ageingTag = ("" if "withAgeing" not in fil else "3000 fb^{-1}")
          if "withAgeing" in fil:
            all_ageingTag = "3000 fb^{-1}"
            plottingStuff["ageingLegend"] = "3000 fb^{-1} ageing"
          else:
            plottingStuff["ageingLegend"] = "No ageing"

          for i in range (len(qualities[cat])) :
            if not os.path.isfile(outputPath + 'results_effis_' + fil + '_' + qualities[cat][i] + '.root') :
              if not qualities[cat][i] in legends :
                print (bcolors.red + "ERROR: '" +  qualities[cat][i]  + "' is not one of the possible qualities" + bcolors.reset)
              else :
                print (bcolors.red + 'ERROR: ' + outputPath + 'results_effis_' + fil + '_' + qualities[cat][i] + '.root + does not exist, maybe running the ntuple production helps' + bcolors.reset)
              continue
            myLegends.append(legends[qualities[cat][i]])
            all_legends.append(legends[fil] + " " + legends[qualities[cat][i]])
            # plottingStuff['markertypedir']["h" + plot + "_AM" + "_" + qualities[cat][i]] = 20
            # plottingStuff['markercolordir']["h" + plot + "_AM" + "_" + qualities[cat][i]] = markerColors[i]
            plottingStuff['markertypedir'].append(20)
            plottingStuff['markercolordir'].append(markerColors[i])
            # plottingStuff['ageingTag'] = ageingTag  # FIXME
            effplot.makeresplot(listofplots, algo, qualities[cat][i], outputPath + 'results_effis_' + fil + '_' + qualities[cat][i] + '.root', plotscaffold)
            all_plots.append(listofplots[-1])

          print "\nCombining and saving\n"
          effplot.combineresplots(listofplots, myLegends, plottingStuff, effPath,  savescaffold+'_0', fil )
          #effplot.combineresplots(listofplots, legends[cat], plottingStuff, effPath,  savescaffold+'zoomIn' )
        if files[cat]:
            del plottingStuff["ageingLegend"]
            plottingStuff['legxlow'] =  0.3075 + 1 * 0.1975
            for i, marker in enumerate(plottingStuff['markertypedir']):
                plottingStuff['markertypedir'][i] = marker + i / len(qualities[cat])
            plottingStuff['ageingTag'] = all_ageingTag
            savescaffold = "h" + plot + "_" + cat
            effplot.combineresplots(all_plots, all_legends, plottingStuff, effPath,  savescaffold+'_0', files[cat][-1] )
            plottingStuff['legxlow'] =  0.3075 + 2 * 0.1975

#if True : sys.exit(1)






#markerColors = []
print "\nBeginning plotting\n"





plottingStuff2 = {}

plottingStuff2['qualities1'] = { 'lowlimityaxis': 0.2,
		      'highlimityaxis': 1,
		      'markersize': 1,
		      'yaxistitle' : 'Efficiency (adim.)',
		      'yaxistitleoffset': 1.5,
		      'xaxistitle': "#eta",
		      'legxlow' : 0.6,
		      #'legxlow' : 0.3075 + 2 * 0.1975,
		      #'legylow': 0.2,
		      'legylow': 0.3,
		      'legxhigh': .95,
		      'legyhigh': .44,
		      'markertypedir':{},
		      'markercolordir':{},
              'PU':'200',
   		    }
plottingStuff2['qualities2'] = { 'lowlimityaxis': 0.5,
		      'highlimityaxis': 1,
		      'markersize': 1,
		      'yaxistitle' : 'Efficiency (adim.)',
		      'yaxistitleoffset': 1.5,
		      'xaxistitle': "#eta",
		      #'legxlow' : 0.5,
		      #'legxlow' : 0.3075 + 2 * 0.1975,
		      'legxlow' : 0.60,
		      #'legylow': 0.2,
		      'legylow': 0.3,
		      'legxhigh': .79,
		      'legyhigh': .44,
		      'markertypedir':{},
		      'markercolordir':{},
          'PU':'200'
   		    }
plottingStuff2['qualities3'] = { 'lowlimityaxis': 0.9,
		      'highlimityaxis': 1,
		      'markersize': 1,
		      'yaxistitle' : 'Efficiency (adim.)',
		      'yaxistitleoffset': 1.5,
		      'xaxistitle': "#eta",
		      #'legxlow' : 0.5,
		      #'legxlow' : 0.3075 + 2 * 0.1975,
		      'legxlow' : 0.6,
		      #'legylow': 0.2,
		      'legylow': 0.3,
		      'legxhigh': .79,
		      'legyhigh': .44,
		      'markertypedir':{},
		      'markercolordir':{},
   		    }

#markerColors = [r.kBlue, r.kRed, r.kGreen, r.kOrange, r.kBlack, r.kMagenta]
chambTag = ["MB1", "MB2", "MB3", "MB4"]

Qualities = {'qualities1':[] , 'qualities2':[], 'qualities3':[] }

Qualities['qualities1'] = ['All', 'correlated']
Qualities['qualities2'] = ['nothreehits', 'legacy']
Qualities['qualities3'] = ['All', 'nothreehits']



for ch in chambTag :
  for plot in ["EffEta"] :
    for key in ['qualities1'] :
    #for key in ['qualities1','qualities2'] :
      plottingStuff2[key]['writeInPlot'] = ch
      listofplots = []
      myLegends = []
      a=0
      for fil in files['norpc'] :
        plotscaffold = "h" + plot + "_" + ch +"_{al}_{ty}"
        savescaffold = "h" + plot + "_" + key + "_" + ch
        

        for i in range (len(Qualities[key])) :
          if not os.path.isfile(outputPath + 'results_effis_' + fil + '_' + Qualities[key][i] + '.root') :
            if not Qualities[key][i] in legends :
              print (bcolors.red + "ERROR: '" +  Qualities[key][i]  + "' is not one of the possible qualities" + bcolors.reset)
            else :
              print (bcolors.red + 'ERROR: ' + outputPath + 'results_effis_' + fil + '_' + Qualities[key][i] + '.root + does not exist, maybe running the ntuple production helps' + bcolors.reset)
            continue
          myLegends.append(legends[fil]+" "+legends[Qualities[key][i]])
          plottingStuff2[key]['markertypedir']["hEff_" + "AM" + "_" + fil+Qualities[key][i]] = 20 + a*6
          plottingStuff2[key]['markercolordir']["hEff_" + "AM" + "_" + fil+Qualities[key][i]] = markerColors[i]
          plottingStuff2[key]['ageingTag'] = ("" if "withAgeing" not in fil else "3000 fb^{-1}")
          effplot.makeWhateverResplot(listofplots, "AM", fil+Qualities[key][i], outputPath + 'results_effis_' + fil + '_' + Qualities[key][i] + '.root', plotscaffold)
        a+=1
      if (len (files['norpc']) > 0 ) :
        print "\nCombining and saving\n"
        effplot.combineEffPlots(listofplots, myLegends, plottingStuff2[key], effPath,  savescaffold+'_0' )


#filesPU = {'mu_pu0':'PU0','mu_pu200':'PU200'}
#filesPU = ['nopu_noage_norpc','pu200_noage_norpc']
filesPU = ['pu200_noage_norpc']

for ch in chambTag :
  for plot in ["EffEta"] :
    for key in ['qualities3'] :
      plottingStuff2[key]['writeInPlot'] = ch
      listofplots = []
      myLegends = []
      a = 0
      for fil in filesPU :
        plotscaffold2 = "h" + plot + "_" + ch +"_{al}_{ty}"
        #plotscaffold2 = "h" + plot + "_PU_" + ch +"_{al}_{ty}"
        savescaffold2 = "h" + plot + "_PU_" + key + "_" + ch
        for i in range (len(Qualities[key])) :
          if not os.path.isfile(outputPath + 'results_effis_' + fil + '_' + Qualities[key][i] + '.root') :
            if not Qualities[key][i] in legends :
              print (bcolors.red + "ERROR: '" +  Qualities[key][i]  + "' is not one of the possible qualities" + bcolors.reset)
            else :
              print (bcolors.red + 'ERROR: ' + outputPath + 'results_effis_' + fil + '_' + Qualities[key][i] + '.root + does not exist, maybe running the ntuple production helps' + bcolors.reset)
            continue
          myLegends.append(filesPU[fil] + " " + legends[Qualities[key][i]])
          plottingStuff2[key]['markertypedir']["hEff_" + "AM" + "_" + fil+Qualities[key][i]] = 20 + a*6
          plottingStuff2[key]['markercolordir']["hEff_" + "AM" + "_" + fil+Qualities[key][i]] = markerColors[i]
          plottingStuff2[key]['ageingTag'] = ("" if "withAgeing" not in fil else "3000 fb^{-1}")
          effplot.makeWhateverResplot(listofplots, "AM", fil+Qualities[key][i], outputPath + 'results_effis_' + fil + '_' + Qualities[key][i] + '.root', plotscaffold2)
        a+=1

      if (len(listofplots) > 0 ) :
        print "\nCombining and saving\n"
        effplot.combineEffPlots(listofplots, myLegends, plottingStuff2[key], effPath,  savescaffold2+'_0' )



filesDM = []
#filesDM = ['PU0_DM_PT10-30_mod_2_']
DMPath = './DMplots/'

chambTags = [ "MB1", "MB2", "MB3", "MB4"]
whTags    = [ "Wh.-2", "Wh.-1", "Wh.0", "Wh.+1", "Wh.+2"]



#for File in filesDM :
for File in files['DM'] :
  res = r.TFile.Open(outputPath + 'results_effis_' + File + '_All' + '.root')
  plottingStuff = { 'lowlimityaxis': 0,
 	            'highlimityaxis': 1,
	            'markersize': 1,
	            'yaxistitle' : 'Efficiency (adim.)',
	            'yaxistitleoffset': 1.5,
	            'xaxistitle': "Local Direction",
	            'legxlow' : 0.5,
	            'legylow': 0.3,
	            'legxhigh': 0.9,
	            'legyhigh': 0.35,
	            'markertypedir':{},
	            'markercolordir':{'AM':r.kRed, 'HB':r.kBlue}
   		    }

  legendsDM = ['AM']
  #legendsDM = ['AM', 'HB']
  plotList = []
  i = 0
  # FULL DETECTOR
  for algo in legendsDM :
    plotscaffold2 = "hEff_{al}_{ty}"
    plottingStuff['markertypedir']["hEff_" + algo + "_" + File ] = 20
    plottingStuff['markercolordir']["hEff_" + algo + "_" + File ] = markerColors[i]
    plottingStuff['ageingTag'] = ("" if "withAgeing" not in fil else "3000 fb^{-1}")
    i+=1
    effplot.makeWhateverResplot(plotList, algo, File, outputPath + 'results_effis_' + File + '_All'  + '.root', plotscaffold2)
  effplot.combineEffPlots(plotList, legendsDM, plottingStuff, DMPath, 'hEffVsSlope_' + File)

  #PER WHEEL AND STATION
  for ch in chambTags :
    for wh in whTags :
      plotList = []
      i=0
      for algo in legendsDM :
        plotscaffold2 = "hEff_" + wh + "_" + ch + "_{al}_{ty}"
        plottingStuff['markertypedir']["hEff_" + algo + "_" + File ] = 20
        plottingStuff['markercolordir']["hEff_" + algo + "_" + File ] = markerColors[i]
        plottingStuff['ageingTag'] = ("" if "withAgeing" not in fil else "3000 fb^{-1}")
        i+=1
        effplot.makeWhateverResplot(plotList, algo, File, outputPath + 'results_effis_' + File + '_All'  + '.root', plotscaffold2)
      effplot.combineEffPlots(plotList, legendsDM, plottingStuff, DMPath, 'hEffVsSlope_' + wh + '_' + ch + '_' + File )


  plottingStuff2 = { 'lowlimityaxis': 0.8,
 	            'highlimityaxis': 1,
	            'markersize': 1,
	            'yaxistitle' : 'Efficiency (adim.)',
	            'yaxistitleoffset': 1.5,
	            'xaxistitle': "Gen Part Lxy",
	            'legxlow' : 0.5,
	            'legylow': 0.3,
	            'legxhigh': 0.9,
	            'legyhigh': 0.35,
	            'markertypedir':{},
	            'markercolordir':{'AM':r.kRed, 'HB':r.kBlue}
   		    }

  # FULL DETECTOR
  plotList = []
  i = 0
  for algo in legendsDM :
    plotscaffold2 = "hEffLxy_{al}_{ty}"
    plottingStuff2['markertypedir']["hEff_" + algo + "_" + File ] = 20
    plottingStuff2['markercolordir']["hEff_" + algo + "_" + File ] = markerColors[i]
    plottingStuff2['ageingTag'] = ("" if "withAgeing" not in fil else "3000 fb^{-1}")
    i+=1
    effplot.makeWhateverResplot(plotList, algo, File, outputPath + 'results_effis_' + File + '_All'  + '.root', plotscaffold2)
  effplot.combineEffPlots(plotList, legendsDM, plottingStuff2, DMPath, 'hEffVsLxy_' + File)

  #PER WHEEL AND STATION
  for ch in chambTags :
    for wh in whTags :
      plotList = []
      i=0
      for algo in legendsDM :
        plotscaffold2 = "hEffLxy_" + wh + "_" + ch + "_{al}_{ty}"
        plottingStuff2['markertypedir']["hEff_" + algo + "_" + File ] = 20
        plottingStuff2['markercolordir']["hEff_" + algo + "_" + File ] = markerColors[i]
        plottingStuff2['ageingTag'] = ("" if "withAgeing" not in fil else "3000 fb^{-1}")
        i+=1
        effplot.makeWhateverResplot(plotList, algo, File, outputPath + 'results_effis_' + File + '_All'  + '.root', plotscaffold2)
      effplot.combineEffPlots(plotList, legendsDM, plottingStuff2, DMPath, 'hEffVsLxy_' + wh + '_' + ch + "_" + File )


#
