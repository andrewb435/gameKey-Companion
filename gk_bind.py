import gk_data
from ui_bind import Ui_windowBind
from PyQt5 import QtWidgets as QtW
from PyQt5 import QtCore as QtC
import gk_gameKey


class BindUI(QtW.QWidget):
    # Signals
    bind_data_return = QtC.pyqtSignal(str, int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_windowBind()
        self.ui.setupUi(self)

        # variables
        self.buttonname = None
        self.currentbind = 0
        self.currentmode = 0
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
        self.ui.bModeKEYB.clicked.connect(self.modeset)
        self.ui.bModeGPAD.clicked.connect(self.modeset)
        self.ui.bModeBOTH.clicked.connect(self.modeset)

    def bind_data_in(self, buttontobind, currentkeybind, currentkeymode):
        self.buttonname = buttontobind
        self.currentbind = currentkeybind
        self.currentmode = currentkeymode
        self.newbind = currentkeybind
        self.newmode = currentkeymode
        self.ui.buttonIndicator.setText(str(self.buttonname))
        self.labelupdate()

    def labelupdate(self):
        self.ui.keyBindingIndicator.setText(gk_gameKey.map_ard_to_txt(self.newbind))

    def clearbind(self):
        # clears current self.newbind and updates label
        self.newbind = 0
        self.labelupdate()
        print("clearbind")

    def acceptbind(self):
        # Accepts new bindings and returns old bindings to bind_data_return signal
        print("acceptbind button", self.buttonname, " key", self.newbind, " mode", self.newmode)
        self.bind_data_return.emit(self.buttonname, self.newbind, self.newmode)
        self.close()

    def cancelbind(self):
        # Cancels new binding, returns old bindings to bind_data_return signal
        self.bind_data_return.emit(self.buttonname, self.currentbind, self.currentmode)
        print("cancel button", self.buttonname)
        self.close()

    def keyoverride(self):
        # Special keys are chosen by button.text(), careful with button naming
        # Converts button.text() to arduino mapping code
        senderbtn = self.sender()
        self.newbind = gk_gameKey.map_txt_to_ard(senderbtn.text())
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
        keyholder = gk_gameKey.map_qt_to_ard(event.key())
        if not ((event.key() == QtC.Qt.Key_Shift)
                or (event.key() == QtC.Qt.Key_Control)
                or (event.key() == QtC.Qt.Key_Alt)):
            self.getmodifiers(event)
            if keyholder is not None:
                if self.mod_keypad:
                    self.newbind = gk_gameKey.map_numpad_to_ard(keyholder)
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
        # Double modifiers control
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.AltModifier):
            self.mod_control = True
            self.mod_alt = True
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.KeypadModifier):
            self.mod_control = True
            self.mod_keypad = True
        # Double modifiers alt
        elif data.modifiers() == (QtC.Qt.AltModifier | QtC.Qt.KeypadModifier):
            self.mod_alt = True
            self.mod_keypad = True
        # triple modifiers shift
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier | QtC.Qt.AltModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_alt = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier | QtC.Qt.KeypadModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_keypad = True
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.AltModifier | QtC.Qt.KeypadModifier):
            self.mod_shift = True
            self.mod_alt = True
            self.mod_keypad = True
        # triple modifiers control
        elif data.modifiers() == (QtC.Qt.ControlModifier | QtC.Qt.AltModifier | QtC.Qt.KeypadModifier):
            self.mod_control = True
            self.mod_alt = True
            self.mod_keypad = True
        # quadruple modifiers
        elif data.modifiers() == (QtC.Qt.ShiftModifier | QtC.Qt.ControlModifier
                                  | QtC.Qt.AltModifier | QtC.Qt.KeypadModifier):
            self.mod_shift = True
            self.mod_control = True
            self.mod_alt = True
            self.mod_keypad = True

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
