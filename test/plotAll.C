#include <fstream>
#include <stdio.h>
#include <string>
#include <stdlib.h>

#include "TROOT.h"
#include "TFile.h"
#include "TGraph.h"
#include "TPostScript.h"
#include "TLine.h"
#include "TText.h"
#include "TH1.h"
#include "TH2.h"
#include "TStyle.h"
#include "TProfile.h"
#include "TNtuple.h"
#include "TRandom.h"
#include "TCanvas.h"


#include <TLatex.h>


//#include "tdrstyle.C"

#include "PlotTemplate.C"

void plotAll( std::string file, std::string ageingTag ){

//  setTDRStyle();

TLatex latex;
latex.SetTextSize(0.03);

TString Lumi = "35.9";

gStyle->SetPalette(1,0);
gStyle->SetOptFit(111111);
 gStyle->SetOptStat(111111);


  gSystem->Load("libRooFit");
  using namespace RooFit;

  std::vector<std::string> chambTags = { "MB1", "MB2", "MB3", "MB4"};
  std::vector<std::string> whTags    = { "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"};
  std::vector<std::string> secTags   = { "Sec1", "Sec2", "Sec3", "Sec4", "Sec5", "Sec6", "Sec7", "Sec8","Sec9","Sec10","Sec11","Sec12","Sec13","Sec14"};
  //std::vector<std::string> magnitudes = { "PhiRes","PhiBRes", "TanPsiRes", "xRes"};
  std::vector<std::string> magnitudes = { "Time", "TimeRes", "PhiRes","PhiBRes", "TanPsiRes", "xRes"};
  std::vector<std::string> algos      = { "AM"};
  //std::vector<std::string> qualTags   = { "3h","4h"};
  //std::vector<std::string> qualTags   = {"Q1", "Q2", "Q3", "Q4"};
  //std::vector<std::string> qualTags   = {"All", "Correlated"};
  //std::vector<std::string> qualTags   = {"Uncorrelated"};
  std::vector<std::string> qualTags   = {"Correlated", "Uncorrelated", "3h", "4h", "All"};
  //std::vector<std::string> qualTags   = { "All"};
  //std::vector<std::string> qualTags   = { "All","Correlated","Legacy"};
  //std::vector<std::string> qualTags   = { "Correlated", "Uncorrelated","3h","4h","All", "Legacy","Q8","Q7","Q6"};


  std::string outputPath = "/eos/home-j/jfernan/L1T/ntuplesResults/";
  TFile *inFile = TFile::Open( (outputPath + "results_resols_" +file + "_.root").c_str() );
  gSystem->Exec("mkdir summaryPlots/"  );
  gSystem->Exec("mkdir summaryPlots/" + TString(file) );
  for (unsigned int i = 0; i < qualTags.size(); i++){
    TString quality = qualTags.at(i);
    gSystem->Exec("mkdir summaryPlots/" + TString(file) + "/" + quality);
  }

  TFile outPlots( "summaryPlots/" + TString (file)+ "/outPlots.root","RECREATE");

  std::map<std::string,std::string> xlabels;
  // xlabels["Time"] = "Trigger Primitive Time (ns)";
  xlabels["Time"] = "Trigger Primitive Time (TDC counts)";
  xlabels["TimeRes"] = "Primitive - Segment Time (ns)";
  xlabels["PhiRes"] = "Primitive - Segment #phi (#murad)";
  xlabels["PhiBRes"] = "Primitive - Segment #phi_{B} (mrad)";
  xlabels["TanPsiRes"] = "Primitive - Segment Local direction (mrad)";
  xlabels["xRes"] = "Primitive - Segment Position (#mum)";

  std::map<std::string,std::string> units;
  // units["Time"] = "ns";
  units["Time"] = "TDC c.";
  units["TimeRes"] = "ns";
  units["PhiRes"] = "#murad";
  units["PhiBRes"] = "mrad";
  units["TanPsiRes"] = "mrad";
  units["xRes"] = "#mum";

  std::map<std::string, float> ranges;
  ranges["TimeAll"  ] = 20;
  ranges["TimeResAll"  ] = 20;
  ranges["PhiResAll"   ] = 50;
  ranges["PhiBResAll"   ] = 3;
  ranges["TanPsiResAll"] = 3;
  ranges["xResAll"     ] = 500;

  ranges["TimeCorrelated"  ] = 20;
  ranges["TimeResCorrelated"  ] = 20;
  ranges["PhiResCorrelated"   ] = 50;
  ranges["PhiBResCorrelated"   ] = 3;
  ranges["TanPsiResCorrelated"] = 3;
  ranges["xResCorrelated"     ] = 500;

  ranges["TimeQ1"  ] = 30;
  ranges["TimeResQ1"  ] = 30;
  ranges["PhiResQ1"   ] = 100;
  ranges["PhiBResQ1"   ] = 100;
  ranges["TanPsiResQ1"] = 100;
  ranges["xResQ1"     ] = 500;

  ranges["TimeQ2"  ] = 30;
  ranges["TimeResQ2"  ] = 30;
  ranges["PhiResQ2"   ] = 100;
  ranges["PhiBResQ2"   ] = 100;
  ranges["TanPsiResQ2"] = 100;
  ranges["xResQ2"     ] = 500;

  ranges["Time3h"  ] = 30;
  ranges["TimeRes3h"  ] = 30;
  ranges["PhiRes3h"   ] = 100;
  ranges["PhiBRes3h"   ] = 100;
  ranges["TanPsiRes3h"] = 100;
  ranges["xRes3h"     ] = 500;

  ranges["TimeQ3"  ] = 20;
  ranges["TimeResQ3"  ] = 20;
  ranges["PhiResQ3"   ] = 50;
  ranges["PhiBResQ3"   ] = 60;
  ranges["TanPsiResQ3"] = 60;
  ranges["xResQ3"     ] = 500;

  ranges["TimeQ4"  ] = 20;
  ranges["TimeResQ4"  ] = 20;
  ranges["PhiResQ4"   ] = 50;
  ranges["PhiBResQ4"   ] = 60;
  ranges["TanPsiResQ4"] = 60;
  ranges["xResQ4"     ] = 500;

  ranges["Time4h"  ] = 30;
  ranges["TimeRes4h"  ] = 30;
  ranges["PhiRes4h"   ] = 100;
  ranges["PhiBRes4h"   ] = 100;
  ranges["TanPsiRes4h"] = 100;
  ranges["xRes4h"     ] = 500;

  ranges["TimeUncorrelated"  ] = 20;
  ranges["TimeResUncorrelated"  ] = 20;
  ranges["PhiResUncorrelated"   ] = 50;
  ranges["PhiBResUncorrelated"   ] = 60;
  ranges["TanPsiResUncorrelated"] = 60;
  ranges["xResUncorrelated"     ] = 500;

  // std::map<std::string, float> ranges;
  // ranges["TimeAll"  ] = 20;
  // ranges["TimeResAll"  ] = 20;
  // ranges["PhiResAll"   ] = 0.00005;
  // ranges["PhiBResAll"   ] = 0.003;
  // ranges["TanPsiResAll"] = 0.003;
  // ranges["xResAll"     ] = 0.05;

  // ranges["TimeLegacy"  ] = 20;
  // ranges["TimeResLegacy"  ] = 20;
  // ranges["PhiResLegacy"   ] = 0.00005;
  // ranges["PhiBResLegacy"   ] = 0.003;
  // ranges["TanPsiResLegacy"] = 0.003;
  // ranges["xResLegacy"     ] = 0.05;

  // ranges["TimeCorrelated"  ] = 20;
  // ranges["TimeResCorrelated"  ] = 20;
  // ranges["PhiResCorrelated"   ] = 0.00005;
  // ranges["PhiBResCorrelated"   ] = 0.003;
  // ranges["TanPsiResCorrelated"] = 0.003;
  // ranges["xResCorrelated"     ] = 0.05;

  // ranges["Time3h"  ] = 20;
  // ranges["TimeRes3h"  ] = 20;
  // ranges["PhiRes3h"   ] = 0.0002;
  // ranges["PhiBRes3h"   ] = 0.1;
  // ranges["TanPsiRes3h"] = 0.1;
  // ranges["xRes3h"     ] = 0.35;

  // ranges["Time4h"  ] = 20;
  // ranges["TimeRes4h"  ] = 20;
  // ranges["PhiRes4h"   ] = 0.0002;
  // ranges["PhiBRes4h"   ] = 0.02;
  // ranges["TanPsiRes4h"] = 0.05;
  // ranges["xRes4h"     ] = 0.05;


  // std::map<std::string,float> ranges;
  // ranges["TimeResAll"  ] = 20;
  // ranges["PhiResAll"   ] = 0.00015;
  // ranges["PhiBResAll"   ] = 0.01;
  // ranges["TanPsiResAll"] = 0.01;
  // ranges["xResAll"     ] = 0.05;
  // ranges["TimeResLegacy"  ] = 20;
  // ranges["PhiResLegacy"   ] = 0.00015;
  // ranges["PhiBResLegacy"   ] = 0.01;
  // ranges["TanPsiResLegacy"] = 0.01;
  // ranges["xResLegacy"     ] = 0.075;
  // ranges["TimeResCorrelated"  ] = 20;
  // ranges["PhiResCorrelated"   ] = 0.00015;
  // ranges["PhiBResCorrelated"   ] = 0.005;
  // ranges["TanPsiResCorrelated"] = 0.005;
  // ranges["xResCorrelated"     ] = 0.15;
  // //ranges["xResCorrelated"     ] = 0.05;
  // ranges["TimeRes3h"  ] = 20;
  // ranges["PhiRes3h"   ] = 0.0002;
  // ranges["PhiBRes3h"   ] = 0.1;
  // ranges["TanPsiRes3h"] = 0.1;
  // ranges["xRes3h"     ] = 0.35;
  // ranges["TimeRes4h"  ] = 20;
  // ranges["PhiRes4h"   ] = 0.0002;
  // ranges["PhiBRes4h"   ] = 0.02;
  // ranges["TanPsiRes4h"] = 0.05;
  // ranges["xRes4h"     ] = 0.05;

  std::map<std::string,float> yaxis;
  yaxis["Time3h"  ] = 500;
  yaxis["TimeRes3h"  ] = 500;
  yaxis["PhiRes3h"   ] = 200;
  yaxis["PhiBRes3h"   ] = 75;
  yaxis["TanPsiRes3h"] = 75;
  yaxis["xRes3h"     ] = 75;
  yaxis["TimeQ1"  ] = 500;
  yaxis["TimeResQ1"  ] = 500;
  yaxis["PhiResQ1"   ] = 200;
  yaxis["PhiBResQ1"   ] = 75;
  yaxis["TanPsiResQ1"] = 75;
  yaxis["xResQ1"     ] = 75;
  yaxis["Time4h"  ] = 4000;
  yaxis["TimeRes4h"  ] = 4000;
  yaxis["PhiRes4h"   ] = 4000;
  yaxis["PhiBRes4h"   ] = 500;
  yaxis["TanPsiRes4h"] = 650;
  yaxis["xRes4h"     ] = 650;
  yaxis["TimeCorrelated"  ] = 1200;
  yaxis["TimeResCorrelated"  ] = 1200;
  //yaxis["TimeResCorrelated"  ] = 3000;
  yaxis["PhiResCorrelated"   ] = 1000;
  //yaxis["PhiResCorrelated"   ] = 3000;
  yaxis["PhiBResCorrelated"   ] = 1500;
  //yaxis["PhiBResCorrelated"   ] = 3000;
  yaxis["TanPsiResCorrelated"] = 1500;
  //yaxis["TanPsiResCorrelated"] = 4000;
  yaxis["xResCorrelated"     ] = 150;
  //yaxis["xResCorrelated"     ] = 500;

 //TFile outPlots = TFile::Open("./outPlots.root","RECREATE");

 char name [128];
 std::map<std::string, TH1*> m_plots;

 for (auto & qual : qualTags ) {
 for (auto & mag : magnitudes ) {
   for (unsigned int i = 0; i < whTags.size(); i++) {
     auto whTag = whTags.at(i);
     m_plots[mag + "AM" + qual + whTag] = new TH1F(("h" + mag + "_AM_" +  qual  + "_" + whTag).c_str(),
							   ( mag + " Seg-TP distribution for " + whTag +  "; ; sigma").c_str(),
							   4,0.5,4.5);

     for (unsigned int j = 0; j < chambTags.size(); j++) {
       auto chambTag = chambTags.at(j);
       m_plots[mag + "AM" + qual + whTag]->GetXaxis()->SetBinLabel(j+1, chambTag.c_str());



       string namePlot = "h" + mag + "_" + "AM" + qual + "_" + whTag + "_" + chambTag + "_P2";
       cout << namePlot << endl;
       inFile->cd();
       TH1F *hResSlope4h1 = (TH1F*)inFile->Get(namePlot.c_str());


     //  TCanvas *canvas10 = new TCanvas(namePlot.c_str(),namePlot.c_str(), 800, 800);
       //TCanvas* canvas10 = CreateCanvas(namePlot.c_str(), false, false);

       //hResSlope4h1->Draw();

       TH2F*  hResSlope4h;
       hResSlope4h=(TH2F*)hResSlope4h1->Clone();
    // hResSlope4h->Draw();
       std::string nameFile;
       std::cout << mag+qual << std::endl;
       RooRealVar x("x","",-ranges[mag+qual],ranges[mag+qual]);

       //x.setRange("small", -5., 5.);

       RooRealVar mean("mean",",mean of Gaussian",0.,-ranges[mag+qual]/2,ranges[mag+qual]/2);
       RooRealVar sigma1("sigma1",",width of narrow Gaussian",ranges[mag+qual]/20,0,ranges[mag+qual]);
       RooRealVar sigma2("sigma2",",width of wide Gaussian",ranges[mag+qual]/2,0,3*ranges[mag+qual]);
       //RooRealVar sigma3("sigma3",",width of wide Gaussian",0.01,0,0.05);
       RooRealVar sigma3("sigma3",",width of wide Gaussian",100,100,200);
       RooRealVar fraction("fraction",",fraction of narrow Gaussian",2./3.,0.,1.);
       RooRealVar fraction2("fraction2",",fraction of narrow Gaussian",1./3.,0.,1.);

       RooGaussian gauss1("gauss1","Narrow Gaussian",x, mean, sigma1);
       RooGaussian gauss2("gauss2","Wide Gaussian",x, mean, sigma2);
       RooGaussian gauss3("gauss3","Wide Gaussian",x, mean, sigma3);

       RooAddPdf twogauss("twogauss","Two Gaussians pdf", RooArgList(gauss1, gauss3), RooArgList(fraction2));
       //RooAddPdf twogauss("twogauss","Two Gaussians pdf",RooArgList(gauss1,gauss2,gauss3),RooArgList(fraction,fraction2));
       //RooAddPdf twogauss("twogauss","Two Gaussians pdf",RooArgList(gauss1,gauss3),fraction);

       RooDataHist data("data","data", x, hResSlope4h);

       // twogauss.fitTo(data,RooFit::Range("small"));
       twogauss.fitTo(data,RooFit::Extended());

       double coreSigma, coreSigmaError;
       if (sigma1.getVal() > sigma3.getVal()) {
         coreSigma = sigma3.getVal();
         coreSigmaError = sigma3.getError();
       } else {
         coreSigma = sigma1.getVal();
         coreSigmaError = sigma1.getError();
       }

       // if (sigma1.getVal() > sigma2.getVal()) {
         // if (sigma2.getVal() > sigma3.getVal()) coreSigma = sigma3.getVal();
         // else coreSigma = sigma2.getVal();
       // } else if ( sigma1.getVal() > sigma3.getVal()) coreSigma = sigma3.getVal();
       // else coreSigma = sigma1.getVal();

       // m_plots[mag + "AM" + qual + whTag]->SetBinContent(j + 1, mean.getVal());
       m_plots[mag + "AM" + qual + whTag]->SetBinContent(j + 1, coreSigma);
       // if (mag == "TimeRes" || mag == "Time") m_plots[mag + "AM" + qual + whTag]->SetBinContent(j + 1, coreSigma);
       // else if (mag == "TanPsiRes" ||  mag == "PhiBRes") m_plots[mag + "AM" + qual + whTag]->SetBinContent(j + 1, coreSigma * 1000);
       // else if (mag == "xRes") m_plots[mag + "AM" + qual + whTag]->SetBinContent(j + 1, coreSigma * 10000);
       // else if (mag == "PhiRes") m_plots[mag + "AM" + qual + whTag]->SetBinContent(j + 1, coreSigma * 1E6);

       TCanvas* canvas1 = CreateCanvas(namePlot.c_str(), false, false);
       //DrawPrelimLabel(canvas1);
       //DrawLumiLabel(canvas1);
       // RooRealVar y("y","",-20, 20);
       // RooDataHist data_y("data_y","data_y", y, hResSlope4h);
       RooPlot* xframe=x.frame();
       hResSlope4h->GetXaxis()->SetRangeUser(-20, 20);
       hResSlope4h->Draw("same");
       data.plotOn(xframe);
       // data_y.plotOn(xframe);
       twogauss.plotOn(xframe);
       //twogauss.plotOn(xframe,Components("gauss1"),LineColor(kRed));
       //twogauss.plotOn(xframe,Components("gauss2"),LineStyle(kDashed));
       //twogauss.plotOn(xframe,Components("gauss3"),LineStyle(kDotted));

       sprintf(name,"%s",namePlot.c_str());
       //xframe->SetTitle(name);
       xframe->SetTitle("");
       //xframe->SetXTitle("Primitive - Segment #Psi (rad) ");
       xframe->SetYTitle("Events");
       xframe->SetXTitle(xlabels[mag].c_str());
       xframe->GetXaxis()->SetTitleOffset(1.2);
       xframe->GetYaxis()->SetTitleOffset(1.6);
       gStyle->SetOptFit(1111);
       //TCanvas *canvas1 = new TCanvas();
       //xframe->GetYaxis()->SetRangeUser(1,yaxis[mag+qual]);
       //xframe->GetYaxis()->SetRangeUser(1,30000); // Better when logy
       xframe->Draw();
       DrawPrelimLabel(canvas1);
       DrawLumiLabel(canvas1);//, ageingTag);

      TLatex tex;
      tex.SetTextSize(0.03);
      tex.DrawLatexNDC(0.76,0.87, (whTag + " " + chambTag).c_str());//typically for Phase-2
      tex.Draw("same");

      TLatex latex;
      sprintf(name, "#sigma = %.1f %s", coreSigma, units[mag].c_str());
      // sprintf(name, "%s\n#sigma = %.1f %s", ageingTag.c_str(), coreSigma, units[mag].c_str());
      // sprintf(name, "#sigma = (%.2f#pm%.2f) %s", coreSigma, coreSigmaError, units[mag].c_str());
      latex.SetTextSize(0.03);
      // latex.DrawLatexNDC(0.7, 0.6, name);
      // latex.Draw("same");

      char ageTitle[128];
      sprintf(ageTitle, "#font[22]{%s}", ageingTag.c_str());

      auto leg = new TLegend(0.65, 0.6, 0.85, 0.7);
      leg->SetHeader(ageTitle, "C");
      leg->AddEntry((TObject*)0, name, "");
      leg->SetBorderSize(0);
      leg->Draw("same");

  //double xPosition = 0.;
       double xPosition = ranges[mag+qual] / 10.;
       //double xPosition = hResSlope4h1->GetXaxis()->GetXmax() / 10.;

/*
       nameFile = "Fraction = "+std::to_string(fraction.getVal());
       sprintf(name,"%s",nameFile.c_str());
       //latex.DrawLatex(xPosition,5000,name);
       nameFile = "Fraction2 = "+std::to_string(fraction2.getVal());
       sprintf(name,"%s",nameFile.c_str());
       //latex.DrawLatex(xPosition,7500,name);
       if (mag == "PhiRes" || mag == "PhiBRes" || mag == "TanPsiRes") {
         nameFile = "Mean = "+std::to_string(mean.getVal()*1000);
         sprintf(name,"%s mrad",nameFile.c_str());
         //latex.DrawLatex(xPosition,3000,name);
         nameFile = "#sigma_{1} = "+std::to_string(sigma1.getVal()*1000. );
         sprintf(name,"%s mrad",nameFile.c_str());
         //latex.DrawLatex(xPosition,2000,name);
         nameFile = "#sigma_{2} = "+std::to_string(sigma2.getVal()*1000.);
         sprintf(name,"%s mrad",nameFile.c_str());
         latex.DrawLatex(xPosition,1200,name);
         nameFile = "#sigma_{3} = "+std::to_string(sigma3.getVal()*1000.);
         sprintf(name,"%s mrad",nameFile.c_str());
         //latex.DrawLatex(xPosition,800,name);
       } else if (mag == "TimeRes") {
         nameFile = "Mean = "+std::to_string(mean.getVal());
         sprintf(name,"%s ns",nameFile.c_str());
         latex.DrawLatex(xPosition,3000,name);
         nameFile = "#sigma_{1} = "+std::to_string(sigma1.getVal() );
         sprintf(name,"%s ns",nameFile.c_str());
         latex.DrawLatex(xPosition,2000,name);
         nameFile = "#sigma_{2} = "+std::to_string(sigma2.getVal());
         sprintf(name,"%s ns",nameFile.c_str());
         latex.DrawLatex(xPosition,1200,name);
         nameFile = "#sigma_{3} = "+std::to_string(sigma3.getVal());
         sprintf(name,"%s ns",nameFile.c_str());
         latex.DrawLatex(xPosition,800,name);
       } else {
         nameFile = "Mean = "+std::to_string(mean.getVal());
         sprintf(name,"%s cm",nameFile.c_str());
         latex.DrawLatex(xPosition,3000,name);
         nameFile = "#sigma_{1} = "+std::to_string(sigma1.getVal() );
         sprintf(name,"%s cm",nameFile.c_str());
         latex.DrawLatex(xPosition,2000,name);
         nameFile = "#sigma_{2} = "+std::to_string(sigma2.getVal());
         sprintf(name,"%s cm",nameFile.c_str());
         latex.DrawLatex(xPosition,1200,name);
         nameFile = "#sigma_{3} = "+std::to_string(sigma3.getVal());
         sprintf(name,"%s cm",nameFile.c_str());
         latex.DrawLatex(xPosition,800,name);

       }
*/
       sprintf(name,"summaryPlots/%s/%s/%s.png",file.c_str(), qual.c_str(), namePlot.c_str());
       //canvas1->SetLogy();
       outPlots.cd();
       gPad->SetName(namePlot.c_str());
       gPad->SaveAs(name);
       gPad->Write();
       sprintf(name,"summaryPlots/%s/%s/%s.pdf",file.c_str(), qual.c_str(), namePlot.c_str());
       //canvas1->SetLogy();
       outPlots.cd();
       gPad->SetName(namePlot.c_str());
       gPad->SaveAs(name);



    }
    outPlots.cd();
    m_plots[mag + "AM" + qual + whTag] -> Write();
    sprintf(name,"summaryPlots/%s/%s/h%s_AM_%s_%s.png",file.c_str(),qual.c_str(),mag.c_str(), qual.c_str(), whTag.c_str());
    TCanvas *canvas1 = new TCanvas();
    m_plots[mag + "AM" + qual + whTag] -> Draw();
    canvas1 -> SaveAs(name);
    sprintf(name,"summaryPlots/%s/%s/h%s_AM_%s_%s.pdf",file.c_str(),qual.c_str(),mag.c_str(), qual.c_str(), whTag.c_str());
    canvas1 -> SaveAs(name);
  }
} //magnitudes
} //qualTags

outPlots.Close();


}
