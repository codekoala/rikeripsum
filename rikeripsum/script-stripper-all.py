#!/usr/bin/env python
# python script-stripper-all.py  1.18s user 0.02s system 99% cpu 1.208 total

import os
import sys

try:
    import cPickle as pickle
except ImportError:
    import pickle  # noqa


NUM_WORDS = ('one', 'two', 'three', 'four', 'five', 'six', 'seven')

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'data', path)


def main():
    lines = {}

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
                        splited = data.split("<p>")[-1].split("<br>")[0]
                        splited = splited.split("'S")[0].split(" ")

                        # long list of words probably isnt a name
                        if len(splited) > 5:
                            continue

                        for name in splited:
                            # charector names are uppercase
                            if name.isupper():
                                charname = name
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
                            line = {"text": dbuffer,
                                    "episode": script_file.replace('.htm', ''),
                                    "word_count": len(dbuffer.split())}
                            record = False
                            if charname in lines:
                                lines[charname].append(line)
                            else:
                                lines[charname] = [line]

    with open(get_data('all_characters.pickle'), 'wb') as pickle_file:
        pickle.dump(lines, pickle_file)

    stats = []
    for name in lines:
        stats.append([len(lines[name]), name])
    stats.sort()

    for num_lines, name in stats:
        sys.stdout.write('{}: {} lines parsed\n'.format(name, num_lines))


if __name__ == '__main__':
    main()
