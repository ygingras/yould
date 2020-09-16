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

import sys
try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # there is no ez_setup if setup tools is installed with apt, among
    # other things
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    print "You don't have setuptools installed.  Put ez_setup.py"
    print "in the same directory as setup.py (this script) and try again."
    print "You can get it here:"
    print "  http://peak.telecommunity.com/dist/ez_setup.py"
    sys.exit(1)

from yould.config import __version__

setup(
    name='yould',
    version=__version__,
    description="a word generator",
    author="Yannick Gingras",
    author_email="ygingras@ygingras.net",
    url="http://ygingras.net/b/tag/yould",
    license='GPL v3 or later',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    package_data = {
       '': ['*.yould', 'NEWS.txt'],
    },
    entry_points={
      'console_scripts': ["yould = yould.generate:main",
                          "yould-train = yould.train:main"],
    },
)
