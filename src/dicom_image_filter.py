import numpy as np
import cv2 as cv
from dataclasses import dataclass

from PyQt5.QtWidgets import (
    QGroupBox,
    QLabel,
    QSlider,
    QSpinBox,
    QDoubleSpinBox,
    QFormLayout,
)

from PyQt5.QtCore import pyqtSignal

@dataclass
class WeightProperties:
    weight: int

    def __post_init__(self):
        self.widget_constructors = [
            self.__widget_weight,
        ]

    def hasWidget(self):
        return len(self.widget_constructors) > 0

    def buildWidget(self, parent, formLayout):
        for row, fn in enumerate(self.widget_constructors):
            fn(row, parent, formLayout)

    def __widget_weight(self, row, parent, formLayout):
        label = QLabel(parent)
        label.setText('weight')
        formLayout.setWidget(row, QFormLayout.LabelRole, label)
        spinbox = QSpinBox(parent)
        spinbox.setValue(self.weight)
        formLayout.setWidget(row, QFormLayout.FieldRole, spinbox)
        spinbox.valueChanged.connect(parent.filter_signal.emit)



@dataclass
class FilterMorphologyProperties:
    kernel_x: int
    kernel_y: int
    iterations: int

    def __post_init__(self):
        self.widget_constructors = [
            self.__widget_kernelx,
            self.__widget_kernely,
            self.__widget_iteration,
        ]

    def hasWidget(self):
        return len(self.widget_constructors) > 0

    def buildWidget(self, parent, formLayout):
        for row, fn in enumerate(self.widget_constructors):
            fn(row, parent, formLayout)

    def __widget_kernelx(self, row, parent, formLayout):
        label = QLabel(parent)
        label.setText('kernel x')
        formLayout.setWidget(row, QFormLayout.LabelRole, label)
        spinbox = QSpinBox(parent)
        spinbox.setValue(self.kernel_x)
        spinbox.valueChanged.connect(lambda _: aetattr(self, 'kernel_x', spinbox.value()))
        formLayout.setWidget(row, QFormLayout.FieldRole, spinbox)
        spinbox.valueChanged.connect(parent.filter_signal.emit)

    def __widget_kernely(self, row, parent, formLayout):
        label = QLabel(parent)
        label.setText('kernel y')
        formLayout.setWidget(row, QFormLayout.LabelRole, label)
        spinbox = QSpinBox(parent)
        spinbox.setValue(self.kernel_y)
        spinbox.valueChanged.connect(lambda _: setattr(self, 'kernel_y', spinbox.value()))
        formLayout.setWidget(row, QFormLayout.FieldRole, spinbox)
        spinbox.valueChanged.connect(parent.filter_signal.emit)

    def __widget_iteration(self, row, parent, formLayout):
        label = QLabel(parent)
        label.setText('iteration')
        formLayout.setWidget(row, QFormLayout.LabelRole, label)
        spinbox = QSpinBox(parent)
        spinbox.setValue(self.iterations)
        spinbox.valueChanged.connect(lambda _: setattr(self, 'iterations', spinbox.value()))
        formLayout.setWidget(row, QFormLayout.FieldRole, spinbox)
        spinbox.valueChanged.connect(parent.filter_signal.emit)

class BaseClassImageFilter:
    _inplace: bool = False
    _display_name: str = ''
    _display_desc: str = ''

    def __init__(self):
        self.properties = None

    def dispatch(self, dicom_ds, pixel_array) -> np.ndarray:
        raise NotImplementedError(f'{self.__class__} dispatch method is not yet overridden')

    def isInplaceOp(self):
        return self._inplace

    def displayName(self):
        return self._display_name


class FilterTransformToHU(BaseClassImageFilter):
    _inplace = False
    _display_name = 'Transform2HU'
    _display_desc = 'Transform to Hounsfield Unit'

    def __init__(self):
        super().__init__()

    def dispatch(self, dicom_ds, pixel_array):
        if not hasattr(dicom_ds, 'RescaleIntercept'):
            return
        if not hasattr(dicom_ds, 'RescaleSlope'):
            return
        slope = dicom_ds.RescaleSlope
        intercept = dicom_ds.RescaleIntercept

        # np.multiply(pixel_array, slope, out=pixel_array)
        # np.add(pixel_array, intercept, out=pixel_array)
        return pixel_array * slope + intercept


class FilterMorphologyDilate(BaseClassImageFilter):
    _inplace = True
    _display_name = 'Dilate'
    _display_desc = 'Dilate Morphological Operation'

    def __init__(self):
        self.properties = FilterMorphologyProperties(5, 5, 1)

    def dispatch(self, dicom_ds, pixel_array):
        kernel = np.ones(
            (
                self.properties.kernel_x,
                self.properties.kernel_y
            ),
            pixel_array.dtype
        )
        cv.dilate(pixel_array, kernel, pixel_array, iterations=self.properties.iterations)

class FilterMorphologyErode(BaseClassImageFilter):
    _inplace = True
    _display_name = 'Erode'
    _display_desc = 'Erode Morphological Operation'

    def __init__(self):
        self.properties = FilterMorphologyProperties(5, 5, 1)

    def dispatch(self, dicom_ds, pixel_array):
        kernel = np.ones(
            (
                self.properties.kernel_x,
                self.properties.kernel_y
            ),
            pixel_array.dtype
        )
        cv.erode(pixel_array, kernel, pixel_array, iterations=self.properties.iterations)


dicom_image_filters = [
    FilterTransformToHU,
    FilterMorphologyDilate,
    FilterMorphologyErode
]



def newFilter(filter_enum):
    return dicom_image_filters[filter_enum]()