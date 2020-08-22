#!/usr/bin/env python3
import argparse
import re
import sys

REGEX_CHAR_HEADING = re.compile(r'^\+\+\+\s+(?P<char_index>\d+)\.\s+(?P<char>\S)\s*$')
REGEX_EXAMPLE_LINE = re.compile(r'^(?P<example>.+)(?P<readings>（.+）)\s*$')
REGEX_WORD_LINE = re.compile(r'^\s*\|\|(?P<word>[^|]+)\|\|(?P<reading>[^|]+)\|\|(?P<glosses>[^|]+)\|\|\s*$')
REGEX_KANJI_LINE = re.compile(r'^\|\|~ \[#\d+ \d+\]\|\|(?P<kanji>.+)\|\|\s*$')
JAPANESE_PUNCT = (0x3000, 0x303f)
HIRAGANA = (0x3040, 0x309f)
KATAKANA = (0x30a0, 0x30ff)
FULL_WIDTH_ROMAN_HALF_WIDTH_KATAKANA = (0xff00, 0xffef)
CJK_UNIFIED = (0x4e00, 0x9faf)
CHAR_SET_LIMITS = [
    JAPANESE_PUNCT,
    HIRAGANA,
    KATAKANA,
    FULL_WIDTH_ROMAN_HALF_WIDTH_KATAKANA,
    CJK_UNIFIED
]
BACK_MATTER_HEADING = '+ Back Matter'


def is_japanese_char(s):
    code_point = ord(s)
    for limits in CHAR_SET_LIMITS:
        lower, upper = limits
        if lower <= code_point <= upper:
            return True

    return False

def words(inf, outf):
    char = ''
    char_index = ''
    word_index = 0
    incomplete_line = ''
    for _line in inf:
        _line = _line.rstrip('\n')
        if _line.endswith(' _'):
            incomplete_line = incomplete_line + _line[:-1]
            continue
        line = incomplete_line + _line
        incomplete_line = ''

        if line.startswith(BACK_MATTER_HEADING):
            break

        match = REGEX_CHAR_HEADING.search(line)
        if match:
            char = match.groupdict( )['char']
            char_index = match.groupdict()['char_index']
            word_index = 0
            continue

        match = REGEX_WORD_LINE.search(line)
        if match:
            word_index += 1
            word = match.groupdict()['word']
            reading = match.groupdict()['reading']
            glosses = match.groupdict()['glosses']
            outf.write('\t'.join([char, char_index, str(word_index), word, reading, glosses]))
            outf.write('\n')


def examples(inf, outf):
    char = None
    char_index = None
    example_index = 0
    for line in inf:

        if line.startswith(BACK_MATTER_HEADING):
            break

        match = REGEX_CHAR_HEADING.search(line)
        if match:
            char = match.groupdict()['char']
            char_index = match.groupdict()['char_index']
            example_index = 0
            continue

        if is_japanese_char(line[0]):
            example_index += 1
            s = line.rstrip()
            match = REGEX_EXAMPLE_LINE.search(s)
            if match:
                example = match.groupdict()['example']
                readings = match.groupdict().get('readings', '') or ''
            else:
                example = s
                readings = ''
            outf.write('\t'.join([char_index, str(example_index), char, example, readings]))
            outf.write('\n')


def kanji(inf, outf):
    for line in inf:
        s = line.rstrip()
        match = REGEX_KANJI_LINE.search(s)
        if match:
            kanji = match.groupdict()['kanji'].split('||')
            outf.write('\n'.join(kanji))
            outf.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--examples', '-e',
                        dest='examples',
                        action='store_true')
    parser.add_argument('--words', '-w',
                        dest='words',
                        action='store_true')
    parser.add_argument('--kanji', '-k',
                        dest='kanji',
                        action='store_true')
    args = parser.parse_args()
    if args.examples:
        examples(sys.stdin, sys.stdout)
    elif args.words:
        words(sys.stdin, sys.stdout)
    elif args.kanji:
        kanji(sys.stdin, sys.stdout)
    else:
        sys.stderr.write('use --words, --examples, or --kanji flag\n')
        sys.exit(-1)
