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

"""utility code to check if a domain is available"""

# naming convention used:
#  - name: a word without the tdl; ex: ygingras
#  - tld:  top level domain without the "."; ex: net
#  - dom:  a domain name with the tld; ex: ygingras.net

import os
from time import sleep
from os import popen
from threading import Thread
import DNS

TIMEOUT = 1.5
WHOIS = "/usr/bin/whois %s"
HOST_SOA = "/usr/bin/host -C %s 2>&1"
#HOST_SOA = "host -C %s "
WHOIS_ERR = dict(com="No match for",
                 net="No match for",                 
                 org="NOT FOUND",
                 info="NOT FOUND",
                 ca="Status:         AVAIL",)

# TODO: should parse resolv.conf
DNS_SERVER = "192.168.0.1"

def dom_tld(dom):
    return os.path.splitext(dom)[1][1:]


def dom_name(dom):
    return os.path.splitext(dom)[0]


def encode(dom):
    try:
        asc = dom.encode("ascii")
        if asc == dom:
            return asc
    except UnicodeEncodeError:
        pass
    name = dom_name(dom).encode("punycode")
    return "xn--%s.%s" % (name, dom_tld(dom))


def new_has_soa(dom):
    try:
        d = DNS.DnsRequest(server=DNS_SERVER, timeout=TIMEOUT)
        r = d.req(name=encode(dom), qtype="SOA")
        return bool(r.answers)
    except DNS.Base.DNSError:
        return False


def has_soa(dom):
    """Look for a soa record.

    Most domains without a soa a available and checking for a soa is
    faster than hitting the whois database."""
    pipe = popen(HOST_SOA % encode(dom))

    res = []
    
    def check():
        rec = pipe.read()
        ecode = pipe.close()
        res.append((rec, ecode))

    th = Thread(target=check)
    th.setDaemon(True)

    th.start()
    th.join(TIMEOUT)
    if res:
        #print "* ok"
        rec, ecode = res.pop()
        return len(rec) == 0 and ecode is None
    else:
        #print "*** timeout"
        return True
    

def has_whois(dom):
    # we only check the first few characters returned by whois but
    # what we are looking for depend on the TLD.
    tld = dom_tld(dom)

    
    #pipe = popen(WHOIS % encode(dom))
    #print WHOIS % dom.encode("utf-8")
    pipe = popen(WHOIS % encode(dom))
    lines = [pipe.readline() for i in range(9)]
    #print "-" * 30
    #print "".join(lines)

    avail = len([l for l in lines if l.startswith(WHOIS_ERR[tld])]) != 0

    if pipe.close():
        raise Exception("whois error")

    return not avail


def available(dom):
    return not new_has_soa(dom) and not has_whois(dom)

