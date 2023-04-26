# ===============================================
# bootstrap.py
# stores default fallback configuration values 
# and various inits
# ===============================================

import sys

# program defaults
app_name                    = b'foobar'
app_path_storage_temp       = './tempstorage'
app_path_storage_resource   = './Resource'
app_fpath_config            = './config.xml'
system_encoding             = sys.getfilesystemencoding()

app_window_min_width            = 640
app_window_min_height           = 480

# sdl2 defaults
from sdl2 import *

app_sdl_init_flags      = SDL_INIT_VIDEO | SDL_INIT_AUDIO
app_sdl_window_flags    = SDL_WINDOW_RESIZABLE | SDL_WINDOW_SHOWN

