# ===============================================
# bootstrap.py
# stores default fallback configuration values 
# and various inits
# ===============================================

import sys, os

# program defaults
app_name                    = b'Simple DICOM Viewer'
app_version                 = b'0.0.0.1'
app_path_storage_temp       = './tempstorage'
app_fpath_license           = './LICENSE'

system_encoding             = sys.getfilesystemencoding()

# pydicom defaults
from pydicom.data import get_testdata_files
test_preset_data_path       = os.path.commonpath(get_testdata_files())

# inits

with open(app_fpath_license, 'r', encoding='utf8') as fo:
    app_prefetch_license = fo.read()

