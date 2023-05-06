import numpy as np
from enum import Flag, auto

class DicomImageFilterFlags(Flag):
    TRANSFORM_HU = auto()

class DicomImageFilter:
    def __init__(self, dicom_ds_weakref):
        if not hasattr(dicom_ds_weakref, 'pixel_array'):
            raise AttributeError('pixel_array attribute is not present on the given object')

        if not isinstance(dicom_ds_weakref.pixel_array, np.ndarray):
            raise ValueError(f'pixel_array is not instance of numpy ndarray')

        self.dicom_ds_wr = dicom_ds_weakref
        self.pixel_array = self.dicom_ds_wr.pixel_array


    def getPixelArray(self):
        return self.pixel_array

    def transformToHU(self):
        if not hasattr(self.dicom_ds_wr, 'RescaleIntercept'):
            return
        if not hasattr(self.dicom_ds_wr, 'RescaleSlope'):
            return
        intercept = self.dicom_ds_wr.RescaleIntercept
        slope = self.dicom_ds_wr.RescaleSlope
        self.pixel_array = self.pixel_array * slope + intercept


