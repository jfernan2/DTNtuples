import sys, os
import time
import ROOT
from ROOT import gSystem
from copy import deepcopy as copy
import CMS_lumi
#import myPlotter_input as effplot 
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from subprocess import call
import myPlotter_input as effplot
from markerColors import markerColors
from allLegends import legends
from collections import OrderedDict

################################# CHANGE BEFORE RUNNING #######################################

categories = ['norpc', 'rpc']
files = OrderedDict([('norpc', []), ('rpc', []), ('DM', [])])
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
files['norpc'].append('rossin_noRPC_noAgeing_alignTrue')
files['norpc'].append('rossin_noRPC_withAgeing_alignTrue')
files['rpc'].append('rossin_withRPC_noAgeing_alignTrue')
files['rpc'].append('rossin_withRPC_withAgeing_alignTrue')
#files['norpc'].append('rossin_noRPC_noAgeing_alignFalse')

qualities = []
#qualities = {'norpc':[],'rpc':[], 'DM':[]}
qualities.append('All')
#qualities['norpc'].append('All')
qualities.append('Correlated')
#qualities['norpc'].append('Correlated')
#qualities['norpc'].append('Legacy')
#qualities['norpc'].append('4h')
#qualities['norpc'].append('3h')

##############################################################################################

path = '/eos/home-j/jfernan/L1T/simulationSamples/'
plotsPath = "./summaryPlots/"
distPath = "./distributionPlots/"
#outputPath = './ntuples/'
outputPath = '/eos/home-j/jfernan/L1T/ntuplesResults/'
eosPath='/eos/home-j/jfernan/L1T/www/resolutionsNote/'

chambTags = ["MB1", "MB2", "MB3", "MB4"]
wheelTags    = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"];
magnitude = ["Time"]
# magnitude = ["Time", "Phi", "PhiB", "TanPsi", "x"]

plottingStuff = { 'lowlimityaxis': 0,
		      'highlimityaxis': {},
		      'markersize': 1,
              'yaxistitle' : {"Time": "Arbitrary units"},
		      'yaxistitleoffset': 1.5,
		      'xaxistitle': {"Time": "Trigger Primitive Time (ns)"},
		      #'xaxistitle': {"Time": "Trigger Primitive - Offline Segment Time (ns)"},
              'xaxislimits': {"Time": (-20, 20)},
		      #'legxlow' : 0.7,
              'legxlow' : 0.6,
		      'legylow': 0.55,
		      'legxhigh': 0.85,
		      'legyhigh': 0.85,
		      'markertypedir':{},
		      'markercolordir':{},
              'ageingTag': "",
              'PU': ""
   		    }

markerColors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kBlack, ROOT.kMagenta]
markers = [20, 26]

if not os.path.isdir(distPath):
    os.mkdir(distPath)
output_dirname = distPath
if not os.path.isdir(output_dirname):
    os.mkdir(output_dirname)

