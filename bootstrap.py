# ===============================================
# bootstrap.py
# stores default fallback configuration values 
# and various inits
# ===============================================

import sys, os

# program defaults
app_name                    = b'foobar'
app_path_storage_temp       = './tempstorage'
app_path_storage_cache      = './cache'
app_path_storage_resource   = './Resource'
app_fpath_config            = './config.xml'
app_fpath_license           = './LICENSE'

system_encoding             = sys.getfilesystemencoding()

app_window_min_width        = 640
app_window_min_height       = 480

# sdl2 defaults
from sdl2 import *

app_sdl_init_flags          = SDL_INIT_VIDEO | SDL_INIT_AUDIO
app_sdl_window_flags        = SDL_WINDOW_RESIZABLE | SDL_WINDOW_SHOWN

# pydicom defaults
from pydicom.data import get_testdata_files
test_preset_data_path       = os.path.commonpath(get_testdata_files())


# inits

with open(app_fpath_license, 'r', encoding='utf8') as fo:
    app_prefetch_license = fo.read()

