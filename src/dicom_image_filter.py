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
    QCheckBox,
)

from PyQt5.QtCore import pyqtSignal

class PropertyWidget:
    @staticmethod
    def newLabel(row, formLayout, text, parent=None):
        label = QLabel(parent)
        label.setText(text)
        formLayout.setWidget(row, QFormLayout.LabelRole, label)
        return label

    @staticmethod
    def newSpinBox(row, formLayout, prop, attr, parent=None):
        spinbox = QSpinBox(parent)
        spinbox.setValue(getattr(prop, attr))
        spinbox.valueChanged.connect(lambda _: setattr(prop, attr, spinbox.value()))
        formLayout.setWidget(row, QFormLayout.FieldRole, spinbox)
        return spinbox

    @staticmethod
    def newDoubleSpinBox(row, formLayout, prop, attr, parent=None):
        spinbox = QDoubleSpinBox(parent)
        spinbox.setValue(getattr(prop, attr))
        spinbox.setSingleStep(.01)
        spinbox.valueChanged.connect(lambda _: setattr(prop, attr, spinbox.value()))
        formLayout.setWidget(row, QFormLayout.FieldRole, spinbox)
        return spinbox

    @staticmethod
    def newCheckBox(row, formLayout, prop, attr, parent=None):
        checkbox = QCheckBox(parent)
        checkbox.setCheckState(getattr(prop, attr))
        checkbox.stateChanged.connect(lambda _: setattr(prop, attr, checkbox.checkState()))
        formLayout.setWidget(row, QFormLayout.FieldRole, checkbox)
        return checkbox

def wrapOdd(num):
    if num != 0 and num % 2 == 0:
        return num // 2 + 1
    return num

class BaseProperties:
    def hasWidget(self):
        return len(self.widget_constructors) > 0
    
    def buildWidget(self, parent, formLayout):
        for row, fn in enumerate(self.widget_constructors):
            fn(row, parent, formLayout)

@dataclass
class WeightProperties(BaseProperties):
    weight: int

    def __post_init__(self):
        self.widget_constructors = [
            self.__widget_weight,
        ]

    def __widget_weight(self, row, parent, formLayout):
        label = QLabel(parent)
        label.setText('weight')
        formLayout.setWidget(row, QFormLayout.LabelRole, label)
        spinbox = QDoubleSpinBox(parent)
        spinbox.setValue(self.weight)
        formLayout.setWidget(row, QFormLayout.FieldRole, spinbox)
        spinbox.valueChanged.connect(parent.filter_signal.emit)


@dataclass
class FilterMorphologyProperties(BaseProperties):
    kernel_x: int
    kernel_y: int
    iterations: int

    def __post_init__(self):
        self.widget_constructors = [
            self.__widget_kernelx,
            self.__widget_kernely,
            self.__widget_iteration,
        ]

    def __widget_kernelx(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'kernel x')
        spinbox = PropertyWidget.newSpinBox(row, formLayout, self, 'kernel_x')
        spinbox.valueChanged.connect(parent.filter_signal.emit)

    def __widget_kernely(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'kernel y')
        spinbox = PropertyWidget.newSpinBox(row, formLayout, self, 'kernel_y')
        spinbox.valueChanged.connect(parent.filter_signal.emit)

    def __widget_iteration(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'iterations')
        spinbox = PropertyWidget.newSpinBox(row, formLayout, self, 'iterations')
        spinbox.valueChanged.connect(parent.filter_signal.emit)


