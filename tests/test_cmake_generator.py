from hamcrest import assert_that, contains_string
from os.path import join

from testing_utils import BaseTestCase as TestCase
from vznncv.cubemx.tools._cmake_generator import generate_cmake_from_make
from vznncv.cubemx.tools._make_parser import parse_variables
from vznncv.cubemx.tools._project_description import build_project_description


class CMakeGeneratorTestCase(TestCase):
    def test_cmake_generation(self):
        project_dir = join(self.FIXTURE_DIR, 'stm32f3_project')
        make_file = join(project_dir, 'Makefile')
        make_vars = parse_variables(make_file)
        project_description = build_project_description(
            make_vars=make_vars,
            project_dir=project_dir
        )

        cmake_file = join(self.get_tmp_dir(), 'CMakeLists.txt')

        generate_cmake_from_make(project_description, cmake_file)

        # check cmake content
        with open(cmake_file, encoding='utf-8') as f:
            cmake_file_content = f.read()

        print(cmake_file_content)

        assert_that(cmake_file_content, contains_string('project(DemoProject)'))

        assert_that(cmake_file_content, contains_string('set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/build)'))

        assert_that(cmake_file_content, contains_string('"Drivers/CMSIS/Include"'))
        assert_that(cmake_file_content, contains_string('"Inc"'))

        assert_that(cmake_file_content, contains_string('"Src/*.cpp"'))
        assert_that(cmake_file_content, contains_string('"startup_stm32f303xc.s"'))

        assert_that(cmake_file_content, contains_string('add_definitions(-DSTM32F303xC)'))

        assert_that(cmake_file_content, contains_string(
            'set(OPTIMIZATION_FLAGS "" CACHE STRING "Optimization/debug flags")'))

        assert_that(cmake_file_content, contains_string('-mfpu=fpv4-sp-d16'))
        assert_that(cmake_file_content, contains_string('-mfloat-abi=hard'))
