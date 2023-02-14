# gk_arduinoascii[x][0] = arduino keymap table code
# gk_arduinoascii[x][1] = Qt:Key keymap code
# gk_arduinoascii[x][2] = String descriptor
gk_arduinoascii = [
    [0, 0, ""],
    [1, 1, "SOH"],
    [2, 2, "STX"],
    [3, 3, "ETX"],
    [4, 4, "EOT"],
    [5, 5, "ENQ"],
    [6, 6, "ACK"],
    [7, 7, "BEL"],
    [8, 8, "BS"],
    [9, 9, "HT"],
    [10, 10, "LF"],
    [11, 11, "VT"],
    [12, 12, "FF"],
    [13, 13, "CR"],
    [14, 14, "SO"],
    [15, 15, "SI"],
    [16, 16, "DLE"],
    [17, 17, "DC1"],
    [18, 18, "DC2"],
    [19, 19, "DC3"],
    [20, 20, "DC4"],
    [21, 21, "NAK"],
    [22, 22, "SYN"],
    [23, 23, "ETB"],
    [24, 24, "CAN"],
    [25, 25, "EM"],
    [26, 26, "SUB"],
    [27, 27, "ESC"],
    [28, 28, "FS"],
    [29, 29, "GS"],
    [30, 30, "RS"],
    [31, 31, "US"],
    [32, 32, "space"],
    [33, 33, "!"],
    [34, 34, "\""],
    [35, 35, "#"],
    [36, 36, "$"],
    [37, 37, "%"],
    [38, 38, "&"],
    [39, 39, "'"],
    [40, 40, "("],
    [41, 41, ")"],
    [42, 42, "*"],
    [43, 43, "+"],
    [44, 44, ","],
    [45, 45, "-"],
    [46, 46, "."],
    [47, 47, "/"],
    [48, 48, "0"],
    [49, 49, "1"],
    [50, 50, "2"],
    [51, 51, "3"],
    [52, 52, "4"],
    [53, 53, "5"],
    [54, 54, "6"],
    [55, 55, "7"],
    [56, 56, "8"],
    [57, 57, "9"],
    [58, 58, ":"],
    [59, 59, ";"],
    [60, 60, "<"],
    [61, 61, "="],
    [62, 62, ">"],
    [63, 63, "?"],
    [64, 64, "@"],
    [65, 65, "A"],
    [66, 66, "B"],
    [67, 67, "C"],
    [68, 68, "D"],
    [69, 69, "E"],
    [70, 70, "F"],
    [71, 71, "G"],
    [72, 72, "H"],
    [73, 73, "I"],
    [74, 74, "J"],
    [75, 75, "K"],
    [76, 76, "L"],
    [77, 77, "M"],
    [78, 78, "N"],
    [79, 79, "O"],
    [80, 80, "P"],
    [81, 81, "Q"],
    [82, 82, "R"],
    [83, 83, "S"],
    [84, 84, "T"],
    [85, 85, "U"],
    [86, 86, "V"],
    [87, 87, "W"],
    [88, 88, "X"],
    [89, 89, "Y"],
    [90, 90, "Z"],
    [91, 91, "["],
    [92, 92, "\\"],
    [93, 93, "]"],
    [94, 94, "^"],
    [95, 95, "_"],
    [96, 96, "`"],
    [97, 97, "a"],
    [98, 98, "b"],
    [99, 99, "c"],
    [100, 100, "d"],
    [101, 101, "e"],
    [102, 102, "f"],
    [103, 103, "g"],
    [104, 104, "h"],
    [105, 105, "i"],
    [106, 106, "j"],
    [107, 107, "k"],
    [108, 108, "l"],
    [109, 109, "m"],
    [110, 110, "n"],
    [111, 111, "o"],
    [112, 112, "p"],
    [113, 113, "q"],
    [114, 114, "r"],
    [115, 115, "s"],
    [116, 116, "t"],
    [117, 117, "u"],
    [118, 118, "v"],
    [119, 119, "w"],
    [120, 120, "x"],
    [121, 121, "y"],
    [122, 122, "z"],
    [123, 123, "{"],
    [124, 124, "|"],
    [125, 125, "}"],
    [126, 126, "~"],
    [127, 0x01000007, "DEL"],
    [128, 0x01000021, "LCtrl"],
    [129, 0x01000020, "LShift"],
    [130, 0x01000023, "LAlt"],
    [131, 0x01000053, "LSuper"],
    [132, 0, "RCtrl"],
    [133, 0, "RShift"],
    [134, 0, "RAlt"],
    [135, 0, "RSuper"],
    [176, 16777220, "Return"],
    [177, 16777216, "Esc"],
    [178, 16777219, "Backsp"],
    [179, 16777217, "Tab"],
    [193, 16777252, "CapsL"],
    [194, 16777264, "F1"],
    [195, 16777265, "F2"],
    [196, 16777266, "F3"],
    [197, 16777267, "F4"],
    [198, 16777268, "F5"],
    [199, 16777269, "F6"],
    [200, 16777270, "F7"],
    [201, 16777271, "F8"],
    [202, 16777272, "F9"],
    [203, 16777273, "F10"],
    [204, 16777274, "F11"],
    [205, 16777275, "F12"],
    [209, 16777222, "Insert"],
    [210, 16777232, "Home"],
    [211, 16777238, "PgUp"],
    [212, 16777223, "Delete"],
    [213, 16777233, "End"],
    [214, 16777239, "PgDn"],
    [215, 16777236, "Right"],
    [216, 16777234, "Left"],
    [217, 16777237, "Down"],
    [218, 16777235, "Up"],
    [220, 0x2F + 0x20000000, "KP_SLASH"],
    [221, 0x2A + 0x20000000, "KP_ASTERISK"],
    [222, 0x2D + 0x20000000, "KP_MINUS"],
    [223, 0x2B + 0x20000000, "KP_PLUS"],
    [225, 0x31 + 0x20000000, "KP_1"],
    [226, 0x32 + 0x20000000, "KP_2"],
    [227, 0x33 + 0x20000000, "KP_3"],
    [228, 0x34 + 0x20000000, "KP_4"],
    [229, 0x35 + 0x20000000, "KP_5"],
    [230, 0x36 + 0x20000000, "KP_6"],
    [231, 0x37 + 0x20000000, "KP_7"],
    [232, 0x38 + 0x20000000, "KP_8"],
    [233, 0x39 + 0x20000000, "KP_9"],
    [234, 0x30 + 0x20000000, "KP_0"],
    [235, 0x2E + 0x20000000, "KP_DOT"],
    [240, 16777276, "F13"],
    [241, 16777277, "F14"],
    [242, 16777278, "F15"],
    [243, 16777279, "F16"],
    [244, 16777280, "F17"],
    [245, 16777281, "F18"],
    [246, 16777282, "F19"],
    [247, 16777283, "F20"],
    [248, 16777284, "F21"],
    [249, 16777285, "F22"],
    [250, 16777286, "F23"],
    [251, 16777287, "F24"],
    [252, 0x0, "LayerD"],
    [253, 0x0, "LayerC"],
    [254, 0x0, "LayerB"],
    [255, 0x0, "LayerA"]
]

