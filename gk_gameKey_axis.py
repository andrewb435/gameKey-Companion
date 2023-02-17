from PyQt5 import QtWidgets
import gk_helper_converts
from gk_data_uimap import gk_uimap_analog as uimap


class GkAxis:
    def __init__(self):
        self.low = 0
        self.center = 511
        self.high = 1023
        self.deadzone = 0
        self.key_up = 0
        self.key_down = 0
        self.analog_mode = 0
        self.invert = 0
        self.rawvalue = 0
        self.label_up = None
        self.label_down = None

    def map_json(self, gk_axisdata):
        self.low = gk_axisdata['low']
        self.center = gk_axisdata['center']
        self.high = gk_axisdata['high']
        self.deadzone = gk_axisdata['deadzone']
        self.key_up = gk_axisdata['key_up']
        self.key_down = gk_axisdata['key_down']
        self.analog_mode = gk_axisdata['analog_mode']
        self.invert = gk_axisdata['invert']

    def map_label(self, ui_in, axis_index):
        uimap_data = uimap[axis_index]
        holding = ui_in.findChild(QtWidgets.QPushButton, uimap_data[1])
        self.label_up = holding
        holding = ui_in.findChild(QtWidgets.QPushButton, uimap_data[2])
        self.label_down = holding

    def load_stickdata(self, stickdata):
        self.low = stickdata['low']
        self.center = stickdata['center']
        self.high = stickdata['high']
        self.deadzone = stickdata['deadzone']
        self.analog_mode = stickdata['analog_mode']
        self.invert = stickdata['invert']

    def get_json(self):
        export_axis = {
            "low": self.low,
            "center": self.center,
            "high": self.high,
            "deadzone": self.deadzone,
            "key_up": self.key_up,
            "key_down": self.key_down,
            "analog_mode": self.analog_mode,
            "invert": self.invert
        }
        return export_axis

    def update_label(self):
        if self.label_up is not None:
            self.label_up.setText(gk_helper_converts.map_ard_to_txt(self.key_up))
            self.label_down.setText(gk_helper_converts.map_ard_to_txt(self.key_down))
