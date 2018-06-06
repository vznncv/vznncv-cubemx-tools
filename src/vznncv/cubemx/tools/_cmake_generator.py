from collections import defaultdict

import fnmatch
import logging
import os
from os.path import join, abspath, isfile, dirname, basename

from ._utils import get_template_environment

logger = logging.getLogger(__name__)


class CMakeGenerator:
    """
    CMakeList.txt generator for STM32 CubeMX project with makefile.
    """

    _GLOB_SOURCES = {'*.c', '*.cpp'}
    _REMOVE_GLOB_SOURCES = {'*_template.*'}

    _STM_HAL_DRIVER = 'Drivers/STM32*HAL*/Src'

    def _process_source_files(self, project_dir, sources):
        # split sources by directories
        source_dirs = defaultdict(lambda: set())
        for source in sources:
            source_path = abspath(join(project_dir, source))
            if not isfile(source_path):
                raise ValueError("Source must contain only files, but it contains {}".format(source))
            source_dir = dirname(source)
            source_basename = basename(source)
            source_dirs[source_dir].add(source_basename)

        # try to add some optimization for source directories
        optimized_source_dirs = {}
        for source_dir, source_files in source_dirs.items():
            source_dir_path = join(project_dir, source_dir)
            dir_files = {dir_file for dir_file in os.listdir(source_dir_path)
                         if isfile(join(source_dir_path, dir_file))}
            glob_files = {
                dir_file for dir_file in dir_files
                if any(fnmatch.fnmatch(dir_file, glob_template)
                       for glob_template in self._GLOB_SOURCES)
            }
            if glob_files and glob_files.issubset(source_files):
                source_info = {
                    'files': source_files - glob_files,
                    'globs': self._GLOB_SOURCES
                }
            else:
                source_info = {'files': source_files}
            optimized_source_dirs[source_dir] = source_info
        # special case for 'Src' directory
        optimized_source_dirs['Src'] = {'globs': self._GLOB_SOURCES}
        # special case for HAL driver
        for source_dir, source_info in optimized_source_dirs.items():
            if fnmatch.fnmatch(source_dir, self._STM_HAL_DRIVER):
                source_info.pop('files', None)
                source_info['globs'] = self._GLOB_SOURCES
                source_info['remove_files'] = {
                    hal_file for hal_file in os.listdir(join(project_dir, source_dir))
                    if any(fnmatch.fnmatch(hal_file, glob_template)
                           for glob_template in self._REMOVE_GLOB_SOURCES)
                }
                break

        # split optimized_source_dirs into 3 category
        globs = []
        remove_files = []
        files = []
        for source_dir in sorted(optimized_source_dirs):
            source_info = optimized_source_dirs[source_dir]
            for source_glob in source_info.get('globs', set()):
                globs.append('{}/{}'.format(source_dir, source_glob).lstrip('/'))
            for source_file in source_info.get('files', set()):
                files.append('{}/{}'.format(source_dir, source_file).lstrip('/'))
            for source_remove_file in source_info.get('remove_files', set()):
                remove_files.append('{}/{}'.format(source_dir, source_remove_file).lstrip('/'))

        return globs, remove_files, files

    def generate_from_make(self, project_description, cmake_file):

        # optimize source file location
        source_globs, source_remove_files, source_files = self._process_source_files(
            project_dir=project_description.project_dir,
            sources=project_description.source_files
        )

        # render cmakefile
        env = get_template_environment()
        cmake_template = env.get_template('CmakeLists.txt')
        cmake_context = {
            'cmake_version': '3.5',
            'project': {
                'name': project_description.target,
                'include_dirs': project_description.include_dirs,
                'source': {
                    'globs': source_globs,
                    'remove_files': source_remove_files,
                    'files': source_files
                },
                'build_dir': project_description.build_dir,
                'definitions': project_description.definitions,
                'mcu_flags': project_description.mcu_flags,
                'optimization_flags': project_description.optimization_flags,
                'ld_script': project_description.ld_script
            }
        }

        cmake_file_content = cmake_template.render(cmake_context)

        # save cmakefile
        with open(cmake_file, 'w', encoding='utf-8') as f:
            f.write(cmake_file_content)


def generate_cmake_from_make(project_description, cmake_file):
    """
    Generate cmake file.

    :param project_description: :class:`ProjectDescription` object
    :param cmake_file: cmake file path
    """
    CMakeGenerator().generate_from_make(project_description, cmake_file)
