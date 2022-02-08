import serial
import time
import gk_data


def map_txt_to_ard(name_in):
    # wrapper for _map_to_data for gk_arduinoascii[][2] (txt) to gk_arduinoascii[][0] (arduino dec)
    return _map_to_data(2, 0, name_in)


def map_ard_to_txt(dec_in):
    # wrapper for _map_to_data for gk_arduinoascii[][0] (arduino dec) to gk_arduinoascii[][2] (txt)
    return _map_to_data(0, 2, int(dec_in))


def map_qt_to_ard(hex_in):
    # wrapper for _map_to_data for gk_arduinoascii[][1] (Qt::Key) to gk_arduinoascii[][0] (arduino dec)
    return _map_to_data(1, 0, int(hex_in))


def _map_to_data(index_in, index_out, map_in):
    # Map arbitrary columns in gk_arduinoascii
    for binding in gk_data.gk_arduinoascii:
        if binding[index_in] == map_in:
            return binding[index_out]


class GkProfileData:
    def __init__(self):
        self.buttons = {}
        self.axes = [GkAxis, GkAxis]


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


class GameKey:
    def __init__(self, comport):
        self.buttons = {}   # button key is button name, value is keybind
        self.buttoncount = 30   # hw button count
        self.axes = []  # GkAxis index is hw position, value is object
        self.axiscount = 2  # hw axis count
        try:
            self.connection = serial.Serial(comport, baudrate=115200, timeout=1)
        except ValueError:
            pass
        self.remotebutton = None
        self.remoteaxes = None
        self.localbind = None
        self.localunbind = None
        self.featureconfig = None
        self.hand = None
        self.bthumb = None
        self.bindex = None
        self.bpinky = None
        self.version = None
        self.devicename = None
        self.hwmap = None
        self.debug = 0

    def init_buttons(self):
        self.buttons.clear()
        for item in self.hwmap:
            if not item[:-1] == "kThumbStick":
                self.buttons[item] = 0

    def init_axes(self):
        # clear out the axes and append to HW limit
        self.axes.clear()
        for x in range(self.axiscount):
            self.axes.append(GkAxis())

    def get_devinfo(self):
        # Connect to every available serial port, check if there are gK devices connected
        if self.debug:
            print("Getting config for gK on", self.connection.port)
        if not self.connection.is_open:
            self.connection.open()
        line = ""
        for x in ["vers", "feat", "getname"]:
            cmd = x + "\n"
            self.connection.write(cmd.encode('ascii'))
            time.sleep(0.010)  # 10ms delay to allow serial to flow
            line += self.connection.readline().decode('ascii')
        line = line.splitlines()
        self.version = line[0]
        self.featureconfig = line[1]
        self.devicename = line[2]
        self.parse_featureflags()
        self.connection.reset_input_buffer()

    def parse_featureflags(self):
        # bitflag parsing for features on the device
        hand_mask = int("00001000", 2)
        thumb_mask = int("00000100", 2)
        pinky_mask = int("00000010", 2)
        index_mask = int("00000001", 2)
        self.hand = (int(self.featureconfig) & hand_mask)
        self.bthumb = (int(self.featureconfig) & thumb_mask)
        self.bpinky = (int(self.featureconfig) & pinky_mask)
        self.bindex = (int(self.featureconfig) & index_mask)
        self.parse_hwmap()

    def parse_hwmap(self):
        if self.hand:   # true is a gk for the right hand, false for left
            print("detected right hand")
            self.hwmap = gk_data.gk_hw_righthand
        else:
            print("detected left hand")
            self.hwmap = gk_data.gk_hw_lefthand

    def get_device(self):
        if not self.connection.is_open:
            self.connection.open()
        self.connection.write("devinfo\n".encode('ascii'))
        time.sleep(0.010)  # 10ms delay to allow serial to flow
        if self.connection.in_waiting > 0:
            line = self.connection.readline().decode('ascii').rstrip()
        else:
            line = None
        self.connection.reset_input_buffer()
        if line == 'gameKey':
            self.init_axes()
            return True
        else:
            return False

    def get_config(self):
        self.get_buttons()
        self.get_axes()
        self.get_analog()

    def get_buttons(self):
        if not self.connection.is_open:
            self.connection.open()
        self.connection.write("getbuttons\n".encode('ascii'))
        time.sleep(0.010)   # 10ms delay to allow serial to flow
        line = self.connection.readline().decode('ascii').rstrip()
        if self.debug:
            print('received getbuttons:', line)
        self.init_buttons()   # re-init the buttons to make sure there's no leftovers from prev config
        self.remotebutton = line
        splitconfig = self.remotebutton.split("&")
        for configitem in splitconfig:
            configitem = configitem.split("=")
            for button_mapping in self.hwmap:
                if self.hwmap[button_mapping] == int(configitem[0]):
                    self.buttons[button_mapping] = int(configitem[1])
                    break
        self.connection.reset_input_buffer()

    def get_axes(self):
        if not self.connection.is_open:
            self.connection.open()
        self.connection.write("getaxes\n".encode('ascii'))
        time.sleep(0.010)   # 10ms delay to allow serial to flow
        line = self.connection.readline().decode('ascii').rstrip()
        if self.debug:
            print('received getaxes:', line)
        self.init_axes()   # re-init the buttons to make sure there's no leftovers from prev config
        self.remoteaxes = line
        splitconfig = self.remoteaxes.split("|")
        for config_item in splitconfig:
            config_item = config_item.split("=")
            cur_axis = self.axes[int(config_item[0])]
            config_params = config_item[1].split("&")
            cur_axis.low = config_params[0]
            cur_axis.center = config_params[1]
            cur_axis.high = config_params[2]
            cur_axis.deadzone = config_params[3]
            cur_axis.key_up = config_params[4]
            cur_axis.key_down = config_params[5]
            cur_axis.analog_mode = config_params[6]
            cur_axis.invert = config_params[7]
            cur_axis.rawvalue = 0
        self.connection.reset_input_buffer()

    def get_analog(self):
        if len(self.axes) < self.axiscount:
            self.init_axes()
        if not self.connection.is_open:
            self.connection.open()
        self.connection.write("reporta\n".encode('ascii'))
        time.sleep(0.010)   # 10ms delay to allow serial to flow
        line = self.connection.readline().decode('ascii').rstrip()
        if self.debug:
            print('received reporta:', line)
        splitconfig = line.split("&")
        for axis_num, axis_data in enumerate(splitconfig):
            self.axes[axis_num].rawvalue = int(axis_data)
        self.connection.reset_input_buffer()

    def sync_axis_limits(self, axis_index, axis_limit_data):
        self.axes[axis_index].low = axis_limit_data[0]
        self.axes[axis_index].center = axis_limit_data[1]
        self.axes[axis_index].high = axis_limit_data[2]

    def sync_axis_dz(self, axis_index, axis_dz_data):
        self.axes[axis_index].deadzone = axis_dz_data

    def set_buttons(self):
        unbind_cmd = "unbind "
        unbind_cntr = 0
        bind_cmd = "bind "
        bind_cntr = 0
        for button in self.buttons:
            binding = self.buttons[button]
            if binding == 0:
                if unbind_cntr > 0:
                    unbind_cmd += "&" + str(self.hwmap[button])
                else:
                    unbind_cmd += str(self.hwmap[button])
                    unbind_cntr += 1
            else:
                if bind_cntr > 0:
                    bind_cmd += "&" + str(self.hwmap[button]) + "=" + str(binding)
                else:
                    bind_cmd += str(self.hwmap[button]) + "=" + str(binding)
                    bind_cntr += 1
        self.localunbind = unbind_cmd + "\n"
        self.localbind = bind_cmd + "\n"
        print("unbind:", self.localunbind, end='')
        print("bind:", self.localbind, end='')

        # unbind
        if self.debug:
            print("Sending unbind...")
        line = ""
        if not self.connection.is_open:
            self.connection.open()
        self.connection.write(self.localunbind.encode('ascii'))
        while self.connection.in_waiting > 0:
            line += self.connection.readline().decode('ascii')
        if self.debug:
            print("Response from unbind:", line, end='')
        self.connection.reset_input_buffer()

        # bind
        print("Sending bind...", end='')
        line = ""
        if not self.connection.is_open:
            self.connection.open()
        self.connection.write(self.localbind.encode('ascii'))
        while self.connection.in_waiting > 0:
            line += self.connection.readline().decode('ascii', 'ignore')
        if self.debug:
            print("Response from bind:", line, end='')
        self.connection.reset_input_buffer()

    def set_axes(self):
        if not self.connection.is_open:
            self.connection.open()
        for index, axis_cur in enumerate(self.axes):
            axis_command = "setaxis "
            axis_command += str(index)+"="
            axis_command += str(axis_cur.low) + "&"
            axis_command += str(axis_cur.center) + "&"
            axis_command += str(axis_cur.high) + "&"
            axis_command += str(axis_cur.deadzone) + "&"
            axis_command += str(axis_cur.key_up) + "&"
            axis_command += str(axis_cur.key_down) + "&"
            axis_command += str(axis_cur.analog_mode) + "&"
            axis_command += str(axis_cur.invert) + "\n"
            print("sending axis config:", axis_command, end='')
            line = ""
            self.connection.write(axis_command.encode('ascii'))
            time.sleep(0.010)   # 10ms delay to allow serial to flow
            while self.connection.in_waiting > 0:
                line += self.connection.readline().decode('ascii', 'ignore')
            if self.debug:
                print("Response from axis config", index, ":", line, end='')
            self.connection.reset_input_buffer()

    def set_eeprom(self):
        if not self.connection.is_open:
            self.connection.open()
        print("saving to device memory")
        line = ""
        self.connection.write("savenv\n".encode('ascii'))
        time.sleep(0.010)  # 10ms delay to allow serial to flow
        while self.connection.in_waiting > 0:
            line += self.connection.readline().decode('ascii', 'ignore')
        if self.debug:
            print("Response from saving to device memory:", end='')
        print(line, end='')
        self.connection.reset_input_buffer()

    def reset_axes_limits(self):
        for axis in self.axes:
            axis.low = 0
            axis.center = 511
            axis.high = 1023
            axis.invert = False
            axis.deadzone = 20

    def get_json(self):
        export = {}
        export_buttons = self.buttons
        export["buttons"] = export_buttons
        export["axes"] = {}
        for axis_index, axis in enumerate(self.axes):
            export["axes"][str(axis_index)] = axis.get_json()
        return export

    def map_json(self, gkconfig_in):
        self.buttons = gkconfig_in['buttons']
        for index_str in gkconfig_in['axes']:
            if int(index_str) < 30:  # 30 max HW buttons
                self.axes[int(index_str)].map_json(gkconfig_in['axes'][index_str])
