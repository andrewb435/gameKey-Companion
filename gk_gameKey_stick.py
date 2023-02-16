
class GkStickAxis:
    def __init__(self):
        self.low = 0
        self.center = 511
        self.high = 1023
        self.deadzone = 200
        self.analog_mode = 0
        self.invert = 0
        self.rawvalue = 0

    def map_json(self, gk_axisdata):
        self.low = gk_axisdata['low']
        self.center = gk_axisdata['center']
        self.high = gk_axisdata['high']
        self.deadzone = gk_axisdata['deadzone']
        self.analog_mode = gk_axisdata['analog_mode']
        self.invert = gk_axisdata['invert']

    def get_json(self):
        export_axis = {
            "low": self.low,
            "center": self.center,
            "high": self.high,
            "deadzone": self.deadzone,
            "analog_mode": self.analog_mode,
            "invert": self.invert
        }
        return export_axis


class GkStick:
    def __init__(self):
        self.axes = [GkStickAxis(), GkStickAxis()]
        self.name = ""

    def set_defaults(self):
        for axis in self.axes:
            axis.low = 0
            axis.center = 511
            axis.high = 1023
            axis.analog_mode = 0
            axis.invert = 0
            axis.deadzone = 200

    def map_json(self, gk_stickdata):
        for axis_index in gk_stickdata['axes']:
            if int(axis_index) < 2:  # 2 max HW axes
                self.axes[int(axis_index)].map_json(gk_stickdata['axes'][axis_index])

    def get_json(self):
        exportblock = {"name": self.name, "axes": {}}
        for axis_index, axis in enumerate(self.axes):
            exportblock["axes"][str(axis_index)] = axis.get_json()
        return exportblock
