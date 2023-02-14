import time
from PyQt5 import QtWidgets
import gk_data
from gk_data import gk_hw_commands as hwcommands
import gk_serial
from gk_gkbutton import GkButton
from gk_gkaxis import GkAxis
from gk_uimap import gk_uimap as uimap


class GkProfileData:
    def __init__(self):
        self.buttons = {}
        self.axes = [GkAxis, GkAxis]


class GameKey:
    def __init__(self, comport):
        self.buttons = {}   # button key is button name, value is keybind
        self.buttoncount = 30   # hw button count
        self.axes = []  # GkAxis index is hw position, value is object
        self.axiscount = 2  # hw axis count
        if not comport == -1:
            self.connection = gk_serial.GkSerial(comport)
        else:
            self.connection = None
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
        self.debug = 1

        # get data from device if there's a connection
        if self.connection:
            self.get_devinfo()
            self.get_config()

    def init_buttons(self):
        self.buttons.clear()
        for item in self.hwmap:
            if not item[:-1] == "kThumbStick":      # String compare to eliminate thumbstick from the button arrays
                self.buttons[item] = GkButton(0, 0, 0, 0, 0)     # init GkButton as blank 0 0

    def init_axes(self):
        # clear out the axes and append to HW limit
        self.axes.clear()
        for x in range(self.axiscount):
            self.axes.append(GkAxis())

    def get_devinfo(self):
        # Connect to every available serial port, check if there are gK devices connected
        if self.debug:
            print("Getting config for gK on", self.connection.connectionPort)
        self.version = self.connection.commandsend(hwcommands["Version"])[0]
        self.featureconfig = self.connection.commandsend(hwcommands["FeatureFlag"])[0]
        self.devicename = self.connection.commandsend(hwcommands["GetDeviceName"])[0]
        self.parse_featureflags()

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

    def get_config(self):
        self.get_buttons()
        self.get_axes()
        self.get_analog()

    def get_buttons(self):
        line = self.connection.commandsend(hwcommands["ReportButtonConfig"])
        if self.debug:
            print('received gtbu:', line)
        self.init_buttons()   # re-init the buttons to make sure there's no leftovers from prev config
        self.remotebutton = line
        if self.remotebutton is not None:
            for buttons_data in self.remotebutton[0].split("|"):
                for button_mapping in self.hwmap:
                    button = buttons_data.split("=")
                    if self.hwmap[button_mapping] == int(button[0]):    # Compare button string to dict mapping
                        button_data = button[1].split("&")
                        self.buttons[button_mapping].button_bind_a = int(button_data[0])
                        self.buttons[button_mapping].button_bind_b = int(button_data[1])
                        self.buttons[button_mapping].button_bind_c = int(button_data[2])
                        self.buttons[button_mapping].button_bind_d = int(button_data[3])
                        self.buttons[button_mapping].button_mode = int(button_data[4])
                        break
        else:
            print("Communication error")

    def get_axes(self):
        line = self.connection.commandsend(hwcommands["ReportAxesConfig"])
        if self.debug:
            print('received gtax:', line)
        self.init_axes()   # re-init the buttons to make sure there's no leftovers from prev config
        self.remoteaxes = line
        if self.remotebutton is not None:
            splitconfig = self.remoteaxes[0].split("|")
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

    def get_analog(self):
        if len(self.axes) < self.axiscount:
            self.init_axes()
        result = self.connection.commandsend(hwcommands["ReportAxesValues"])
        if self.debug:
            print('received repa:', result)
        if result is not None:
            splitconfig = result[0].split("&")
            for axis_num, axis_data in enumerate(splitconfig):
                self.axes[axis_num].rawvalue = int(axis_data)
        else:
            print("Communication error")

    def sync_axis_limits(self, axis_index, axis_limit_data):
        self.axes[axis_index].low = axis_limit_data[0]
        self.axes[axis_index].center = axis_limit_data[1]
        self.axes[axis_index].high = axis_limit_data[2]

    def sync_axis_dz(self, axis_index, axis_dz_data):
        self.axes[axis_index].deadzone = axis_dz_data

    def set_buttons(self):
        bindings = ["", "", ""]
        cmdset = 0
        segment = 0
        if self.connection:
            for button in self.buttons:
                button_id = str(self.hwmap[button])
                bind_a = str(self.buttons[button].button_bind_a)
                bind_b = str(self.buttons[button].button_bind_b)
                bind_c = str(self.buttons[button].button_bind_c)
                bind_d = str(self.buttons[button].button_bind_d)
                mode = str(self.buttons[button].button_mode)
                bindings[cmdset] += button_id + "=" + bind_a + "&" + bind_b + "&" + bind_c + "&" + bind_d + "&" + mode
                if segment < 9:
                    bindings[cmdset] += "|"
                    segment += 1
                else:
                    segment = 0
                    cmdset += 1
            for bindstring in bindings:
                cmd = "bind " + bindstring
                result = self.connection.commandsend(cmd)
                print("bindcmd: " + cmd)
                if result:
                    print("Return from device: ")
                    for x in result:
                        print(x)

    def set_axes(self):
        if not self.connection.is_open:
            self.connection.open()
        for index, axis_cur in enumerate(self.axes):
            axis_command = "stax "
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
        self.connection.write("savnv\n".encode('ascii'))
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
        exportblock = {"buttons": {}, "axes": {}}
        for button_object in self.buttons:
            exportblock["buttons"][button_object] = self.buttons[button_object].get_json()
        for axis_index, axis in enumerate(self.axes):
            exportblock["axes"][str(axis_index)] = axis.get_json()
        return exportblock

    def map_button_labels(self, ui_in):
        ui = ui_in
        for button in self.buttons:
            for index, sublist in enumerate(uimap):
                if button in sublist:
                    button_uimap_index = index
                    break
            self.buttons[button].label_a = ui.findChild(QtWidgets.QLabel, uimap[button_uimap_index][1])
            self.buttons[button].label_b = ui.findChild(QtWidgets.QLabel, uimap[button_uimap_index][2])
            self.buttons[button].label_c = ui.findChild(QtWidgets.QLabel, uimap[button_uimap_index][3])
            self.buttons[button].label_d = ui.findChild(QtWidgets.QLabel, uimap[button_uimap_index][4])

    def map_json(self, gkconfig_in):
        for button_name in gkconfig_in['buttons']:
            self.buttons[button_name].map_json(gkconfig_in['buttons'][button_name])
        for index_str in gkconfig_in['axes']:
            if int(index_str) < 30:  # 30 max HW buttons
                self.axes[int(index_str)].map_json(gkconfig_in['axes'][index_str])

    def update_all_labels(self, active_layer_in):
        for button in self.buttons:
            self.buttons[button].update_label(active_layer_in)
