import os
from unittest import TestCase


# unittest for package src.confighandler
from src.config_handler import (
    ConfigType, 
    config_pool, 
    newConfig
)

class Test_ConfigHandler(TestCase):
    def setUp(self):
        self.tgt_prebuilt_xml   = 'foo.xml'
        self.tgt_prebuilt_json  = 'foo.json'
        self.tgt_prebuilt_ini   = 'foo.ini'

        self.tgt_prebuilt = [
            self.tgt_prebuilt_xml,
            self.tgt_prebuilt_json,
            self.tgt_prebuilt_ini
        ]

        self.tgt_prebuilt_payload_xml = """"""
        self.tgt_prebuilt_payload_json = """"""
        self.tgt_prebuilt_payload_ini = """"""

        with open(self.tgt_prebuilt_xml, 'w') as fo:
            fo.write(self.tgt_prebuilt_payload_xml)

        with open(self.tgt_prebuilt_json, 'w') as fo:
            fo.write(self.tgt_prebuilt_payload_json)

        with open(self.tgt_prebuilt_ini, 'w') as fo:
            fo.write(self.tgt_prebuilt_payload_ini)


    def tearDown(self):
        for fp in self.tgt_prebuilt:
            if os.path.exists(fp):
                os.remove(fp)

    def test_class_initiation(self):
        pass


if __name__ == '__main__':
    pass