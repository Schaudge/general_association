# General Association (GA)
a general (common) association package for two (larger) sorted genome location files

## Feature
1. flexible function (a special class of map-reduce framework)
2. python paradigm and design pattern applied

## Install and Usage
1. a basic usage (without install):
```
python3 ga/association.py <test/1.vcf> <test/2.vcf> [associated_output] [left_outer_output] [right_outer_output]
```
see ga/association.py for details.

2. install the package
```
python3 setup.py install [--prefix PATH dir]
```
then call the command thereafter
```
ga <test/1.vcf> <test/2.vcf>
```

## Output
[associated_out] (association.out for default) keeps all associated (overlap) records.

[left_outer_output] keeps left non-associated records.

[right_outer_output] keeps right non-associated records.

## Extend
In all most cases, you need only add a record keep rule callable (e.g. `new_add_compare`) for two (associated) under-compared records in particular application. Then call the `iterative_overlap_block` function's `identity_keep_rule` parameter with `new_add_compare`.

For some depth improvements, you would rewrite the `custom_dedup_callable` and `identity_keep_rule` simultaneously for adaptation.
