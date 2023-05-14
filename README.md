# Simple DICOM File Viewer 


A DICOM file viewer built using matplotlib backend and PyQT5 Gui framework. This repository was created as a personal excercise on implementing MVC Design Pattern Framework ([Wikipedia](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)), which translates into lacks of code quality, no performance requirement, sheer size of changes between versions/iterations, and absent of test suites. Use it at your own risk.

# Installation

## virtualenv

This repository have built shell scripts appendded for such case. Namely `venv-setup.sh` and `venv-remove.sh` to install and remove virtualenv respectively. Mind the directory of where the shell is ran from.

## Other enviromnents

For manual install into your local system's python or conda, you'll need to run `pip install requirements.txt` to install the requirements and launch the app by running `python3 main.py`

# Resources and Further Read

## DICOM related

- `pydicom` file reader library https://github.com/pydicom/pydicom
- `pydicom` docs https://pydicom.github.io/pydicom/dev/index.html
- DICOM File Standard https://dicom.nema.org/medical/dicom/current/output/html/part05.html
- Sample source https://medimodel.com/sample-dicom-files/human_skull_2_dicom_file/
- Pre-processing example https://towardsdatascience.com/medical-image-pre-processing-with-python-d07694852606

## Qt GUI lib

- for pyside2 (Qt5) https://doc.qt.io/qtforpython-5/
- PyQT translated from c++ Qt binding https://doc-snapshots.qt.io/qtforpython-dev/index.html
- PyQT examples https://github.com/pyqt/examples

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