gk_numpadascii = [
    [220, 47, "KP_Slash"],
    [221, 42, "KP_ASTERISK"],
    [222, 45, "KP_MINUS"],
    [223, 43, "KP_PLUS"],
    [225, 49, "KP_1"],
    [226, 50, "KP_2"],
    [227, 51, "KP_3"],
    [228, 52, "KP_4"],
    [229, 53, "KP_5"],
    [230, 54, "KP_6"],
    [231, 55, "KP_7"],
    [232, 56, "KP_8"],
    [233, 57, "KP_9"],
    [234, 48, "KP_0"],
    [235, 46, "KP_DOT"]
]

gk_hw_lefthand = {
    "kPinky1": 0,
    "kPinky2": 1,
    "kPinky3": 2,
    "kPinky4": 3,
    "kPinky5": 4,
    "kRing1": 5,
    "kRing2": 6,
    "kRing3": 7,
    "kRing4": 8,
    "kRing5": 9,
    "kMiddle1": 10,
    "kMiddle2": 11,
    "kMiddle3": 12,
    "kMiddle4": 13,
    "kMiddle5": 14,
    "kIndex1": 15,
    "kIndex2": 16,
    "kIndex3": 17,
    "kIndex4": 18,
    "kIndex5": 19,
    "kThumbNavUp": 20,
    "kThumbNavFwd": 21,
    "kThumbNavDown": 22,
    "kThumbNavBack": 23,
    "kThumbNavPush": 24,
    "kIndexAddon": 25,
    "kPinkyAddon": 26,
    "kThumbStickPush": 27,
    "kThumbBAddon": 28,
    "None": 29,
    "kThumbStickN": 100,
    "kThumbStickE": 101,
    "kThumbStickS": 102,
    "kThumbStickW": 103
}

