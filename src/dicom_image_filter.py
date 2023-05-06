import numpy as np
from enum import Flag, auto
import cv2 as cv


class DicomImageFilterFlags(Flag):
    __DEFAULT = auto()
    IGNORE = auto()
    TRANSFORM_HU = auto()
    DILATE = auto()
    ERODE = auto()

class ImageFilters:

    @staticmethod
    def transformToHU(dicom_ds, pixel_array):
        if not hasattr(dicom_ds, 'RescaleIntercept'):
            return
        if not hasattr(dicom_ds, 'RescaleSlope'):
            return
        intercept = dicom_ds.RescaleIntercept
        slope = dicom_ds.RescaleSlope

        return pixel_array * slope + intercept

    @staticmethod
    def dilate(dicom_ds, pixel_array):
        kernel = np.ones((5,5), np.uint8)
        return cv.dilate(pixel_array, kernel, iterations=1)

    @staticmethod
    def erode(dicom_ds, pixel_array):
        kernel = np.ones((5,5), np.uint8)
        return cv.erode(pixel_array, kernel, iterations=1)


image_filters = {
    DicomImageFilterFlags.TRANSFORM_HU : ImageFilters.transformToHU,
    DicomImageFilterFlags.DILATE : ImageFilters.dilate,
    DicomImageFilterFlags.ERODE : ImageFilters.erode,
}



class DicomImageFilterContainer:
    def __init__(self, dicom_ds_weakref):
        if not hasattr(dicom_ds_weakref, 'pixel_array'):
            raise AttributeError('pixel_array attribute is not present on the given object')

        if not isinstance(dicom_ds_weakref.pixel_array, np.ndarray):
            raise ValueError(f'pixel_array is not instance of numpy ndarray')

        self.__filter_steps = []
        self.dicom_ds_wr = dicom_ds_weakref
        self.pixel_array = self.dicom_ds_wr.pixel_array
        self.filter_flags = DicomImageFilterFlags.__DEFAULT

    def setFilterFlags(self, filter_flags):
        if DicomImageFilterFlags.IGNORE in filter_flags:
            return

        for k in image_filters.keys():
            if k == DicomImageFilterFlags.__DEFAULT:
                continue
            if k in filter_flags:
                filter_fn = image_filters.get(k)
                assert callable(filter_fn)
                self.__filter_steps.append(filter_fn)

    def getPixelArray(self):
        ret_arr = self.pixel_array.copy()
        for fil in self.__filter_steps:
            ret_arr = fil(self.dicom_ds_wr, ret_arr)
        return ret_arr




