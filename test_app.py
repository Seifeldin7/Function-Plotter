import pytest

from PySide2.QtWidgets import QLineEdit
from PySide2 import QtCore
import plotter


@pytest.fixture
def app(qtbot):
    plotter_app = plotter.App()
    qtbot.addWidget(plotter_app)

    return plotter_app


def test_title(app):
    assert app.title == "Function Plotter"


def test_validation_empty_input(app):
    assert app.validate_input('', '0', '2') == "Function should not be empty."


def test_validation_empty_max(app):
    assert app.validate_input('x', '0', '') == "Max value should not be empty."


def test_validation_empty_min(app):
    assert app.validate_input('x', '', '2') == "Min value should not be empty."


def test_validation_no_x(app):
    assert app.validate_input('z', '0', '2') == "Input should be a function of x."


def test_validation_wrong_format(app):
    assert app.validate_input('x//3', '0', '2') == "Please check the input format."


def test_validate_regex_wrong_example(app):
    assert app.validate_by_regex('x***3') == False


def test_validate_regex_wrong_example(app):
    assert app.validate_by_regex('x**3') == True

@pytest.fixture
def plot_field(qtbot):
    field = QLineEdit()
    field.setText('x**3')
    qtbot.addWidget(field)
    return field

@pytest.fixture
def min_field(qtbot):
    field = QLineEdit()
    field.setText('3')
    qtbot.addWidget(field)
    return field

@pytest.fixture
def max_field(qtbot):
    field = QLineEdit()
    field.setText('4')
    qtbot.addWidget(field)
    return field


def test_plot(app, plot_field, max_field, min_field):
    app.plot(plot_field, max_field, min_field)
    assert app.chart.min_val == float(min_field.text())
    assert app.chart.max_val == float(max_field.text())
    assert app.chart.y == plot_field.text().replace('x', 'self.x').replace('^', '**')


def test_flow_when_plot_btn_is_pressed(app, qtbot):
    app.min_field.setText('3')
    app.max_field.setText('4')
    app.plot_field.setText('x')
    qtbot.mouseClick(app.plot_btn, QtCore.Qt.LeftButton)

    assert app.chart.min_val == float(app.min_field.text())
    assert app.chart.max_val == float(app.max_field.text())
    assert app.chart.y == app.plot_field.text().replace('x', 'self.x').replace('^', '**')