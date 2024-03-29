from PyQt5 import QtWidgets
import gk_data_tables
import gk_helper_converts
from gk_data_uimap import gk_uimap_button as uimap


class GkButton:
    def __init__(self, binda, bindb, bindc, bindd, mode):
        self.button_bind_a = binda
        self.button_bind_b = bindb
        self.button_bind_c = bindc
        self.button_bind_d = bindd
        self.button_mode = mode
        self.label_a = None
        self.label_b = None
        self.label_c = None
        self.label_d = None

    def map_json(self, gk_buttondata):
        self.button_bind_a = gk_buttondata['bind_a']
        self.button_bind_b = gk_buttondata['bind_b']
        self.button_bind_c = gk_buttondata['bind_c']
        self.button_bind_d = gk_buttondata['bind_d']
        self.button_mode = gk_buttondata['mode']

    def map_label(self, ui_in, button_name):
        button_uimap_index = 0
        for index, sublist in enumerate(uimap):
            if button_name in sublist:
                button_uimap_index = index
                break
        uimap_data = uimap[button_uimap_index]
        self.label_a = ui_in.findChild(QtWidgets.QLabel, uimap_data[1])
        self.label_b = ui_in.findChild(QtWidgets.QLabel, uimap_data[2])
        self.label_c = ui_in.findChild(QtWidgets.QLabel, uimap_data[3])
        self.label_d = ui_in.findChild(QtWidgets.QLabel, uimap_data[4])

    def get_button_bind(self, activelayer_in):
        if activelayer_in == 0:
            return self.button_bind_a
        if activelayer_in == 1:
            return self.button_bind_b
        if activelayer_in == 2:
            return self.button_bind_c
        if activelayer_in == 3:
            return self.button_bind_d

    def set_button_bind(self, bind_in, activelayer_in):
        if activelayer_in == 0:
            self.button_bind_a = bind_in
        if activelayer_in == 1:
            self.button_bind_b = bind_in
        if activelayer_in == 2:
            self.button_bind_c = bind_in
        if activelayer_in == 3:
            self.button_bind_d = bind_in
        self.button_mode = self.check_mode()
        self.update_label_singleton()

    def set_special_button(self, bind_in):
        self.button_bind_a = bind_in
        self.button_mode = self.check_mode()

    def get_button_mode(self):
        return self.button_mode

    def check_mode(self):
        lowrange = gk_helper_converts.map_txt_to_ard("LayerD")
        highrange = gk_helper_converts.map_txt_to_ard("LayerA")
        if (lowrange <= self.button_bind_a <= highrange
                or lowrange <= self.button_bind_b <= highrange
                or lowrange <= self.button_bind_c <= highrange
                or lowrange <= self.button_bind_d <= highrange):
            return gk_data_tables.gk_hw_keymode["LAYER"]
        elif (self.button_bind_a != 0
              or self.button_bind_b != 0
              or self.button_bind_c != 0
              or self.button_bind_d != 0):
            return gk_data_tables.gk_hw_keymode["KEYB"]
        else:
            return gk_data_tables.gk_hw_keymode["NONE"]

    def get_json(self):
        export_button = {
            "bind_a": self.button_bind_a,
            "bind_b": self.button_bind_b,
            "bind_c": self.button_bind_c,
            "bind_d": self.button_bind_d,
            "mode": self.button_mode
        }
        return export_button

    def update_label(self, active_layer_in):
        fade_offset = 10
        if self.label_a is not None:
            self.update_label_singleton()
            if active_layer_in == 0:
                self.label_a.setStyleSheet(gk_data_tables.gk_layercolor[0])
                self.label_b.setStyleSheet(gk_data_tables.gk_layercolor[1 + fade_offset])
                self.label_c.setStyleSheet(gk_data_tables.gk_layercolor[2 + fade_offset])
                self.label_d.setStyleSheet(gk_data_tables.gk_layercolor[3 + fade_offset])
            if active_layer_in == 1:
                self.label_a.setStyleSheet(gk_data_tables.gk_layercolor[0 + fade_offset])
                self.label_b.setStyleSheet(gk_data_tables.gk_layercolor[1])
                self.label_c.setStyleSheet(gk_data_tables.gk_layercolor[2 + fade_offset])
                self.label_d.setStyleSheet(gk_data_tables.gk_layercolor[3 + fade_offset])
            if active_layer_in == 2:
                self.label_a.setStyleSheet(gk_data_tables.gk_layercolor[0 + fade_offset])
                self.label_b.setStyleSheet(gk_data_tables.gk_layercolor[1 + fade_offset])
                self.label_c.setStyleSheet(gk_data_tables.gk_layercolor[2])
                self.label_d.setStyleSheet(gk_data_tables.gk_layercolor[3 + fade_offset])
            if active_layer_in == 3:
                self.label_a.setStyleSheet(gk_data_tables.gk_layercolor[0 + fade_offset])
                self.label_b.setStyleSheet(gk_data_tables.gk_layercolor[1 + fade_offset])
                self.label_c.setStyleSheet(gk_data_tables.gk_layercolor[2 + fade_offset])
                self.label_d.setStyleSheet(gk_data_tables.gk_layercolor[3])

    def update_label_singleton(self):
        if self.label_a is not None:
            self.label_a.setText(gk_helper_converts.map_ard_to_txt(self.button_bind_a))
        if self.label_b is not None:
            self.label_b.setText(gk_helper_converts.map_ard_to_txt(self.button_bind_b))
        if self.label_c is not None:
            self.label_c.setText(gk_helper_converts.map_ard_to_txt(self.button_bind_c))
        if self.label_d is not None:
            self.label_d.setText(gk_helper_converts.map_ard_to_txt(self.button_bind_d))
