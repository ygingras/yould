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

# King James Bible
BOOKS = [8010, 8011, 8012, 8013, 8014, 8015, 8016, 8017, 8018, 8019,
         8001, 8020, 8021, 8022, 8023, 8024, 8025, 8026, 8027, 8028,
         8029, 8002, 8030, 8031, 8032, 8033, 8034, 8035, 8036, 8037,
         8038, 8039, 8003, 8040, 8041, 8042, 8043, 8044, 8045, 8046,
         8047, 8048, 8049, 8004, 8050, 8051, 8052, 8053, 8054, 8055,
         8056, 8057, 8058, 8059, 8005, 8060, 8061, 8062, 8063, 8064,
         8065, 8066, 8006, 8007, 8008, 8009]
  

BASE_URL = "http://www.gutenberg.org/"
MAIN_URL = BASE_URL + "etext/%d"
DL_PAT = compile(r'<td class="pgdbfilesdownload"><a href="(/(?:dirs|files)/.*?.txt)"')
MAX = 2**22

for book in BOOKS:
    try:
        data = urlopen(MAIN_URL % book).read(MAX)
        print(book, end=' ') 
        dl = DL_PAT.findall(data)[0]
        print(dl)
        stream = urlopen(BASE_URL + dl)
        open("%04d.txt" % book, "w").write(stream.read(MAX))
    except:
        print("Error")
    
