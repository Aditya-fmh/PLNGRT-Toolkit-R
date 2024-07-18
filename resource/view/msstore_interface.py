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

class StoreInterface(ScrollArea):
    """ MS Store interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Microsoft Store Related App"), self)
        
        # Checking Software
        self.mstoreGroup = SettingCardGroup(self.tr('Microsoft Store'), self.scrollWidget)
        self.mstoreCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.SHOPPING_CART,
            self.tr('Microsoft Store (Recommended)'),
            self.tr('This will install older version of microsoft store, need to update later'),
            self.mstoreGroup
        )
        
        self.aloneGroup = SettingCardGroup(self.tr('Standalone Install (Optional)'), self.scrollWidget)
        self.reqCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.APPLICATION,
            self.tr('Requirement'),
            self.tr('Install this first if you are gonna use standalone installer'),
            self.aloneGroup
        )
        self.calcCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.CALENDAR,
            self.tr('Calculator'),
            self.tr('Install Calculator'),
            self.aloneGroup
        )
        self.cameraCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.CAMERA,
            self.tr('Camera'),
            self.tr('Install Windows Camera'),
            self.aloneGroup
        )
        self.paintCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.PALETTE,
            self.tr('Paint'),
            self.tr('Install Paint'),
            self.aloneGroup
        )
        self.paint3dCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.PALETTE,
            self.tr('Paint 3D'),
            self.tr('Install Paint 3D'),
            self.aloneGroup
        )
        self.photosCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.PHOTO,
            self.tr('Photos'),
            self.tr('Install Microsoft Photos'),
            self.aloneGroup
        )
        self.whatsCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.PHONE,
            self.tr('WhatsApp'),
            self.tr('Install WhatsApp'),
            self.aloneGroup
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
        self.mstoreGroup.addSettingCard(self.mstoreCard)
        
        self.aloneGroup.addSettingCard(self.reqCard)
        self.aloneGroup.addSettingCard(self.calcCard)
        self.aloneGroup.addSettingCard(self.cameraCard)
        self.aloneGroup.addSettingCard(self.paintCard)
        self.aloneGroup.addSettingCard(self.paint3dCard)
        self.aloneGroup.addSettingCard(self.photosCard)
        self.aloneGroup.addSettingCard(self.whatsCard)

        # add activator card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.mstoreGroup)
        self.expandLayout.addWidget(self.aloneGroup)
       
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