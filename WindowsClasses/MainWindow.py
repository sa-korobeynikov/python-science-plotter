from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
import pyqtgraph as pg
from functools import partial


from Forms.MainWindowForm import Ui_MainWindow

from Apps.DataManager import DataManager
from Apps.LoadDataThread import DataLoadThread
from Apps.Signals import Signals


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
        self.legends = []
        self.current_frame = 0
        self.num_frames = 0
        self.signals = Signals()

        self.data_mngr_thread = DataLoadThread(self.signals.thread_finished)
        self.signals.thread_finished.connect(self.init_plot)

        self.DM: 'DataManager' = None

    def callback(self, point):
        y = point.y()
        h = self.mainUI.plot_widget.frameGeometry().height() // len(self.subplots_data)
        sbpl_index = int(y//h)
        if sbpl_index == len(self.subplots_data):
            sbpl_index = len(self.subplots_data) - 1
        p = self.subplots_data[sbpl_index].vb.mapSceneToView(point)
        self.mainUI.x_pos.setText('x: {:0.6g}'.format(p.x()))
        self.mainUI.y_pos.setText('y: {:0.6g}'.format(p.y()))



    def init_plot(self):
        self.DM = self.data_mngr_thread.DM
        DM = self.DM

        self.mainUI.frames_slider.setValue(0)

        self.num_frames = self.DM.get_frames_count() - 1
        self.current_frame = 0
        self.set_current_frame_lineedit()

        self.mainUI.frames_slider.setMinimum(0)
        self.mainUI.frames_slider.setMaximum(self.num_frames)
        self.set_enabled(True)

        for i in self.subplots_data:
            self.mainUI.plot_widget.removeItem(i)

        self.subplots_data = []
        self.plots_data = []

        for i in range(DM.get_subplots_num()):
            sbpl_params = {
                'row': i,
                'col': 0,
                'enableMenu': True,
            }
            sbpl_title = DM.get_subplot_title(i)
            if sbpl_title is not None:
                sbpl_params['title'] = sbpl_title

            self.subplots_data.append(self.mainUI.plot_widget.addPlot(**sbpl_params))
            self.subplots_data[i].getAxis('bottom').setPen('k')
            self.subplots_data[i].getAxis('left').setPen('k')

            self.subplots_data[i].scene().sigMouseMoved.connect(self.callback)

            x, y = DM.get_frame(i, 0)
            self.plots_data.append([])

            for j in range(DM.get_plots_num(i)):
                pl_sett = DM.get_plot_setting(i, j)

                pen_params = dict()
                if pl_sett['color'] is not None:
                    pen_params['color'] = tuple(pl_sett['color'])
                else:
                    pen_params['color'] = 'k'

                if pl_sett['line_type'] is not None:
                    line_type = pl_sett['line_type']
                    if line_type == 'solid':
                        pen_params['style'] = QtCore.Qt.SolidLine
                    elif line_type == 'dash':
                        pen_params['style'] = QtCore.Qt.DashLine
                    elif line_type == 'dot':
                        pen_params['style'] = QtCore.Qt.DotLine
                    elif line_type == 'dashdot':
                        pen_params['style'] = QtCore.Qt.DashDotLine
                    elif line_type == 'dashdotdot':
                        pen_params['style'] = QtCore.Qt.DashDotDotLine

                pen_params['width'] = 1.5

                self.plots_data[i].append(self.subplots_data[i].plot(x, y[j], pen=pg.mkPen(**pen_params)))
                # print(self.plots_data[i][j].scene())
                # self.plots_data[i][j].scene().sigMouseMove.connect(lambda evt: print(123))

        self.create_legend()



        self.mainUI.parameters_table.setRowCount(0)
        self.mainUI.parameters_table.setRowCount(DM.get_params_num())
        if self.DM.get_params_num():
            params_vals = DM.get_params(0)
            for i, par_name in enumerate(DM.parameters_names):
                self.mainUI.parameters_table.setItem(i, 0, QtWidgets.QTableWidgetItem(par_name))
                self.mainUI.parameters_table.setItem(i, 1, QtWidgets.QTableWidgetItem(params_vals[i]))
                self.mainUI.parameters_table.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled)
                self.mainUI.parameters_table.item(i, 1).setFlags(QtCore.Qt.ItemIsEnabled)

        self.mainUI.x_pos.setText('x: -')
        self.mainUI.y_pos.setText('y: -')


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

        if self.DM.get_params_num():
            for i, param_val in enumerate(self.DM.get_params(tick)):
                self.mainUI.parameters_table.setItem(i, 1, QtWidgets.QTableWidgetItem(param_val))

    def create_legend(self):
        self.legends.clear()
        for i in range(self.DM.get_subplots_num()):
            self.legends.append(None)
            for j in range(self.DM.get_plots_num(i)):
                pl_sett = self.DM.get_plot_setting(i, j)
                if pl_sett['title'] is not None:
                    if self.legends[i] is None:
                        legend = pg.LegendItem(offset=(60, 20))
                        self.legends[i] = legend
                        self.legends[i].setParentItem(self.subplots_data[i])
                    self.legends[i].addItem(self.plots_data[i][j], name=pl_sett['title'])




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
            self.mainUI.load_data_button.setEnabled(True)

    def set_enabled(self, status: 'bool'):
        mainUI = self.mainUI
        mainUI.run_button.setEnabled(status)
        mainUI.stop_button.setEnabled(status)

        mainUI.frames_counter.setEnabled(status)
        mainUI.frames_slider.setEnabled(status)

        mainUI.fps_sb.setEnabled(status)
        mainUI.open_cfg_file_button.setEnabled(status)
        mainUI.parameters_table.setEnabled(status)

    def load_data(self):
        self.timer.stop()
        self.set_enabled(False)
        QtWidgets.QApplication.processEvents()

        filename = self.mainUI.file_path.text()
        self.data_mngr_thread.set_filename(filename)
        self.data_mngr_thread.start()

    def fps_change(self):
        val = self.mainUI.fps_sb.value()
        if self.timer.isActive():
            self.timer.stop()
            self.timer.setInterval(1000//val)
            self.timer.start()
        else:
            self.timer.setInterval(1000 // val)
