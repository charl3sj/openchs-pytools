#!/usr/bin/env python3
"""Convert CHS requirements from xlsx to json
Usage:
    xljs -i <excel-file> (ps | --print-sheet-names | -s <sheet-name>)
    xljs -h --help
"""
import uuid

from docopt import docopt
import os, sys
import xlrd
import json


def validated_fyl(_fyl):
    if not os.path.exists(_fyl):
        print(f'{_fyl} not found', file=sys.stderr)
        sys.exit(1)
    return _fyl


def print_if_ps(_args, _xl):
    if _args['ps'] or _args['--print-sheet-names']:
        print(_xl.sheet_names())
        sys.exit()


def validated_sheet_name(sheet_name, _xl):
    if sheet_name not in _xl.sheet_names():
        print(f'{sheet_name} not found', file=sys.stderr)
        sys.exit(1)
    return sheet_name


def gen_feGs(_sheet, row_num, fegs=[], feg_num=1):
    def gen_fes(_row_num, fes=[]):
        if _row_num == _sheet.nrows or _sheet.cell(_row_num, 1).ctype == 0:
            return
        fe = {
            'name': _sheet.cell_value(_row_num, 1),
            'uuid': str(uuid.uuid4()),
            'type': _sheet.cell_value(_row_num, 2).title(),
            'concept': {
                'uuid': '',
                'name': '',
            },
            'displayOrder': _sheet.cell_value(_row_num, 0),
            'mandatory': True if _sheet.cell(_row_num, 3).value == 1 else False
        }
        fes.append(fe)
        gen_fes(_row_num + 1, fes)
        return fes, len(fes) + _row_num

    if row_num >= _sheet.nrows or _sheet.cell(row_num, 0).ctype == 0:
        return
    feg_name = _sheet.cell_value(row_num, 0)
    fes, new_row_num = gen_fes(row_num + 1)
    feg = {
        'name': feg_name,
        'uuid': str(uuid.uuid4()),
        'display': feg_name,
        'displayOrder': feg_num,
        'formElements': fes
    }
    fegs.append(feg)
    gen_feGs(_sheet, new_row_num, feg_num=feg_num+1)
    return fegs


if __name__ == '__main__':
    args = docopt(__doc__)
    fyl = validated_fyl(args['<excel-file>'])
    xl = xlrd.open_workbook(fyl)
    print_if_ps(args, xl)
    sheet = xl.sheet_by_name(validated_sheet_name(args['<sheet-name>'], xl))
    fEGs = gen_feGs(sheet, 1)
    form = {
        'name': sheet.name,
        'uuid': str(uuid.uuid4()),
        'type': '',
        'formElementGroups': fEGs
    }
    print(json.dumps(form, indent=4))
