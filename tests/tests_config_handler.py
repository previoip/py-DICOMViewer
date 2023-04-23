import os
import unittest


# unittest for package src.confighandler
from src.config_handler import (
    ConfigType, 
    newConfig,
    _config_pool
)

# globals
script_dir = os.path.dirname(__file__) 

class TestAttrs:
    fp_emp_xml   = os.path.join(script_dir, 'test_empty.xml')
    fp_emp_json  = os.path.join(script_dir, 'test_empty.json')
    fp_emp_ini   = os.path.join(script_dir, 'test_empty.ini')
    fp_def_xml   = os.path.join(script_dir, 'test.xml')
    fp_def_json  = os.path.join(script_dir, 'test.json')
    fp_def_ini   = os.path.join(script_dir, 'test.ini')

    def initAttrs(self):
        self.ls_def = [
            self.fp_def_xml,
            self.fp_def_json,
            self.fp_def_ini
        ]


class Test_ConfigHandler(TestAttrs, unittest.TestCase):
    def setUp(self):
        self.initAttrs()

    def tearDown(self):
        for fp in self.ls_def:
            if os.path.exists(fp):
                os.remove(fp)

    def test_class_initiation(self):
        pass


if __name__ == '__main__':
    unittest.main()