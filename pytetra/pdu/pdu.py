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
    def __init__(self, name, sz=None):
        self.name = name
        self.sz = sz

    def dissect(self, pkt, bits):
        sz = self.sz or len(bits)
        res = bits[:sz]
        del bits[:sz]
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
        return '%s\n\t' % (self.__class__.__name__, ) + '\n\t'.join('%s: %s' % item for item in self.fields.items())

class TypedPdu(Pdu):
    def __init__(self, bits):
        self.fields = OrderedDict()
        # Type 1
        for field in self.type1:
            self.fields[field.name] = field.dissect(self, bits)
        # Type 2
        obit = bits.pop(0)
        if obit:
            for field in self.type2:
                pbit = bits.pop(0)
                if pbit:
                    self.fields[field.name] = field.dissect(self, bits)
        # TODO : type 3 and 4
