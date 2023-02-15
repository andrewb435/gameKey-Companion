import os
import pathlib
import platform
import json
from PyQt5.QtWidgets import QFileDialog


class GkProfileList:
    def __init__(self):
        self.user_home = str(pathlib.Path.home())
        self.config_path = self.get_base_config_path()
        self.stick_path = self.get_stick_config_path()
        self.check_config_paths()
        self.gamepad_profiles = []
        self.stick_profiles = []
        self.get_gamepad_profile_list()
        self.get_stick_profile_list()

    # General config file handling
    def get_base_config_path(self):
        if platform.system() == 'Linux':
            return "/.local/share/gameKeyCompanion"
        if platform.system() == 'Windows':
            return "\\AppData\\Roaming\\gameKeyCompanion"

    def get_stick_config_path(self):
        if platform.system() == 'Linux':
            return "/stick"
        if platform.system() == 'Windows':
            return "\\stick"

    def check_config_paths(self):
        path = self.user_home + self.config_path
        path_stick = self.user_home + self.config_path + self.stick_path
        if os.path.exists(path) and os.path.exists(path_stick):
            return
        else:
            if not os.path.exists(path):
                os.makedirs(path)
            if not os.path.exists(path_stick):
                os.makedirs(path_stick)
            return

    def get_gamepad_profile_list(self):
        self.gamepad_profiles = []
        path = self.user_home + self.config_path
        print("scanning", path, "for config files")
        for item in os.scandir(path):
            if item.is_file():
                self.gamepad_profiles.append(GkProfileListItem(item))

    def get_stick_profile_list(self):
        self.stick_profiles = []
        path = self.user_home + self.config_path + self.stick_path
        print("scanning", path, "for stick config files")
        for item in os.scandir(path):
            if item.is_file():
                self.stick_profiles.append(GkProfileListItem(item))

    def output_gamepad_config_file(self, gk_json, config_name):
        for item in self.gamepad_profiles:
            if config_name == item.config.name:
                file = open(item.config.path, "w")
                file.write(json.dumps(gk_json, indent=4))
                file.close()

    def output_stick_config_file(self, gk_json, config_name):
        for item in self.stick_profiles:
            if config_name == item.config.name:
                file = open(item.config.path, "w")
                file.write(json.dumps(gk_json, indent=4))
                file.close()

    def load_gamepad_profile(self, config_name):
        for item in self.gamepad_profiles:
            if config_name == item.config.name:
                file = open(item.config.path, "r")
                gkjson = json.load(file)
                file.close()
                return gkjson

    def load_stick_profile(self, config_name):
        for item in self.stick_profiles:
            if config_name == item.config.name:
                file = open(item.config.path, "r")
                gkjson = json.load(file)
                file.close()
                return gkjson

    def save_as_profile(self, file, gk_json):
        stream = open(file, "w")
        stream.write(json.dumps(gk_json, indent=4))
        stream.close()
        self.get_gamepad_profile_list()

    def save_as_stick(self, file, stick_json):
        stream = open(file, "w")
        stream.write(json.dumps(stick_json, indent=4))
        stream.close()
        self.get_stick_profile_list()


class GkProfileListItem:
    def __init__(self, config_in):
        self.config = config_in


class GkStickProfileListItem:
    def __init__(self, config_in):
        self.config = config_in