for mag in magnitude:
    for qual in qualities: 
    # for qual in qualities[cat]: 
        for ich in range(1, 5):
            for iwh in range(-2, 3):
                listofplots = []
                sigmas = []
                mylegends = []
                num = 0
                plottingStuff['ageingTag'] = ""
                plottingStuff['PU'] = ""
                for icat, cat in enumerate(files):
                    if not files[cat]: 
                        continue
                    # dirname = "{}/{}/".format(plotsPath, cat)
                    # if not os.path.isdir(dirname):
                        # raise Exception(dirname + " does not exist")
                    for ifile, fil in enumerate(files[cat]):
                    
                        distscaffold = "h" + mag + "_" + "AM" + qual + "_" + "{wh}" + "_" + "{ch}" + "_P2"
                        plotscaffold = "h" + mag + "_{al}_" + qual + "_{wh}"
                        savescaffold = "h" + mag + "_{al}_" + qual + "_wh{iwh}_mb{ich}"

                        if "withAgeing" in fil:
                            plottingStuff['ageingTag'] = "3000 fb^{-1}"
                        if "pu" in fil.lower():
                            plottingStuff['PU'] = lookForPU(suffix)
                        elif "rossin" in fil.lower():
                            plottingStuff['PU'] = "PU200"

                        num += 1
                        print outputPath + 'results_resols_' + fil + '_.root'
                        file = ROOT.TFile.Open(outputPath + 'results_resols_' + fil + '_.root')
                        namePlot = distscaffold.format(wh = wheelTags[iwh + 2], ch = chambTags[ich - 1])
                        print namePlot
                        listofplots.append(copy(file.Get(namePlot).Clone()))
                        listofplots[-1].SetMarkerColor(markerColors[ifile])
                        listofplots[-1].SetLineColor(markerColors[ifile])
                        listofplots[-1].SetMarkerStyle(markers[icat])
                        listofplots[-1].SetLineWidth(3)
                        
                        # obtain sigma for this wh and st
                        sigma_file = ROOT.TFile.Open(plotsPath + fil + '/' +  'outPlots.root')
                        sigma_plot = sigma_file.Get(plotscaffold.format(al = "AM", wh = wheelTags[iwh + 2]))
                        sigmas.append(sigma_plot.GetBinContent(ich))
                        
                        print legends[fil]
                        mylegends.append(legends[fil])

                print "\nCombining and saving\n"

                c   = ROOT.TCanvas("c", "c", 800, 800)
                listofplots[0].GetYaxis().SetTitleOffset(plottingStuff['yaxistitleoffset'])
                #listofplots[0].GetYaxis().SetTitle(plottingStuff['yaxistitle'])

                leg = ROOT.TLegend(plottingStuff['legxlow'], plottingStuff['legylow'], plottingStuff['legxhigh'], plottingStuff['legyhigh'])
                plot_maximum = -1
                
                o = ROOT.TObject()
                for iplot in range(len(listofplots)):
                    if iplot != 0:
                        leg.AddEntry(o, " ", "")
                    listofplots[iplot].Scale(1. / listofplots[iplot].Integral())
                    if listofplots[iplot].GetMaximum() > plot_maximum:
                        plot_maximum = listofplots[iplot].GetMaximum()
                    leg.AddEntry(listofplots[iplot], mylegends[iplot], "PL")
                    leg.AddEntry(o, "#sigma = {:.2f}".format(sigmas[iplot]), "")
                    

                listofplots[0].SetTitle("; " + plottingStuff['xaxistitle'][mag] + "; " + plottingStuff['yaxistitle'][mag])
                listofplots[0].SetMaximum(1.1 * plot_maximum)
                listofplots[0].GetXaxis().SetRangeUser(*plottingStuff['xaxislimits'][mag])
                for iplot in range(len(listofplots)):
                    listofplots[iplot].Draw("P" + (iplot != 0) * "same")
            
                leg.Draw()
                ROOT.gPad.Update()
                firsttex = ROOT.TLatex()
                firsttex.SetTextSize(0.03)
                firsttex.DrawLatexNDC(0.11,0.91,"#scale[1.5]{CMS} Phase-2 Simulation #font[12]{Preliminary}")
                firsttex.Draw("same");

                secondtext = ROOT.TLatex()
                toDisplay  = ROOT.TString("%s%s" % (
                    ("" if plottingStuff["ageingTag"] == "" else "%s, " % plottingStuff["ageingTag"]),
                    ("" if plottingStuff["PU"] == "" else "%s" % plottingStuff["PU"])))
                secondtext.SetTextSize(0.035)
                secondtext.SetTextAlign(31)
                secondtext.DrawLatexNDC(0.90, 0.91, toDisplay.Data())
                secondtext.Draw("same")
               
                tex = ROOT.TLatex()
                tex.SetTextSize(0.03);
                tex.DrawLatexNDC(0.76,0.87, "Wh%s%s MB%s" % (("" if iwh <= 0 else "+"), iwh, ich))
                tex.Draw("same");

                ROOT.TGaxis.SetMaxDigits(4)
                ROOT.gPad.Update()
                c.Update()
                
                for ext in ["png", "pdf", "root"]:
                    c.SaveAs(output_dirname + "/" + savescaffold.format(al="AM", ich=ich, iwh=iwh) + "." + ext)
                c.Close(); del c
                                    
                    
                    











