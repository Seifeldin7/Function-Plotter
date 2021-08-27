import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np


class Canvas(FigureCanvas):
    def __init__(self, parent):
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(self.fig)
        self.x = np.linspace(-2, 2, 100)
        self.y = None
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
        self.x = np.linspace(-2, 2, 100)
        y = self.x
        print(y)
        self.ax.plot(self.x, y)

        self.ax.set(xlabel='x', ylabel='y',
                    title='Function')
        self.ax.grid()

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = np.fromstring(y, dtype=np.uint8)

    def plot(self):
        self.y = self.x**2
        self.ax.cla()
        self.ax.plot(self.x, self.y)
        self.ax.grid()
        self.draw()

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.title = "Function Plotter"
        self.height = 800
        self.width = 1000
        self.top = 0
        self.left = 0
        self.chart = Canvas(self)

        self.layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setLayout(self.layout)
        win = QWidget()
        self.layout.addWidget(win)
        grid_layout = QGridLayout()
        win.setLayout(grid_layout)
        plot_field = QLineEdit(self)
        plot_field.setStyleSheet("background-color: black; color: white;")
        plot_btn = QPushButton("Plot", self)
        plot_btn.setStyleSheet("background-color: #51E000; color: white; ")
        plot_btn.clicked.connect(lambda: self.plot(plot_field))

        grid_layout.addWidget(plot_field, 1, 1)
        grid_layout.addWidget(plot_btn, 1, 2)
        grid_layout.addWidget(self.chart, 2, 1)
        win.show()

    def plot(self, plot_field):
        y = plot_field.text()
        #self.chart.setY(y)
        self.chart.plot()

def main():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app = QApplication(sys.argv)
    app.setPalette(palette)
    ex = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()