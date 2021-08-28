import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
import re


class Canvas(FigureCanvas):
    def __init__(self, parent):
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(self.fig)
        self.x = np.linspace(-100, 100, 100)
        self.y = None
        self.max_val = 0
        self.min_val = 0
        self.setParent(parent)

        self.ax.set(xlabel='x', ylabel='y',
                    title='Function')
        self.ax.grid()

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_min(self, min_val):
        self.min_val = min_val

    def set_max(self, max_val):
        self.max_val = max_val

    def plot(self):
        self.ax.cla()
        self.x = np.linspace(self.min_val, self.max_val, 100)
        self.ax.plot(self.x, eval(self.y))
        self.ax.grid()
        self.draw()


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.title = "Function Plotter"
        self.chart = Canvas(self)

        self.layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setLayout(self.layout)
        win = QWidget()
        self.layout.addWidget(win)
        grid_layout = QGridLayout()
        h_layout = QHBoxLayout()
        win.setLayout(grid_layout)
        self.plot_field = QLineEdit(self)
        self.min_field = QLineEdit(self)
        self.max_field = QLineEdit(self)
        min_lbl = QLabel("Min: ", self)
        max_lbl = QLabel("Max: ", self)
        self.plot_btn = QPushButton("Plot", self)

        self.min_field.setStyleSheet("background-color: black; color: white;")
        self.min_field.setFixedWidth(150)
        min_lbl.setStyleSheet("color: white;")
        self.max_field.setStyleSheet("background-color: black; color: white;")
        self.max_field.setFixedWidth(150)
        max_lbl.setStyleSheet("color: white;")
        self.plot_field.setStyleSheet("background-color: black; color: white;")
        self.plot_btn.setStyleSheet("background-color: rgb(23, 82, 198); color: white; ")

        self.plot_btn.clicked.connect(lambda: self.plot(self.plot_field, self.max_field, self.min_field))

        grid_layout.addWidget(self.plot_field, 1, 1)
        grid_layout.addWidget(self.plot_btn, 1, 2)
        min_max_widget = QWidget(self)
        min_max_widget.setLayout(h_layout)
        h_layout.addWidget(min_lbl)
        h_layout.addWidget(self.min_field)
        h_layout.addWidget(max_lbl)
        h_layout.addWidget(self.max_field)
        grid_layout.addWidget(min_max_widget, 2, 1)
        grid_layout.addWidget(self.chart, 3, 1)
        win.show()

    def plot(self, plot_field, max_field, min_field):
        max_value = max_field.text()
        min_value = min_field.text()
        y = plot_field.text()
        message = self.validate_input(y, min_value, max_value)
        if message:
            self.display_dialog(message)
            return
        max_value = float(max_value)
        min_value = float(min_value)
        y = y.replace('x', 'self.x').replace('^', '**')
        self.chart.set_y(y)
        self.chart.set_max(max_value)
        self.chart.set_min(min_value)
        self.chart.plot()

    def validate_input(self, input_val, min_val, max_val):
        message = None
        if not min_val:
            message = "Min value should not be empty."
        elif not max_val:
            message = "Max value should not be empty."
        elif not input_val:
            message = "Function should not be empty."
        elif 'x' not in input_val:
            message = "Input should be a function of x."
        elif not self.validate_by_regex(input_val):
            message = "Please check the input format."
        return message

    def display_dialog(self, message):
        mbox = QMessageBox()
        mbox.setText(message)
        mbox.setStyleSheet("color: black;")
        mbox.setStandardButtons(QMessageBox.Ok)
        mbox.exec_()

    def validate_by_regex(self, input_val):
        regex = re.compile(r'((x|\d+)(\+|-|\*|/|\**)?)+', re.I)
        match = regex.fullmatch(str(input_val).replace(' ', ''))
        return bool(match)


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
