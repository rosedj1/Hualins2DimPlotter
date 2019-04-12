#!/bin/bash
#####################################################################################################
## PURPOSE: A general-use 2-D histo plotter.
## SYNTAX:  <script.py> -t <tag_name>
## NOTES:   The <tag_name> is defined as a "small dictionary" in plot_paraConfigurations_2D.py.
##          It contains all the plotting parameters that go into the 2-D plot.
##          
## AUTHOR:  Hualin Mei, modified by Jake Rosenzweig
## DATE:    2019-04-10
## UPDATED: 2019-04-11
#####################################################################################################

#____________________________________________________________________________________________________
# User Parameters
from ROOT import *
from array import array

from tdrStyle import *
setTDRStyle()
ROOT.gROOT.SetBatch(kTRUE)

from paraConfigurations_2D import *

import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('-t', dest='tag', type=str, help='for each plot')
# Example tags from plot_paraConfigurations_2D.py
# DY_MC2016_e_eta1_eta2_ifMassZErr_2_3
# mass4lErr_reco_refit_2e2mu
# Z4L_mu_eta_pt
# H4L_mu_residual_pt_eta_0p9_1p4
# mass4l_massZ2_2016Data
# pTErr_eta_2016_mu_mc_0p9
# pTErr_pT_eta_0p9_data
# pT1Err_eta1_eta_0p2_data
# ...and many more examples
    args = parser.parse_args()
    return args

args=ParseOption()

tag = args.tag
paraConfig = paraConfigs[tag] # tag is key; unlocks value which is a small dictionary

# Import the values from the predefined small dictionary found in plot_paraConfigurations_2D.py
rootPath1 = paraConfig['rootPath1'] 
#rootPath2 = paraConfig['rootPath2']
rootfile1 = paraConfig['rootfile1']
#rootfile2 = paraConfig['rootfile2']
tree1 = paraConfig['tree1']
#tree2 = paraConfig['tree2']
binInfo_x = paraConfig['binInfo_x']
binInfo_y = paraConfig['binInfo_y']
vars1_x = paraConfig['vars1_x']
vars1_y = paraConfig['vars1_y']
#vars2_x = paraConfig['vars2_x']
#vars2_y = paraConfig['vars2_y']
cuts1 = paraConfig['cuts1']
#cuts2 = paraConfig['cuts2']
weight1 = paraConfig['weight1']
#weight2 = paraConfig['weight2']
xTitle = paraConfig['xTitle']
yTitle = paraConfig['yTitle']
#legend1 = paraConfig['legend1']
#legend2 = paraConfig['legend2']
savePath = paraConfig['savePath']
saveName = paraConfig['saveName']
if 'doLogZ' in paraConfig:
   doLogZ = paraConfig['doLogZ']
latexNote1 = paraConfig['latexNote1']
#latexNote2 = paraConfig['latexNote2']

f1 = TFile(rootPath1 + rootfile1, 'READ')
#f2 = TFile(rootPath2 + rootfile2, 'READ')
t1 = f1.Get(tree1)
#t2 = f2.Get(tree2)

# Prepare empty 2D histo for each vars 
# hists1 is a list of histos
hists1 = [ TH2F('hist1_'+str(i), '',binInfo_x[0], 
                                    binInfo_x[1], 
                                    binInfo_x[2], 
                                    binInfo_y[0], 
                                    binInfo_y[1], 
                                    binInfo_y[2]) for i in range(len(vars1_x)) ]
#hists2 = [ TH1F('hist2_'+str(i),'', binInfo[0], binInfo[1], binInfo[2]) for i in range(len(vars2)) ]

#HIST1 = TH2F('HIST1', '', binInfo_x[0], 
#                          binInfo_x[1], 
#                          binInfo_x[2], 
#                          binInfo_y[0], 
#                          binInfo_y[1], 
#                          binInfo_y[2])
#HIST2 = TH1F('HIST2', '', binInfo[0], binInfo[1], binInfo[2])

