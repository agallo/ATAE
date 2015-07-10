#!/usr/bin/python

__author__ = 'agallo'

# use peeringDB 2.0 API to see if a given ASN lists itself on the Equinix-Ashburn IX

import urllib, json
from argparse import ArgumentParser
from prettytable import PrettyTable


# setup some command line arguments

parser = ArgumentParser(description="use peeringDB 2.0 API to see if a given ASN lists itself"
                                    " on the Equinix-Ashburn IX")

parser.add_argument('ASN', metavar='ASN', type=int, nargs='+')

args = parser.parse_args()

ASNlist = args.ASN


def processASNs(ASNlist):

    mbrasn = []
    mbrname = []
    mbrpolicy = []
    for ASN in ASNlist:

        skipindex = False

        baseurl = "https://beta.peeringdb.com/api/asn/" + str(ASN)

        raw = urllib.urlopen(baseurl)

        try:
            jresponse = json.load(raw)
        except ValueError:
            skipindex = True
            pass

        if not skipindex:
            name = jresponse['data'][0]['name']
            policy = jresponse['data'][0]['policy_general']
            faclist = jresponse['data'][0]['facility_set']
            for index, facility in enumerate(d['facility'] for d in faclist):
                if facility == 1:
                    # print "YAY! " + name + " is at Equinix-Ashburn"
                    mbrasn.append(ASN)
                    mbrname.append(name)
                    mbrpolicy.addpend(policy)
            # ixcount = index + 1
            # if ixcount == 1:
            #    print name + " is present at " + str(ixcount) + " IX"
            # else:
            #    print name + "  is present at " + str(ixcount) + " IXs"
        else:
            print str(ASN) + " does not appear to be in the peeringDB(peeringDB returned zero length doc)."

    return mbrasn, mbrname, mbrpolicy


def main():
    mbrasn, mbrname = processASNs(ASNlist)
    print "******SUMMARY"
    print "The following networks are listed as Equinix-Ashburn Participants"
    t = PrettyTable(['ASN', 'Network Name', 'In Ashburn?', 'policy'])
    for a, n, p in zip(mbrasn, mbrname):
        t.add_row([str(a), n, 'future', p])

    print t


main()
