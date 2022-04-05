from ui_main import Ui_windowMain
from gk_bind import BindUI
from PyQt5 import QtWidgets
import gk_gameKey
import gk_profiles

# Serial
import serial.tools.list_ports
import serial
import gk_data

# Global gameKey list
gamekeylist = []


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main UI setup
        self.ui = Ui_windowMain()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        # Binding UI setup
        self.bindui = BindUI()

        # gk_cur setup
        self.gk_cur = gk_gameKey.GameKey(-1)

        # Profile setup
        self.ui.bConfigRefresh.clicked.connect(self.profile_reload)
        self.profile_data = gk_profiles.GkProfileList()
        self.ui.bConfigSave.clicked.connect(self.profile_save)
        self.ui.bConfigLoad.clicked.connect(self.profile_load)
        self.profile_reload()
        self.ui.configChooser.currentTextChanged.connect(self.profile_load)
        self.ui.bConfigSaveAs.clicked.connect(self.profile_saveas)

        # Button UI actions
        self.ui.bScanSerial.clicked.connect(self.get_serial)
        self.ui.bRetrieve.clicked.connect(self.get_config)
        self.ui.bClearAll.clicked.connect(self.bind_clearall)
        self.ui.bSendAll.clicked.connect(self.set_config)
        self.ui.bSaveEEPROM.clicked.connect(self.save_eeprom)

        # Analog Axes
        self.ui.bUpdateAnalog.clicked.connect(self.get_analog)
        self.ui.bSendAxes.clicked.connect(self.set_axes)
        self.ui.iXInvert.clicked.connect(self.axis_invert)
        self.ui.iYInvert.clicked.connect(self.axis_invert)

        '''
        Button Bind actions
        '''
        # Pinky
        self.ui.kPinkyB1.clicked.connect(self.bind_window)
        self.ui.kPinkyB2.clicked.connect(self.bind_window)
        self.ui.kPinkyB3.clicked.connect(self.bind_window)
        self.ui.kPinkyB4.clicked.connect(self.bind_window)
        self.ui.kPinkyB5.clicked.connect(self.bind_window)
        self.ui.kPinkyBAddon.clicked.connect(self.bind_window)

        # Ring
        self.ui.kRingB1.clicked.connect(self.bind_window)
        self.ui.kRingB2.clicked.connect(self.bind_window)
        self.ui.kRingB3.clicked.connect(self.bind_window)
        self.ui.kRingB4.clicked.connect(self.bind_window)
        self.ui.kRingB5.clicked.connect(self.bind_window)

        # Middle
        self.ui.kMiddleB1.clicked.connect(self.bind_window)
        self.ui.kMiddleB2.clicked.connect(self.bind_window)
        self.ui.kMiddleB3.clicked.connect(self.bind_window)
        self.ui.kMiddleB4.clicked.connect(self.bind_window)
        self.ui.kMiddleB5.clicked.connect(self.bind_window)

        # Index
        self.ui.kIndexB1.clicked.connect(self.bind_window)
        self.ui.kIndexB2.clicked.connect(self.bind_window)
        self.ui.kIndexB3.clicked.connect(self.bind_window)
        self.ui.kIndexB4.clicked.connect(self.bind_window)
        self.ui.kIndexB5.clicked.connect(self.bind_window)
        self.ui.kIndexBAddon.clicked.connect(self.bind_window)

        # ThumbNav
        self.ui.kThumbNavN.clicked.connect(self.bind_window)
        self.ui.kThumbNavE.clicked.connect(self.bind_window)
        self.ui.kThumbNavS.clicked.connect(self.bind_window)
        self.ui.kThumbNavW.clicked.connect(self.bind_window)
        self.ui.kThumbNavPush.clicked.connect(self.bind_window)

        # ThumbStick
        self.ui.kThumbStickN.clicked.connect(self.bind_window)
        self.ui.kThumbStickE.clicked.connect(self.bind_window)
        self.ui.kThumbStickS.clicked.connect(self.bind_window)
        self.ui.kThumbStickW.clicked.connect(self.bind_window)
        self.ui.kThumbStickPush.clicked.connect(self.bind_window)

        # Deadzone dial
        self.ui.dialXdz.valueChanged.connect(self.update_dz)
        self.ui.dialYdz.valueChanged.connect(self.update_dz)

        # Thumb Outer Button
        self.ui.kThumbBAddon.clicked.connect(self.bind_window)

        # ComboBox UI actions
        self.ui.comList.currentTextChanged.connect(self.devicechange)

        # QtRangeSlider from superqt
        self.ui.sliderXrange.setValue((100, 500, 900))
        self.ui.sliderXrange.setHandleLabelPosition(self.ui.sliderXrange.LabelPosition.LabelsBelow)
        self.ui.sliderYrange.setValue((100, 500, 900))
        self.ui.sliderYrange.setHandleLabelPosition(self.ui.sliderYrange.LabelPosition.LabelsBelow)

        self.ui.sliderXrange.valueChanged.connect(self.axis_limits_changed)
        self.ui.sliderYrange.valueChanged.connect(self.axis_limits_changed)
        self.ui.dialXdz.valueChanged.connect(self.axis_dz_changed)
        self.ui.dialYdz.valueChanged.connect(self.axis_dz_changed)

        # Set up label color indicators
        self.ui.lKEYBColor.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode[self.ui.lKEYBColor.text()]])
        self.ui.lGPADColor.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode[self.ui.lGPADColor.text()]])
        self.ui.lBOTHColor.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode[self.ui.lBOTHColor.text()]])

    def get_serial(self):
        comports = list(serial.tools.list_ports.comports())
        if len(comports) <= 0:
            self.ui.comList.clear()
            gamekeylist.clear()
        if len(comports) > 0:
            self.ui.comList.clear()
            gamekeylist.clear()
            counter = 0
            for x in comports:
                # Check the comport for a device responding with "gameKey"
                gamekeylist.append(gk_gameKey.GameKey(x.device))
                if gamekeylist[counter].get_device():
                    gamekeylist[counter].get_devinfo()
                    gamekeylist[counter].get_config()
                    self.ui.comList.addItem(x.device)
                    counter += 1
                else:
                    del gamekeylist[counter]

    def get_config(self):
        self.gk_cur.get_config()
        self.update_labels()

    def devicechange(self):
        if len(gamekeylist) > 0:
            if len(gamekeylist[self.ui.comList.currentIndex()].buttons) > 0:
                if len(gamekeylist[self.ui.comList.currentIndex()].axes) > 0:
                    self.gk_cur = gamekeylist[self.ui.comList.currentIndex()]
                    self.update_labels()

    def update_dz(self):
        self.ui.oXdz.setText(str(self.ui.dialXdz.value()))
        self.ui.oYdz.setText(str(self.ui.dialYdz.value()))

    def update_labels(self):
        # device labels
        self.ui.lDevName.setText(self.gk_cur.devicename)
        self.ui.lDevFirmware.setText(self.gk_cur.version)

        try:
            # Pinky
            self.ui.kPinkyB1.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kPinkyB1.objectName()].button_bind)
            )
            self.ui.kPinkyB1.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kPinkyB1.objectName()].button_mode]
            )
            self.ui.kPinkyB2.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kPinkyB2.objectName()].button_bind)
            )
            self.ui.kPinkyB2.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kPinkyB2.objectName()].button_mode]
            )
            self.ui.kPinkyB3.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kPinkyB3.objectName()].button_bind)
            )
            self.ui.kPinkyB3.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kPinkyB3.objectName()].button_mode]
            )
            self.ui.kPinkyB4.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kPinkyB4.objectName()].button_bind)
            )
            self.ui.kPinkyB4.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kPinkyB4.objectName()].button_mode]
            )
            self.ui.kPinkyB5.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kPinkyB5.objectName()].button_bind)
            )
            self.ui.kPinkyB5.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kPinkyB5.objectName()].button_mode]
            )
            self.ui.kPinkyBAddon.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kPinkyBAddon.objectName()].button_bind)
            )
            self.ui.kPinkyBAddon.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kPinkyBAddon.objectName()].button_mode]
            )

            # Ring
            self.ui.kRingB1.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kRingB1.objectName()].button_bind)
            )
            self.ui.kRingB1.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kRingB1.objectName()].button_mode]
            )
            self.ui.kRingB2.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kRingB2.objectName()].button_bind)
            )
            self.ui.kRingB2.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kRingB2.objectName()].button_mode]
            )
            self.ui.kRingB3.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kRingB3.objectName()].button_bind)
            )
            self.ui.kRingB3.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kRingB3.objectName()].button_mode]
            )
            self.ui.kRingB4.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kRingB4.objectName()].button_bind)
            )
            self.ui.kRingB4.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kRingB4.objectName()].button_mode]
            )
            self.ui.kRingB5.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kRingB5.objectName()].button_bind)
            )
            self.ui.kRingB5.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kRingB5.objectName()].button_mode]
            )

            # Middle
            self.ui.kMiddleB1.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kMiddleB1.objectName()].button_bind)
            )
            self.ui.kMiddleB1.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kMiddleB1.objectName()].button_mode]
            )
            self.ui.kMiddleB2.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kMiddleB2.objectName()].button_bind)
            )
            self.ui.kMiddleB2.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kMiddleB2.objectName()].button_mode]
            )
            self.ui.kMiddleB3.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kMiddleB3.objectName()].button_bind)
            )
            self.ui.kMiddleB3.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kMiddleB3.objectName()].button_mode]
            )
            self.ui.kMiddleB4.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kMiddleB4.objectName()].button_bind)
            )
            self.ui.kMiddleB4.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kMiddleB4.objectName()].button_mode]
            )
            self.ui.kMiddleB5.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kMiddleB5.objectName()].button_bind)
            )
            self.ui.kMiddleB5.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kMiddleB5.objectName()].button_mode]
            )

            # Index
            self.ui.kIndexB1.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kIndexB1.objectName()].button_bind)
            )
            self.ui.kIndexB1.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kIndexB1.objectName()].button_mode]
            )
            self.ui.kIndexB2.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kIndexB2.objectName()].button_bind)
            )
            self.ui.kIndexB2.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kIndexB2.objectName()].button_mode]
            )
            self.ui.kIndexB3.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kIndexB3.objectName()].button_bind)
            )
            self.ui.kIndexB3.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kIndexB3.objectName()].button_mode]
            )
            self.ui.kIndexB4.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kIndexB4.objectName()].button_bind)
            )
            self.ui.kIndexB4.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kIndexB4.objectName()].button_mode]
            )
            self.ui.kIndexB5.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kIndexB5.objectName()].button_bind)
            )
            self.ui.kIndexB5.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kIndexB5.objectName()].button_mode]
            )
            self.ui.kIndexBAddon.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kIndexBAddon.objectName()].button_bind)
            )
            self.ui.kIndexBAddon.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kIndexBAddon.objectName()].button_mode]
            )

            # ThumbNavsrcinput
            self.ui.kThumbNavN.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kThumbNavN.objectName()].button_bind)
            )
            self.ui.kThumbNavN.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kThumbNavN.objectName()].button_mode]
            )
            self.ui.kThumbNavE.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kThumbNavE.objectName()].button_bind)
            )
            self.ui.kThumbNavE.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kThumbNavE.objectName()].button_mode]
            )
            self.ui.kThumbNavS.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kThumbNavS.objectName()].button_bind)
            )
            self.ui.kThumbNavS.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kThumbNavS.objectName()].button_mode]
            )
            self.ui.kThumbNavW.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kThumbNavW.objectName()].button_bind)
            )
            self.ui.kThumbNavW.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kThumbNavW.objectName()].button_mode]
            )
            self.ui.kThumbNavPush.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kThumbNavPush.objectName()].button_bind)
            )
            self.ui.kThumbNavPush.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kThumbNavPush.objectName()].button_mode]
            )

            # Thumb Outer Button
            self.ui.kThumbBAddon.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kThumbBAddon.objectName()].button_bind)
            )
            self.ui.kThumbBAddon.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kThumbBAddon.objectName()].button_mode]
            )

            # ThumbStick Button
            self.ui.kThumbStickPush.setText(gk_gameKey.map_ard_to_txt(
                self.gk_cur.buttons[self.ui.kThumbStickPush.objectName()].button_bind)
            )
            self.ui.kThumbStickPush.setStyleSheet(
                gk_data.gk_colormode[self.gk_cur.buttons[self.ui.kThumbStickPush.objectName()].button_mode]
            )

            # ThumbStick Axis
            self.ui.kThumbStickN.setText(gk_gameKey.map_ard_to_txt(self.gk_cur.axes[0].key_up))      # N X+
            self.ui.kThumbStickS.setText(gk_gameKey.map_ard_to_txt(self.gk_cur.axes[0].key_down))    # S X-
            self.ui.kThumbStickE.setText(gk_gameKey.map_ard_to_txt(self.gk_cur.axes[1].key_up))      # E Y+
            self.ui.kThumbStickW.setText(gk_gameKey.map_ard_to_txt(self.gk_cur.axes[1].key_down))    # W Y-

            # X Axis
            self.ui.sliderXrange.setValue(
                (
                    int(self.gk_cur.axes[0].low),
                    int(self.gk_cur.axes[0].center),
                    int(self.gk_cur.axes[0].high)
                )
            )
            if int(self.gk_cur.axes[0].invert) == 1:
                self.ui.iXInvert.setChecked(True)
            else:
                self.ui.iXInvert.setChecked(False)

            # Y Axis
            self.ui.sliderYrange.setValue(
                (
                    int(self.gk_cur.axes[1].low),
                    int(self.gk_cur.axes[1].center),
                    int(self.gk_cur.axes[1].high)
                )
            )
            if int(self.gk_cur.axes[1].invert) == 1:
                self.ui.iYInvert.setChecked(True)
            else:
                self.ui.iYInvert.setChecked(False)

            # Deadzone dial
            self.ui.dialXdz.setValue(int(self.gk_cur.axes[0].deadzone))
            self.ui.oXdz.setText(str(self.gk_cur.axes[0].deadzone))
            self.ui.dialYdz.setValue(int(self.gk_cur.axes[1].deadzone))
            self.ui.oYdz.setText(str(self.gk_cur.axes[1].deadzone))
        except KeyError:
            print("keyError")

    def bind_clearall(self):
        self.gk_cur.init_buttons()
        self.gk_cur.reset_axes_limits()
        self.update_labels()

    def set_config(self):
        self.gk_cur.set_buttons()
        self.set_axes()

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

    def bind_window(self):
        srcinput = self.sender()
        currentkeybind = 0
        currentkeymode = 0
        try:
            currentkeybind = self.gk_cur.buttons[srcinput.objectName()].button_bind
            currentkeymode = self.gk_cur.buttons[srcinput.objectName()].button_mode
        except KeyError:
            if srcinput.objectName() == 'kThumbStickN':
                currentkeybind = self.gk_cur.axes[0].key_up
            elif srcinput.objectName() == 'kThumbStickS':
                currentkeybind = self.gk_cur.axes[0].key_down
            if srcinput.objectName() == 'kThumbStickE':
                currentkeybind = self.gk_cur.axes[1].key_up
            elif srcinput.objectName() == 'kThumbStickW':
                currentkeybind = self.gk_cur.axes[1].key_down

        # Set up some button details
        self.bindui.ui.bModeKEYB.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode["KEYB"]])
        self.bindui.ui.bModeGPAD.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode["GPAD"]])
        self.bindui.ui.bModeBOTH.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode["BOTH"]])
        self.bindui.ui.keyBindingIndicator.setStyleSheet(gk_data.gk_colormode[currentkeymode])

        self.bindui.bind_data_return.connect(self.set_bind)
        self.bindui.bind_data_in(srcinput.objectName(), currentkeybind, currentkeymode)
        self.bindui.show()

    def get_analog(self):
        self.gk_cur.get_analog()
        self.ui.oXCur.setText(str(self.gk_cur.axes[0].rawvalue))
        self.ui.oYCur.setText(str(self.gk_cur.axes[1].rawvalue))

    def set_bind(self, newbutton, newkeybind, newkeymode):
        if newbutton == 'kThumbStickN':
            self.gk_cur.axes[0].key_up = newkeybind
        elif newbutton == 'kThumbStickS':
            self.gk_cur.axes[0].key_down = newkeybind
        if newbutton == 'kThumbStickE':
            self.gk_cur.axes[1].key_up = newkeybind
        elif newbutton == 'kThumbStickW':
            self.gk_cur.axes[1].key_down = newkeybind
        else:
            self.gk_cur.buttons[newbutton].button_bind = newkeybind
            self.gk_cur.buttons[newbutton].button_mode = newkeymode
        print("new btn ", str(newbutton), " key", str(newkeybind), " mode", str(newkeymode))
        self.update_labels()

    def save_eeprom(self):
        self.gk_cur.set_eeprom()

    def profile_load(self):
        if self.ui.configChooser.currentIndex() > 0:
            # index > 'Onboard' profile
            self.gk_cur.map_json(self.profile_data.load_profile(self.ui.configChooser.currentText()))
            self.update_labels()
        elif self.ui.configChooser.currentIndex() == 0:
            # index = 'Onboard' profile
            self.gk_cur.get_config()
            self.update_labels()

    def profile_reload(self):
        self.profile_data.get_profile_list()
        # Store the current selection for after rebuild
        curprofile = self.ui.configChooser.currentText()
        self.ui.configChooser.clear()
        self.ui.configChooser.addItem("Onboard")
        for profileitem in self.profile_data.profile_items:
            self.ui.configChooser.addItem(profileitem.config.name)
        if self.ui.configChooser.findText(curprofile) > 0:
            # Return the current selection to selected status
            self.ui.configChooser.setCurrentIndex(self.ui.configChooser.findText(curprofile))
        else:
            # set to Onboard if nothing else
            self.ui.configChooser.setCurrentIndex(0)

    def profile_save(self):
        if self.ui.configChooser.currentIndex() > 0:
            # Skip 'Onboard' index 0
            self.profile_data.output_json(self.gk_cur.get_json(), self.ui.configChooser.currentText())
        elif self.ui.configChooser.currentIndex() == 0:
            # 'Onboard' index 0
            self.set_config()

    def profile_saveas(self):
        save_dialog = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save as...',
            self.profile_data.user_home + self.profile_data.config_path,
            filter="*.json"
        )
        file = save_dialog[0] + ".json"
        self.profile_data.save_as(file, self.gk_cur.get_json())
        self.profile_reload()
