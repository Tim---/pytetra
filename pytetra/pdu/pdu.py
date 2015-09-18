#!/usr/bin/env python

class Field:
    pass

class UIntField(Field):
    def __init__(self, name, sz):
        self.name = name
        self.sz = sz

    def dissect(self, bits):
        res = int(''.join(map(str, bits[:self.sz])), 2)
        del bits[:self.sz]
        return res

class BitsField(Field):
    def __init__(self, name, sz):
        self.name = name
        self.sz = sz

    def dissect(self, bits):
        res = bits[:self.sz]
        del bits[:self.sz]
        return res

class Pdu(object):
    @classmethod
    def parse(cls, bits):
        res = {}
        for field in cls.fields_desc:
            res[field.name] = field.dissect(bits)
        return res
