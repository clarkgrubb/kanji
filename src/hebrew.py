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
            if len(parts) != 5:
                sys.stderr.write(f'WARNING bad line {line}')
            else:
                hebrew = parts[1]
                english = parts[2]
                chapter = parts[3]
                sys.stdout.write('\t'.join([hebrew, english, chapter]))
                sys.stdout.write('\n')


if __name__ == '__main__':
    hebrew(DEFAULT_INPUT if len(sys.argv) < 2 else sys.argv[1])
