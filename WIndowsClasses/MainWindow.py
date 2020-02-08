from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

from Forms.MainWindowForm import Ui_MainWindow

from Apps.DataManager import DataManager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.mainUI = Ui_MainWindow()
        self.mainUI.setupUi(self)

        self.mainUI.plot_widget.setBackground('w')

        self.mainUI.run_button.clicked.connect(self.run_timer)
        self.mainUI.stop_button.clicked.connect(self.stop_timer)

        self.mainUI.open_cfg_file_button.clicked.connect(self.open_cfg_file)
        self.mainUI.load_data_button.clicked.connect(self.load_data)

        self.mainUI.fps_sb.valueChanged.connect(self.fps_change)

        self.mainUI.frames_slider.valueChanged.connect(self.on_slider_changed)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.update_plot)

        self.subplots_data = []
        self.plots_data = []
        self.current_frame = 0
        self.num_frames = 0

        self.DM = None

    def init_plot(self):
        DM = self.DM

        for i in self.subplots_data:
            self.mainUI.plot_widget.removeItem(i)

        self.subplots_data = []
        self.plots_data = []

        for i in range(DM.get_subplots_num()):
            self.subplots_data.append(self.mainUI.plot_widget.addPlot(row=i, col=0, enableMenu=True))
            self.subplots_data[i].getAxis('bottom').setPen('k')
            self.subplots_data[i].getAxis('left').setPen('k')

            x, y = DM.get_frame(i, 0)
            self.plots_data.append([])
            for j in range(DM.get_plots_num(i)):
                self.plots_data[i].append(self.subplots_data[i].plot(x, y[j], pen='k'))

    def update_plot(self, tick=-1):
        if tick == -1:
            tick = self.current_frame + 1
            self.current_frame = tick + 0
        if tick == self.num_frames:
            self.timer.stop()
        DM = self.DM
        for i in range(DM.get_subplots_num()):
            x, y = DM.get_frame(i, tick)
            self.plots_data.append([])
            for j in range(DM.get_plots_num(i)):
                self.plots_data[i][j].setData(x, y[j])

        self.set_current_frame_lineedit()
        self.mainUI.frames_slider.blockSignals(True)
        self.mainUI.frames_slider.setValue(tick)
        self.mainUI.frames_slider.blockSignals(False)

    def set_current_frame_lineedit(self):
        self.mainUI.frames_counter.setText("{} / {}".format(self.current_frame, self.num_frames))

    def on_slider_changed(self):
        val = self.mainUI.frames_slider.value()
        self.current_frame = val
        self.set_current_frame_lineedit()
        self.update_plot(val)

    def run_timer(self):
        if self.current_frame != self.num_frames:
            self.timer.start()

    def stop_timer(self):
        self.timer.stop()

    def open_cfg_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Config file (*.cfg)")
        if dlg.exec_():
            filename = dlg.selectedFiles()
            filename = filename[0]
            self.mainUI.file_path.setText(filename)

    def load_data(self):
        mainUI = self.mainUI

        self.timer.stop()
        filename = self.mainUI.file_path.text()

        mainUI.run_button.setEnabled(False)
        mainUI.stop_button.setEnabled(True)

        mainUI.frames_counter.setEnabled(False)
        mainUI.frames_slider.setEnabled(False)

        mainUI.fps_sb.setEnabled(False)

        self.DM = DataManager(filename)

        mainUI.run_button.setEnabled(True)
        mainUI.stop_button.setEnabled(True)

        mainUI.frames_counter.setEnabled(True)
        mainUI.frames_slider.setEnabled(True)
        self.mainUI.frames_slider.setValue(0)

        mainUI.fps_sb.setEnabled(True)

        self.num_frames = self.DM.get_frames_count() - 1
        self.current_frame = 0
        self.set_current_frame_lineedit()

        self.mainUI.frames_slider.setMinimum(0)
        self.mainUI.frames_slider.setMaximum(self.num_frames)

        self.init_plot()

    def fps_change(self):
        val = self.mainUI.fps_sb.value()
        self.timer.stop()
        self.timer.setInterval(1000//val)
        self.timer.start()
