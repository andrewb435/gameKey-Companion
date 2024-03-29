"""
    gameKey-Companion is a configuration utility for gameKey devices
    Copyright (C) 2022 Andrew Baum

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# UI
from gk_ui_main import MainUI
from PyQt5 import QtWidgets as QtW
import platform
version = "2.0.3"

if platform.system() == 'Linux':
    print("Linux detected!")
elif platform.system() == 'Windows':
    print("Windows detected!")

if __name__ == '__main__':
    app = QtW.QApplication([])
    mainui = MainUI()
    mainui.show()
    mainui.get_serial()
    app.exec_()
