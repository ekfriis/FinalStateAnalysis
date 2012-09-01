import ROOT
import glob
import FinalStateAnalysis.StatTools.limitplot as limitplot

gg_limit = limitplot.get_limit_info(glob.glob("combo/ind_gg*.cls.json"))
tt_limit = limitplot.get_limit_info(glob.glob("combo/ind_leptonic_tt*.cls.json"))
zh_limit = limitplot.get_limit_info(glob.glob("combo/ind_leptonic_zh*.cls.json"))
ww_limit = limitplot.get_limit_info(glob.glob("combo/ind_leptonic_ww*.cls.json"))
bb_limit = limitplot.get_limit_info(glob.glob("combo/ind_bb*.cls.json"))
combo_limit = limitplot.get_limit_info(glob.glob("combo/comb_all*.cls.json"))

canvas = ROOT.TCanvas("c", "c", 800, 800)
canvas.SetRightMargin(0.05)
canvas.SetLeftMargin(1.1*canvas.GetLeftMargin())

masses = range(110, 150) + range(150, 210, 10)
frame = ROOT.TH1F("frame", "frame", 1, masses[0], masses[-1])

frame.GetYaxis().SetTitle("95% CL upper limit on #sigma/#sigma_{SM}")
frame.GetXaxis().SetTitle("m_{H} (GeV)")
frame.SetMaximum(100)
frame.SetMinimum(0.8)
canvas.SetLogy(True)
canvas.SetGridx(1)
canvas.SetGridy(1)

graphs = {
    'gg' : {'c' : 2, 'label' : 'V#gamma#gamma', 'd' : gg_limit},
    'tt' : {'c' : 4, 'label' : '2l#tau_{h}', 'd' : tt_limit},
    'zh' : {'c' : 8, 'label' : '4L', 'd' : zh_limit},
    'ww' : {'c' : 6, 'label' : '3l', 'd' : ww_limit},
    'bb' : {'c' : ROOT.EColor.kAzure+7, 'label' : 'Vbb', 'd' : bb_limit},
    'comb' : {'c' : 1, 'label' : 'Combination', 'd' : combo_limit},
}


legend = ROOT.TLegend(0.53, 0.71, 0.93, 0.93, "", "brNDC")
#legend = ROOT.TLegend(0.20+0.31, 0.15+0.07, 0.6+0.31, 0.37+0.07, "", "brNDC")
legend.SetBorderSize(1)
legend.SetFillStyle(1001)
legend.SetFillColor(0)

width = 2
exp_style = 2

frame.Draw()

import FinalStateAnalysis.Utilities.styling as styling
cms_label = styling.cms_preliminary(
    5000,
    is_preliminary=False,
    lumi_on_top = True,
)
cms_label.Draw()

for type in ['comb', 'zh', 'tt', 'ww', 'gg', 'bb']:
    graphs[type]['exp'] = limitplot.build_exp_line(graphs[type]['d'], ('cls', ''))
    graphs[type]['obs'] = limitplot.build_obs_line(graphs[type]['d'], ('cls', ''))
    color = graphs[type]['c']
    graphs[type]['exp'].SetLineWidth(width)
    graphs[type]['exp'].SetLineStyle(exp_style)
    graphs[type]['exp'].SetLineColor(color)
    graphs[type]['obs'].SetLineWidth(width)
    graphs[type]['obs'].SetLineColor(color)

    graphs[type]['exp'].Draw()
    graphs[type]['obs'].Draw()

    if type == 'comb':
        legend.AddEntry(graphs[type]['obs'], "Combined observed", "l")
        legend.AddEntry(graphs[type]['exp'], "Combined expected", "l")
    else:
        legend.AddEntry(graphs[type]['obs'], graphs[type]['label'], "l")

legend.Draw()
canvas.SaveAs("limit_comparison.pdf")
