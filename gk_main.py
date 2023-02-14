import gk_serial
from ui_main import Ui_windowMain
from gk_bind import BindUI
from PyQt5 import QtWidgets
import gk_gameKey
import gk_helpers
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
        self.gk_cur = None
        self.activeLayer = 0

        # label colors
        self.init_colors()

        # Profile setup
        self.ui.bConfigRefresh.clicked.connect(self.profile_reload)
        self.profile_data = gk_profiles.GkProfileList()
        self.ui.bConfigSave.clicked.connect(self.profile_save)
        self.ui.bConfigLoad.clicked.connect(self.profile_load)
        self.profile_reload()
        # self.ui.configChooser.currentTextChanged.connect(self.profile_load) # Load from file on select
        self.ui.bConfigSaveAs.clicked.connect(self.profile_saveas)

        # Button UI actions
        self.ui.bScanSerial.clicked.connect(self.get_serial)
        self.ui.bRetrieve.clicked.connect(self.get_config)
        self.ui.bClearAll.clicked.connect(self.bind_clearall)
        self.ui.bSendAll.clicked.connect(self.set_config)
        self.ui.bSaveEEPROM.clicked.connect(self.save_eeprom)

        # Layer Radio actions
        self.ui.rLayerA.clicked.connect(self.change_layer)
        self.ui.rLayerB.clicked.connect(self.change_layer)
        self.ui.rLayerC.clicked.connect(self.change_layer)
        self.ui.rLayerD.clicked.connect(self.change_layer)
        self.currentLayer = 0

        '''
        Button Bind actions
        '''
        # Pinky
        self.ui.kPinky1.clicked.connect(self.bind_window)
        self.ui.kPinky2.clicked.connect(self.bind_window)
        self.ui.kPinky3.clicked.connect(self.bind_window)
        self.ui.kPinky4.clicked.connect(self.bind_window)
        self.ui.kPinky5.clicked.connect(self.bind_window)
        self.ui.kPinkyAddon.clicked.connect(self.bind_window)

        # Ring
        self.ui.kRing1.clicked.connect(self.bind_window)
        self.ui.kRing2.clicked.connect(self.bind_window)
        self.ui.kRing3.clicked.connect(self.bind_window)
        self.ui.kRing4.clicked.connect(self.bind_window)
        self.ui.kRing5.clicked.connect(self.bind_window)

        # Middle
        self.ui.kMiddle1.clicked.connect(self.bind_window)
        self.ui.kMiddle2.clicked.connect(self.bind_window)
        self.ui.kMiddle3.clicked.connect(self.bind_window)
        self.ui.kMiddle4.clicked.connect(self.bind_window)
        self.ui.kMiddle5.clicked.connect(self.bind_window)

        # Index
        self.ui.kIndex1.clicked.connect(self.bind_window)
        self.ui.kIndex2.clicked.connect(self.bind_window)
        self.ui.kIndex3.clicked.connect(self.bind_window)
        self.ui.kIndex4.clicked.connect(self.bind_window)
        self.ui.kIndex5.clicked.connect(self.bind_window)
        self.ui.kIndexAddon.clicked.connect(self.bind_window)

        # ThumbNav
        self.ui.kThumbNavUp.clicked.connect(self.bind_window)
        self.ui.kThumbNavFwd.clicked.connect(self.bind_window)
        self.ui.kThumbNavDown.clicked.connect(self.bind_window)
        self.ui.kThumbNavBack.clicked.connect(self.bind_window)
        self.ui.kThumbNavPush.clicked.connect(self.bind_window)

        # ThumbStick
        self.ui.kThumbStickN.clicked.connect(self.bind_window)
        self.ui.kThumbStickE.clicked.connect(self.bind_window)
        self.ui.kThumbStickS.clicked.connect(self.bind_window)
        self.ui.kThumbStickW.clicked.connect(self.bind_window)
        self.ui.kThumbStickPush.clicked.connect(self.bind_window)

        # Thumb Outer Button
        self.ui.kThumbBAddon.clicked.connect(self.bind_window)

        # ComboBox UI actions
        self.ui.comList.currentTextChanged.connect(self.devicechange)

    def init_colors(self):
        # Set up label color indicators
        self.ui.lKEYBColor.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode[self.ui.lKEYBColor.text()]])
        self.ui.lGPADColor.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode[self.ui.lGPADColor.text()]])
        self.ui.lBOTHColor.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode[self.ui.lBOTHColor.text()]])

        # Layer Selector
        self.ui.rLayerA.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.rLayerB.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.rLayerC.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.rLayerD.setStyleSheet(gk_data.gk_layercolor[3])

        # Pinky
        # Layer 0 / A
        self.ui.lPinkyA1.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lPinkyA2.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lPinkyA3.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lPinkyA4.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lPinkyA5.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lPinkyAAddon.setStyleSheet(gk_data.gk_layercolor[0])
        # Layer 1 / B
        self.ui.lPinkyB1.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lPinkyB2.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lPinkyB3.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lPinkyB4.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lPinkyB5.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lPinkyBAddon.setStyleSheet(gk_data.gk_layercolor[1])
        # Layer 2 / C
        self.ui.lPinkyC1.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lPinkyC2.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lPinkyC3.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lPinkyC4.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lPinkyC5.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lPinkyCAddon.setStyleSheet(gk_data.gk_layercolor[2])
        # Layer 3 / D
        self.ui.lPinkyD1.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lPinkyD2.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lPinkyD3.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lPinkyD4.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lPinkyD5.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lPinkyDAddon.setStyleSheet(gk_data.gk_layercolor[3])

        # Ring
        # Layer 0 / A
        self.ui.lRingA1.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lRingA2.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lRingA3.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lRingA4.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lRingA5.setStyleSheet(gk_data.gk_layercolor[0])
        # Layer 1 / B
        self.ui.lRingB1.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lRingB2.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lRingB3.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lRingB4.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lRingB5.setStyleSheet(gk_data.gk_layercolor[1])
        # Layer 2 / C
        self.ui.lRingC1.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lRingC2.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lRingC3.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lRingC4.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lRingC5.setStyleSheet(gk_data.gk_layercolor[2])
        # Layer 3 / D
        self.ui.lRingD1.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lRingD2.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lRingD3.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lRingD4.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lRingD5.setStyleSheet(gk_data.gk_layercolor[3])

        # Middle
        # Layer 0 / A
        self.ui.lMiddleA1.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lMiddleA2.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lMiddleA3.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lMiddleA4.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lMiddleA5.setStyleSheet(gk_data.gk_layercolor[0])
        # Layer 1 / B
        self.ui.lMiddleB1.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lMiddleB2.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lMiddleB3.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lMiddleB4.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lMiddleB5.setStyleSheet(gk_data.gk_layercolor[1])
        # Layer 2 / C
        self.ui.lMiddleC1.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lMiddleC2.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lMiddleC3.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lMiddleC4.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lMiddleC5.setStyleSheet(gk_data.gk_layercolor[2])
        # Layer 3 / D
        self.ui.lMiddleD1.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lMiddleD2.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lMiddleD3.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lMiddleD4.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lMiddleD5.setStyleSheet(gk_data.gk_layercolor[3])

        # Index
        # Layer 0 / A
        self.ui.lIndexA1.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lIndexA2.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lIndexA3.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lIndexA4.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lIndexA5.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lIndexAAddon.setStyleSheet(gk_data.gk_layercolor[0])
        # Layer 1 / B
        self.ui.lIndexB1.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lIndexB2.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lIndexB3.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lIndexB4.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lIndexB5.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lIndexBAddon.setStyleSheet(gk_data.gk_layercolor[1])
        # Layer 2 / C
        self.ui.lIndexC1.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lIndexC2.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lIndexC3.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lIndexC4.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lIndexC5.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lIndexCAddon.setStyleSheet(gk_data.gk_layercolor[2])
        # Layer 3 / D
        self.ui.lIndexD1.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lIndexD2.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lIndexD3.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lIndexD4.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lIndexD5.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lIndexDAddon.setStyleSheet(gk_data.gk_layercolor[3])

        # Thumb Nav
        # Layer 0 / A
        self.ui.lThumbNavUpA.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lThumbNavFwdA.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lThumbNavDownA.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lThumbNavBackA.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.lThumbNavPushA.setStyleSheet(gk_data.gk_layercolor[0])
        # Layer 1 / B
        self.ui.lThumbNavUpB.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lThumbNavFwdB.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lThumbNavDownB.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lThumbNavBackB.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.lThumbNavPushB.setStyleSheet(gk_data.gk_layercolor[1])
        # Layer 2 / C
        self.ui.lThumbNavUpC.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lThumbNavFwdC.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lThumbNavDownC.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lThumbNavBackC.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.lThumbNavPushC.setStyleSheet(gk_data.gk_layercolor[2])
        # Layer 3 / D
        self.ui.lThumbNavUpD.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lThumbNavFwdD.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lThumbNavDownD.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lThumbNavBackD.setStyleSheet(gk_data.gk_layercolor[3])
        self.ui.lThumbNavPushD.setStyleSheet(gk_data.gk_layercolor[3])

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
                print("Trying device " + x.device)
                device = gk_serial.GkSerial(x.device)
                cmd = gk_data.gk_hw_commands["DeviceInfo"]
                result = device.commandsend(cmd)
                if result:
                    result = result[0]
                if result == "gameKey":
                    print("gameKey found at " + x.device)
                    gamekeylist.append(gk_gameKey.GameKey(x.device))
                    self.ui.comList.addItem(x.device)
                else:
                    print("Device " + x.device + " did not respond correctly, \"" + str(result) + "\"")

    def get_config(self):
        self.gk_cur.get_config()
        self.gk_cur.map_button_labels(self)
        self.gk_cur.update_all_labels(self.activeLayer)

    def devicechange(self):
        if len(gamekeylist) > 0:
            if len(gamekeylist[self.ui.comList.currentIndex()].buttons) > 0:
                if len(gamekeylist[self.ui.comList.currentIndex()].axes) > 0:
                    self.gk_cur = gamekeylist[self.ui.comList.currentIndex()]

    def bind_clearall(self):
        self.gk_cur.init_buttons()
        self.gk_cur.reset_axes_limits()
        self.gk_cur.update_all_labels()

    def set_config(self):
        self.gk_cur.set_buttons()

    def bind_window(self):
        srcinput = self.sender()
        currentkeybinds = [0, 0, 0, 0]
        currentkeymode = 0
        try:
            currentkeybinds[0] = self.gk_cur.buttons[srcinput.objectName()].button_bind_a
            currentkeybinds[1] = self.gk_cur.buttons[srcinput.objectName()].button_bind_b
            currentkeybinds[2] = self.gk_cur.buttons[srcinput.objectName()].button_bind_c
            currentkeybinds[3] = self.gk_cur.buttons[srcinput.objectName()].button_bind_d
            currentkeymode = self.gk_cur.buttons[srcinput.objectName()].button_mode
        except KeyError:
            if srcinput.objectName() == 'kThumbStickN':
                currentkeybinds[0] = self.gk_cur.axes[0].key_up
            elif srcinput.objectName() == 'kThumbStickS':
                currentkeybinds[0] = self.gk_cur.axes[0].key_down
            if srcinput.objectName() == 'kThumbStickE':
                currentkeybinds[0] = self.gk_cur.axes[1].key_up
            elif srcinput.objectName() == 'kThumbStickW':
                currentkeybinds[0] = self.gk_cur.axes[1].key_down

        # Set up some button details
        self.bindui.ui.bModeKEYB.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode["KEYB"]])
        self.bindui.ui.bModeGPAD.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode["GPAD"]])
        self.bindui.ui.bModeBOTH.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode["BOTH"]])
        # self.bindui.ui.keyBindingIndicator.setStyleSheet(gk_data.gk_colormode[currentkeymode])

        self.bindui.bind_data_return.connect(self.set_bind)
        self.bindui.bind_data_in(srcinput.objectName(), currentkeybinds, currentkeymode)
        self.bindui.show()

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

    def change_layer(self):
        srcinput = self.sender()
        if srcinput.objectName() == "rLayerA":
            self.activeLayer = 0
        elif srcinput.objectName() == "rLayerB":
            self.activeLayer = 1
        elif srcinput.objectName() == "rLayerC":
            self.activeLayer = 2
        elif srcinput.objectName() == "rLayerD":
            self.activeLayer = 3
        self.gk_cur.update_all_labels(self.activeLayer)
