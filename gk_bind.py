from ui_bind import Ui_windowBind
from PyQt5 import QtWidgets as QtW
from PyQt5 import QtCore as QtC
import gk_gameKey


class BindUI(QtW.QWidget):
    # Signals
    bind_data_return = QtC.pyqtSignal(str, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_windowBind()
        self.ui.setupUi(self)

        # variables
        self.buttonname = None
        self.currentbind = 0
        self.newbind = 0
        self.shifted = False

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

    def bind_data_in(self, buttontobind, currentkeybind):
        self.buttonname = buttontobind
        self.currentbind = currentkeybind
        self.newbind = currentkeybind
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
        print("acceptbind button", self.buttonname, " key", self.newbind)
        self.bind_data_return.emit(self.buttonname, self.newbind)
        self.close()

    def cancelbind(self):
        # Cancels new binding, returns old bindings to bind_data_return signal
        self.bind_data_return.emit(self.buttonname, self.currentbind)
        print("cancel button", self.buttonname)
        self.close()

    def keyoverride(self):
        # Special keys are chosen by button.text(), careful with button naming
        # Converts button.text() to arduino mapping code
        senderbtn = self.sender()
        self.newbind = gk_gameKey.map_txt_to_ard(senderbtn.text())
        self.labelupdate()
        print("special key override", self.newbind)

    def keyPressEvent(self, event):
        # Set shifted status to true when shift is pressed
        if event.key() == 16777248:
            self.shifted = True
        else:
            keyholder = gk_gameKey.map_qt_to_ard(event.key())
            if 65 <= keyholder <= 90:
                if self.shifted:
                    self.newbind = keyholder
                else:
                    self.newbind = keyholder + 32
            else:
                self.newbind = keyholder
        if not event.key() == 16777248:
            self.labelupdate()

    def keyReleaseEvent(self, event):
        # Set shifted status to false when shift is released
        if event.key() == 16777248:
            self.shifted = False
