#!/usr/bin/env python
import re
from Hooks.scans.parser import parse

scanre=re.compile("http://[^/]+/(?:showscan|waves).pl\?scan_id=([0-9a-zA-Z]+)")

with open("1000scans.txt") as f:
    for x in f:
        scanid = scanre.match(x).group(1)
        parse(1, "scan", scanid).start()

print "Done."
