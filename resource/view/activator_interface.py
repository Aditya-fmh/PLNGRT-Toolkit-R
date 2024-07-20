# coding:utf-8
from config import cfg, CODE_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, HyperlinkCard, PrimaryPushSettingCard, ScrollArea, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFontDialog, QFileDialog
import os
import sys
import subprocess

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ActivatorInterface(ScrollArea):
    """ Activator interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Activator"), self)
        
        # All-in-One Activator
        self.aioGroup = SettingCardGroup(self.tr('All-in-One Activator'), self.scrollWidget)
        self.aioCard = PrimaryPushSettingCard(
            self.tr('Activate'),
            FIF.COMMAND_PROMPT,
            self.tr('All-in-One Microsft Office & Windows Activator (Recommended)'),
            self.tr('This script support all office and windows version'),
            self.aioGroup
        )
        
        # IDM Activator
        self.idmGroup = SettingCardGroup(self.tr('IDM Activator'), self.scrollWidget)
        self.idmCard = PrimaryPushSettingCard(
            self.tr('Activate'),
            FIF.COMMAND_PROMPT,
            self.tr('IDM Activator'),
            self.tr('Choose freeze trial duration, activation not working anymore'),
            self.idmGroup
        )

        # office activator
        self.officeGroup = SettingCardGroup(self.tr('Office Activator'), self.scrollWidget)
        self.officeaioCard = PrimaryPushSettingCard(
            self.tr('Activate'),
            FIF.COMMAND_PROMPT,
            self.tr('Microsoft Office AIO'),
            self.tr('This script support all office version'),
            self.officeGroup
        )
        
        # windows activator
        self.windowsGroup = SettingCardGroup(self.tr('Windows Activator'), self.scrollWidget)
        self.w10Card = PrimaryPushSettingCard(
            self.tr('Activate'),
            FIF.COMMAND_PROMPT,
            self.tr('Windows 10'),
            self.tr('Support any Windows 10 Edition'),
            self.windowsGroup
        )
        self.w11Card = PrimaryPushSettingCard(
            self.tr('Activate'),
            FIF.COMMAND_PROMPT,
            self.tr('Windows 11'),
            self.tr('Support any Windows 11 Edition'),
            self.windowsGroup
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
        self.aioGroup.addSettingCard(self.aioCard)
        self.idmGroup.addSettingCard(self.idmCard)
        self.officeGroup.addSettingCard(self.officeaioCard)
        self.windowsGroup.addSettingCard(self.w10Card)
        self.windowsGroup.addSettingCard(self.w11Card)

        # add activator card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.aioGroup)
        self.expandLayout.addWidget(self.idmGroup)
        self.expandLayout.addWidget(self.officeGroup)
        self.expandLayout.addWidget(self.windowsGroup)
        
    # activator button action
    def runAIO(self):
        script_path = get_resource_path('resource/script/aio.cmd')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def runIDM(self):
        powershell_command = 'irm https://massgrave.dev/ias | iex'
        subprocess.run(['powershell', '-Command', powershell_command], shell=True)
    
    def runOfficeAIO(self):
        script_path = get_resource_path('resource/script/aso.cmd')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def runW10(self):
        script_path = get_resource_path('resource/script/w10.cmd')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def runW11(self):
        script_path = get_resource_path('resource/script/w11.cmd')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.themeChanged.connect(self.__onThemeChanged)

       
        self.aioCard.clicked.connect(self.runAIO)
        self.idmCard.clicked.connect(self.runIDM)
        self.officeaioCard.clicked.connect(self.runOfficeAIO)
        self.w10Card.clicked.connect(self.runW10)
        self.w11Card.clicked.connect(self.runW11)