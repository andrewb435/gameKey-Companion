import gk_data
from ui_stick import Ui_windowStick
from PyQt5 import QtWidgets as QtW
from PyQt5 import QtCore as QtC
import gk_gameKey


class StickUI(QtW.QWidget):
    # Signals

    stick_data_return = QtC.pyqtSignal(str, int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_windowStick()
        self.ui.setupUi(self)

        # Variables

        # Analog Axes
        self.ui.bUpdateAnalog.clicked.connect(self.get_analog)
        self.ui.bSendAxes.clicked.connect(self.set_axes)
        self.ui.iXInvert.clicked.connect(self.axis_invert)
        self.ui.iYInvert.clicked.connect(self.axis_invert)
        self.ui.radioXModeAnalog.clicked.connect(self.axis_mode)
        self.ui.radioXModeDigital.clicked.connect(self.axis_mode)
        self.ui.radioYModeAnalog.clicked.connect(self.axis_mode)
        self.ui.radioYModeDigital.clicked.connect(self.axis_mode)

        # Deadzone dial
        self.ui.dialXdz.valueChanged.connect(self.update_dz)
        self.ui.dialYdz.valueChanged.connect(self.update_dz)

        # QtRangeSlider from superqt
        self.ui.sliderXrange.setValue((100, 500, 900))
        self.ui.sliderXrange.setHandleLabelPosition(self.ui.sliderXrange.LabelPosition.LabelsBelow)
        self.ui.sliderYrange.setValue((100, 500, 900))
        self.ui.sliderYrange.setHandleLabelPosition(self.ui.sliderYrange.LabelPosition.LabelsBelow)

        self.ui.sliderXrange.valueChanged.connect(self.axis_limits_changed)
        self.ui.sliderYrange.valueChanged.connect(self.axis_limits_changed)
        self.ui.dialXdz.valueChanged.connect(self.axis_dz_changed)
        self.ui.dialYdz.valueChanged.connect(self.axis_dz_changed)

        # Thumbstick mode color indicators
        self.ui.radioXModeDigital.setStyleSheet(gk_data.gk_colormode[0])
        self.ui.radioXModeAnalog.setStyleSheet(gk_data.gk_colormode[1])
        self.ui.radioYModeDigital.setStyleSheet(gk_data.gk_colormode[0])
        self.ui.radioYModeAnalog.setStyleSheet(gk_data.gk_colormode[1])

    def update_dz(self):
        self.ui.oXdz.setText(str(self.ui.dialXdz.value()))
        self.ui.oYdz.setText(str(self.ui.dialYdz.value()))

    def update_labels(self):
        # X Axis
        self.ui.sliderXrange.setValue(
            (
                int(self.gk_cur.axes[0].low),
                int(self.gk_cur.axes[0].center),
                int(self.gk_cur.axes[0].high)
            )
        )
        # X Invert
        if int(self.gk_cur.axes[0].invert) == 1:
            self.ui.iXInvert.setChecked(True)
        else:
            self.ui.iXInvert.setChecked(False)
        # X Mode
        if int(self.gk_cur.axes[0].analog_mode) == 0:
            self.ui.radioXModeDigital.setChecked(True)
        else:
            self.ui.radioXModeAnalog.setChecked(True)

        # Y Axis
        self.ui.sliderYrange.setValue(
            (
                int(self.gk_cur.axes[1].low),
                int(self.gk_cur.axes[1].center),
                int(self.gk_cur.axes[1].high)
            )
        )
        # Y Invert
        if int(self.gk_cur.axes[1].invert) == 1:
            self.ui.iYInvert.setChecked(True)
        else:
            self.ui.iYInvert.setChecked(False)
        # Y Mode
        if int(self.gk_cur.axes[1].analog_mode) == 0:
            self.ui.radioYModeDigital.setChecked(True)
        else:
            self.ui.radioYModeAnalog.setChecked(True)

        # Deadzone dial
        self.ui.dialXdz.setValue(int(self.gk_cur.axes[0].deadzone))
        self.ui.oXdz.setText(str(self.gk_cur.axes[0].deadzone))
        self.ui.dialYdz.setValue(int(self.gk_cur.axes[1].deadzone))
        self.ui.oYdz.setText(str(self.gk_cur.axes[1].deadzone))

    def set_axes(self):
        x_range = self.ui.sliderXrange.sliderPosition()
        self.gk_cur.axes[0].low = int(x_range[0])
        self.gk_cur.axes[0].center = int(x_range[1])
        self.gk_cur.axes[0].high = int(x_range[2])
        self.gk_cur.axes[0].deadzone = int(self.ui.dialXdz.sliderPosition())

        y_range = self.ui.sliderYrange.sliderPosition()
        self.gk_cur.axes[1].low = int(y_range[0])
        self.gk_cur.axes[1].center = int(y_range[1])
        self.gk_cur.axes[1].high = int(y_range[2])
        self.gk_cur.axes[1].deadzone = int(self.ui.dialYdz.sliderPosition())

        self.gk_cur.set_axes()

    def axis_invert(self):
        inputbtn = self.sender()
        if inputbtn.objectName() == "iXInvert":
            self.gk_cur.axes[0].invert = int(self.ui.iXInvert.isChecked())
        elif inputbtn.objectName() == "iYInvert":
            self.gk_cur.axes[1].invert = int(self.ui.iYInvert.isChecked())

    def axis_mode(self):
        self.gk_cur.axes[0].analog_mode = int(self.ui.radioXModeAnalog.isChecked())
        self.gk_cur.axes[1].analog_mode = int(self.ui.radioYModeAnalog.isChecked())

    def axis_limits_changed(self):
        inputbtn = self.sender()
        if inputbtn.objectName() == 'sliderXrange':
            self.gk_cur.sync_axis_limits(0, self.ui.sliderXrange.value())
        elif inputbtn.objectName() == 'sliderYrange':
            self.gk_cur.sync_axis_limits(1, self.ui.sliderYrange.value())

    def axis_dz_changed(self):
        inputbtn = self.sender()
        if inputbtn.objectName() == 'dialXdz':
            self.gk_cur.sync_axis_dz(0, self.ui.dialXdz.value())
        elif inputbtn.objectName() == 'dialYdz':
            self.gk_cur.sync_axis_dz(1, self.ui.dialYdz.value())

    def get_analog(self):
        self.gk_cur.get_analog()
        self.ui.oXCur.setText(str(self.gk_cur.axes[0].rawvalue))
        self.ui.oYCur.setText(str(self.gk_cur.axes[1].rawvalue))