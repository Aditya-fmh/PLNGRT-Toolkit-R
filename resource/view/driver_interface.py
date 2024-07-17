# coding:utf-8
from config import cfg, KEYTEST_URL, LCDTEST_URL, MICTEST_URL, SPEAKERTEST_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, HyperlinkCard, PrimaryPushSettingCard, ScrollArea, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme)
from qfluentwidgets import (FluentIcon as FIF, MessageBox, AvatarWidget, CaptionLabel, HyperlinkButton, QColor, BodyLabel, setFont, RoundMenu, Action,)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel
import os
import sys
import subprocess
import zipfile
import tempfile

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DriverInterface(ScrollArea):
    """ Driver interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Driver & Update"), self)
        
        # Checking Software
        self.winupdateGroup = SettingCardGroup(self.tr('Windows Update'), self.scrollWidget)
        self.wumgrCard = PrimaryPushSettingCard(
            self.tr('Run'),
            FIF.UPDATE,
            self.tr('Windows Update Manager (WUMGR)'),
            self.tr('This will install missing/outdated driver and install Windows Update'),
            self.winupdateGroup
        )
        self.wumtCard = PrimaryPushSettingCard(
            self.tr('Run'),
            FIF.UPDATE,
            self.tr('Windows Update MiniTool (WUMT)'),
            self.tr('This will install missing/outdated driver and install Windows Update'),
            self.winupdateGroup
        )
        
        # IDM Activator
        self.driverGroup = SettingCardGroup(self.tr('Driver Update'), self.scrollWidget)
        self.drvboosterCard = PrimaryPushSettingCard(
            self.tr('Run'),
            FIF.UPDATE,
            self.tr('Driver Booster (Recommended)'),
            self.tr('This only install missing/outdated driver'),
            self.driverGroup
        )
        
        self.extraGroup = SettingCardGroup(self.tr('Extra Driver'), self.scrollWidget)
        self.hpfnCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.UPDATE,
            self.tr('HP Fn Key'),
            self.tr('Enable Function key for some HP laptops'),
            self.driverGroup
        )
        self.t440Card = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.UPDATE,
            self.tr('T440p Camera'),
            self.tr('This will fix T440p bluescreen when opening camera'),
            self.driverGroup
        )
        
        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

         # initialize style sheet
        self.__setQss()
        
        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'dark' if isDarkTheme() else 'light'
        qss_path = get_resource_path(f'resource/qss/{theme}/setting_interface.qss')
        with open(qss_path, encoding='utf-8') as f:
            self.setStyleSheet(f.read())
            
    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)

        # chang the theme of setting interface
        self.__setQss()
    
    def __initLayout(self):
        self.settingLabel.move(60, 63)

        # add cards to group
        self.winupdateGroup.addSettingCard(self.wumgrCard)
        self.winupdateGroup.addSettingCard(self.wumtCard)
        
        self.driverGroup.addSettingCard(self.drvboosterCard)
        
        self.extraGroup.addSettingCard(self.hpfnCard)
        self.extraGroup.addSettingCard(self.t440Card)

        # add activator card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.winupdateGroup)
        self.expandLayout.addWidget(self.driverGroup)
        self.expandLayout.addWidget(self.extraGroup)
       
    # checking button action
    def run_cpuz(self):
        """ Run the CPU-Z executable """
        exe_path = get_resource_path('resource/checking/cpuz/cpuz_x64.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        # Run the executable with elevated privileges using nircmd
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.themeChanged.connect(self.__onThemeChanged)