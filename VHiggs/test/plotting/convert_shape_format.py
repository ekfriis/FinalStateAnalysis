import ROOT
import sys

input = ROOT.TFile('wh_shapes_raw.root')
output = ROOT.TFile('vhtt_llt_shapes.root', "RECREATE")

mmt_out = output.mkdir('mmt')
emt_out = output.mkdir('emt')

mmt_in = input.Get('mmt_mumu_final_MuTauMass')
emt_in = input.Get("emt_emu_final_SubleadingMass")

for sample in ['WZ', 'ZZ', 'tribosons', 'data_obs', 'fakes']:
    mmt_shape = mmt_in.Get(sample)
    mmt_out.cd()
    mmt_shape.Write()

    emt_shape = emt_in.Get(sample)
    emt_out.cd()
    emt_shape.Write()

for mass in range(110, 165, 5):
    if mass == 155:
        continue
    for indir, outdir in [(mmt_in, mmt_out),
                          (emt_in, emt_out)]:
        vh = indir.Get('VH%i' % mass).Clone()
        vhww = indir.Get('VH_hww%i' % mass).Clone()
        outdir.cd()
        vh.Write()
        vhww.Write()

