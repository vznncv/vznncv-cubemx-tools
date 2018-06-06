import click
import logging
import os

from vznncv.cubemx.tools._project_processor import process_project


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def main():
    logging.basicConfig(level=logging.INFO)


@main.command(name='generate-cmake-project', help='Generate CMakeLists.txt and OpenOCD scripts for CubeMX project')
@click.option('--overwrite/--no-overwrite', 'overwrite',
              default=True, help='overwrite existed files')
@click.argument('project-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True),
                default=lambda: os.getcwd())
def generate_cmake_project(project_dir, overwrite):
    logging.info("Generate files ..")
    process_project(
        project_dir,
        overwrite=overwrite
    )
    logging.info("Complete")


if __name__ == '__main__':
    main()
