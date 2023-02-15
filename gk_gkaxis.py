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

    def map_json(self, gk_axisdata):
        self.low = gk_axisdata['low']
        self.center = gk_axisdata['center']
        self.high = gk_axisdata['high']
        self.deadzone = gk_axisdata['deadzone']
        self.key_up = gk_axisdata['key_up']
        self.key_down = gk_axisdata['key_down']
        self.analog_mode = gk_axisdata['analog_mode']
        self.invert = gk_axisdata['invert']

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
