#!/usr/bin/env python3
# coding: utf8
"""
Author: Schaudge King
Create Time: 2020-03-20
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from abc import abstractmethod
from ga.var_record import VarRecord


class InputFormat(object):
    def __init__(self, rst_type):
        self.out = rst_type

    @abstractmethod
    def __call__(self, line) -> VarRecord:
        pass


class VcfInputFormat(InputFormat):
    def __init__(self, rst_type):
        super().__init__(rst_type)

    def __call__(self, line) -> VarRecord:
        chrom, pos, __, ref, alt, __, __, infos = line.strip().split("\t")[:8]
        return self.out(chrom, pos, ref, alt, infos)


class CompactInputFormat(InputFormat):
    def __init__(self, rst_type):
        super().__init__(rst_type)

    def __call__(self, line) -> VarRecord:
        chrom, pos, ref, alt, infos = line.strip().split(":")[:5]
        return self.out(chrom, pos, ref, alt, infos)
