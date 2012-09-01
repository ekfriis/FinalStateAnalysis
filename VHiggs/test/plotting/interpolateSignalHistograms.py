#!/usr/bin/env python

'''

Take the shape files and produce additional histograms using horizontal
interpolation.

Author: Evan K. Friis, UW Madison

'''

import bisect
import logging
import os
import pprint
import re
import sys

log = logging.getLogger("statshapes")
logging.basicConfig(level=logging.DEBUG)

from FinalStateAnalysis.StatTools.morph import morph
from rootpy.io import open, cp, rm, DoesNotExist

def find_all_keys(f):
    ''' Find all folders (and corresponding masses)

    Assumes (true now) that all keys have the same masses

    '''

    folders = set([])
    vhtt_masses = set([])
    vhww_masses = set([])

    for thing in f.walk(class_pattern='TH1*'):
        path, subdirs, histos = thing
        log.info("==> examining directory %s", path)
        if not histos:
            continue
        folders.add(path)

        vhtt_re = re.compile('VH(?P<mass>[0-9]+)$')
        vhww_re = re.compile('VH_hww(?P<mass>[0-9]+)$')
        for histo in histos:
            ttmatch = vhtt_re.match(histo)
            if ttmatch:
                log.info("==> found tautau histo %s", histo)
                vhtt_masses.add(int(ttmatch.group('mass')))
            wwmatch = vhww_re.match(histo)
            if wwmatch:
                log.info("==> found WW histo %s", histo)
                vhww_masses.add(int(wwmatch.group('mass')))

    return folders, vhtt_masses, vhww_masses

def find_best_interp_points(target, existing):
    sorted_existing = sorted(existing)
    insert_index = bisect.bisect_left(sorted_existing, target)
    if insert_index == 0:
        print sorted_existing
        print sorted_existing[0], target
        assert(sorted_existing[0] > target)
        return sorted_existing[0], sorted_existing[1]
    if insert_index == len(sorted_existing):
        assert(sorted_existing[-1] < target)
        return sorted_existing[-2], sorted_existing[-1]
    else:
        assert(sorted_existing[insert_index-1] < target)
        assert(sorted_existing[insert_index] > target)
        return sorted_existing[insert_index-1], sorted_existing[insert_index]

if __name__ == "__main__":
    filename = sys.argv[1]
    log.info("Updating file: %s", filename)
    f = open(filename, 'update')
    folders, vhtt_masses, vhww_masses = find_all_keys(f)
    #target_masses = set([100, 150, 160] + range(110, 160+1, 0.5))
    target_masses = set(range(110, 161) + [0.5 + x for x in range(110, 160)])

    vhtt_target_masses = target_masses - vhtt_masses
    vhww_target_masses = target_masses - vhww_masses

    def formatter(x):
        if abs(x/int(x)) - 1 < 1e-5:
            return "%i" % x
        else:
            return "%0.1f" % x

    rules = {
        'tt' : {
            'target_masses' : vhtt_target_masses,
            'existing' : vhtt_masses,
            'label' : 'tautau',
            'name' : lambda mass : 'VH%s' % formatter(mass)
        },
        'ww' : {
            'target_masses' : vhww_target_masses,
            'existing' : vhww_masses,
            'label' : 'WW',
            'name' : lambda mass : 'VH_hww%s' % formatter(mass)
        },
    }

    for rule, rule_info in rules.iteritems():
        for mass in sorted(rule_info['target_masses']):
            low, high = find_best_interp_points(
                mass, rule_info['existing'])

            log.info("Interpolating m=%f %s histogram between %f and %f",
                     mass, rule_info['label'], low, high)
            for folder in folders:
                log.debug("Doing shape folder %s", folder)
                # Switch to the folder
                name = rule_info['name']
                print name(low)
                print name(high)
                low_hist = f.get(os.path.join(folder, name(low)))
                high_hist = f.get(os.path.join(folder, name(high)))
                print low_hist
                f.cd(folder)
                new_hist = morph(
                    name(mass), "VH%s m=%f" % (rule_info['label'], mass),
                    mass, low_hist, low, high_hist, high)
                print low_hist

                log.debug(
                    "mean/norm low:%0.2f/%0.2f high:%0.2f/%0.2f new:%0.2f/%0.2f",
                    low_hist.GetMean(), low_hist.Integral(),
                    high_hist.GetMean(), high_hist.Integral(),
                    new_hist.GetMean(), new_hist.Integral())
                new_hist.Write()
