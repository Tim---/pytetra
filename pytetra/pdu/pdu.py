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
    def __init__(self, bits):
        self.fields = OrderedDict()
        for field in self.fields_desc:
            self.fields[field.name] = field.dissect(self, bits)

    def __getattr__(self, attr):
        return self.fields[attr]
        
    def __repr__(self):
        return '\n'.join('%s: %s' % item for item in self.fields.items())
