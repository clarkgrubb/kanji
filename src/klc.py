#!/usr/bin/env python3
import os
import re
import sys

DEFAULT_INPUT = os.path.expanduser('~/Source/clarkgrubb/wikidot/kanji-learners-course.txt')
RX_HEADER = re.compile(r'^~\s*(?P<index>\d+):\s*(?P<character>\S)\s*$')

def klc(path):
    with open(path) as f:
        index = ''
        character = ''
        for line in f:
            parts = line.rstrip().split('||')
            if len(parts) != 5:
                sys.stderr.write(f'WARNING bad line {line}')
            else:
                match = RX_HEADER.search(parts[3])
                if match:
                    index = match.groupdict()['index']
                    character = match.groupdict()['character']
                else:
                    word = parts[1]
                    phonetic = parts[2].strip('/')
                    gloss = parts[3]
                    if not word.startswith('?') and not word.startswith('#'):
                        sys.stdout.write('\t'.join([index, character, word, phonetic, gloss]))
                        sys.stdout.write('\n')


if __name__ == '__main__':
    klc(DEFAULT_INPUT if len(sys.argv) < 2 else sys.argv[1])
