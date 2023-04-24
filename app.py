from bootstrap import *
from sdl2 import *
from ctypes import byref

from src.config_manager import (
    newConfigFromPath,
    saveAllConfig
)

class CApp:
    def __init__(self):
        self._app_config_default    = newConfigFromPath('default', app_fpath_config)
        self._app_name              = app_name
        self._app_sdl_windowpos_x   = app_sdl_windowpos_x
        self._app_sdl_windowpos_y   = app_sdl_windowpos_y
        self._app_sdl_windowsize_w  = app_sdl_windowsize_w
        self._app_sdl_windowsize_h  = app_sdl_windowsize_h
        self._app_sdl_window_flags  = app_sdl_window_flags
        self._sdl_running           = False
        self._sdl_window            = None


    def onInit(self) -> int: 
        
        self._app_config_default.load()
        cfg_root = self._app_config_default.data.getroot()
        if cfg_root is not None and cfg_root.get('start_default') == '1':
            cfg_app = cfg_root.find('App')
            if cfg_app.get('window_size_w') is not None:
                self._app_sdl_windowsize_w = int(cfg_app.get('window_size_w'))
            if cfg_app.get('window_size_h') is not None:
                self._app_sdl_windowsize_h = int(cfg_app.get('window_size_h'))

        errno = SDL_Init(app_sdl_init_flags)
        if errno != 0:
            return errno

        self._sdl_window = SDL_CreateWindow(
            self._app_name,
            self._app_sdl_windowpos_x,
            self._app_sdl_windowpos_y,
            self._app_sdl_windowsize_w,
            self._app_sdl_windowsize_h,
            self._app_sdl_window_flags
        )

        if not self._sdl_window:
            return -1

        return 0


    def onEvent(self, event) -> int:

        if event.type == SDL_QUIT:
            self._sdl_running = False
            return 1

        else:
            return 0

    def onLoop(self):
        ...

    def onRender(self):
        ...

    def onCleanup(self): 
        SDL_DestroyWindow(self._sdl_window)
        SDL_Quit()
        saveAllConfig()


    def onExecute(self):
        if self.onInit() != 0:
            return -1

        event = SDL_Event()

        self._sdl_running = True
        while self._sdl_running:
            while SDL_PollEvent(byref(event)):
                if self.onEvent(event) != 0:
                    break

            self.onLoop()
            self.onRender()

        self.onCleanup()
        return 0


def main():
    app = CApp()
    return app.onExecute()