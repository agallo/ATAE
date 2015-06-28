#!/usr/bin/python

__author__ = 'agallo'

# use peeringDB 2.0 API to see if a given ASN lists itself on the Equinix-Ashburn IX
# TODO change arg parsing to allow for multiple space separated ASNs

import urllib, json
import sys
from argparse import ArgumentParser

# setup some command line arguments

parser = ArgumentParser(description="use peeringDB 2.0 API to see if a given ASN lists itself"
                                    " on the Equinix-Ashburn IX")

parser.add_argument('ASN', metavar='ASN', type=int)

args = parser.parse_args()

ASN = args.ASN


baseurl = "https://beta.peeringdb.com/api/asn/" + str(ASN)

raw = urllib.urlopen(baseurl);

try:
    jresponse = json.load(raw)
except ValueError:
    print "JSON ValueError (probably zero length doc returned), most likely because " + str(ASN) + " isn't in the PeeringDB"
    sys.exit(1)

faclist = jresponse['data'][0]['facility_set']

for index, facility in enumerate(d['facility'] for d in faclist):
    if facility == 1:
        print "YAY! They're at Equinix-Ashburn"

ixcount = index + 1
if ixcount == 1:
    print "This ASN is present at " + str(ixcount) + " IX"
else:
    print "This ASN is present at " + str(ixcount) + " IXs"

