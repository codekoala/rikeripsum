#!/usr/bin/env python

import argparse
import gzip
import os
import random

_ROOT = os.path.abspath(os.path.dirname(__file__))
DEFAULT_CHAR = 'riker'
LINES = {}


def get_data(path):
    return os.path.join(_ROOT, 'data', '{}.gzc'.format(path))


def generate_paragraph(sentence_count=None, character=DEFAULT_CHAR):
    """Generates a 'paragraph' consisting of sentence_count 'sentences'.
    If sentence_count is not provided, a random number between two and
    ten will be chosen.

    """

    if not sentence_count:
        sentence_count = random.choice(range(2, 10))

    paragraph = ''
    for i in range(sentence_count):
        paragraph += ' ' + generate_sentence(character=character)

    return paragraph.strip()


def generate_sentence(word_count=None, character=DEFAULT_CHAR):
    """Returns a 'sentence'. A sentence is actually one line of dialog
    by William Riker, and may in fact consiste of multiple sentences.
    If a word_count is provided, the generator will attempt to return
    a sentence with that number of words. Or come as close as possible.
    Note that higher numbers of word will become increasingly unique to
    the distribution and may result in a less 'random' sentence.

    """

    if character not in LINES:
        LINES[character] = load_data(character)

    pool = LINES[character][:]
    if word_count:
        pool = [
            line for line in pool
            if line['word_count'] == word_count
        ]

    if not pool:
        if word_count == 1:
            raise ImpossibleSentenceError(
                "Couldn't generate a sentence with the requested number of "
                "words."
            )

        else:
            # recursive callback, trying one less words each time.
            return generate_sentence(word_count - 1, character)

    return random.choice(pool)['text']


def load_data(character=DEFAULT_CHAR):
    """Loads up sentence data. All methods in this class which use
    phrase data should call this if global lines == None.

    """

    lines = []
    with gzip.open(get_data(character), 'rb') as fh:
        for line in fh:
            wc, ep, text = line.decode('utf-8').strip().split(';', 2)
            lines.append({
                'text': text,
                'episode': ep,
                'word_count': int(wc),
            })

    return lines


class ImpossibleSentenceError(Exception):
    """
    Called when the engine is unable to fufill the request due to lack of
    potential data. This would usually be raised if a number of sentences was
    requested which the engine did not have data to fulfill.

    """


def main():

    parser = argparse.ArgumentParser(description='Print Riker quotes.')
    parser.add_argument('-c', '--count', dest='count', type=int,
                        help='minimum number of words in the sentence')

    parser.add_argument('-s', '--speaker', default=DEFAULT_CHAR,
                        help='name of the character to grab quotes from')

    args = parser.parse_args()

    print(generate_sentence(args.count, args.speaker))


if __name__ == '__main__':
    main()
