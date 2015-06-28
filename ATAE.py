#!/usr/bin/python

__author__ = 'agallo'

# use peeringDB 2.0 API to see if a given ASN lists itself on the Equinix-Ashburn IX

import urllib, json
from argparse import ArgumentParser

# setup some command line arguments

parser = ArgumentParser(description="use peeringDB 2.0 API to see if a given ASN lists itself"
                                    " on the Equinix-Ashburn IX")

parser.add_argument('ASN', metavar='ASN', type=int)

args = parser.parse_args()

ASN = args.ASN


baseurl = "https://beta.peeringdb.com/api/asn/" + str(ASN)

print baseurl

'''


raw = urllib.urlopen(baseurl);
jresponse = json.load(raw)

faclist = jresponse['data'][0]['facility_set']

for index, facility in enumerate(d['facility'] for d in faclist):
    if facility == 1:
        print "YAY! They're at Equinix-Ashburn"
    print index, facility
'''