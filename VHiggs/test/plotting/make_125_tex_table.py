
import FinalStateAnalysis.StatTools.limitplot as limitplot
import sys

gg_limit = limitplot.get_limit_info(["combo/ind_gg_125.cls.json"])
tt_limit = limitplot.get_limit_info(["combo/ind_leptonic_tt_125.cls.json"])
zh_limit = limitplot.get_limit_info(["combo/ind_leptonic_zh_125.cls.json"])
ww_limit = limitplot.get_limit_info(["combo/ind_leptonic_ww_125.cls.json"])
bb_limit = limitplot.get_limit_info(["combo/ind_bb_125.cls.json"])
combo_limit = limitplot.get_limit_info(["combo/comb_all_125.cls.json"])

print gg_limit


sys.stdout.write(
    ' & '.join(['Channel', '-2$\\sigma$', '-1$\\sigma$', 'Expected',
                '+1$\\sigma$', '+2$\\sigma$', 'Observed']) + '\\\\\n'
)

template = ' & '.join([
    '{channel:20s}',
    '{-2:5.2f}', '{-1:5.2f}', '{exp:5.2f}', '{+1:5.2f}',
    '{+2:5.2f}', '{obs:5.2f}']) + '\\\\\n'


for channel, data in [
    ('$3\\ell$', ww_limit),
    ('$2\\ell\\tau_h$', ww_limit),
    ('$4L$', zh_limit),
    ('$\gamma\gamma$', gg_limit),
    ('$\\bbbar$', bb_limit)]:

    sys.stdout.write(template.format(channel=channel,
        **data.values()[0][125]))

sys.stdout.write('\\hline')
sys.stdout.write(template.format(channel='Combined',
        **combo_limit.values()[0][125]))
