from PyQt5 import QtWidgets
import sys

from WindowsApp.MainApp import MainApp
# from WindowsClasses.MainWindow import ApplicationWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    appMainWindow = MainApp()
    # appMainWindow = ApplicationWindow()
    appMainWindow.show()

    sys.exit(app.exec_())