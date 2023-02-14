import gk_data
import gk_helpers


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

    def map_label(self, label_in_a, label_in_b, label_in_c, label_in_d):
        self.label_a = label_in_a
        self.label_b = label_in_b
        self.label_c = label_in_c
        self.label_d = label_in_d

    def get_json(self):
        export_button = {
            "bind_a": self.button_bind_a,
            "bind_b": self.button_bind_b,
            "bind_c": self.button_bind_c,
            "bind_d": self.button_bind_d,
            "mode": self.button_mode
        }
        return export_button

    def update_label(self, button_name_in, active_layer_in):
        fade_offset = 10

        if self.label_a is not None:
            self.label_a.setText(gk_helpers.map_ard_to_txt(self.button_bind_a))
            self.label_b.setText(gk_helpers.map_ard_to_txt(self.button_bind_b))
            self.label_c.setText(gk_helpers.map_ard_to_txt(self.button_bind_c))
            self.label_d.setText(gk_helpers.map_ard_to_txt(self.button_bind_d))
            if active_layer_in == 0:
                self.label_a.setStyleSheet(gk_data.gk_layercolor[0])
                self.label_b.setStyleSheet(gk_data.gk_layercolor[1 + fade_offset])
                self.label_c.setStyleSheet(gk_data.gk_layercolor[2 + fade_offset])
                self.label_d.setStyleSheet(gk_data.gk_layercolor[3 + fade_offset])
            if active_layer_in == 1:
                self.label_a.setStyleSheet(gk_data.gk_layercolor[0 + fade_offset])
                self.label_b.setStyleSheet(gk_data.gk_layercolor[1])
                self.label_c.setStyleSheet(gk_data.gk_layercolor[2 + fade_offset])
                self.label_d.setStyleSheet(gk_data.gk_layercolor[3 + fade_offset])
            if active_layer_in == 2:
                self.label_a.setStyleSheet(gk_data.gk_layercolor[0 + fade_offset])
                self.label_b.setStyleSheet(gk_data.gk_layercolor[1 + fade_offset])
                self.label_c.setStyleSheet(gk_data.gk_layercolor[2])
                self.label_d.setStyleSheet(gk_data.gk_layercolor[3 + fade_offset])
            if active_layer_in == 3:
                self.label_a.setStyleSheet(gk_data.gk_layercolor[0 + fade_offset])
                self.label_b.setStyleSheet(gk_data.gk_layercolor[1 + fade_offset])
                self.label_c.setStyleSheet(gk_data.gk_layercolor[2 + fade_offset])
                self.label_d.setStyleSheet(gk_data.gk_layercolor[3])

