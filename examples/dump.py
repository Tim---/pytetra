#!/usr/bin/env python

from pytetra.stack import TetraStack
from collections import deque

stack = TetraStack()

with open('testnet.bits', 'rb') as fd:
    for data in iter(lambda: map(ord, fd.read(512)), []):
        stack.phy.feed(data)
