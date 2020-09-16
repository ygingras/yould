#!/usr/bin/python

# Yould: a generator for pronounceable random words
# Copyright (C) 2007 Yannick Gingras <ygingras@ygingras.net>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from optparse import OptionParser

from prob import *

BODY_TAG = " OF THE PROJECT GUTENBERG EBOOK"

def gut_strip(file):
    """Strip project gutenberg prolog.  Generator version"""
    in_body = False
    for line in file:
        if not in_body:
            if line.find("START"+BODY_TAG) == -1:
                continue
            else:
                in_body = True
        elif line.find("END"+BODY_TAG) != -1:
            break
        else:
            yield(line)

def main():
    parser = OptionParser(usage="%prog PROB_FILE TEXT1 [TEXT2 ...]")
    
    parser.add_option("-e", "--encoding", dest="encoding", default="utf-8",
                      help="encoding of the text, default is UTF-8")
    parser.add_option("-g", "--gutenberg",
                      action="store_true", dest="gutenberg", default=False,
                      help=("assume that texts are Project Gutenberg ebooks and"
                            " skip the prolog "))
    
    (opts, args) = parser.parse_args()
    if not args:
        parser.error("Insufficient number of arguments")

    probpath = args[0]
    if os.path.isfile(probpath):
        trainset = load_trainset(probpath)
    else:
        trainset = TrainSet()
        
    for f in args[1:]:
        
        in_body = False
        file = f == "-" and sys.stdin or open(f)
        if opts.gutenberg:
            file = gut_strip(file)
        for line in file:
            line = unicode(line, opts.encoding)
            trainset.learn(line, True)

    trainset.update_probs()
    trainset.save(probpath)

if __name__ == "__main__":
    main()

