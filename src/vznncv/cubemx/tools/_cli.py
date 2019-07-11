import click
import logging
import os


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


@main.command(name='generate-cmake-project', help='Generate CMakeLists.txt and OpenOCD scripts for CubeMX project')
@click.option('--overwrite/--no-overwrite', 'overwrite',
              default=True, help='overwrite existed files')
@click.option('--autodiscover-sources', '-s', default=False, is_flag=True)
@click.argument('project-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True),
                default=lambda: os.getcwd())
def generate_cmake_project(project_dir, overwrite, autodiscover_sources):
    logging.info("Generate files ..")

    from vznncv.cubemx.tools._project_processor import process_project
    process_project(
        project_dir,
        overwrite=overwrite,
        autodiscover_sources=autodiscover_sources
    )

    logging.info("Complete")


if __name__ == '__main__':
    main()
