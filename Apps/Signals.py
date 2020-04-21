from PyQt5.QtCore import pyqtSignal, QObject


class Signals(QObject):
    thread_finished = pyqtSignal()


