import os

import logging
from os.path import join, exists
import stat

from vznncv.cubemx.tools._cmake_generator import generate_cmake_from_make
from vznncv.cubemx.tools._make_parser import parse_variables
from vznncv.cubemx.tools._project_description import build_project_description
from vznncv.cubemx.tools._utils import get_template_environment

logger = logging.getLogger(__name__)


def add_executable_flag(script_file):
    """
    Try to add executable flag to file.
    """
    try:
        statinfo = os.stat(script_file)
        os.chmod(script_file, statinfo.st_mode | stat.S_IEXEC)
    except Exception:
        logger.warning("Fail to make file '{}' executable".format(script_file))


def generate_build_script(project_description, script_file):
    env = get_template_environment()
    build_script_template = env.get_template('build.sh')
    build_script_context = build_script_template.render(build_dir=project_description.build_dir)
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(build_script_context)
    add_executable_flag(script_file)


def generate_flush_script(project_description, script_file):
    env = get_template_environment()
    build_script_template = env.get_template('upload-app.sh')
    build_script_context = build_script_template.render(build_dir=project_description.build_dir)
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(build_script_context)
    add_executable_flag(script_file)


def generate_openocd_script(project_description, script_file):
    env = get_template_environment()
    build_script_template = env.get_template('openocd_stm.cfg')
    build_script_context = build_script_template.render(stm_target="{}x".format(project_description.stm_series))
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(build_script_context)


def generate_gitignore(project_description, script_file):
    env = get_template_environment()
    gitignore_template = env.get_template('gitignore_template')
    gitignore_text = gitignore_template.render()
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(gitignore_text)


def write_file(dst_file, project_description, generate_fun, overwrite):
    if exists(dst_file):
        if overwrite:
            logger.info("Overwrite file '{}'".format(dst_file))
            generate_fun(project_description, dst_file)
        else:
            logger.info("File '{}' already exists. Skip ...".format(dst_file))
    else:
        logger.info("Create file '{}'".format(dst_file))
        generate_fun(project_description, dst_file)


def process_project(project_dir, overwrite=True, autodiscover_sources=False):
    """
    Prepare generated cubemx project for cmake and openocd usage.

    :param project_dir: project_directory
    :param autodiscover_sources: autodiscover source files instead of Makefile usage
    :param overwrite: overwrite existed files
    """
    # parse makefile
    make_file = join(project_dir, 'Makefile')
    make_vars = parse_variables(make_file)
    project_description = build_project_description(
        make_vars=make_vars,
        project_dir=project_dir,
        optimization_flags=["-g", "-O0"],
        autodiscover_sources=autodiscover_sources
    )

    # generate cmake
    write_file(
        dst_file=join(project_dir, 'CMakeLists.txt'),
        project_description=project_description,
        generate_fun=generate_cmake_from_make,
        overwrite=overwrite
    )
    # generate build script
    write_file(
        dst_file=join(project_dir, 'build.sh'),
        project_description=project_description,
        generate_fun=generate_build_script,
        overwrite=overwrite
    )
    # generate upload script
    write_file(
        dst_file=join(project_dir, 'upload-app.sh'),
        project_description=project_description,
        generate_fun=generate_flush_script,
        overwrite=overwrite
    )
    # generate openocd script
    write_file(
        dst_file=join(project_dir, 'openocd_stm.cfg'),
        project_description=project_description,
        generate_fun=generate_openocd_script,
        overwrite=False
    )
    # generate .gitignore
    write_file(
        dst_file=join(project_dir, '.gitignore'),
        project_description=project_description,
        generate_fun=generate_gitignore,
        overwrite=False
    )
