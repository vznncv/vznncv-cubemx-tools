from os.path import isdir, basename, join, dirname

import shutil
import tempfile
from unittest import TestCase


class BaseTestCase(TestCase):
    FIXTURE_DIR = join(dirname(__file__), 'fixtures')

    def get_tmp_dir(self):
        tmp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp_dir)
        return tmp_dir

    def get_tmp_copy(self, fixture_dir):
        tmp_dir = self.get_tmp_dir()
        if not isdir(fixture_dir):
            raise ValueError("{} isn't directory".format(fixture_dir))
        fixture_name = basename(fixture_dir)
        tmp_fixture_dir = join(tmp_dir, fixture_name)
        shutil.copytree(fixture_dir, tmp_fixture_dir)
        return tmp_fixture_dir
