# coding:utf-8
from config import cfg, KEYTEST_URL, LCDTEST_URL, MICTEST_URL, SPEAKERTEST_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, HyperlinkCard, PrimaryPushSettingCard, ScrollArea, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFontDialog, QFileDialog
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

class CheckingInterface(ScrollArea):
    """ Checking interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Checking Software & Web"), self)
        
        # Checking Software
        self.checkingGroup = SettingCardGroup(self.tr('Checking Software'), self.scrollWidget)
        self.batteryCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('Battery Info View'),
            self.tr('Check battery condition i.e Battery Health and Battery Capacity'),
            self.checkingGroup
        )
        self.cpuzCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('CPU-Z'),
            self.tr('Check PC/Laptop detailed specification'),
            self.checkingGroup
        )
        self.crystalCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('Crystal Disk Info'),
            self.tr('Check SSD condition like health, lifetime write and other parameter'),
            self.checkingGroup
        )
        self.gpuzCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('GPU-Z'),
            self.tr('Check GPU detailed specification'),
            self.checkingGroup
        )
        self.sentinelCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('HD Sentinel'),
            self.tr('Check SSD/HDD Condition like performance, health, lifetme write/start and stop count'),
            self.checkingGroup
        )
        self.hwmCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('HWMonitor'),
            self.tr('Check detailed specification'),
            self.checkingGroup
        )
        self.speccyCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('Speccy'),
            self.tr('Another app to check specification'),
            self.checkingGroup
        )
        
        
        # IDM Activator
        self.chkwebGroup = SettingCardGroup(self.tr('Checking Web'), self.scrollWidget)
        self.keyCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('Keyboard Test'),
            self.tr('Test Keyboard Functionality'),
            self.chkwebGroup
        )
        self.lcdCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('LCD Test'),
            self.tr('Check LCD for Black Spot or White Spot or any other error'),
            self.chkwebGroup
        )
        self.micCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('Microphone Test'),
            self.tr('Test Microphone Functionality'),
            self.chkwebGroup
        )
        self.speakerCard = PrimaryPushSettingCard(
            self.tr('Check'),
            FIF.COMMAND_PROMPT,
            self.tr('Speaker Test'),
            self.tr('Test Speaker Left & Right Functionality'),
            self.chkwebGroup
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
        self.checkingGroup.addSettingCard(self.batteryCard)
        self.checkingGroup.addSettingCard(self.cpuzCard)
        self.checkingGroup.addSettingCard(self.crystalCard)
        self.checkingGroup.addSettingCard(self.gpuzCard)
        self.checkingGroup.addSettingCard(self.sentinelCard)
        self.checkingGroup.addSettingCard(self.hwmCard)
        self.checkingGroup.addSettingCard(self.speccyCard)
        
        self.chkwebGroup.addSettingCard(self.keyCard)
        self.chkwebGroup.addSettingCard(self.lcdCard)
        self.chkwebGroup.addSettingCard(self.micCard)
        self.chkwebGroup.addSettingCard(self.speakerCard)

        # add activator card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.checkingGroup)
        self.expandLayout.addWidget(self.chkwebGroup)
        
    # checking button action
    def extract_and_run_battery(self):
        """ Extract and run the battery check executable """
        zip_path = get_resource_path('resource/checking/batteryinfoview.zip')
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the zip file to the temporary directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            exe_path = os.path.join(temp_dir, 'BatteryInfoView.exe')
            subprocess.run([exe_path], check=True)
            
    def run_cpuz(self):
        """ Run the CPU-Z executable """
        exe_path = get_resource_path('resource/checking/cpuz/cpuz_x64.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        # Run the executable with elevated privileges using nircmd
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
    
    def run_crystal(self):
        """ Run Crystal Disk Info executable """
        exe_path = get_resource_path('resource/checking/crystaldisk/DiskInfo64A.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        # Run the executable with elevated privileges using nircmd
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_gpuz(self):
        """ Run GPU-Z executable """
        exe_path = get_resource_path('resource/checking/gpuz.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        # Run the executable with elevated privileges using nircmd
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_sentinel(self):
        """ Run HDSentinel executable """
        exe_path = get_resource_path('resource/checking/hdsentinel/HDSentinel.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        # Run the executable with elevated privileges using nircmd
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_hwm(self):
        """ Run HWMonitor executable """
        exe_path = get_resource_path('resource/checking/hwmonitor/HWMonitor_x64.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        # Run the executable with elevated privileges using nircmd
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_speccy(self):
        """ Run Speccy executable """
        exe_path = get_resource_path('resource/checking/spsetup132/Speccy64.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        # Run the executable with elevated privileges using nircmd
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.themeChanged.connect(self.__onThemeChanged)

        self.batteryCard.clicked.connect(self.extract_and_run_battery)
        self.cpuzCard.clicked.connect(self.run_cpuz)
        self.crystalCard.clicked.connect(self.run_crystal)
        self.gpuzCard.clicked.connect(self.run_gpuz)
        self.sentinelCard.clicked.connect(self.run_sentinel)
        self.hwmCard.clicked.connect(self.run_hwm)
        self.speccyCard.clicked.connect(self.run_speccy)
        
        self.keyCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(KEYTEST_URL)))
        self.lcdCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(LCDTEST_URL)))
        self.micCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(MICTEST_URL)))
        self.speakerCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(SPEAKERTEST_URL)))
        