import app, sys

import xml.etree.ElementTree as ET

if __name__ == '__main__':
    # sys.exit(app.main())
    tree = ET.parse('config.xml')
    root = tree.getroot()
    app = root[0]
    app.set('window_size_x', '100')

    tree.write('conf.xml')