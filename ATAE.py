#!/usr/bin/python

__author__ = 'agallo'

# use peeringDB 2.0 API to see if a given ASN lists itself on the Equinix-Ashburn IX
# TODO better reporting inside loop to explain which ASNs are in Ashburn


import urllib, json
import sys
from argparse import ArgumentParser

# setup some command line arguments

parser = ArgumentParser(description="use peeringDB 2.0 API to see if a given ASN lists itself"
                                    " on the Equinix-Ashburn IX")

parser.add_argument('ASN', metavar='ASN', type=int, nargs='+')

args = parser.parse_args()

ASNlist = args.ASN


def processASNs(ASNlist):

    for ASN in ASNlist:

        baseurl = "https://beta.peeringdb.com/api/asn/" + str(ASN)

        raw = urllib.urlopen(baseurl)

        try:
            jresponse = json.load(raw)
        except ValueError:
            print "JSON ValueError (probably zero length doc returned), most likely because " + str(ASN) + " isn't in the PeeringDB"
#            sys.exit(1)
            pass

        name = jresponse['data'][0]['name']
        faclist = jresponse['data'][0]['facility_set']

        for index, facility in enumerate(d['facility'] for d in faclist):
            if facility == 1:
                print "YAY! " + name + " is at Equinix-Ashburn"

        ixcount = index + 1
        if ixcount == 1:
            print name + " is present at " + str(ixcount) + " IX"
        else:
            print name + "  is present at " + str(ixcount) + " IXs"


def main():
    processASNs(ASNlist)

main()
