import gk_data


def map_txt_to_ard(name_in):
    # wrapper for _map_to_data for gk_arduinoascii[][2] (txt) to gk_arduinoascii[][0] (arduino dec)
    return _map_to_data(2, 0, name_in)


def map_ard_to_txt(dec_in):
    # wrapper for _map_to_data for gk_arduinoascii[][0] (arduino dec) to gk_arduinoascii[][2] (txt)
    return _map_to_data(0, 2, int(dec_in))


def map_qt_to_ard(hex_in):
    # wrapper for _map_to_data for gk_arduinoascii[][1] (Qt::Key) to gk_arduinoascii[][0] (arduino dec)
    return _map_to_data(1, 0, int(hex_in))


def map_numpad_to_ard(map_in):
    for numkey in gk_data.gk_numpadascii:
        if numkey[1] == map_in:
            return numkey[0]


def _map_to_data(index_in, index_out, map_in):
    # Map arbitrary columns in gk_arduinoascii
    for binding in gk_data.gk_arduinoascii:
        if binding[index_in] == map_in:
            return binding[index_out]
