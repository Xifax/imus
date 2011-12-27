# -*- coding=utf-8 -*-
"""
Main application script. Console version.
"""

# internal #
import sys

# external #
from PyQt4.QtGui import QApplication, QIcon

# own #
from ui.gui.widget import ImusWidget
from db.library import Track, Redis

def main():
        app = QApplication(sys.argv)
        #app.setWindowIcon(QIcon(paths['icon']))

        gui = ImusWidget()
        gui.show()

        sys.exit(app.exec_())

def test():
    r = Redis()
    r.update(Track('test', 'lalal', 'ohoho', 'oops'))
    print 'Lookup results ~ ', r.lookup('test')
    print 'Recreated track ~ ', r.retrieve(r.lookup('test').pop())

if __name__ == '__main__':
    main()
