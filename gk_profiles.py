import os
import pathlib
import platform
import json
from PyQt5.QtWidgets import QFileDialog


class GkProfileList:
    def __init__(self):
        self.user_home = str(pathlib.Path.home())
        self.config_path = self.get_config_path()
        self.profile_items = []
        self.get_profile_list()

    def get_config_path(self):
        if platform.system() == 'Linux':
            return "/.local/share/gameKeyCompanion"
        if platform.system() == 'Windows':
            return "gameKeyCompanion"

    def get_profile_list(self):
        self.profile_items = []
        path = self.user_home + self.config_path
        print("scanning", path, "for config files")
        for item in os.scandir(path):
            if item.is_file():
                self.profile_items.append(GkProfileListItem(item))

    def output_json(self, gk_json, config_name):
        for item in self.profile_items:
            if config_name == item.config.name:
                file = open(item.config.path, "w")
                file.write(json.dumps(gk_json, indent=4))
                file.close()

    def load_profile(self, config_name):
        for item in self.profile_items:
            if config_name == item.config.name:
                file = open(item.config.path, "r")
                gkjson = json.load(file)
                file.close()
                return gkjson

    def save_as(self, file, gk_json):
        stream = open(file, "w")
        stream.write(json.dumps(gk_json, indent=4))
        stream.close()
        self.get_profile_list()


class GkProfileListItem:
    def __init__(self, config_in):
        self.config = config_in
