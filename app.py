from src.constants import *
from sdl2 import *
from ctypes import byref
# from src.confighandler import ConfigType


class CApp:
    def __init__(self):
        self._running = False
        self._sdl_window = None

    def onInit(self) -> int: 

        if SDL_Init(APP_SDL_INIT_FLAGS) != 0:
            return -1

        self._sdl_window = SDL_CreateWindow(
            APP_NAME,
            APP_SDL_WINDOWPOS_X,
            APP_SDL_WINDOWPOS_Y,
            APP_SDL_WINDOWSIZE_W,
            APP_SDL_WINDOWSIZE_H,
            APP_SDL_WINDOW_FLAGS
        )

        return 0


    def onEvent(self, event) -> int:

        if event.type == SDL_QUIT:
            self._running = False
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


    def onExecute(self):
        if self.onInit() != 0:
            return -1

        event = SDL_Event()

        self._running = True
        while self._running:
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