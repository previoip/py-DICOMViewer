# ===============================================
# bootstrap.py
# stores default fallback configuration values 
# and various inits
# ===============================================

# sdl2 defaults
from sdl2 import *

app_name                = b'foobar'
app_sdl_init_flags      = SDL_INIT_VIDEO | SDL_INIT_AUDIO
app_sdl_windowsize_w    = 640
app_sdl_windowsize_h    = 480
app_sdl_windowpos_x     = SDL_WINDOWPOS_UNDEFINED
app_sdl_windowpos_y     = SDL_WINDOWPOS_UNDEFINED
app_sdl_window_flags    = SDL_WINDOW_RESIZABLE | SDL_WINDOW_SHOWN

# program defaults
app_path_storage_temp       = './tempstorage'
app_path_storage_resource   = './Resource'
app_fpath_config            = './config.xml'