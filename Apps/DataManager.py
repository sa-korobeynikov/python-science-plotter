import json
import os


class DataManager:
    cfg = None
    coordinates = None
    data = None

    def __init__(self, config_file):
        self.data = []
        self.coordinates = []

        with open(config_file) as f_cfg:
            self.cfg = json.load(f_cfg)
            f_cfg.close()

        for f in self.cfg['data_files']:
            with open(os.path.dirname(config_file) + '\\' + f) as f_data:
                data_plot = list()
                coordinates = f_data.readline().split(' ')
                self.coordinates.append([float(i) for i in coordinates])
                f_data.readline()
                tmp_data = list()
                tmp_line = f_data.readline().split('\t')
                num_plots = len(tmp_line)
                for i in range(num_plots):
                    tmp_data.append([])
                    tmp_data[i].append(float(tmp_line[i]))
                line = None
                while line != '':
                    line = f_data.readline()
                    if line == "\n" or line == '':
                        if len(tmp_data[0]) != 0:
                            data_plot.append(tmp_data.copy())
                            tmp_data = [[] for _ in range(num_plots)]
                    else:
                        for i, val in enumerate(line.split('\t')):
                            tmp_data[i].append(float(val))
                f_data.close()
            self.data.append(data_plot.copy())

    def get_frames_count(self):
        return len(self.data[0])

    def get_frame(self, subplot, tick):
        return self.coordinates[subplot], self.data[subplot][tick]

    def get_subplots_num(self):
        return len(self.data)

    def get_plots_num(self, subplot):
        return len(self.data[subplot][0])
