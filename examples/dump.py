#!/usr/bin/env python

from pytetra.stack import TetraStack
from pytetra.layer.user import UserLayer
import sys


class MyUserLayer(UserLayer):
    def pdu_indication(self, layer, pdu):
        print '%s: %s' % (layer, pdu)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage : dump.py <filename>"

    stack = TetraStack(MyUserLayer)
    with open(sys.argv[1], 'rb') as fd:
        for data in iter(lambda: map(ord, fd.read(512)), []):
            stack.phy.feed(data)
