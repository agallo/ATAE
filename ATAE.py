#!/usr/bin/python

__author__ = 'agallo'

# use peeringDB 2.0 API to see if a given ASN lists itself on the Equinix-Ashburn IX
# TODO - maybe use prettytable/tabulate/panda to form the summary table?

import urllib, json
from argparse import ArgumentParser

# setup some command line arguments

parser = ArgumentParser(description="use peeringDB 2.0 API to see if a given ASN lists itself"
                                    " on the Equinix-Ashburn IX")

parser.add_argument('ASN', metavar='ASN', type=int, nargs='+')

args = parser.parse_args()

ASNlist = args.ASN


def processASNs(ASNlist):

    mbrasn = []
    mbrname = []
    for ASN in ASNlist:

        skipindex = False

        baseurl = "https://beta.peeringdb.com/api/asn/" + str(ASN)

        raw = urllib.urlopen(baseurl)

        try:
            jresponse = json.load(raw)
        except ValueError:
            # print "JSON ValueError (probably zero length doc returned), most likely because " + str(ASN) + " isn't in the PeeringDB"
            skipindex = True
            pass

        if not skipindex:
            name = jresponse['data'][0]['name']
            faclist = jresponse['data'][0]['facility_set']
            for index, facility in enumerate(d['facility'] for d in faclist):
                if facility == 1:
                    # print "YAY! " + name + " is at Equinix-Ashburn"
                    mbrasn.append(ASN)
                    mbrname.append(name)
            # ixcount = index + 1
            # if ixcount == 1:
            #    print name + " is present at " + str(ixcount) + " IX"
            # else:
            #    print name + "  is present at " + str(ixcount) + " IXs"
        else:
            print str(ASN) + " does not appear to be in the peeringDB(peeringDB returned zero length doc)."

    return mbrasn, mbrname


def main():
    mbrasn, mbrname = processASNs(ASNlist)
    print "******SUMMARY"
    print "The following networks are listed as Equinix-Ashburn Participants"
    print "ASN" + "\t" + "Network Name"
    for a, n in zip(mbrasn, mbrname):
        print str(a) + '\t' + n


main()
