#!/usr/bin/python

# Yould: a generator for pronounceable random words
# Copyright (C) 2007, 2020 Yannick Gingras <ygingras@ygingras.net>

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

"""probabilities, frequencies, loading, and training stuff"""

FORMAT_VERSION = 2

from pickle import load, dump
from pprint import pformat, pprint
from pkg_resources import resource_filename, resource_exists, resource_listdir
from random import random
from collections import deque
from threading import Timer
import re
import os
from . import data
from .data import trainsets


WORD_PAT = re.compile(r"\b(\w+)\b", re.UNICODE) 

# The main data structure is a probability table.  For training, we
# also need a occurence count table.  IO is done with pickle.

class TrainSet:
    """Character based markov chain with a memory of 2 past steps."""
    
    def __init__(self, counts={}, probs={}, words=set()):
        # ex: counts[('l', 'a')] = (12, {'a':8, 'c':4})
        self.counts = counts
        # ex: probs[('c', 'r')] = [(.1, 'e'), (.07, 'a'),...,(.001, 'z')]
        self.probs  = probs
        self.words  = words
        
        self.timer = None
        self.timedout = False

        self.init_cache()

    def init_cache(self, size=8000):
        # caching (don't repeat words)
        # there are two parts: a set for fast hit test and a dequeue
        # to keep only the most recent stuff
        self.max_cache = size
        self.cache_h = set()
        self.cache_l = deque()

    def cache_word(self, word):
        self.cache_h.add(word)
        self.cache_l.append(word)
        if len(self.cache_l) > self.max_cache:
            old = self.cache_l.popleft()
            self.cache_h.remove(old)

    def _timeout(self):
        # shoud only be called by a Timer
        self.timer = None
        self.timedout = True

    def start_timer(self, max_secs):
        self.timedout = False
        self.timer = Timer(max_secs, self._timeout)
        self.timer.start()

    def save(self, path):
        dump(dict(version=FORMAT_VERSION,
                  counts=self.counts,
                  probs=self.probs,
                  words=self.words),
             open(path, "wb"),
             -1)


    def seal(self):
        """ Make the probability table final.

        A sealed probability table can't be retrained but it uses much
        less RAM.
        """
        self.counts = None
        

    def learn(self, data, count_only=False, min_len=3, max_len=14):
        """Add the transition frequencies of data to the prob tables.

        Data should be human readable unicode text.
        """
        # count
        for match in WORD_PAT.finditer(data):
            word = match.group()
            # trim digits (too ugly with the regexp)
            word = "".join([c for c in word if c.isalpha()])
            if not (min_len <= len(word) <= max_len):
                continue

            self.words.add(word.lower())
            
            # the first two letters of a word also have transitions
            prev = pprev = None
            for c in word:
                nb_trs, trs_h  = self.counts.get((pprev, prev), (0, {}))
                trs_h[c] = trs_h.get(c, 0) + 1
                self.counts[(pprev, prev)] = (nb_trs+1, trs_h)

                pprev = prev
                prev = c

            # transition to word end
            nb_trs, trs_h  = self.counts.get((pprev, prev), (0, {}))
            trs_h[None] = trs_h.get(None, 0) + 1
            self.counts[(pprev, prev)] = (nb_trs+1, trs_h)
            
        if not count_only:
            self.update_probs()

    def update_probs(self):
        self.probs = {}
        for k in list(self.counts.keys()):
            nb_trs, trs_h = self.counts[k]
            self.probs[k] = [ (1.0*freq/nb_trs, nc)
                              for nc, freq in list(trs_h.items())]
            self.probs[k].sort()
            self.probs[k].reverse()


    def get_c(self, trans, draw):
        tot = 0
        for prob, c in trans:
            tot += prob
            if tot >= draw:
                return c
        return c


    def _gen(self):
        "generate a word"
        choices = []
        pprev = prev = None
        c = self.get_c(self.probs[(None, None)], random())
        while c != None:
            choices.append(c)
            pprev = prev
            prev = c
            c = self.get_c(self.probs[(pprev, prev)], random())

        word = "".join(choices)
        return word

    def gen(self, non_word=True, minl=3, maxl=18, regexp=""):
        """Generate a word that matches the criteria.

        None is returned if timeout occurred before we could find a word.
        """
        word = self._gen()
        lword = word.lower()
        match = re.search(regexp, lword)
        while (non_word and lword in self.words) \
                  or lword in self.cache_h \
                  or not(minl <= len(word) <= maxl) \
                  or not match:
            if self.timedout:
                return None
            word = self._gen()
            lword = word.lower()
            match = re.search(regexp, lword)
        
        self.cache_word(lword)
        return word


def list_trainsets():
    # FIXME: won't work with a zipped egg
    return [f for f, e in
            [t for t in map(os.path.splitext,
                       resource_listdir(data.__name__, "trainsets")) if t[1] == ".yould"]]
    
            
def find_trainset(name):
    if os.path.isfile(name):
        return load_trainset(name)
    elif resource_exists(trainsets.__name__, name):
        return load_trainset(resource_filename(trainsets.__name__, name))
    elif resource_exists(trainsets.__name__, name+".yould"):
        return load_trainset(resource_filename(trainsets.__name__, name+".yould"))
    else:
        raise Exception("Can't find training set '%s'" % name)
    

def load_trainset(path):
    data = load(open(path, "rb"))
    if data["version"] != FORMAT_VERSION:
        raise Exception("This file format is not supported.")
    return TrainSet(data["counts"], data["probs"], data["words"])

