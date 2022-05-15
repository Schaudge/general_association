#!/usr/bin/env python3
# Written By Schaudge King
# 2020-03-18
# streamed association for two well-sorted genome files (e.g. vcf)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ga.record_creater import RecordReaderWrapper
from ga.output_factory import AssociatedRuleOutput
from ga.parse_factory import *


def custom_dedup_callable(unit_list: list, dedup_rule: callable) -> dict:
    uniq_index_dict = {}
    for record in unit_list:
        current_index = record.context()  # ref:alt string
        if current_index in uniq_index_dict:
            uniq_index_dict[current_index] = dedup_rule(uniq_index_dict[current_index], record)
        else:
            uniq_index_dict[current_index] = record
    return uniq_index_dict


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
    with RecordReaderWrapper(filename_1, parse_callable) as input1, \
            RecordReaderWrapper(filename_2, parse_callable) as input2:
        while input1.has_next() and input2.has_next():
            compare_unit1, compare_unit2 = next(input1), next(input2)
            while compare_unit1[0] != compare_unit2[0] and input1.has_next() and input2.has_next():
                if compare_unit1[0] < compare_unit2[0]:
                    while input1.has_next() and compare_unit1[0] < compare_unit2[0]:
                        # write non-overlap record in input file1
                        if rule_based_output.left_out:
                            for __, record in custom_dedup_callable(compare_unit1, identity_keep_rule).items():
                                rule_based_output.left_out.write(record.format() + "\n")
                        compare_unit1 = next(input1)
                elif compare_unit1[0] > compare_unit2[0]:
                    while input2.has_next() and compare_unit1[0] > compare_unit2[0]:
                        # write non-overlap record in input file2
                        if rule_based_output.right_out:
                            for __, record in custom_dedup_callable(compare_unit2, identity_keep_rule).items():
                                rule_based_output.right_out.write(record.format() + "\n")
                        compare_unit2 = next(input2)
            else:
                if compare_unit1[0] == compare_unit2[0]:
                    overlap_counts += 1
                    for __, record in custom_dedup_callable(compare_unit1 + compare_unit2, identity_keep_rule).items():
                        rule_based_output.overlap_out.write(record.format() + "\n")

        # single input end of file
        if input1.has_next():
            if rule_based_output.left_out:
                while input1.has_next():
                    for __, record in custom_dedup_callable(next(input1), identity_keep_rule).items():
                        rule_based_output.left_out.write(record.format() + "\n")
        elif input2.has_next():
            if rule_based_output.right_out:
                while input2.has_next():
                    for __, record in custom_dedup_callable(next(input1), identity_keep_rule).items():
                        rule_based_output.right_out.write(record.format() + "\n")

        return overlap_counts


# The following function need to be rewritten for (input) particular data,
# And record1, record2 are parsed by the 'parse_callable' parameter in `iterative_overlap_block` function
def max_allele_freq_compare(record1: VarRecord, record2: VarRecord) -> VarRecord:
    if record1.infos.split("AF_MID=")[1].split(";") > record2.infos.split("AF_MID=")[1].split(";"):
        return record1
    else:
        return record2


def add_info_field(record1: VarRecord, record2: VarRecord) -> VarRecord:
    raw_record_dict = {}
    for info_field in record1.infos.split(";"):
        raw_k, raw_v = info_field.split("=")
        raw_record_dict[raw_k] = raw_v
    for supp in record2.infos.split(";"):
        add_k, add_v = supp.split("=")
        if add_k not in raw_record_dict:
            raw_record_dict[add_k] = add_v
    record1.infos = ";".join([_k + "=" + _v for _k, _v in raw_record_dict])
    return record1


def main():
    from sys import argv
    ref_file1 = argv[1]
    ref_file2 = argv[2]
    vcf_parse_func = PositionBlockParseMachine().generate_parse_callable("vcf")
    record_keep_rule = add_info_field if "clinvar" in ref_file2 else max_allele_freq_compare
    ruled_based_output = AssociatedRuleOutput(argv[3:], all_to_one=False)
    counts = iterative_overlap_block(ref_file1, ref_file2, vcf_parse_func, record_keep_rule, ruled_based_output)
    print("Total overlap counts for same position were {} in two input files!".format(counts))


if __name__ == '__main__':
    main()

