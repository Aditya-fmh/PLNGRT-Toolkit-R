# coding:utf-8
from config import cfg
from qfluentwidgets import (SettingCardGroup, PrimaryPushSettingCard, PrimarySplitPushButton, ScrollArea, ExpandLayout, Theme, setTheme, isDarkTheme, FluentIcon as FIF)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
import os, sys, subprocess

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ExtraInterface(ScrollArea):
    """ Extra Tweak Interface """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # Label
        self.settingLabel = QLabel(self.tr("Extra Windows Option"), self)
        
        self.securityGroup = SettingCardGroup(self.tr('Extra Option'), self.scrollWidget)
        self.defenderCard = PrimaryPushSettingCard(
            self.tr('Run Script'),
            FIF.COMMAND_PROMPT,
            self.tr('Enable/Disable Windows Defender'),
            self.tr('This will run a script to enable/disable windows defender'),
            self.securityGroup
        )
        
        # New Serial Number Card
        self.serialNumberCard = PrimaryPushSettingCard(
            self.tr('Check Serial Number'),
            FIF.COMMAND_PROMPT,
            self.tr('Show Device Serial Number'),
            self.tr('This will display the device serial number in a popup'),
            self.securityGroup
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
        self.securityGroup.addSettingCard(self.defenderCard)
        self.securityGroup.addSettingCard(self.serialNumberCard)

        # add card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.securityGroup)
       
    # Button Action Goes Here
    def toggle_defender(self):
        script_path = get_resource_path('C:\Windows\AtlasModules\Scripts\ScriptWrappers\ToggleDefender.ps1')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        # Using os.system to run the PowerShell script directly
        os.system(f'powershell -ExecutionPolicy Bypass -File "{script_path}"')
    
    # New method to get the device serial number
    def get_serial_number(self):
        serial_number = subprocess.check_output("wmic bios get serialnumber", shell=True).decode().splitlines()[1].strip()
        return serial_number

    # New method to show the serial number in a popup
    def show_serial_number(self):
        serial_number = self.get_serial_number()
        QMessageBox.information(self, self.tr("Device Serial Number"), serial_number)

    # Button Slot Goes Here    
    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.themeChanged.connect(self.__onThemeChanged)
        
        self.defenderCard.clicked.connect(self.toggle_defender)
        self.serialNumberCard.clicked.connect(self.show_serial_number)  # Connect the new card to the slot