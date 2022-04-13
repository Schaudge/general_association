#!/usr/bin/env python3
# Written By Schaudge King
# 2020-03-18
# streamed association for two well-sorted genome files (e.g. vcf)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from utilities.block_compare.record_creater import RecordReaderWrapper
from utilities.block_compare.parse_factory import *


def iterative_block_overlap(filename_1, filename_2, parse_callable):
    """
    find overlap (identical equation)
    *** counts (other association should be implemented by ...) ***
    for two variation record files (e.g. vcf) in one block

    Parameters
    ----------
    filename_1: string
          the first file name used for overlap query
    filename_2: string
          the second file name used for overlap query
    parse_callable: callable
          generate object from *** each line *** for those input files

    Returns
    -------
          overlap counts of two input files.

    """
    overlap_counts = 0
    with open("association.out", "w") as output:
        with RecordReaderWrapper(filename_1, parse_callable) as input1, \
                RecordReaderWrapper(filename_2, parse_callable) as input2:
            while input1.has_next() and input2.has_next():
                compare_unit1, compare_unit2 = next(input1), next(input2)
                while compare_unit1[0] != compare_unit2[0] and input1.has_next() and input2.has_next():
                    if compare_unit1[0] < compare_unit2[0]:
                        while input1.has_next() and compare_unit1 < compare_unit2:
                            compare_unit1 = next(input1)
                            # write non-overlap record in input file1
                            for single_record in compare_unit1:
                                output.write(single_record.format() + "\n")
                    elif compare_unit1[0] > compare_unit2[0]:
                        while input2.has_next() and compare_unit1 > compare_unit2:
                            compare_unit2 = next(input2)
                            # write non-overlap record in input file2
                            for single_record in compare_unit2:
                                output.write(single_record.format() + "\n")
                else:
                    if compare_unit1[0] == compare_unit2[0]:
                        same_position_info_set = {}
                        for element1 in compare_unit1:
                            median_allele_frac = float(element1.infos.split("AF_MID=")[1].split(";")[0])
                            same_position_info_set[element1.context()] = median_allele_frac, element1.format()
                        for element2 in compare_unit2:
                            median_allele_frac = float(element2.infos.split("AF_MID=")[1].split(";")[0])
                            element2_identity = element2.context()
                            if element2_identity in same_position_info_set:
                                overlap_counts += 1
                                if median_allele_frac > same_position_info_set[element2_identity][0]:
                                    same_position_info_set[element2_identity] = median_allele_frac, element2.format()
                            else:
                                same_position_info_set[element1.context] = median_allele_frac, element1.format()

                            # write association result for same position overlap records
                            for __, (__, out) in same_position_info_set.items():
                                output.write(out + "\n")

            return overlap_counts


if __name__ == '__main__':
    ref_file1 = sys.argv[1]
    ref_file2 = sys.argv[2]
    vcf_parse_func = PositionBlockParseMachine().generate_parse_callable("vcf")
    counts = iterative_block_overlap(ref_file1, ref_file2, vcf_parse_func)
    print("Total overlap counts were {} in two input comparision files!".format(counts))

