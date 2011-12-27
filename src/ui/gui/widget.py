# -*- coding=utf-8 -*-

# external #
from PyQt4.QtGui import QWidget, QGridLayout, \
                        QGroupBox, QLabel, QPushButton, QApplication, QFont, \
                        QComboBox, QProgressBar, QToolTip, QMessageBox, QPixmap, \
                        QLineEdit

from PyQt4.QtCore import Qt, QObject, QEvent, QTimer, QThread, pyqtSignal, QSize

# own #
#from conf.const import *
from db.library import Redis, Crawler

class ImusWidget(QWidget):

    def __init__(self, parent=None):
        super(ImusWidget, self).__init__(parent)

        self.create_ui()
        self.compose_ui()

        self.init_composition()
        self.init_contents()
        self.init_actions()

        self.on_start()

    def create_ui(self):
        self.layout = QGridLayout()

        self.directory = QLineEdit()
        self.search = QLineEdit()
        self.info = QLabel('Nothing to info about')

        self.scan = QPushButton('&Scan')

    def compose_ui(self):
        self.layout.addWidget(self.directory, 0, 0)
        self.layout.addWidget(self.search, 1, 0)
        self.layout.addWidget(self.info, 2, 0)
        self.layout.addWidget(self.scan, 3, 0)

        self.setLayout(self.layout)

    def init_composition(self):
        #self.setWindowTitle(NAME + ' ' + __version__)
        desktop = QApplication.desktop()
        WIDTH = 800
        HEIGHT = 600
        self.setGeometry((desktop.width() - WIDTH)/2,
                        (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)

    def init_contents(self):
        self.directory.setPlaceholderText('Folder to scan')
        self.search.setPlaceholderText('Key to search')
        self.info.setMaximumWidth(640)
        self.info.setMaximumHeight(480)
        self.info.setAlignment(Qt.AlignCenter)

    def init_actions(self):
        self.scan.clicked.connect(self.update_lib)
        self.search.textChanged.connect(self.lookup_variants)

    def on_start(self):
        self.r = Redis()
        self.crawler = Crawler(self.r)

    ##### actions #####

    def update_lib(self):
        if not self.directory.text().isEmpty():
            self.crawler.crawl(unicode(self.directory.text()))
        self.info.setText('Redis keys: %d' % len(self.r.lookup('*')))

    def lookup_variants(self):
        #TODO: should not lookup queries under 2 symbols (in case those aren't kanji/hanzi)
        if not self.search.text().isEmpty():
            #TODO: implement option to search case-independent (e.g., convert to small case)
            found = self.r.lookup(self.search.text())
            if found:
                self.info.setText(unicode('<hr/>'.join(found), 'utf-8'))
            else:
                self.info.setText('Nothing matches')
                #self.adjustSize()
            self.adjustSize()

    ##### events #####

    def onResizeEvent(self, event):
        pass
