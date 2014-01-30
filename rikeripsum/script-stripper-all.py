#!/usr/bin/env python
# python script-stripper-all.py  1.18s user 0.02s system 99% cpu 1.208 total

from collections import defaultdict
import argparse
import os
import re
import sys
import zlib

import six


NUM_WORDS = ('one', 'two', 'three', 'four', 'five', 'six', 'seven')
CHAR_RE = re.compile(r"[^\w\-']+")

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'data', path)


def main(only_characters=None):
    lines = defaultdict(list)

    # check every script for all seasons
    for season_num in NUM_WORDS:
        season_dir = 'scripts/season%s' % season_num
        for script_file in os.listdir(season_dir):
            record = False
            dbuffer = ""
            charname = ""

            with open('scripts/season%s/%s' % (season_num, script_file)) as f:

                # look for pattern indicating charector name
                for data in f:
                    if "<p>" in data and "<br>" in data:
                        bits = data.split("<p>")[-1].split("<br>")[0]
                        bits = bits.split("'S")[0].split(" ")

                        # long list of words probably isnt a name
                        if len(bits) > 5:
                            continue

                        for name in bits:
                            # charector names are uppercase
                            if name.isupper():
                                charname = CHAR_RE.sub('-', name).lower()
                                record = True
                                dbuffer = ""
                                break

                    # if name was just found, extract dialog until </p>
                    elif record:
                        dbuffer += data
                        if "</p>" in data:
                            dbuffer = dbuffer.replace("<br>", "").replace("</p>", "")
                            dbuffer = dbuffer.replace("\r", "").replace("\n", "")
                            dbuffer = dbuffer.replace("\a", "").strip()
                            dbuffer = ' '.join(dbuffer.split())
                            line = map(str, (
                                len(dbuffer.split()),
                                script_file.replace('.htm', ''),
                                dbuffer
                            ))
                            record = False

                            if only_characters is None or charname in only_characters:
                                lines[charname].append(line)

    for character, char_lines in lines.items():
        with open(get_data(character), 'wb') as fh:
            data = '\n'.join(map(';'.join, char_lines))
            small = zlib.compress(six.b(data))
            fh.write(small)

    stats = sorted((len(l), n) for n, l in lines.items())
    for num_lines, name in stats:
        sys.stdout.write('{}: {} lines parsed\n'.format(name, num_lines))


if __name__ == '__main__':
    cli = argparse.ArgumentParser()
    cli.add_argument('-c', '--character', nargs='+', required=False)

    opts = cli.parse_args()

    main(opts.character)
