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
        left_keep_only = True if "left_keep_only" in kwargs and kwargs["left_keep_only"] else False
        right_keep_only = True if "right_keep_only" in kwargs and kwargs["right_keep_only"] else False
        out_paths = args if len(args) and len(args[0]) else ["association.out"]
        self.overlap_out = open(out_paths[0], "w")
        self.left_out = (open(out_paths[1], "w") if len(out_paths) > 1 else self.overlap_out) \
            if detached_keep or left_keep_only else None
        self.right_out = (open(out_paths[2], "w") if len(out_paths) > 1 else self.overlap_out) \
            if detached_keep or right_keep_only else None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.overlap_out:
            self.overlap_out.close()
        if self.left_out:
            self.left_out.close()
        if self.right_out:
            self.right_out.close()

    def __repr__(self):
        post_flags = ["associated"]
        post_file_names = [self.overlap_out.name]
        if self.left_out:
            post_flags.insert(0, "left")
            if self.left_out != self.overlap_out:
                post_file_names.insert(0, self.left_out.name)
        if self.right_out:
            post_flags.append("right")
            if self.right_out != self.overlap_out:
                post_file_names.append(self.right_out.name)
        postfix_print = "/".join(post_flags) + " records into: " + ", ".join(post_file_names) + \
                        (" respectively." if len(post_file_names) > 1 else ".")
        return postfix_print


def main():
    print(AssociatedRuleOutput("join.out"))
    print(AssociatedRuleOutput("outer_join.out", all_to_one=True))
    print(AssociatedRuleOutput("inner_join.out", "left_join.out", "right_join.out"))


if __name__ == '__main__':
    main()
