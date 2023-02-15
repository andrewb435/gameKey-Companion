from ui_bind import Ui_windowBind
from PyQt5 import QtWidgets as QtW
from PyQt5 import QtCore as QtC
import gk_gameKey
import gk_data
import gk_helpers


class BindUI(QtW.QWidget):
    # Signals
    bind_data_return = QtC.pyqtSignal(str, int, int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_windowBind()
        self.ui.setupUi(self)

        # variables
        self.buttonname = None
        self.currentlayer = None
        self.currentbind = 0
        self.currentmode = 0
        self.newlayer = None
        self.newbind = 0
        self.newmode = 0
        self.mod_shift = False
        self.mod_control = False
        self.mod_alt = False
        self.mod_meta = False
        self.mod_keypad = False

        # Button UI actions
        self.ui.bClear.clicked.connect(self.clearbind)
        self.ui.bAccept.clicked.connect(self.acceptbind)
        self.ui.bCancel.clicked.connect(self.cancelbind)

        # F-key UI Bind Overrides
        self.ui.bF13.clicked.connect(self.keyoverride)
        self.ui.bF14.clicked.connect(self.keyoverride)
        self.ui.bF15.clicked.connect(self.keyoverride)
        self.ui.bF16.clicked.connect(self.keyoverride)
        self.ui.bF17.clicked.connect(self.keyoverride)
        self.ui.bF18.clicked.connect(self.keyoverride)
        self.ui.bF19.clicked.connect(self.keyoverride)
        self.ui.bF20.clicked.connect(self.keyoverride)
        self.ui.bF21.clicked.connect(self.keyoverride)
        self.ui.bF22.clicked.connect(self.keyoverride)
        self.ui.bF23.clicked.connect(self.keyoverride)
        self.ui.bF24.clicked.connect(self.keyoverride)

        # Mod-key UI Bind Overrides
        self.ui.bLShift.clicked.connect(self.keyoverride)
        self.ui.bLCtrl.clicked.connect(self.keyoverride)
        self.ui.bLSuper.clicked.connect(self.keyoverride)
        self.ui.bLAlt.clicked.connect(self.keyoverride)
        self.ui.bRAlt.clicked.connect(self.keyoverride)
        self.ui.bRSuper.clicked.connect(self.keyoverride)
        self.ui.bRCtrl.clicked.connect(self.keyoverride)
        self.ui.bRShift.clicked.connect(self.keyoverride)

        # Mode sets
        self.ui.bShiftLayerA.clicked.connect(self.keyoverride)
        self.ui.bShiftLayerB.clicked.connect(self.keyoverride)
        self.ui.bShiftLayerC.clicked.connect(self.keyoverride)
        self.ui.bShiftLayerD.clicked.connect(self.keyoverride)

        # Set up some button details
        self.ui.bShiftLayerA.setStyleSheet(gk_data.gk_layercolor[0])
        self.ui.bShiftLayerB.setStyleSheet(gk_data.gk_layercolor[1])
        self.ui.bShiftLayerC.setStyleSheet(gk_data.gk_layercolor[2])
        self.ui.bShiftLayerD.setStyleSheet(gk_data.gk_layercolor[3])
        # self.bindui.ui.keyBindingIndicator.setStyleSheet(gk_data.gk_colormode[currentkeymode])

    def bind_data_in(self, buttontobind, currentkeybinds_in, currentkeymode_in, currentlayer_in):
        self.buttonname = buttontobind
        self.currentlayer = currentlayer_in
        self.currentbind = currentkeybinds_in
        self.currentmode = currentkeymode_in
        self.newlayer = currentlayer_in
        self.newbind = currentkeybinds_in
        self.newmode = currentkeymode_in
        self.ui.buttonIndicator.setText(str(self.buttonname))
        self.labelupdate()

    def labelupdate(self):
        self.ui.keyBindingIndicator.setText(gk_helpers.map_ard_to_txt(self.newbind))
        self.layerlabel()

    def layerlabel(self):
        self.ui.buttonLayerIndicator.setText(gk_data.gk_layername[self.newlayer])
        if self.currentlayer == self.newlayer:
            self.ui.buttonLayerIndicator.setStyleSheet(gk_data.gk_layercolor[self.newlayer])
        else:
            self.ui.buttonLayerIndicator.setStyleSheet(gk_data.gk_layercolor[self.newlayer] + gk_data.gk_layercolor[99])

    def clearbind(self):
        # clears current self.newbind and updates label
        self.newbind = 0
        self.labelupdate()
        print("clearbind")

    def acceptbind(self):
        # Accepts new bindings and returns old bindings to bind_data_return signal
        print("acceptbind button", self.buttonname, " key", self.newbind, " mode", self.newmode)
        self.bind_data_return.emit(self.buttonname, self.newbind, self.newmode, self.newlayer)
        self.close()

    def cancelbind(self):
        # Cancels new binding, returns old bindings to bind_data_return signal
        self.bind_data_return.emit(self.buttonname, self.currentbind, self.currentmode, self.currentlayer)
        print("cancel button", self.buttonname)
        self.close()

    def keyoverride(self):
        # Special keys are chosen by button.text(), careful with button naming
        # Converts button.text() to arduino mapping code
        senderbtn = self.sender()
        if senderbtn.text() == "LayerA" or \
                senderbtn.text() == "LayerB" or \
                senderbtn.text() == "LayerC" or \
                senderbtn.text() == "LayerD":
            self.newlayer = 0
            self.newmode = gk_data.gk_hw_keymode["LAYER"]
        else:
            self.newlayer = self.currentlayer
            self.newmode = gk_data.gk_hw_keymode["KEYB"]

        self.newbind = gk_helpers.map_txt_to_ard(senderbtn.text())
        self.labelupdate()
        print("special key override", self.newbind)

    def modeset(self):
        senderbtn = self.sender()
        self.ui.keyBindingIndicator.setStyleSheet(gk_data.gk_colormode[gk_data.gk_hw_keymode[senderbtn.text()]])
        self.newmode = gk_data.gk_hw_keymode[senderbtn.text()]

    def translate_numpad(self, incomingbind):
        outgoingbind = None
        return outgoingbind

    def keyPressEvent(self, event):
        keyholder = gk_helpers.map_qt_to_ard(event.key())
        if not ((event.key() == QtC.Qt.Key_Shift)
                or (event.key() == QtC.Qt.Key_Control)
                or (event.key() == QtC.Qt.Key_Alt)):
            self.getmodifiers(event)
            if keyholder is not None:
                if self.mod_keypad:
                    self.newbind = gk_helpers.map_numpad_to_ard(keyholder)
                elif 65 <= keyholder <= 90 and not self.mod_shift:
                    self.newbind = keyholder + 32
                else:
                    self.newbind = keyholder
                self.labelupdate()
                self.mod_shift = False
                self.mod_control = False
                self.mod_alt = False
                self.mod_meta = False
                self.mod_keypad = False

    # def keyReleaseEvent(self, event):

    def getmodifiers(self, data):
        # There has GOT to be a more efficient way to do this
        # Singleton modifiers
        if data.modifiers() == QtC.Qt.ShiftModifier:
            self.mod_shift = True
        elif data.modifiers() == QtC.Qt.ControlModifier:
            self.mod_control = True
        elif data.modifiers() == QtC.Qt.AltModifier:
            self.mod_alt = True
        elif data.modifiers() == QtC.Qt.KeypadModifier:
            self.mod_keypad = True
        elif data.modifiers() == QtC.Qt.MetaModifier:
            self.mod_meta = True
        # Double modifiers shift
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier):
            self.mod_shift = True
            self.mod_control = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.AltModifier):
            self.mod_shift = True
            self.mod_alt = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.KeypadModifier):
            self.mod_shift = True
            self.mod_keypad = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.MetaModifier):
            self.mod_shift = True
            self.mod_meta = True
        # Double modifiers control
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.AltModifier):
            self.mod_control = True
            self.mod_alt = True
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.KeypadModifier):
            self.mod_control = True
            self.mod_keypad = True
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.MetaModifier):
            self.mod_control = True
            self.mod_meta = True
        # Double modifiers alt
        elif data.modifiers() == (QtC.Qt.AltModifier | QtC.Qt.KeypadModifier):
            self.mod_alt = True
            self.mod_keypad = True
        elif data.modifiers() == (QtC.Qt.AltModifier | QtC.Qt.MetaModifier):
            self.mod_alt = True
            self.mod_meta = True
        # Double modifiers keypad
        elif data.modifiers() == (QtC.Qt.KeypadModifier | QtC.Qt.MetaModifier):
            self.mod_keypad = True
            self.mod_meta = True
        # triple modifiers shift
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier | QtC.Qt.AltModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_alt = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier | QtC.Qt.KeypadModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_keypad = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier | QtC.Qt.MetaModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_meta = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.AltModifier | QtC.Qt.KeypadModifier):
            self.mod_shift = True
            self.mod_alt = True
            self.mod_keypad = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.AltModifier | QtC.Qt.MetaModifier):
            self.mod_shift = True
            self.mod_alt = True
            self.mod_meta = True
        # triple modifiers control
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.AltModifier | QtC.Qt.KeypadModifier):
            self.mod_control = True
            self.mod_alt = True
            self.mod_keypad = True
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.AltModifier | QtC.Qt.MetaModifier):
            self.mod_control = True
            self.mod_alt = True
            self.mod_meta = True
        # quadruple modifiers
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier
                                  | QtC.Qt.AltModifier | QtC.Qt.KeypadModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_alt = True
            self.mod_keypad = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier
                                  | QtC.Qt.AltModifier | QtC.Qt.MetaModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_alt = True
            self.mod_meta = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.AltModifier
                                  | QtC.Qt.KeypadModifier | QtC.Qt.MetaModifier):
            self.mod_shift = True
            self.mod_alt = True
            self.mod_keypad = True
            self.mod_meta = True
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.AltModifier
                                  | QtC.Qt.KeypadModifier | QtC.Qt.MetaModifier):
            self.mod_control = True
            self.mod_alt = True
            self.mod_keypad = True
            self.mod_meta = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier
                                  | QtC.Qt.KeypadModifier | QtC.Qt.MetaModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_keypad = True
            self.mod_meta = True
        # all five modifiers
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier
                                  | QtC.Qt.AltModifier | QtC.Qt.KeypadModifier | QtC.Qt.MetaModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_alt = True
            self.mod_keypad = True
            self.mod_meta = True
        # Clear modifiers
        elif data.modifiers() == QtC.Qt.NoModifier:
            self.mod_shift = False
            self.mod_control = False
            self.mod_alt = False
            self.mod_meta = False
            self.mod_keypad = False
        else:
            self.mod_shift = False
            self.mod_control = False
            self.mod_alt = False
            self.mod_meta = False
            self.mod_keypad = False
