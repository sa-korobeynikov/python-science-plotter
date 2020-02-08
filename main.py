from PyQt5 import QtWidgets
import sys

from WIndowsClasses.MainWindow import MainWindow
# from WIndowsClasses.MainWindow import ApplicationWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    appMainWindow = MainWindow()
    # appMainWindow = ApplicationWindow()
    appMainWindow.show()

    sys.exit(app.exec_())