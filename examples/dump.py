#!/usr/bin/env python

from pytetra.stack import TetraStack
import sys

if len(sys.argv) != 2:
    print "Usage : dump.py <filename>"

stack = TetraStack()
with open(sys.argv[1], 'rb') as fd:
    for data in iter(lambda: map(ord, fd.read(512)), []):
        stack.phy.feed(data)
