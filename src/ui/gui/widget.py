# -*- coding=utf-8 -*-

# TODO: display benchmarked time, that search took
# TODO: group results, hide/mark empty results
# TODO: hotkeys for search field
# TODO: implement something like table with groups, instead of single qlabel

# std #
import sys
from time import time

# external #
from PyQt4.QtGui import QWidget, QGridLayout, \
                        QGroupBox, QLabel, QPushButton, QApplication, QFont, \
                        QComboBox, QProgressBar, QToolTip, QMessageBox, QPixmap, \
                        QLineEdit, QTableWidget

from PyQt4.QtCore import Qt, QObject, QEvent, QTimer, QThread, pyqtSignal, QSize, QPoint

# own #
#from conf.const import *
from db.library import Track, Redis, Crawler

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
        self.bench = QLabel('0.0')

        self.results = QTableWidget()

        self.scan = QPushButton('&Scan')
        self.leave = QPushButton('&Quit')

    def compose_ui(self):
        self.layout.addWidget(self.directory, 0, 0, 1, 2)
        self.layout.addWidget(self.search, 1, 0, 1, 2)
        self.layout.addWidget(self.info, 2, 0, 1, 2)
        self.layout.addWidget(self.scan, 3, 0)
        self.layout.addWidget(self.leave, 3, 1)
        self.layout.addWidget(self.bench, 4, 0, 1, 2)

        self.setLayout(self.layout)

    def init_composition(self):
        #self.setWindowTitle(NAME + ' ' + __version__)
        desktop = QApplication.desktop()
        WIDTH = 800
        HEIGHT = 600
        self.setGeometry((desktop.width() - WIDTH)/2,
                        (desktop.height() - HEIGHT)/2, WIDTH, HEIGHT)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

    def init_contents(self):
        self.directory.setPlaceholderText('Folder to scan')
        self.search.setPlaceholderText('Key to search')
        self.info.setMaximumWidth(640)
        self.info.setMaximumHeight(480)
        self.info.setAlignment(Qt.AlignCenter)

    def init_actions(self):
        self.scan.clicked.connect(self.update_lib)
        self.leave.clicked.connect(self.close)
        self.search.textChanged.connect(self.lookup_variants)

    def on_start(self):
        """
        Post-launch initialization.
        """
        self.r = Redis()
        self.crawler = Crawler(self.r)
        self.mpost = QPoint()
        self.lookup_task = None

    ##### actions #####

    def update_lib(self):
        if not self.directory.text().isEmpty():
            self.crawler.crawl(unicode(self.directory.text()))
        self.info.setText('Redis keys: %d' % len(self.r.lookup('*')))

    def lookup_variants(self):
        ##TODO: should not lookup queries under 2 symbols (in case those aren't kanji/hanzi)
        # Temporarily! May not work properly in many-many cases
        if not self.search.text().isEmpty():
        #if len(self.search.text()) > 1:
            # If lookut thread already initialized
            if self.lookup_task is not None:
                # If not finished yet - stop
                if not self.lookup_task.isFinished():
                    #print 'not finished!'
                    self.lookup_task.quit()
                # Update search query and restart
                self.lookup_task.update(self.search.text())
                self.lookup_task.start()
            # If not - let's create it and bind signals
            else:
                self.lookup_task = Lookup(self.r, self.search.text())
                self.lookup_task.done.connect(self.lookup_results)
                self.lookup_task.benchmark.connect(self.lookup_time)
                self.lookup_task.start()

        ##TODO: should not lookup queries under 2 symbols (in case those aren't kanji/hanzi)
        #if not self.search.text().isEmpty():
            ##TODO: implement option to search case-independent (e.g., convert to small case)
            #found = self.r.lookup(self.search.text())
            #if found:
                #self.info.setText(unicode('<hr/>'.join(found), 'utf-8'))
            #else:
                #self.info.setText('Nothing matches')
                ##self.adjustSize()
            #self.adjustSize()

    def lookup_results(self, found):
        if found:
            print Track.structure(self.r.retrieve(found))
            text = ''
            for track in self.r.retrieve(found):
                text += track.info()
                text += '<hr/>'

            try:
                self.info.setText(unicode(text, 'utf-8'))
            except TypeError:
                self.info.setText(text)
            # TEST: getting from Redis
            #self.info.setText(unicode('<hr/>'.join(found), 'utf-8'))
        else:
            self.info.setText('Nothing matches')
        self.adjustSize()

    def lookup_time(self, measured):
        #print measured
        self.bench.setText(str(measured))

    ##### events #####

    def onResizeEvent(self, event):
        pass

    def mousePressEvent(self, event):
        self.mpos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            diff = QPoint(event.pos() - self.mpos)
            newpos = QPoint(self.pos() + diff)

            self.move(newpos)

    def close(self, event):
        # TODO: implement 'minimize to tray' and all that stuff
        sys.exit()

class Lookup(QThread):

    done = pyqtSignal(list)
    benchmark = pyqtSignal(float)

    def __init__(self, redis, text, parent=None):
        super(Lookup, self).__init__(parent)
        self.text = text
        self.r = redis
        self.found = []

    def run(self):
        began = time()
        try:
            self.found = self.r.lookup(self.text)
            self.benchmark.emit(time() - began)
        except Exception:
            pass

        self.done.emit(self.found)

    def update(self, text):
        self.text = text
        self.found = []
