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
    stack.phy.feed_from_file(sys.argv[1])
