#!/usr/bin/env python3
# Written By Schaudge King
# 2020-03-18
# streamed association for two well-sorted genome files (e.g. vcf)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from contextlib import ExitStack
from record_creater import RecordReaderWrapper
from parse_factory import *
from output_factory import AssociatedRuleOutput


def iterative_overlap_block(filename_1: str, filename_2: str, parse_callable: callable,
                            identity_keep_rule: callable, rule_based_output: AssociatedRuleOutput):
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
    identity_keep_rule: callable
          the record keep rule for same associated identity
    rule_based_output: AssociatedRuleOutput
          the rule based output instance of AssociatedRuleOutput!

    Returns
    -------
          overlap counts of two input files.

    """
    overlap_counts = 0
    with ExitStack() as out_stack:
        # set up the output file (rules: all in one, only overlap one, separate three)
        associated_outputs = [out_stack.enter_context(open(out, "w")) for out in rule_based_output.out_paths]
        overlap_output = associated_outputs[0]
        if rule_based_output.keep_left:
            left_output = associated_outputs[1] if len(associated_outputs) > 1 else associated_outputs[0]
        if rule_based_output.keep_right:
            right_output = associated_outputs[2] if len(associated_outputs) > 1 else associated_outputs[0]

        with RecordReaderWrapper(filename_1, parse_callable) as input1, \
                RecordReaderWrapper(filename_2, parse_callable) as input2:
            while input1.has_next() and input2.has_next():
                compare_unit1, compare_unit2 = next(input1), next(input2)
                while compare_unit1[0] != compare_unit2[0] and input1.has_next() and input2.has_next():
                    if compare_unit1[0] < compare_unit2[0]:
                        while input1.has_next() and compare_unit1[0] < compare_unit2[0]:
                            # write non-overlap record in input file1
                            if rule_based_output.keep_left:
                                for __, record in custom_dedup(compare_unit1, identity_keep_rule).items():
                                    left_output.write(record.format() + "\n")
                            compare_unit1 = next(input1)
                    elif compare_unit1[0] > compare_unit2[0]:
                        while input2.has_next() and compare_unit1[0] > compare_unit2[0]:
                            # write non-overlap record in input file2
                            if rule_based_output.keep_right:
                                for __, record in custom_dedup(compare_unit2, identity_keep_rule).items():
                                    right_output.write(record.format() + "\n")
                            compare_unit2 = next(input2)
                else:
                    if compare_unit1[0] == compare_unit2[0]:
                        overlap_counts += 1
                        for __, record in custom_dedup(compare_unit1 + compare_unit2, identity_keep_rule).items():
                            overlap_output.write(record.format() + "\n")

            # single input end of file
            if input1.has_next():
                if rule_based_output.keep_left:
                    while input1.has_next():
                        for __, record in custom_dedup(next(input1), identity_keep_rule).items():
                            left_output.write(record.format() + "\n")
            elif input2.has_next():
                if rule_based_output.keep_right:
                    while input2.has_next():
                        for __, record in custom_dedup(next(input1), identity_keep_rule).items():
                            right_output.write(record.format() + "\n")

            return overlap_counts


def max_allele_freq_compare(record1: str, record2: str):
    return record1.split("AF_MID=")[1].split(";") > record2.split("AF_MID=")[1].split(";")


def custom_dedup(unit_list: list, dedup_rule: callable) -> dict:
    uniq_index_dict = {}
    for record in unit_list:
        current_index = record.context()
        if current_index in uniq_index_dict:
            if dedup_rule(record.infos, uniq_index_dict[current_index].infos):
                uniq_index_dict[current_index] = record
        else:
            uniq_index_dict[current_index] = record
    return uniq_index_dict


if __name__ == '__main__':
    ref_file1 = sys.argv[1]
    ref_file2 = sys.argv[2]
    vcf_parse_func = PositionBlockParseMachine().generate_parse_callable("vcf")
    ruled_based_output = AssociatedRuleOutput(sys.argv[3:], all_to_one=False)
    counts = iterative_overlap_block(ref_file1, ref_file2, vcf_parse_func, max_allele_freq_compare, ruled_based_output)
    print("Total overlap counts for same position were {} in two input files!".format(counts))

