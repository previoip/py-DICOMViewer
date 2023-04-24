from bootstrap import *
from sdl2 import *
from ctypes import byref


class CApp:
    def __init__(self):
        self._running = False
        self._sdl_window = None

    def onInit(self) -> int: 

        errno = SDL_Init(app_sdl_init_flags)
        if errno != 0:
            return errno

        self._sdl_window = SDL_CreateWindow(
            app_name,
            app_sdl_windowpos_x,
            app_sdl_windowpos_y,
            app_sdl_windowsize_w,
            app_sdl_windowsize_h,
            app_sdl_window_flags
        )

        if not self._sdl_window:
            return -1

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