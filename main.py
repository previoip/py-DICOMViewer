from app import AppQT 
import sys

if __name__ == '__main__':
    app = AppQT(sys.argv)
    sys.exit(app.onExec())