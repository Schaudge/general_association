#!/usr/bin/env python3
# coding: utf8
"""
Author: Schaudge King
Create Time: 2020-03-19
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from abc import abstractmethod


class VarRecord(object):
    def __init__(self, chrom, pos, ref, alt, infos=""):
        self.chrom = self.__chrom2int(chrom)
        self.pos = int(pos) if type(pos) == str else pos
        self.ref = ref
        self.alt = alt
        self.infos = infos

    def __repr__(self):
        return str(self.chrom) + ":" + str(self.pos) + ":" + self.ref + "-" + self.alt

    @abstractmethod
    def block_flag(self) -> int:
        return self.pos

    @abstractmethod
    def context(self) -> str:
        return self.ref + ":" + self.alt

    def format(self) -> str:
        return self.__chrom_str() + "\t" + str(self.pos) + "\t.\t" + self.ref + "\t" + self.alt + \
               "\t.\t.\t" + self.infos

    @staticmethod
    def __chrom2int(chrom):
        if type(chrom) == str:
            chrom = 23 if chrom == "X" else (24 if chrom == "Y" else int(chrom))
        elif type(chrom) != int:
            raise
        return chrom

    def __chrom_str(self):
        return str(self.chrom) if self.chrom < 22 else ("Y" if self.chrom > 23 else "X")


class GenomePosRecord(VarRecord):
    def __init__(self, chrom, pos, ref, alt, infos):
        super().__init__(chrom, pos, ref, alt, infos)

    def __eq__(self, other):
        if self.chrom == other.chrom and self.pos == other.pos:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.chrom != other.chrom or self.pos != other.pos:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.chrom < other.chrom:
            return True
        elif self.chrom == other.chrom and self.pos < other.pos:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.chrom > other.chrom:
            return True
        elif self.chrom == other.chrom and self.pos > other.pos:
            return True
        else:
            return False

    def context(self) -> str:
        return self.ref + ":" + self.alt

    def block_flag(self) -> int:
        return self.pos
