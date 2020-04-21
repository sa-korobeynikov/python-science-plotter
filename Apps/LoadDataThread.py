from PyQt5.QtCore import QThread, pyqtSignal, QObject
from Apps.DataManager import DataManager

class DataLoadThread(QThread):
    def __init__(self, signal: 'pyqtSignal'):
        QThread.__init__(self)
        self.__signal = signal
        self.DM: 'DataManager' = None
        self.filename = ''

    def set_filename(self, filename):
        self.filename = filename

    def run(self):
        self.DM = DataManager(self.filename)
        self.__signal.emit()