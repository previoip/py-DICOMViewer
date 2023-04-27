from app import QtApp
import sys

if __name__ == '__main__':
    app = QtApp(*sys.argv)
    sys.exit(app.onExec())