#!/usr/bin/python

__author__ = 'agallo'

# use peeringDB 2.0 API to see if a given ASN lists itself on the Equinix-Ashburn IX
# TODO - suppress lookup of networks not in non-Ashburn
# TODO - create different tables for non-Ashburn networks
# TODO - accept list of ASNs in a file (would need to sort & dedup the list)

import urllib, json
from argparse import ArgumentParser
from prettytable import PrettyTable
import pythonwhois



# setup some command line arguments

parser = ArgumentParser(description="use peeringDB 2.0 API to see if a given ASN lists itself"
                                    " on the Equinix-Ashburn IX")

parser.add_argument('ASN', metavar='ASN', type=int, nargs='+')

args = parser.parse_args()

ASNlist = args.ASN


def getASname(ASN):
    whoisstring = 'AS' + str(ASN)
    ASNname = pythonwhois.net.get_whois_raw(whoisstring, server='whois.cymru.com')
    return ASNname[0][8:-1]

def processASNs(ASNlist):

    mbrasn = []
    mbrname = []
    mbrpolicy = []
    mbrash = []
    for ASN in ASNlist:

        skipindex = False

        baseurl = "https://beta.peeringdb.com/api/asn/" + str(ASN)

        raw = urllib.urlopen(baseurl)
        # if we get a blank doc, json.load can't parse the response and will throw an error
        try:
            jresponse = json.load(raw)
        except ValueError:
            skipindex = True
            pass

        if not skipindex:
            name = jresponse['data'][0]['name']
            policy = jresponse['data'][0]['policy_general']
            faclist = jresponse['data'][0]['netfac_set']
            for index, facility in enumerate(d['fac_id'] for d in faclist):
                if facility == 1:
                    # print "YAY! " + name + " is at Equinix-Ashburn"
                    mbrasn.append(ASN)
                    mbrname.append(name)
                    mbrpolicy.append(policy)
                    mbrash.append(True)
            # ixcount = index + 1
            # if ixcount == 1:
            #    print name + " is present at " + str(ixcount) + " IX"
            # else:
            #    print name + "  is present at " + str(ixcount) + " IXs"
        else:
            # print str(ASN) + " does not appear to be in the peeringDB(peeringDB returned zero length doc)."
            mbrasn.append(ASN)
            mbrname.append(getASname(ASN))
            mbrpolicy.append('n/a')
            mbrash.append(False)

    return mbrasn, mbrname, mbrpolicy, mbrash


def main():
    mbrasn, mbrname, mbrpolicy, mbrash = processASNs(ASNlist)
    print "******SUMMARY"
    print "The following networks are listed as Equinix-Ashburn Participants"
    t = PrettyTable(['ASN', 'Network Name', 'In Ashburn?', 'policy'])
    for a, n, l, p, in zip(mbrasn, mbrname, mbrash, mbrpolicy):
        t.add_row([str(a), n, l, p])

    print t


main()