@dataclass
class FilterKMeansClusterProperties(BaseProperties):
    invert: bool = False
    gaussian_kernel_size: int = 0
    ncluster: int = 4
    maxiter: int = 10
    epsilon: float = 1.0

    def __post_init__(self):
        self.widget_constructors = [
            self.__widget_invert,
            self.__widget_gaussianblur,
            self.__widget_ncluster,
            self.__widget_maxiter,
            self.__widget_epsilon,
        ]

    def __widget_ncluster(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'n cluster')
        spinbox = PropertyWidget.newSpinBox(row, formLayout, self, 'ncluster')
        spinbox.setMaximum(20)
        spinbox.setMinimum(1)
        spinbox.valueChanged.connect(parent.filter_signal.emit)

    def __widget_maxiter(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'max iter')
        spinbox = PropertyWidget.newSpinBox(row, formLayout, self, 'maxiter')
        spinbox.setMinimum(1)
        spinbox.valueChanged.connect(parent.filter_signal.emit)

    def __widget_epsilon(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'epsilon')
        spinbox = PropertyWidget.newDoubleSpinBox(row, formLayout, self, 'epsilon')
        spinbox.setMaximum(1.0)
        spinbox.setMinimum(0.0)
        spinbox.valueChanged.connect(parent.filter_signal.emit)

    def __widget_invert(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'invert')
        checkbox = PropertyWidget.newCheckBox(row, formLayout, self, 'invert')
        checkbox.stateChanged.connect(parent.filter_signal.emit)

    def __widget_gaussianblur(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'gaussian blur k size')
        spinbox = PropertyWidget.newSpinBox(row, formLayout, self, 'gaussian_kernel_size')
        spinbox.setMinimum(0)
        spinbox.setMaximum(200)
        spinbox.valueChanged.connect(parent.filter_signal.emit)


        
@dataclass
class WindowingProperties(BaseProperties):
    width: int
    level: int

    def __post_init__(self):
        self.widget_constructors = [
            self.__widget_level,
            self.__widget_width,
        ]

    def __widget_level(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'level')
        spinbox = PropertyWidget.newSpinBox(row, formLayout, self, 'level')
        spinbox.setMaximum(9999)
        spinbox.valueChanged.connect(parent.filter_signal.emit)

    def __widget_width(self, row, parent, formLayout):
        label = PropertyWidget.newLabel(row, formLayout, 'width')
        spinbox = PropertyWidget.newSpinBox(row, formLayout, self, 'width')
        spinbox.setMaximum(9999)
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

    def displayDesc(self):
        return self._display_desc


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


class FilterKMeansClustering(BaseClassImageFilter):
    _inplace = False
    _display_name = 'KMeansClusteringMask'
    _display_desc = 'opencv K-Means Clustering Masking'

    def __init__(self):
        super().__init__()
        self.properties = FilterKMeansClusterProperties()

    def dispatch(self, dicom_ds, pixel_array):
        # a rough implemetation copied from this article without using scikit-image
        # https://stackoverflow.com/questions/52802910/opencv-color-segmentation-using-kmeans

        criteria = (
            cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
            self.properties.maxiter,
            self.properties.epsilon
        )

        h, w  = pixel_array.shape
        pixel_array_cp = pixel_array.copy()
        if self.properties.gaussian_kernel_size > 0:
            gaussian_kernel_size = self.properties.gaussian_kernel_size * 2 + 1
            cv.GaussianBlur(pixel_array_cp, (gaussian_kernel_size, gaussian_kernel_size), 0, pixel_array_cp) 

        pixel_array_1d = pixel_array_cp.reshape(h*w, 1)

        Z = np.float32(pixel_array_1d)
        K = self.properties.ncluster

        _, labels, centers = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_PP_CENTERS)
        label_count = np.bincount(labels.ravel().astype(int))
        label_count[0] = 0

        mask = (labels == label_count.argmax()).astype(float)

        mask = mask.reshape(h, w)

        if self.properties.invert:
            mask = 1 - mask

        return pixel_array * mask

class FilterWindowing(BaseClassImageFilter):
    _inplace = False
    _display_name = 'CTWindowing'
    _display_desc = 'numpy Threshold-like HU Gray Level Mapping'

    def __init__(self):
        self.properties = WindowingProperties(40, 48)

    def dispatch(self, dicom_ds, pixel_array):
        img_min = self.properties.level - self.properties.width // 2
        img_max = self.properties.level + self.properties.width // 2
        pixel_array[pixel_array < img_min] = img_min
        pixel_array[pixel_array > img_max] = img_max
        return pixel_array


class FilterMorphologyDilate(BaseClassImageFilter):
    _inplace = True
    _display_name = 'Dilate'
    _display_desc = 'opencv2 Dilate Morphological Operation'

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
    _display_desc = 'opencv2 Erode Morphological Operation'

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
    FilterWindowing,
    FilterMorphologyDilate,
    FilterMorphologyErode,
    FilterKMeansClustering
]

def newFilter(filter_enum):
    return dicom_image_filters[filter_enum]()