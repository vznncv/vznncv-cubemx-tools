import logging
from os.path import join, exists

from vznncv.cubemx.tools._cmake_generator import generate_cmake_from_make
from vznncv.cubemx.tools._make_parser import parse_variables
from vznncv.cubemx.tools._project_description import build_project_description
from vznncv.cubemx.tools._utils import get_template_environment

logger = logging.getLogger(__name__)


def generate_build_script(project_description, script_file):
    env = get_template_environment()
    build_script_template = env.get_template('build.sh')
    build_script_context = build_script_template.render(build_dir=project_description.build_dir)
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(build_script_context)


def generate_flush_script(project_description, script_file):
    env = get_template_environment()
    build_script_template = env.get_template('flush.sh')
    build_script_context = build_script_template.render(build_dir=project_description.build_dir)
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(build_script_context)


def generate_openocd_script(project_description, script_file):
    env = get_template_environment()
    build_script_template = env.get_template('openocd_stm.cfg')
    build_script_context = build_script_template.render(stm_target="{}x".format(project_description.stm_series))
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(build_script_context)


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


def process_project(project_dir, overwrite=True):
    """
    Prepare generated cubemx project for cmake and openocd usage.

    :param project_dir: project_directory
    :param overwrite: overwrite existed files
    """
    # parse makefile
    make_file = join(project_dir, 'Makefile')
    make_vars = parse_variables(make_file)
    project_description = build_project_description(
        make_vars=make_vars,
        project_dir=project_dir
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
    # generate flush script
    write_file(
        dst_file=join(project_dir, 'flush.sh'),
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
