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
    [127, 16777223, "DEL"],
    [128, 16777249, "LCtrl"],
    [129, 16777248, "LShift"],
    [130, 16777251, "LAlt"],
    [131, 16777250, "LSuper"],
    [132, 0, "RCtrl"],
    [133, 0, "RShift"],
    [134, 0, "RAlt"],
    [135, 0, "RSuper"],
    [176, 16777220, "Return"],
    [177, 16777216, "Esc"],
    [178, 16777219, "Backspace"],
    [179, 16777217, "Tab"],
    [193, 16777252, "CapsLock"],
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
    [251, 16777287, "F24"]
]

gk_hw_lefthand = {
    "kPinkyB1": 0,
    "kPinkyB2": 1,
    "kPinkyB3": 2,
    "kPinkyB4": 3,
    "kPinkyB5": 4,
    "kRingB1": 5,
    "kRingB2": 6,
    "kRingB3": 7,
    "kRingB4": 8,
    "kRingB5": 9,
    "kMiddleB1": 10,
    "kMiddleB2": 11,
    "kMiddleB3": 12,
    "kMiddleB4": 13,
    "kMiddleB5": 14,
    "kIndexB1": 15,
    "kIndexB2": 16,
    "kIndexB3": 17,
    "kIndexB4": 18,
    "kIndexB5": 19,
    "kThumbNavN": 20,
    "kThumbNavE": 21,
    "kThumbNavS": 22,
    "kThumbNavW": 23,
    "kThumbNavPush": 24,
    "kIndexBAddon": 25,
    "kPinkyBAddon": 26,
    "kThumbStickPush": 27,
    "kThumbBAddon": 28,
    "None": 29,
    "kThumbStickN": 100,
    "kThumbStickE": 101,
    "kThumbStickS": 102,
    "kThumbStickW": 103
}

gk_hw_righthand = {
    "kIndexBAddon": 0,
    "kPinkyBAddon": 1,
    "kThumbStickPush": 2,
    "kThumbBAddon": 3,
    "None": 4,
    "kThumbNavN": 5,
    "kThumbNavE": 6,
    "kThumbNavS": 7,
    "kThumbNavW": 8,
    "kThumbNavPush": 9,
    "kIndexB1": 10,
    "kIndexB2": 11,
    "kIndexB3": 12,
    "kIndexB4": 13,
    "kIndexB5": 14,
    "kMiddleB1": 15,
    "kMiddleB2": 16,
    "kMiddleB3": 17,
    "kMiddleB4": 18,
    "kMiddleB5": 19,
    "kRingB1": 20,
    "kRingB2": 21,
    "kRingB3": 22,
    "kRingB4": 23,
    "kRingB5": 24,
    "kPinkyB1": 25,
    "kPinkyB2": 26,
    "kPinkyB3": 27,
    "kPinkyB4": 28,
    "kPinkyB5": 29,
    "kThumbStickN": 100,
    "kThumbStickE": 101,
    "kThumbStickS": 102,
    "kThumbStickW": 103
}

gk_hw_keymode = {
    "KEYB": 0,
    "GPAD": 1,
    "BOTH": 2
}

gk_colormode = {
    # Colors from https://lospec.com/palette-list/ibm-color-blind-safe
    0: "",
    1: "background-color: #648FFF",
    2: "background-color: #FE6100",
}