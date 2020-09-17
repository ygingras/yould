#!/usr/bin/env python3

# Yould: a generator for pronounceable random words
# Copyright (C) 2007,2020 Yannick Gingras <ygingras@ygingras.net>

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

import sys
import re

from .prob import find_trainset, list_trainsets
from .config import __version__

from pprint import pprint
from optparse import OptionParser

def main():
    parser = OptionParser()
    
    parser.add_option("-t", "--training-set", dest="trainset", default="kjb",
                      help="encoding of the text, default is UTF-8")
    parser.add_option("-o", "--output", dest="output", default=None,
                      help="save output in FILE", metavar="FILE")
    parser.add_option("-R", "--regexp", dest="regexp", default="",
                      help="validate generated words agains REGEXP")
    parser.add_option("-n", dest="nb_words", default=1, type=int,
                      help="number of words to generate")
    parser.add_option("-T", "--timeout", dest="max_secs", default=None,
                      type=int, help="give up after MAX_SECS")
    parser.add_option("-m", "--minimum", dest="min", default=4, type=int,
                      help="minimum word length")
    parser.add_option("-M", "--maximum", dest="max", default=12, type=int,
                      help="maximum word length")
    parser.add_option("-d", "--dump",
                      action="store_true", dest="dump", default=False,
                      help="dump the training set in human readable format and exit")
    parser.add_option("-r", "--real-words",
                      action="store_true", dest="real_words", default=False,
                      help="include words seen during training")
    parser.add_option("-V", "--version",
                      action="store_true", dest="version", default=False,
                      help="print software version")
    parser.add_option("--list-sets",
                      action="store_true", dest="list", default=False,
                      help="list the available training sets")

    (opts, args) = parser.parse_args()
    if args:
        parser.error("Unrecognized arguments: %s" % ", ".join(args))

    if opts.version:
        print("Yould %s" % __version__)
        sys.exit(0)
    
    if opts.list:
        print(", ".join(list_trainsets()))
        sys.exit(0)
    
    trainset = find_trainset(opts.trainset)
    
    if opts.dump:
        # TODO: we could have something more readable than that
        pprint(trainset.probs)
        sys.exit(0)

    if opts.output:
        out = open(out, "w")
    else:
        out = sys.stdout

    if opts.regexp:
        opts.regexp = re.compile(opts.regexp, re.UNICODE)

    trainset.init_cache(opts.nb_words)
    if opts.max_secs:
        trainset.start_timer(opts.max_secs)
    for i in range(opts.nb_words):
        word = trainset.gen(not opts.real_words,
                            opts.min,
                            opts.max,
                            opts.regexp)
        if not word:
            sys.exit(1)
        
        # TODO: locale dependant encoding
        out.write(word)
        out.write("\n")


if __name__ == "__main__":
    main()

