#!/usr/bin/env python

from collections import defaultdict
import argparse
import gzip
import os
import re
import sys

from six.moves import reduce
import six

from treksum import get_data, _ROOT


_SCRIPTS = os.path.join(_ROOT, 'scripts')
NUM_WORDS = ('one', 'two', 'three', 'four', 'five', 'six', 'seven')
CHAR_RE = re.compile(r"[^\w\-']+")
REPLACE = ('<br>', '</p>', '\r', '\n', '\a')


def _stripper(acc, r):
    """
    Remove any occurences of *r* in *acc*.

    :param str acc:
        The string which contains substrings that need to be removed.
    :param str r:
        The character or substring to remove from *acc*.

    :returns:
        *acc* with no more occurrences of *r*
    :rtype: str

    """

    return str.replace(acc, r, '')


def process_script(fh):
    """
    Process a specific episode's script and look for lines from each character.
    Each line found will be yielded to the calling scope.

    :param file fh:
        The file-like object to process as the script.

    :yields:
        A tuple containing the character's name, the number of words in the
        line, and the actual line from the script.

    """

    record = False
    dbuffer = ""
    charname = ""

    # look for pattern indicating charector name
    for data in fh:
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
                dbuffer = reduce(_stripper, REPLACE, dbuffer).strip()
                words = dbuffer.split()

                # clean up the spacing
                dbuffer = ' '.join(words)

                yield (charname, len(words), dbuffer)

                record = False


def main(only_characters=None):
    """
    Extract each line from all episodes of Star Trek: The Next Generation's
    scripts. Each character's individual lines will be stored in a gzipped CSV
    file (though using a semicolon instead of commas).

    :param iterable only_characters: (optional)
        If specified, only lines from specified characters will be serialized
        to disk.

    """

    lines = defaultdict(list)

    # check every script for all seasons
    for season_num in NUM_WORDS:
        season_dir = os.path.join(_SCRIPTS, 'season%s' % season_num)
        for script_file in os.listdir(season_dir):
            episode = script_file.replace('.htm', '')
            with open(os.path.join(season_dir, script_file)) as f:
                for charname, words, line in process_script(f):
                    if only_characters is None or charname in only_characters:
                        lines[charname].append((str(words), episode, line))

    for character, char_lines in lines.items():
        with gzip.open(get_data(character), 'wb') as fh:
            data = '\n'.join(map(';'.join, char_lines))
            fh.write(six.b(data))

    stats = sorted((len(l), n) for n, l in lines.items())
    for num_lines, name in stats:
        sys.stdout.write('{}: {} lines parsed\n'.format(name, num_lines))


if __name__ == '__main__':
    cli = argparse.ArgumentParser()
    cli.add_argument('-c', '--character', nargs='+', required=False)

    opts = cli.parse_args()

    main(opts.character)
