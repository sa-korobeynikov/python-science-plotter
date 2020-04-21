# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designes\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(980, 832)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setEnabled(False)
        self.run_button.setGeometry(QtCore.QRect(10, 640, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_button.sizePolicy().hasHeightForWidth())
        self.run_button.setSizePolicy(sizePolicy)
        self.run_button.setObjectName("run_button")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setEnabled(False)
        self.stop_button.setGeometry(QtCore.QRect(100, 640, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy)
        self.stop_button.setObjectName("stop_button")
        self.label_fps = QtWidgets.QLabel(self.centralwidget)
        self.label_fps.setGeometry(QtCore.QRect(300, 650, 22, 13))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_fps.sizePolicy().hasHeightForWidth())
        self.label_fps.setSizePolicy(sizePolicy)
        self.label_fps.setObjectName("label_fps")
        self.frames_counter = QtWidgets.QLabel(self.centralwidget)
        self.frames_counter.setEnabled(False)
        self.frames_counter.setGeometry(QtCore.QRect(860, 630, 101, 20))
        self.frames_counter.setAlignment(QtCore.Qt.AlignCenter)
        self.frames_counter.setObjectName("frames_counter")
        self.frames_slider = QtWidgets.QSlider(self.centralwidget)
        self.frames_slider.setEnabled(False)
        self.frames_slider.setGeometry(QtCore.QRect(10, 600, 960, 22))
        self.frames_slider.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frames_slider.setMaximum(1)
        self.frames_slider.setPageStep(1)
        self.frames_slider.setSliderPosition(0)
        self.frames_slider.setOrientation(QtCore.Qt.Horizontal)
        self.frames_slider.setInvertedAppearance(False)
        self.frames_slider.setInvertedControls(False)
        self.frames_slider.setObjectName("frames_slider")
        self.fps_sb = QtWidgets.QSpinBox(self.centralwidget)
        self.fps_sb.setEnabled(False)
        self.fps_sb.setGeometry(QtCore.QRect(330, 650, 91, 22))
        self.fps_sb.setMinimum(1)
        self.fps_sb.setMaximum(10000)
        self.fps_sb.setProperty("value", 25)
        self.fps_sb.setObjectName("fps_sb")
        self.open_cfg_file_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_cfg_file_button.setGeometry(QtCore.QRect(20, 710, 75, 23))
        self.open_cfg_file_button.setObjectName("open_cfg_file_button")
        self.file_path = QtWidgets.QLabel(self.centralwidget)
        self.file_path.setGeometry(QtCore.QRect(110, 710, 841, 16))
        self.file_path.setText("")
        self.file_path.setObjectName("file_path")
        self.load_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_data_button.setEnabled(False)
        self.load_data_button.setGeometry(QtCore.QRect(20, 750, 75, 23))
        self.load_data_button.setObjectName("load_data_button")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(130, 750, 81, 20))
        self.status_label.setText("")
        self.status_label.setObjectName("status_label")
        self.plot_widget = GraphicsLayoutWidget(self.centralwidget)
        self.plot_widget.setGeometry(QtCore.QRect(0, 0, 980, 590))
        self.plot_widget.setObjectName("plot_widget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Science Plotter"))
        self.run_button.setText(_translate("MainWindow", "Run"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.label_fps.setText(_translate("MainWindow", "FPS:"))
        self.frames_counter.setText(_translate("MainWindow", "0 / 0"))
        self.open_cfg_file_button.setText(_translate("MainWindow", "Open file"))
        self.load_data_button.setText(_translate("MainWindow", "Load data"))
from pyqtgraph import GraphicsLayoutWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