gk_hw_righthand = {
    "kThumbNavUp": 0,
    "kThumbNavFwd": 1,
    "kThumbNavDown": 2,
    "kThumbNavBack": 3,
    "kThumbNavPush": 4,
    "kIndex1": 5,
    "kIndex2": 6,
    "kIndex3": 7,
    "kIndex4": 8,
    "kIndex5": 9,
    "kMiddle1": 10,
    "kMiddle2": 11,
    "kMiddle3": 12,
    "kMiddle4": 13,
    "kMiddle5": 14,
    "kRing1": 15,
    "kRing2": 16,
    "kRing3": 17,
    "kRing4": 18,
    "kRing5": 19,
    "kPinky1": 20,
    "kPinky2": 21,
    "kPinky3": 22,
    "kPinky4": 23,
    "kPinky5": 24,
    "kIndexAddon": 25,
    "kPinkyAddon": 26,
    "kThumbStickPush": 27,
    "kThumbBAddon": 28,
    "None": 29,
    "kThumbStickN": 100,
    "kThumbStickE": 101,
    "kThumbStickS": 102,
    "kThumbStickW": 103
}

gk_hw_keymode = {
    "KEYB": 1,
    "GPAD": 2,
    "BOTH": 3,
    "LAYER": 4
}

gk_hw_commands = {
    "ReportAxesValues": "repa",
    "DeviceInfo": "devi",
    "Bind": "bind",
    "SetConfigMode": "conf",
    "SetDebugMode": "de",
    "SuperDebugMode": "sde",
    "Version": "vers",
    "SaveEEPROM": "savnv",
    "FeatureFlag": "feat",
    "GetDeviceName": "gtna",
    "ReportButtonConfig": "gtbu",
    "ReportAxesConfig": "gtax",
    "SetDeviceName": "stna",
    "SetAxisConfig": "stax"
}

gk_colormode = {
    # Colors from https://lospec.com/palette-list/ibm-color-blind-safe
    1: "",
    2: "background-color: #648FFF",
    3: "background-color: #FE6100",
    4: ""
}

gk_layercolor = {
    # Colors from https://github.com/filipworksdev/colorblind-palette-16
    0: "background-color: rgba(37,37,37,255); color: rgba(255,255,255,255); border-radius: 6px",
    1: "background-color: rgba(0,73,73,255); color: rgba(255,255,255,255); border-radius: 6px",
    2: "background-color: rgba(73, 0, 146, 255); color: rgba(255,255,255,255); border-radius: 6px",
    3: "background-color: rgba(143, 78, 0, 255); color: rgba(255,255,255,255); border-radius: 6px",
    10: "background-color: rgba(37,37,37,100); color: rgba(255,255,255,100); border-radius: 6px",
    11: "background-color: rgba(0,73,73,100); color: rgba(255,255,255,100); border-radius: 6px",
    12: "background-color: rgba(73, 0, 146, 100); color: rgba(255,255,255,100); border-radius: 6px",
    13: "background-color: rgba(143, 78, 0, 100); color: rgba(255,255,255,100); border-radius: 6px",
}
