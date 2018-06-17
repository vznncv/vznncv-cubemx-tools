from hamcrest import assert_that, contains_string
from os.path import join, exists

from testing_utils import BaseTestCase as TestCase
from vznncv.cubemx.tools._project_processor import process_project


class CMakeGeneratorTestCase(TestCase):
    def check_file_exists_and_contains(self, filepath, substring):
        assert_that(exists(filepath), 'File "{}" doesn\'t exists')
        with open(filepath, encoding='utf-8') as f:
            text = f.read()
        assert_that(text, contains_string(substring))

    def check_cmake(self, project_dir):
        cmake_file = join(project_dir, 'CMakeLists.txt')

        with open(cmake_file, encoding='utf-8') as f:
            cmake_file_content = f.read()

        assert_that(cmake_file_content, contains_string('project(DemoProject)'))

        assert_that(cmake_file_content, contains_string('set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/build)'))

        assert_that(cmake_file_content, contains_string('"Drivers/CMSIS/Include"'))
        assert_that(cmake_file_content, contains_string('"Inc"'))

        assert_that(cmake_file_content, contains_string('"Src/*.cpp"'))
        assert_that(cmake_file_content, contains_string('"startup_stm32f303xc.s"'))

        assert_that(cmake_file_content, contains_string('add_definitions(-DSTM32F303xC)'))

        assert_that(cmake_file_content, contains_string(
            'set(PROJECT_OPTIMIZATION_FLAGS "-g -O0" CACHE STRING "Optimization/debug flags")'
        ))

        assert_that(cmake_file_content, contains_string('-mfpu=fpv4-sp-d16'))
        assert_that(cmake_file_content, contains_string('-mfloat-abi=hard'))

    def test_process_project(self):
        project_dir = self.get_tmp_copy(join(self.FIXTURE_DIR, 'stm32f3_project'))

        process_project(project_dir, overwrite=True)

        self.check_file_exists_and_contains(join(project_dir, 'CMakeLists.txt'), 'project')
        self.check_file_exists_and_contains(join(project_dir, 'build.sh'), 'build_dir="build"')
        self.check_file_exists_and_contains(join(project_dir, 'openocd_stm.cfg'), 'source [find target/stm32f3x.cfg]')
        self.check_file_exists_and_contains(join(project_dir, 'upload-app.sh'), 'build_dir="build"')
