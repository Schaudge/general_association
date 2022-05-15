#!/usr/bin/env python3
# coding: utf8
"""
Author: Schaudge King
Create Time: 2020-03-21
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ga.input_format import *
from ga.var_record import *


class BlockParseFuncMachine(object):
    @abstractmethod
    def generate_parse_callable(self, rst_type) -> callable:
        pass


class ChromBlockParseMachine(BlockParseFuncMachine):

    def generate_parse_callable(self, rst_type):
        pass


class PositionBlockParseMachine(BlockParseFuncMachine):

    def generate_parse_callable(self, rst_type) -> callable:
        """

        :rtype:
        """
        return_record = GenomePosRecord
        if rst_type == "vcf":
            applied_func = VcfInputFormat(return_record)
        elif rst_type == "compact":
            applied_func = CompactInputFormat(return_record)
        else:
            raise
        return applied_func

