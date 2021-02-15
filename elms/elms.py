from pathlib import Path
import csv
import re
import numpy as np
from edgeml import bes2hdf5


def read_elm_shotlist(verbose=False):
    file = Path(__file__).parent / 'elm-shotlist.csv'
    rx = re.compile(r"^\s+(?P<runid>\w+)\s+(?P<shot>\d+)\s*$")
    shotlist = []
    runids = []
    with file.open() as f:
        reader = csv.reader(f)
        for irow, row in enumerate(reader):
            if irow==0:
                continue
            match = rx.match(row[0])
            if verbose:
                print(irow, row, match)
            assert(match)
            runids.append(match.group('runid'))
            shotlist.append(eval(match.group('shot')))
    return runids, shotlist


def package_elms(max_shots=None):
    _, shotlist = read_elm_shotlist()
    shotlist = np.array(shotlist)
    if max_shots:
        shotlist = shotlist[0:max_shots]
    print(shotlist[0], shotlist[-1], shotlist.size)
    bes2hdf5.package_bes(shots=shotlist,
                         verbose=True,
                         with_signals=False)


def package_8x8_sublist(max_shots=None):
    shotlist = bes2hdf5.make_8x8_sublist(
            path='/home/smithdr/edgeml/elms/data/elm_metadata/bes_metadata.hdf5',
            upper_inboard_channel=56,
            noplot=True)
    if max_shots:
        shotlist = shotlist[0:max_shots]
    bes2hdf5.package_bes(shots=shotlist,
                         channels=np.arange(1,65),
                         verbose=True,
                         with_signals=True)


if __name__=='__main__':
    # runids, shotlist = read_elm_shotlist()
    # bes2hdf5.print_metadata_summary('data/elm_metadata/bes_metadata.hdf5', only_8x8=True)
    # shotlist = bes2hdf5.make_8x8_sublist(path='data/elm_metadata/bes_metadata.hdf5', upper_inboard_channel=56)
    package_8x8_sublist()
