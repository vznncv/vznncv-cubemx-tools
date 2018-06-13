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

    def test_process_project(self):
        project_dir = self.get_tmp_copy(join(self.FIXTURE_DIR, 'stm_project'))

        process_project(project_dir, overwrite=True)

        self.check_file_exists_and_contains(join(project_dir, 'CMakeLists.txt'), 'project')
        self.check_file_exists_and_contains(join(project_dir, 'build.sh'), 'build_dir="build"')
        self.check_file_exists_and_contains(join(project_dir, 'openocd_stm.cfg'), 'source [find target/stm32f3x.cfg]')
        self.check_file_exists_and_contains(join(project_dir, 'upload-app.sh'), 'build_dir="build"')
