from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QLabel

from WindowsClasses.MainWindow import MainWindow


class MainApp(MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

    def get_pos(self, point):
        y = point.y()
        h = self.mainUI.plot_widget.frameGeometry().height() // len(self.subplots_data)
        sbpl_index = int(y // h)
        if sbpl_index == len(self.subplots_data):
            sbpl_index = len(self.subplots_data) - 1
        p = self.subplots_data[sbpl_index].vb.mapSceneToView(point)
        self.statusbar_xpos.setText('{:0.6g}'.format(p.x()))
        self.statusbar_ypos.setText('{:0.6g}'.format(p.y()))

    def select_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Config file (*.cfg)")
        if dlg.exec_():
            filename = dlg.selectedFiles()
            filename = filename[0]

            self.file_path = filename

            path = filename.split('/')
            lbl_width = self.statusbar_filepath.width()
            for i in range(len(path) - 1, 0, -1):
                filename_text = path[-1]
                for j, path_elem in enumerate(path[-(i + 1):-1][::-1]):
                    if j != len(path) - 1:
                        filename_text = "/" + filename_text
                    filename_text = path_elem + filename_text
                if i != len(path) - 1:
                    filename_text = ".../" + filename_text

                filename_text_width = self.statusbar_filepath.fontMetrics(). \
                    boundingRect(filename_text).width()

                if lbl_width >= filename_text_width:
                    self.statusbar_filepath.setText(filename_text)
                    break

            self.mainUI.load_data_button.setEnabled(True)
