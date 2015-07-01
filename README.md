# ATAE

Are They At Equinix?

This script uses the new peeringDB 2.0 API to check if a given ASN is listed as a member of the Equinix-Ashburn Internet Exchange.

The command takes one or more ASNs (space separated) as arguments.  The script will query the peeringDB to see if ```facility == 1 ```.  This valus is hardcoded in the script because, right now, that's the only one I'm interested in.  You must *a priori* know the facilit ID in the peeringDB if you want to change this to search for another IX.

NOTE: Currently peeringDB returns results for a org's *primary* ASN.  If the network uses an ASN other than its primary at Equinix-Ashburn, the script will not detect this.
