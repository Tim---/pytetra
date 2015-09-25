#!/usr/bin/env python

from collections import OrderedDict

class Field:
    pass

class UIntField(Field):
    def __init__(self, name, sz):
        self.name = name
        self.sz = sz

    def dissect(self, pkt, bits):
        res = int(''.join(map(str, bits[:self.sz])), 2)
        del bits[:self.sz]
        return res

class BitsField(Field):
    def __init__(self, name, sz):
        self.name = name
        self.sz = sz

    def dissect(self, pkt, bits):
        res = bits[:self.sz]
        del bits[:self.sz]
        return res

class ConditionalField(Field):
    def __init__(self, field, cond):
        self.field = field
        self.name = field.name
        self.cond = cond

    def dissect(self, pkt, bits):
        if self.cond(pkt):
            return self.field.dissect(pkt, bits)
        else:
            return None

class Pdu(object):
    @classmethod
    def parse(cls, bits):
        pkt = OrderedDict()
        for field in cls.fields_desc:
            pkt[field.name] = field.dissect(pkt, bits)
        return pkt
