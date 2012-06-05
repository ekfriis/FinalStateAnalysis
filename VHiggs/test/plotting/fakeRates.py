'''

Measure jet->mu, jet->e, and jet->tau fake rates in trilepton event topologies.

'''

import copy
import logging
import os
import re
import sys

import ROOT
import FinalStateAnalysis.PatTools.data as data_tool

# Logging options
logging.basicConfig(filename='fakeRates.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("fakerates")
h1 = logging.StreamHandler(sys.stdout)
h1.level = logging.INFO
log.addHandler(h1)

ROOT.gROOT.SetBatch(True)
canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

# Dimuon selection
base_dimuon_selection = [
    #'(run < 5 && m1Pt > 13.5 || m1Pt > 13.365)',
    #'(run < 5 && m2Pt > 9 || m2Pt > 8.91)',
    'm1Pt > 18',
    'm2Pt > 9',
    'm1AbsEta < 2.1',
    'm2AbsEta < 2.1',
    'm1RelPFIsoDB < 0.15',
    'm2RelPFIsoDB < 0.15',
    'm1PFIDTight > 0.5',
    'm2PFIDTight > 0.5',
    'muVetoPt5 < 0.5',
    'bjetCSVVeto < 1', # Against ttbar
    'doubleMuPass > 0.5 ',
    #'(m1_hltDiMuonL3PreFiltered7 | m2_hltDiMuonL3p5PreFiltered8 |'
        #'m1_hltSingleMu13L3Filtered13)',
    #'(m2_hltDiMuonL3PreFiltered7 | m2_hltDiMuonL3p5PreFiltered8)',
    'm1Charge*m2Charge < 0',
    'metEt < 30',
    'abs(m1DZ) < 0.2',
    'abs(m2DZ) < 0.2',
]

base_qcd_selection = [
    'm1Pt > 18',
    'm2Pt > 9',
    'm1AbsEta < 2.1',
    'm2AbsEta < 2.1',
    'm1RelPFIsoDB > 0.5',
    'm1PFIDTight > 0.5',
    'muVetoPt5 < 1',
    #'bjetCSVVeto > 0', # For ttbar
    'doubleMuPass > 0.5 ',
    'm1Charge*m2Charge > 0', # Same sign (to kill DY)
    'abs(m1DZ) < 0.2',
    'abs(m2DZ) < 0.2',
    'tLooseMVAIso < 0.5',
    'abs(m1DZ) < 0.2',
    'abs(m2DZ) < 0.2',
    'abs(tDZ) < 0.2',
]

base_qcd_for_taus_selection = [
    'm1Pt > 18',
    'm2Pt > 9',
    'm1AbsEta < 2.1',
    'm2AbsEta < 2.1',
    'm1RelPFIsoDB > 0.5',
    'm2RelPFIsoDB > 0.5',
    'muVetoPt5 < 1',
    #'bjetCSVVeto > 0', # For ttbar
    'doubleMuPass > 0.5 ',
    'abs(m1DZ) < 0.2',
    'abs(m2DZ) < 0.2',
]

# Stupid names are different, fix this
base_dimuon_emm = [
    x.replace('m1', 'Mu1').replace('m2', 'Mu2')
    for x in base_dimuon_selection
]

# Version where we trigger on the MuEG
base_dimuon_emm_MuEG = [
    x.replace('doubleMuPass', 'Mu17Ele8All_HLT') for x in base_dimuon_emm
]


fakerates = {
    'tau' : {
        'ntuple' : 'mmt',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'Zjets',
        'varname' : 'tJetPt',
        'vartitle' : 't Jet p_{T}',
        'var' : 'tJetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_selection,
        'control_plots' : [
        ],
        'final_cuts' : [],
        'denom' : [
            'm1_m2_Mass > 86',
            'm1_m2_Mass < 95',
            't_MtToMET < 40',
            'tPt > 20',
            'tAbsEta < 2.3',
            'tDecayFinding > 0.5',
            'abs(tDZ) < 0.2',
        ],
        'num' : [
            'tLooseMVAIso > 0.5'
        ],
    },
    'tauQCD' : {
        'ntuple' : 'mmt',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'Zjets',
        'varname' : 'tJetPt',
        'vartitle' : 't Jet p_{T}',
        'var' : 'tJetPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_qcd_for_taus_selection,
        'control_plots' : [
        ],
        'final_cuts' : [],
        'denom' : [
            'tPt > 20',
            'tAbsEta < 2.3',
            'tDecayFinding > 0.5',
            'metEt < 30',
            'abs(tDZ) < 0.2',
        ],
        'num' : [
            'tLooseMVAIso > 0.5'
        ],
    },
    'tauTauPt' : {
        'ntuple' : 'mmt',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'Zjets',
        'varname' : 'tPt',
        'vartitle' : 't p_{T}',
        'var' : 'tPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_selection,
        'control_plots' : [
        ],
        'final_cuts' : [],
        'denom' : [
            'm1_m2_Mass > 86',
            'm1_m2_Mass < 95',
            't_MtToMET < 40',
            'tPt > 20',
            'tAbsEta < 2.3',
            'tDecayFinding > 0.5',
            'abs(tDZ) < 0.2',
        ],
        'num' : [
            'tLooseMVAIso > 0.5'
        ],
    },
    'tauQCDTauPt' : {
        'ntuple' : 'mmt',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'Zjets',
        'varname' : 'tPt',
        'vartitle' : 't p_{T}',
        'var' : 'tPt',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_qcd_for_taus_selection,
        'control_plots' : [
        ],
        'final_cuts' : [],
        'denom' : [
            'tPt > 20',
            'tAbsEta < 2.3',
            'tDecayFinding > 0.5',
            'metEt < 30',
            'abs(tDZ) < 0.2',
        ],
        'num' : [
            'tLooseMVAIso > 0.5'
        ],
    },
    'mu' : {
        'ntuple' : 'mmm',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'Zjets',
        'varname' : 'MuJetPt',
        'var' : 'm3_JetPt',
        'vartitle' : 'Mu Jet p_{T}',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_selection,
        'control_plots' : [
        ],
        'final_cuts' : [],
        'denom' : [
            'm3_hltDiMuonL3p5PreFiltered8 > 0.5',
            'm3PixHits > 0.5',
            'm3JetBtag < 3.3',
            'm3Pt > 10',
            'm3AbsEta < 2.1',
            'm1_m2_Mass > 85',
            'm1_m2_Mass < 95',
            'm3_MtToMET < 20',
            'abs(m3DZ) < 0.2',
        ],
        'num' : [
            'm3PFIDTight > 0.5',
            'm3RelPFIsoDB < 0.3',
        ]
    },
    'muQCD' : {
        'ntuple' : 'mmt',
        'pd' : 'data_DoubleMu',
        'exclude' : ['*DoubleE*', '*MuEG*'],
        'mc_pd' : 'QCDMu',
        'varname' : 'MuJetPt',
        'var' : 'm2_JetPt',
        'vartitle' : 'Mu Jet p_{T}',
        'varbinning' : [100, 0, 100],
        'rebin' : 10,
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_qcd_selection,
        'control_plots' : [],
        'final_cuts' : [],
        'denom' : [
            'm2PixHits > 0.5',
            'm2JetBtag < 3.3',
            'm2AbsEta < 2.5',
            'm2Pt > 10',
            'metEt < 20',
            'abs(m2DZ) < 0.2',
        ],
        'num' : [
            'm2PFIDTight > 0.5',
            'm2RelPFIsoDB < 0.3',
        ]
    },
    'eMuEG' : {
        'ntuple' : 'emm',
        'pd' : 'data_MuEG',
        'exclude' : ['*DoubleE*', '*DoubleMu*'],
        'mc_pd' : 'Zjets',
        'varname' : 'EJetPt',
        'var' : 'Elec_JetPt',
        'vartitle' : 'Electron Jet p_{T}',
        'varbinning' : [100, 0, 100],
        'rebin' : 5,
        'evtType' : '#mu#mu + jet',
        'base_cuts' : base_dimuon_emm_MuEG,
        'control_plots' : [],
        'final_cuts' : [],
        'denom' : [
            'Mu17Ele8All_HLT > 0.5',
            'ElecPt > 10',
            'ElecAbsEta < 2.5',
            'Mu1_Mu2_Mass > 86',
            'Mu1_Mu2_Mass < 95',
            'Elec_MtToMET < 30',
            'Elec_EBtag < 3.3',
            'Elec_MissingHits < 0.5',
            'Elec_hasConversion < 0.5',
            'abs(ElecDZ) < 0.2',
            'NIsoElecPt10_Nelectrons < 0.5',
        ],
        'num' : [
            'Elec_EID_MITID > 0.5',
            'Elec_ERelIso < 0.3',
        ]
    },
}

# Hack to split by eta
varname_extractor = re.compile('(?P<var>\w+)AbsEta\s*<\s*[0-9\.]+')
for fr in list(fakerates.keys()):
    # For now, skip the eat split
    continue
    info = fakerates[fr]
    barrel_info_clone = copy.deepcopy(info)
    endcap_info_clone = copy.deepcopy(info)
    # Figure out variable name
    varname = None
    for cut in info['denom']:
        match = varname_extractor.match(cut)
        if match:
            varname = match.group('var')
    assert(varname)
    barrel_info_clone['denom'].append('%sAbsEta <= 1.48' % varname)
    endcap_info_clone['denom'].append('%sAbsEta > 1.48' % varname)
    fakerates[fr + '_endcap'] = endcap_info_clone
    fakerates[fr + '_barrel'] = barrel_info_clone

output_file = ROOT.TFile("results_fakeRates.root", "RECREATE")
for data_set, skips, int_lumi in [
    #('2011A', ['2011B', 'EM', 'DoubleE'], 2170),
    #('2011B', ['2011A', 'v1_d', 'EM'], 2170),
    ('2011AB', ['EM', 'DoubleE', 'ZZ'], 4900)]:
    log.info("Plotting dataset: %s", data_set)

    samples, plotter = data_tool.build_data(
        'VH', '2012-06-03-7TeV-Higgs', 'scratch_results',
        int_lumi, skips, count='emt/skimCounter')

    legend = plotter.build_legend(
        '/emt/skimCounter',
        include = ['*'],
        exclude = ['*data*','*VH*'],
        drawopt='lf')

    def saveplot(filename):
        # Save the current canvas
        filetype = '.pdf'
        #legend.Draw()
        canvas.SetLogy(False)
        canvas.Update()
        canvas.Print(os.path.join(
            "plots", 'fakeRates', data_set, filename + filetype))
        canvas.SetLogy(True)
        canvas.Update()
        canvas.Print(os.path.join(
            "plots", 'fakeRates', data_set, filename + '_log' + filetype))


    for fr_type, fr_info in fakerates.iteritems():
        log.info("Plotting fake rate type: %s", fr_type)
        # Draw the Z-mumu mass
        denom_selection_list = \
                fr_info['base_cuts'] + fr_info['denom']
        denom_selection = " && ".join(denom_selection_list)

        num_selection_list = denom_selection_list + fr_info['num']
        num_selection = ' && '.join(num_selection_list)

        weight = '(pu2011AB)'

        # List of final plots to make
        to_plot = [
            (fr_type + 'Num' + fr_info['varname'], '%s mass (tight)' % fr_info['vartitle'], fr_info['vartitle'], fr_info['rebin']),
            (fr_type + 'Denom' + fr_info['varname'], '%s mass (loose)' % fr_info['vartitle'], fr_info['vartitle'], fr_info['rebin']),
        ]

        for label, var, title, binning in fr_info['control_plots']:
            log.info("Plotting control plot %s", label)
            plotter.register_tree(
                fr_type + label + 'Denom',
                '/%s/final/Ntuple' % fr_info['ntuple'],
                var,
                denom_selection,
                w = weight,
                binning = binning,
                include = ['*'],
                exclude = fr_info['exclude'],
            )

            plotter.register_tree(
                fr_type + label + 'Num',
                '/%s/final/Ntuple' % fr_info['ntuple'],
                var,
                num_selection,
                w = weight,
                binning = binning,
                include = ['*'],
                exclude = fr_info['exclude'],
            )
            to_plot.append(
                (fr_type + label + 'Denom', "%s (loose)" % title, title, 1)
            )
            to_plot.append(
                (fr_type + label + 'Num', "%s (tight)" % title, title, 1)
            )

        # Add the final cuts in
        denom_selection_list += fr_info['final_cuts']
        denom_selection = " && ".join(denom_selection_list)

        num_selection_list += fr_info['final_cuts']
        num_selection = ' && '.join(num_selection_list)

        plotter.register_tree(
            fr_type + 'Denom' + fr_info['varname'],
            '/%s/final/Ntuple' % fr_info['ntuple'],
            fr_info['var'],
            denom_selection,
            w = weight,
            binning = fr_info['varbinning'],
            include = ['*'],
            exclude = fr_info['exclude'],
        )

        plotter.register_tree(
            fr_type + 'Num' + fr_info['varname'],
            '/%s/final/Ntuple' % fr_info['ntuple'],
            fr_info['var'],
            num_selection,
            w = weight,
            binning = fr_info['varbinning'],
            include = ['*'],
            exclude = fr_info['exclude'],
        )

        # Make plots
        for name, title, xtitle, rebin in to_plot:

            stack = plotter.build_stack(
                '/%s/final/Ntuple:%s' % (fr_info['ntuple'], name),
                include = ['*'],
                exclude = ['*data*'],
                title = title,
                show_overflows = True,
                rebin = rebin,
            )
            data = plotter.get_histogram(
                fr_info['pd'],
                '/%s/final/Ntuple:%s' % (fr_info['ntuple'], name),
                show_overflows = True,
                rebin = rebin,
            )
            stack.Draw()
            stack.GetXaxis().SetTitle(xtitle)
            data.Draw("pe, same")
            legend.Draw()
            stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)
            stack.GetHistogram().SetTitle(
                 xtitle + ' in ' + fr_info['evtType'] + ' events')

            saveplot(fr_type + '_' + name)

        # Make efficiency curve
        data_num = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Num' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )

        data_denom = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Denom' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )

        mc_num = plotter.get_histogram(
            fr_info['mc_pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Num' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )

        mc_denom = plotter.get_histogram(
            fr_info['mc_pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Denom' + fr_info['varname']),
            show_overflows = True,
            rebin = fr_info['rebin'],
        )

        frame = ROOT.TH1F("frame",
                          'Fake rate in ' + fr_info['evtType'] + ' events',
                          100, 0, 100)
        frame.GetXaxis().SetTitle(fr_info['vartitle'])
        frame.SetMinimum(1e-3)
        frame.SetMaximum(1.0)

        data_curve = ROOT.TGraphAsymmErrors(data_num.th1, data_denom.th1)
        data_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
        data_fit_func.SetParameter(0, 0.02)
        data_fit_func.SetParLimits(0, 0.0, 1)
        data_fit_func.SetParameter(1, 1.87)
        data_fit_func.SetParameter(2, -9.62806e-02)
        data_fit_func.SetLineColor(ROOT.EColor.kBlack)
        data_curve.Fit(data_fit_func)

        mc_curve = ROOT.TGraphAsymmErrors(mc_num.th1, mc_denom.th1)
        mc_curve.SetMarkerColor(ROOT.EColor.kRed)
        mc_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
        mc_fit_func.SetParameter(0, 0.02)
        mc_fit_func.SetParLimits(0, 0.0, 1)
        mc_fit_func.SetParameter(1, 1.87)
        mc_fit_func.SetParameter(2, -9.62806e-02)
        mc_fit_func.SetLineColor(ROOT.EColor.kRed)
        mc_curve.Fit(mc_fit_func)

        canvas.Clear()
        multi = ROOT.TMultiGraph("fake_rates", "Fake Rates")
        multi.Add(mc_curve, "pe")
        multi.Add(data_curve, "pe")

        frame.Draw()
        multi.Draw("pe")

        data_fit_func.Draw('same')
        mc_fit_func.Draw('same')
        saveplot(fr_type + "_fakerate")

        # Make efficiency curve
        data_num = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Num' + fr_info['varname']),
            show_overflows = True,
        )

        data_denom = plotter.get_histogram(
            fr_info['pd'],
            '/%s/final/Ntuple:%s' % (
                fr_info['ntuple'], fr_type + 'Denom' + fr_info['varname']),
            show_overflows = True,
        )
        output_file.cd()
        data_denom.Write("_".join([data_set, fr_type, 'data_denom']))
        data_num.Write("_".join([data_set, fr_type, 'data_num']))
