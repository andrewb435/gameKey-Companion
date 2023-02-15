import os
from ui_stick import Ui_windowStick
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import gk_data
from gk_gkstick import GkStick


class StickUI(QtWidgets.QWidget):
    # Signals

    stick_data_return = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_windowStick()
        self.ui.setupUi(self)

        # Variables
        self.stick = GkStick()
        self.stick_profile = None
        self.profile_ctrl = None

        # Analog Axes
        self.ui.bSaveStickAs.clicked.connect(self.stick_save_as)
        self.ui.bSaveStick.clicked.connect(self.stick_save)
        self.ui.bResetStick.clicked.connect(self.stick_reset)
        self.ui.bCancel.clicked.connect(self.cancel)
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
        self.ui.radioXModeDigital.setStyleSheet(gk_data.gk_colormode[1])
        self.ui.radioXModeAnalog.setStyleSheet(gk_data.gk_colormode[2])
        self.ui.radioYModeDigital.setStyleSheet(gk_data.gk_colormode[1])
        self.ui.radioYModeAnalog.setStyleSheet(gk_data.gk_colormode[2])

    def update_dz(self):
        self.ui.oXdz.setText(str(self.ui.dialXdz.value()))
        self.ui.oYdz.setText(str(self.ui.dialYdz.value()))

    def update_labels(self):
        # Name
        self.ui.lName.setText(self.stick.name)
        # X Axis
        self.ui.sliderXrange.setValue(
            (
                int(self.stick.axes[0].low),
                int(self.stick.axes[0].center),
                int(self.stick.axes[0].high)
            )
        )
        # X Invert
        if int(self.stick.axes[0].invert) == 1:
            self.ui.iXInvert.setChecked(True)
        else:
            self.ui.iXInvert.setChecked(False)
        # X Mode
        if int(self.stick.axes[0].analog_mode) == 0:
            self.ui.radioXModeDigital.setChecked(True)
        else:
            self.ui.radioXModeAnalog.setChecked(True)

        # Y Axis
        self.ui.sliderYrange.setValue(
            (
                int(self.stick.axes[1].low),
                int(self.stick.axes[1].center),
                int(self.stick.axes[1].high)
            )
        )
        # Y Invert
        if int(self.stick.axes[1].invert) == 1:
            self.ui.iYInvert.setChecked(True)
        else:
            self.ui.iYInvert.setChecked(False)
        # Y Mode
        if int(self.stick.axes[1].analog_mode) == 0:
            self.ui.radioYModeDigital.setChecked(True)
        else:
            self.ui.radioYModeAnalog.setChecked(True)

        # Deadzone dial
        self.ui.dialXdz.setValue(int(self.stick.axes[0].deadzone))
        self.ui.oXdz.setText(str(self.stick.axes[0].deadzone))
        self.ui.dialYdz.setValue(int(self.stick.axes[1].deadzone))
        self.ui.oYdz.setText(str(self.stick.axes[1].deadzone))

    def stick_reset(self):
        self.stick.set_defaults()
        self.update_labels()

    def set_axes(self):
        x_range = self.ui.sliderXrange.sliderPosition()
        self.stick.axes[0].low = int(x_range[0])
        self.stick.axes[0].center = int(x_range[1])
        self.stick.axes[0].high = int(x_range[2])
        self.stick.axes[0].deadzone = int(self.ui.dialXdz.sliderPosition())

        y_range = self.ui.sliderYrange.sliderPosition()
        self.stick.axes[1].low = int(y_range[0])
        self.stick.axes[1].center = int(y_range[1])
        self.stick.axes[1].high = int(y_range[2])
        self.stick.axes[1].deadzone = int(self.ui.dialYdz.sliderPosition())

    def axis_invert(self):
        inputbtn = self.sender()
        if inputbtn.objectName() == "iXInvert":
            self.stick.axes[0].invert = int(self.ui.iXInvert.isChecked())
        elif inputbtn.objectName() == "iYInvert":
            self.stick.axes[1].invert = int(self.ui.iYInvert.isChecked())

    def axis_mode(self):
        self.stick.axes[0].analog_mode = int(self.ui.radioXModeAnalog.isChecked())
        self.stick.axes[1].analog_mode = int(self.ui.radioYModeAnalog.isChecked())

    def axis_limits_changed(self):
        inputbtn = self.sender()
        if inputbtn.objectName() == 'sliderXrange':
            axis_limit_data = self.ui.sliderXrange.value()
            self.stick.axes[0].low = axis_limit_data[0]
            self.stick.axes[0].center = axis_limit_data[1]
            self.stick.axes[0].high = axis_limit_data[2]
        elif inputbtn.objectName() == 'sliderYrange':
            axis_limit_data = self.ui.sliderYrange.value()
            self.stick.axes[1].low = axis_limit_data[0]
            self.stick.axes[1].center = axis_limit_data[1]
            self.stick.axes[1].high = axis_limit_data[2]

    def axis_dz_changed(self):
        inputbtn = self.sender()
        if inputbtn.objectName() == 'dialXdz':
            axis_dz_data = self.ui.dialXdz.value()
            self.stick.axes[0].deadzone = axis_dz_data
        elif inputbtn.objectName() == 'dialYdz':
            axis_dz_data = self.ui.dialYdz.value()
            self.stick.axes[1].deadzone = axis_dz_data

    def stick_input(self, profile_name_in, axisdata_in):
        self.stick.name = profile_name_in
        self.stick.map_json(axisdata_in)
        self.update_labels()

    def profile_input(self, profile_name_in, profile_list_in):
        self.stick.name = profile_name_in
        self.stick.map_json(profile_list_in)
        self.update_labels()

    def stick_save(self):
        if self.stick.name == "Onboard":
            self.stick_save_as()
        else:
            export_json = self.stick.get_json()
            self.profile_ctrl.output_stick_config_file(export_json, self.stick.name)
        self.stick_data_return.emit(self.stick.name)
        self.close()

    def stick_save_as(self):
        save_dialog = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save as...',
            self.profile_ctrl.user_home + self.profile_ctrl.config_path + self.profile_ctrl.stick_path,
            filter="*.json"
        )
        file = save_dialog[0].rstrip(".json") + ".json"
        self.stick.name = file.split(os.sep)[-1]
        export_json = self.stick.get_json()
        self.profile_ctrl.save_as_stick(file, export_json)
        self.stick_data_return.emit(self.stick.name)
        self.close()

    def cancel(self):
        self.close()
