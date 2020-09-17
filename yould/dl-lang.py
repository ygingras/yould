#!/usr/bin/python

# Copyright 2007, 2020 Yannick Gingras <ygingras@ygingras.net>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
# MA 02110-1301 USA

from urllib.request import urlopen
from re import compile
from random import sample
from optparse import OptionParser
import sys

BASE_URL = "http://www.gutenberg.org/"
MAIN_URL = BASE_URL + "etext/%s"
LANG_URL="http://www.gutenberg.org/browse/languages/%s"
#DL_PAT = compile(r'<td class="pgdbfilesdownload"><a href="(/(?:dirs|files)/.*?.txt)"')
DL_PAT = compile(r'class="pgdbfilesencoding">(?:iso-8859-1|us-ascii)</td>.*?<td class="pgdbfilesdownload"><a href="(/(?:dirs|files)/.*?.txt)"')
LANG_PAT = compile(r'<li class="pgdbetext"><a href="/etext/(.+?)">')
MAX = 2**22

def fetch(url):
    return urlopen(url).read(MAX)

def getsample(books, nb_books):
    for book in sample(books, min(len(books), nb_books)):
        print(book, end=' ') 
        try:
            data = fetch(MAIN_URL % book)
            dl = DL_PAT.findall(data)[0]
            open("%s.txt" % book, "w").write(fetch(BASE_URL + dl))
            print(BASE_URL + dl)
        except:
            print("* Error *")

# Langs with enough stuff: zh, nl, en, fi, fr, de, it, pt, es, tl
# Langs that won't parse: zh, en
def getlang(lang):
    return LANG_PAT.findall(fetch(LANG_URL % lang))

def main():
    parser = OptionParser(usage="%prog LANG")
    
    parser.add_option("-n", "--sample-size", dest="nb_books", default=50,
                      type=int,
                      help="number of books to download, default is 50")
    
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_usage()
        parser.exit()
    
    getsample(getlang(args[0]), opts.nb_books)

if __name__ == "__main__":
    main()
