#!/usr/bin/env python
"""Generate form rules from form json
Usage:
    rulegen -i <json-file> [-d <out-dir>]
    rulegen -h --help
"""
import uuid
from docopt import docopt
import os, sys
import json


def validated_fyl(_fyl):
    if not os.path.exists(_fyl):
        print(f'{_fyl} not found', file=sys.stderr)
        sys.exit(1)
    return _fyl


def make_rules_file(file_id, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return open(f"{os.path.join(output_dir, file_id)}Rules.json", 'w')


def generate_rules_file(out_file, file_id, form_uuid, fe_names):
    from kitchensink import (header, declare_rule, define_class,
                             close_class, define_method,)

    out_file.write(header)
    out_file.write(declare_rule(file_id, form_uuid))
    out_file.write(define_class(file_id, uuid.uuid4()))
    for fe_name in fe_names:
        out_file.write(define_method(fe_name))
    out_file.write(close_class())


if __name__ == '__main__':
    args = docopt(__doc__)
    fyl = open(validated_fyl(args['<json-file>']))
    fyl_id = fyl.name.split('/')[-1].rstrip('.json')
    form = json.load(fyl)

    all_fe_names = [elem['name'] for grp in form['formElementGroups']
                    for elem in grp['formElements']]

    with make_rules_file(fyl_id, args['<out-dir>'] or "_rules") as rules_file:
        generate_rules_file(rules_file, fyl_id, form['uuid'], all_fe_names)

    print(f"Generated {rules_file.name}")
