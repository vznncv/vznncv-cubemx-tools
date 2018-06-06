from collections import namedtuple

import re


def parse_make_var_array(var_value):
    values = re.split(r'(?<!\\)\s+', var_value)
    values = [val.strip() for val in values]
    values = [val for val in values if val]
    return values


def parse_make_var_defines(var_value):
    raw_defines = parse_make_var_array(var_value)
    defines = []
    for define in raw_defines:
        if not define.startswith('-D'):
            raise ValueError("Invalid definition: {}".format(define))
        defines.append(define[2:])
    return defines


def parse_make_var_paths(var_value):
    paths = parse_make_var_array(var_value)
    return [p.lstrip('/') for p in paths]


def parse_make_var_single_value(var_value):
    values = parse_make_var_array(var_value)
    if len(values) != 1:
        raise ValueError("The '{}' doesn't contain single value".format(var_value))
    return values[0]


def parse_make_var_path(var_value):
    return parse_make_var_single_value(var_value).lstrip('/')


def parse_make_var_includes(var_value):
    raw_paths = parse_make_var_array(var_value)
    paths = []
    for raw_path in raw_paths:
        if not raw_path.startswith('-I'):
            raise ValueError("Make include option should have -I prefix, but it was {}".format(raw_path))
        paths.append(raw_path[2:])
    return paths


def detect_stm_series(defines):
    for define in defines:
        m = re.search(r'(?P<stm_series>stm32[fl]\d)', define, re.IGNORECASE)
        if m:
            return m.group('stm_series').lower()
    raise ValueError('Cannot detect stm series from definitions: {}'.format(defines))


ProjectDescription = namedtuple('ProjectDescription', [
    'build_dir',
    'target',
    'stm_series',
    'project_dir',

    'source_files',
    'include_dirs',
    'definitions',
    'mcu_flags',
    'optimization_flags',
    'ld_script'
])


def build_project_description(make_vars, project_dir, optimization_flags=None):
    build_dir = parse_make_var_path(make_vars.get('BUILD_DIR', 'build'))
    target = parse_make_var_single_value(make_vars['TARGET'])

    c_sources = parse_make_var_paths(make_vars['C_SOURCES'])
    asm_sources = parse_make_var_paths(make_vars['ASM_SOURCES'])
    periflib_sources = parse_make_var_paths(make_vars['PERIFLIB_SOURCES'])

    as_includes = parse_make_var_includes(make_vars['AS_INCLUDES'])
    c_includes = parse_make_var_includes(make_vars['C_INCLUDES'])

    c_defs = parse_make_var_defines(make_vars['C_DEFS'])
    as_defs = parse_make_var_defines(make_vars['AS_DEFS'])

    mcu_flags = parse_make_var_array(make_vars['MCU'])

    ld_script = parse_make_var_path(make_vars['LDSCRIPT'])

    stm_series = detect_stm_series(c_defs)

    return ProjectDescription(
        build_dir=build_dir,
        target=target,
        stm_series=stm_series,
        project_dir=project_dir,

        source_files=sorted(set(c_sources) | set(asm_sources) | set(periflib_sources)),
        include_dirs=sorted(set(c_includes) | set(as_includes)),
        definitions=sorted(set(c_defs) | set(as_defs)),
        mcu_flags=mcu_flags,
        optimization_flags=optimization_flags or '',

        ld_script=ld_script
    )
