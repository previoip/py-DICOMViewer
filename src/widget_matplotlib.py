
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)


# HEY
# you might read this and asks yourself what?
# I've found a method to exclude toolitem for
# matplotlib navigation toolbar derived from
# qt5agg backend. Just in case you might be 
# wondering why, usually canvas object have 
#      remove_toolitem()
# bound method to remove toolbar item which 
# is missing in the backend implementation.

# but by looking at the source code, the items
# is a class attribute on its own and thus
# removing it is as straightforward as follows.


class WidgetMplToolbar(NavigationToolbar): pass

__ti = WidgetMplToolbar.toolitems # or NavigationToolbar2QT.toolitems
__ti.pop(
    __ti.index(
        next(filter(
            lambda a: 'configure_subplots' in a,
            __ti 
        ))
    )
)

# what the above just do uis to remove
# 'configure_subplots' button, which in this
# app, this toolbar always raises UserWarning
# compat with tight_layout, which I find jarring

# you can check it at the following git 
# https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/backends/backend_qt.py#L624



class WidgetMplCanvas(FigureCanvas):
    def __init__(self, parent):
        self.fig, self.ax = plt.subplots(
            dpi=72,
            layout="constrained"
        )
        super().__init__(self.fig)
        self.__pixel_arr = []
        self.__axImg = None
        self.__dicom_ds_wr = None
        self.setParent(parent)
        self.ax.margins(0)
        self.ax.set_aspect('auto', 'datalim')
        self.cmap = plt.cm.gray

    def resizeFitToParentWidget(self):
        parent_frame_geom = self.parent().frameGeometry()
        self.setGeometry(parent_frame_geom)

    def updateImage(self):
        if self.__axImg is not None:
            self.cmap = self.__axImg.get_cmap()
        if self.__pixel_arr is None or len(self.__pixel_arr) == 0:
            return
        self.ax.cla()
        self.__axImg = self.ax.imshow(self.__pixel_arr, cmap=self.cmap)
        self.draw()

    def setArr(self, pixel_arr):
        self.__pixel_arr = pixel_arr

    def getDsWr(self):
        return self.__dicom_ds_wr

    def setDsWr(self, obj):
        self.__dicom_ds_wr = obj


    def dispatchSetArr(self, diocom_ds):
        if not hasattr(diocom_ds, 'pixel_array'):
            raise AttributeError('pixel_array attribute is not present on the given object')
        self.setDsWr(diocom_ds)
        if hasattr(diocom_ds, 'getPixelArray'):
            self.setArr(diocom_ds.getPixelArray())
        else:
            self.setArr(diocom_ds.pixel_array)
