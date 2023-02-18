# gameKey Companion #
![gameKey Companion UI](/docs/gameKeyCompanion.png)

This is the desktop application to configure gameKey devices.

With the 2.0 release (compatible with the 2.0 firmware on the device), it supports 4 shift layers per non-thumbstick key, but layer shift keys can only be layer shift keys - not other key bindings on other layers.

2.0 also brings separated analog axis settings, allowing a profile for the min/max/center/dz calibrations to be separated from the main keybindings.

It reads the status of the current gameKey selected in the serial port drop down, fetches the onboard memory profile, and can save/load profiles stored on your computer.

This will eventually be cross-platform, and may even work on Windows as-is, but at the moment has only been tested on Linux.

It will read the device feature flags from the gameKey Firmware to determine if it is a left or right hand device and apply the proper hardware map to bind the keys correctly, though the interface will not truly reflect the relative positioning of each finger at this time.
