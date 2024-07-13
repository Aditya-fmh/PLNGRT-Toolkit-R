# coding:utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QGuiApplication, QFont
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            ColorConfigItem, OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator, ConfigSerializer, __version__)

class Config(QConfig):
    """ Config of application """

    # main window
    enableAcrylicBackground = ConfigItem(
        "MainWindow", "EnableAcrylicBackground", False, BoolValidator())
    minimizeToTray = ConfigItem(
        "MainWindow", "MinimizeToTray", True, BoolValidator())
    playBarColor = ColorConfigItem("MainWindow", "PlayBarColor", "#225C7F")
    recentPlaysNumber = RangeConfigItem(
        "MainWindow", "RecentPlayNumbers", 300, RangeValidator(10, 300))
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)

    # software update
    checkUpdateAtStartUp = ConfigItem(
        "Update", "CheckUpdateAtStartUp", True, BoolValidator())

YEAR = 2024
AUTHOR = "Aditya F"
VERSION = __version__
CODE_URL = "https://github.com/Aditya-fmh/PLNGRT-Toolkit-R"
FEEDBACK_URL = "https://github.com/Aditya-fmh/PLNGRT-Toolkit-R/issues"
RELEASE_URL = "https://github.com/Aditya-fmh"
KEYTEST_URL = "https://en.key-test.ru/"
LCDTEST_URL = "https://lcdtech.info/en/tests/dead.pixel.htm"
MICTEST_URL = "https://webcammictest.com/check-mic.html"
SPEAKERTEST_URL = "https://youtu.be/6TWJaFD6R2s?si=qy0Ab2HChFMiRdar&t=5"


cfg = Config()
qconfig.load('config/config.json', cfg)