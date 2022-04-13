#!/usr/bin/env python
# coding: utf8
"""
Author: Schaudge King
Create Time: 2020-03-18
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import gzip


class RecordReaderWrapper(object):
    """
    Wrapper the input file read!
    :param filename: string, which is readable for information process
    :param vcf_version: bool, vcf record format (True)
            chr1    1234155 rs2134123   A   G ---> True
            chr1    1234155 A   G             ---> False
    :param sep: separator for the input file records
    """

    def __init__(self, filename, parse_func):
        self.stateOfEOF = False
        self.handle = gzip.open(filename, 'rt') if filename[-3:] == ".gz" else open(filename, 'r')
        self.parse_func = parse_func
        self.reserved_flag, self.reserved_record = self.__read_first_line()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handle.close()

    def __iter__(self):
        return self

    def __next__(self):
        current_record_list = [self.reserved_record]
        for line in self.handle:
            stop, record = self.__parse_current_line(line)
            if stop:
                self.reserved_record = record
                break
            else:
                current_record_list.append(record)
            try:
                next_line = next(self.handle)
                stop, record = self.__parse_current_line(next_line)
                if stop:
                    self.reserved_record = record
                    break
                else:
                    current_record_list.append(record)
            except StopIteration:
                self.stateOfEOF = True
                break
        else:
            if not self.stateOfEOF:
                self.stateOfEOF = True
            else:
                raise StopIteration
        return current_record_list

    def has_next(self):
        return not self.stateOfEOF

    def __read_first_line(self):
        first_line = "#"
        while first_line.startswith("#"):
            first_line = self.handle.readline()
        if first_line:
            record = self.parse_func(first_line)
            return record.block_flag(), record
        else:
            self.stateOfEOF = True
            return 0, None

    def __parse_current_line(self, line):
        record = self.parse_func(line)
        if record.block_flag() != self.reserved_flag:
            self.reserved_flag = record.block_flag()
            return True, record
        else:
            return False, record
