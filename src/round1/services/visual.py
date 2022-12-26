import sys
import json
import matplotlib
from datetime import datetime

matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

with open('C:/Users/User/Documents/GitHub/Hackathon-DatSanta-2022/result.json', 'r') as result:
    move = json.loads(result.read())['moves']


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.autofmt_xdate()
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, x_list, y_list, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=10, height=10, dpi=100)
        sc.axes.plot(x_list, y_list)

        self.setCentralWidget(sc)


x_list = []
y_list = []
for item in move:
    x_list.append(datetime.utcfromtimestamp(item['x']))
    y_list.append(item['y'])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(x_list, y_list)
    w.show()
    sys.exit(app.exec_())
