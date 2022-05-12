#!/usr/bin/env python3
# coding: utf8
"""
Author: Schaudge King
Create Time: 2022-05-12
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class AssociatedRuleOutput(object):
    def __init__(self, *args, **kwargs):
        detached_keep = True if len(args) > 2 or ("all_to_one" in kwargs and kwargs["all_to_one"]) else False
        self.keep_left = detached_keep
        self.keep_right = detached_keep
        self.out_paths = args if len(args) and len(args[0]) else ["association.out"]

    def __repr__(self):
        association_operator = "keep" if self.keep_left else "discard"
        if self.keep_left and len(self.out_paths) == 3:
            return "associated records into: " + self.out_paths[0] + ", " + \
                   association_operator + " detached records into: " + ", ".join(self.out_paths[1:]) + " respectively."
        elif self.keep_left:
            return association_operator + " all records into: " + self.out_paths[0] + "."
        else:
            return "associated records into: " + self.out_paths[0] + ", " + association_operator + " detached records."


def main():
    print(AssociatedRuleOutput("join.out"))
    print(AssociatedRuleOutput("outer_join.out", all_to_one=True))
    print(AssociatedRuleOutput("inner_join.out", "left_join.out", "right_join.out"))


if __name__ == '__main__':
    main()