# Make 2-D projection of tree into histo. 
for i in range(len(vars1_x)):
    t1.Project(hists1[i].GetName(), vars1_y[i]+':'+vars1_x[i], weight1[i]+"*("+cuts1[i]+")")
    if i == 0:
       HIST1 = hists1[0].Clone()
    else:
       HIST1.Add(hists1[i])
'''
for i in range(len(vars2)):
    t2.Project(hists2[i].GetName(), vars2[i], weight2[i]+"*"+cuts2[i])
    if i == 0:
       HIST2 = hists2[0].Clone()
    else:
       HIST2.Add(hists2[i])
'''

#HIST1.Scale(1/HIST1.Integral())
#HIST2.Scale(1/HIST2.Integral())

c1 = TCanvas("c1", "c1", 800, 800)
if 'doLogZ' in paraConfig:
  if doLogZ:
   c1.SetLogz()
c1.SetGrid()
c1.SetTopMargin(0.1)
c1.SetLeftMargin(0.15)
c1.SetRightMargin(0.15)
dummy = TH2D("dummy","dummy",1, binInfo_x[1], binInfo_x[2], 1, binInfo_y[1], binInfo_y[2])
HIST1.SetMinimum(0)
dummy.SetMinimum(0)
#yMax1 = HIST1.GetMaximum()*1.5
#yMax2 = HIST2.GetMaximum()*1.5
#yMax = max(yMax1,yMax2)
#dummy.SetMaximum(0.1)
dummy.SetLineColor(0)
dummy.SetMarkerColor(0)
dummy.SetLineWidth(0)
dummy.SetMarkerSize(0)
dummy.GetYaxis().SetTitle(yTitle)
dummy.GetYaxis().SetTitleOffset(1.3)
dummy.GetXaxis().SetTitle(xTitle)
dummy.Draw()

HIST1.Scale(1/HIST1.Integral())
HIST1.Draw('COLZ1 same')
#HIST1.Draw('COLZ2 same')
#print HIST1.GetCorrelationFactor(1,2)
#print HIST1.GetCovariance(1,2)
#print 'x', HIST1.GetMean(1), HIST1.GetStdDev(1)
#print 'y', HIST1.GetMean(1), HIST1.GetStdDev(2)

#HIST1.SetMaximum(0.008)
#HIST2.Draw('hist same')

#HIST1.SetLineColor(1)
#HIST2.SetLineColor(2)
#HIST1.SetLineWidth(1)
#HIST2.SetLineWidth(1)

legend = ROOT.TLegend(0.15,0.75,0.42,0.9)
#legend.AddEntry(HIST1, legend1, 'l')
#legend.AddEntry(HIST2, legend2, 'l')
legend.SetTextSize(0.03)
legend.SetLineWidth(2)
legend.SetFillColor(0)
legend.SetBorderSize(1)
#legend.Draw('SAME')

latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.3*c1.GetTopMargin())
latex.SetTextFont(42)
latex.SetTextAlign(11)
latex.DrawLatex(0.45, 0.85, latexNote1)
#if len(latexNote2) > 0:
#   latex.DrawLatex(0.45, 0.75, latexNote2)
c1.SetGrid()
HIST1.Draw('COLZ1 same')
#c1.Update()
c1.SaveAs(savePath+saveName+'.png')
c1.SaveAs(savePath+saveName+'.pdf')

with open(savePath + saveName + ".txt", "w") as myfile:
   myfile.write('rootPath: ' + rootPath1 + '\n')
   myfile.write('rootfile: ' + rootfile1 + '\n')
   for i in range(len(vars1_x)):
       myfile.write('var_x: ' + vars1_x[i] + '\n')
       myfile.write('var_y: ' + vars1_y[i] + '\n')
       myfile.write('cut: ' + cuts1[i] + '\n')
myfile.close()
