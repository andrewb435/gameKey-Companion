# gameKey Companion #
![gameKey Companion UI](/docs/gameKeyCompanion.png)

This is the desktop application to configure gameKey devices.

As of right now it's still in rough shape, and needs refactoring on the serial interfaces.

It reads the status of the current gameKey selected in the serial port drop down, fetches the onboard memory profile, and can save/load profiles stored on your computer.

This will eventually be cross-platform, and may even work on Windows as-is, but at the moment has only been tested on Linux.

It will read the device feature flags from the gameKey Firmware to determine if it is a left or right hand device and apply the proper hardware map to bind the keys correctly, though the interface will not truly reflect the relative positioning of each finger at this time.
