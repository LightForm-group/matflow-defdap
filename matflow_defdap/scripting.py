import re
from textwrap import dedent

import black
import autopep8

from pkg_resources import resource_string


def get_snippet(name):
    'Get a Python snippet function (as a string) from the snippets directory.'
    return resource_string('matflow_defdap', f'snippets/{name}').decode()


def parse_python_func_return(func_str):
    """Get a list of the variable names in a Python function return statement.

    The return statement may return a tuple (with parenthesis or not) or a single variable.

    """

    out = []
    match = re.search(r'return \(*([\S\s][^\)]+)\)*', func_str)
    if match:
        match_clean = match.group(1).strip().strip(',')
        out = [i.strip() for i in match_clean.split(',')]

    return out


def parse_python_func_imports(func_str):
    """Get a list of import statement lines from a (string) Python function."""

    import_lines = func_str.split('def ')[0].strip()
    match = re.search(r'((?:import|from)[\S\s]*)', import_lines)
    out = []
    if match:
        out = match.group(1).splitlines()

    return out


def get_snippet_signature(script_name):
    'Get imports, inputs and outputs of a Python snippet function.'
    snippet_str = get_snippet(script_name)
    def_line = re.search(r'def\s(.*)\(([\s\S]*?)\):', snippet_str).groups()
    func_name = def_line[0]
    func_ins = [i.strip() for i in def_line[1].split(',')]

    if script_name != func_name + '.py':
        msg = ('For simplicity, the snippet function name should be the same as the '
               'snippet file name.')
        raise ValueError(msg)

    func_outs = parse_python_func_return(snippet_str)
    func_imports = parse_python_func_imports(snippet_str)

    out = {
        'name': func_name,
        'imports': func_imports,
        'inputs': func_ins,
        'outputs': func_outs,
    }
    return out


def get_snippet_call(script_name):
    sig = get_snippet_signature(script_name)
    outs_fmt = ', '.join(sig['outputs'])
    ins_fmt = ', '.join(sig['inputs'])
    ret = f'{sig["name"]}({ins_fmt})'
    if outs_fmt:
        ret = f'{outs_fmt} = {ret}'
    return ret


def get_wrapper_script(script_name, snippets, outputs):

    ind = '    '
    sigs = [get_snippet_signature(i['name']) for i in snippets]
    all_ins = [j for i in sigs for j in i['inputs']]
    all_outs = [j for i in sigs for j in i['outputs']]

    for i in outputs:
        if i not in all_outs:
            raise ValueError(f'Cannot output "{i}". No functions return this name.')

    # Required inputs are those that are not output by any snippet
    req_ins = list(set(all_ins) - set(all_outs))
    req_ins_fmt = ', '.join(req_ins)

    main_sig = [f'def main({req_ins_fmt}):']
    main_body = [ind + get_snippet_call(i['name']) for i in snippets]
    main_outs = ['\n' + ind + f'return {", ".join([i for i in outputs])}']
    main_func = main_sig + main_body + main_outs

    req_imports = [
        'import sys',
        'import json',
        'import hickle',
        'from pathlib import Path',
    ]
    out = req_imports
    out += main_func
    snippet_funcs = '\n'.join([get_snippet(i['name']) for i in snippets])

    out = '\n'.join(out) + '\n' + snippet_funcs + '\n'
    out += dedent('''\
        if __name__ == '__main__':        
            inputs = hickle.load(sys.argv[1])
            outputs = main(**inputs)
            hickle.dump(outputs, 'outputs.hdf5')

    ''')

    out = autopep8.fix_code(out)
    out = black.format_str(out, mode=black.FileMode())

    return out
