import numpy as np
import cv2 as cv
from dataclasses import dataclass

from PyQt5.QtWidgets import (
    QLabel,
    QSlider,
    QDoubleSpinBox,
)

@dataclass
class WeightProperties:
    weight: int

    def __post_init__(self):
        self.widget = None

@dataclass
class FilterMorphologyProperties:
    kernel_x: int
    kernel_y: int
    iterations: int

    def __post_init__(self):
        self.widget = None


class BaseClassImageFilter:
    _inplace: bool = False
    _filter_display_name: str = ''
    _filter_display_desc: str = ''

    def __init__(self):
        self.properties = None

    def dispatch(self, dicom_ds, pixel_array) -> np.ndarray:
        raise NotImplementedError(f'{self.__class__} dispatch method is not yet overridden')

    def isInplaceOp(self):
        return self._inplace

    def displayName(self):
        return self._filter_display_name


class FilterTransformToHU(BaseClassImageFilter):
    _inplace = True
    _filter_display_name = 'Transform2HU'
    _filter_display_desc = 'Transform to Hounsfield Unit'

    def dispatch(self, dicom_ds, pixel_array):
        if not hasattr(dicom_ds, 'RescaleIntercept'):
            return
        if not hasattr(dicom_ds, 'RescaleSlope'):
            return
        slope = dicom_ds.RescaleSlope
        intercept = dicom_ds.RescaleIntercept

        np.multiply(pixel_array, slope, out=pixel_array)
        np.add(pixel_array, intercept, out=pixel_array)

class FilterMorphologyDilate(BaseClassImageFilter):
    _inplace = True
    _filter_display_name = 'Dilate'
    _filter_display_desc = 'Dilate Morphological Operation'

    def __init__(self):
        self.properties = FilterMorphologyProperties(5, 5, 1)

    def dispatch(self, dicom_ds, pixel_array):
        kernel = np.ones(
            (
                self.properties.kernel_x,
                self.properties.kernel_y
            ),
            pixel_array.type
        )
        cv.dilate(pixel_array, kernel, pixel_array, iterations=self.properties.iterations)

class FilterMorphologyErode(BaseClassImageFilter):
    _inplace = True
    _filter_display_name = 'Erode'
    _filter_display_desc = 'Erode Morphological Operation'

    def __init__(self):
        self.properties = FilterMorphologyProperties(5, 5, 1)


    def dispatch(self, dicom_ds, pixel_array):
        kernel = np.ones(
            (
                self.properties.kernel_x,
                self.properties.kernel_y
            ),
            pixel_array.type
        )
        cv.dilate(pixel_array, kernel, pixel_array, iterations=self.properties.iterations)


dicom_image_filters = [
    FilterTransformToHU,
    FilterMorphologyDilate,
    FilterMorphologyErode
]

def newFilter(filter_enum):
    return dicom_image_filters[filter_enum]()

class DicomImageFilterContainer:
    def __init__(self, dicom_ds_weakref):
        if not hasattr(dicom_ds_weakref, 'pixel_array'):
            raise AttributeError('pixel_array attribute is not present on the given object')

        if not isinstance(dicom_ds_weakref.pixel_array, np.ndarray):
            raise ValueError(f'pixel_array is not instance of numpy ndarray')

        self.__filter_steps = []
        self.dicom_ds_wr = dicom_ds_weakref
        self.pixel_array = self.dicom_ds_wr.pixel_array


    def getPixelArray(self):
        ret_arr = self.pixel_array.copy()
        for fil in self.__filter_steps:
            ret_arr = fil(self.dicom_ds_wr, ret_arr)
        return ret_arr