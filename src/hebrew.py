#!/usr/bin/env python3
import os
import re
import sys

DEFAULT_INPUT = os.path.expanduser('~/Source/clarkgrubb/wikidot/hebrew.txt')

def hebrew(path):
    with open(path) as f:
        index = ''
        character = ''
        for line in f:
            parts = line.rstrip().split('||')
            if len(parts) != 7:
                sys.stderr.write(f'WARNING bad line {line}')
            else:
                hebrew = parts[1]
                akkadian = parts[2]
                aramaic = parts[3]
                english = parts[4]
                chapter = parts[5]
                if 'Hebrew' not in hebrew:
                    sys.stdout.write('\t'.join([hebrew, akkadian, aramaic, english, chapter]))
                    sys.stdout.write('\n')


if __name__ == '__main__':
    hebrew(DEFAULT_INPUT if len(sys.argv) < 2 else sys.argv[1])
