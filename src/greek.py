#!/usr/bin/env python3
import os
import re
import sys

DEFAULT_INPUT = os.path.expanduser('~/Source/clarkgrubb/wikidot/greek.txt')

def greek(path):
    with open(path) as f:
        index = ''
        character = ''
        for line in f:
            parts = line.rstrip().split('||')
            if len(parts) != 5:
                sys.stderr.write(f'WARNING bad line {line}')
            else:
                greek = parts[1]
                latin = parts[2]
                english = parts[3]
                chapter = parts[4]
                if greek != 'Greek':
                    sys.stdout.write('\t'.join([greek, latin, english, chapter]))
                    sys.stdout.write('\n')


if __name__ == '__main__':
    greek(DEFAULT_INPUT if len(sys.argv) < 2 else sys.argv[1])
