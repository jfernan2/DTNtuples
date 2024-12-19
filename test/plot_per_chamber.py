import itertools
import ROOT
ROOT.gROOT.SetBatch(True)
chambTags = [ "MB1", "MB2", "MB3", "MB4"]
whTags    = [ "Wh-2", "Wh-1", "Wh0", "Wh+1", "Wh+2"]
secTags   = [ "Sec1", "Sec2", "Sec3", "Sec4", "Sec5", "Sec6", "Sec7", "Sec8","Sec9","Sec10","Sec11","Sec12","Sec13","Sec14"]

mag = "xRes"
qual = "All"
folder = "./distributions/"
input_file = "/eos/user/j/jfernan/L1T/ntuplesResults/results_resols_rossin_noRPC_noAgeing_alignTrue_.root"
file = ROOT.TFile.Open(input_file)

histos = {}

mean_limits = {
    "xRes": (-0.05, 0.05)
}

for tag in secTags + whTags + chambTags:
    histos[tag] = ROOT.TH1F("h%s_AM%s_%s" % (mag, qual, tag), "; Mean; ", 20, mean_limits[mag][0], mean_limits[mag][1])


for (whTag, secTag, chambTag) in itertools.product(whTags, secTags, chambTags):
    namePlot = "h" + mag + "_" + "AM" + qual + "_" + whTag + "_" + chambTag + "_" + secTag + "_P2"
    plot = file.Get(namePlot).Clone()

    histos[secTag].Fill(plot.GetMean())
    histos[whTag].Fill(plot.GetMean())
    histos[chambTag].Fill(plot.GetMean())

    c = ROOT.TCanvas()
    plot.Draw()
    #c.SaveAs(folder + "/" + namePlot + ".pdf")
    #c.SaveAs(folder + "/" + namePlot + ".png")

ROOT.gStyle.SetOptStat(111111)
for tag in secTags + whTags + chambTags:
    c = ROOT.TCanvas()
    histos[tag].Draw()

    namePlot = "h%s_mean_AM%s_%s" % (mag, qual, tag)
    c.SaveAs(folder + "/" + namePlot + ".pdf")
    c.SaveAs(folder + "/" + namePlot + ".png")
