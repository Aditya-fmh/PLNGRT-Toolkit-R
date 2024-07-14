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

class StandardInterface(ScrollArea):
    """ Standard interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Standard Apps"), self)
        
        # Checking Software
        self.essentialGroup = SettingCardGroup(self.tr('System Essential Apps'), self.scrollWidget)
        self.dx11Card = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.APPLICATION,
            self.tr('DirectX 11'),
            self.tr('DX11 Offline Installer'),
            self.essentialGroup
        )
        self.dx12Card = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.APPLICATION,
            self.tr('DirectX 12'),
            self.tr('DX12 Offline Installer'),
            self.essentialGroup
        )
        self.vcrCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.APPLICATION,
            self.tr('VisualCppRedist AIO'),
            self.tr('AIO Repack of Microsoft Visual C++ Redistributable'),
            self.essentialGroup
        )
        self.webviewCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.APPLICATION,
            self.tr('WebView2 Runtime'),
            self.tr('Some newer app require this'),
            self.essentialGroup
        )
        
        # IDM Activator
        self.commonGroup = SettingCardGroup(self.tr('Common Apps'), self.scrollWidget)
        self.aimpCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.MUSIC,
            self.tr('AIMP'),
            self.tr('Some Music Player'),
            self.commonGroup
        )
        self.canvaCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.PHOTO,
            self.tr('Canva'),
            self.tr('Online Photo Editor'),
            self.commonGroup
        )
        self.capcutCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.VIDEO,
            self.tr('Capcut'),
            self.tr('Some Video Editor'),
            self.commonGroup
        )
        self.chromeCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.GLOBE,
            self.tr('Google Chrome'),
            self.tr('Some Google Browser'),
            self.commonGroup
        )
        self.firefoxCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.GLOBE,
            self.tr('Mozilla Firefox'),
            self.tr('Some Other Browser'),
            self.commonGroup
        )
        self.nitroCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.DOCUMENT,
            self.tr('NitroPDF'),
            self.tr('Some PDF Editor/Viewer'),
            self.commonGroup
        )
        self.telegramCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.SEND,
            self.tr('Telegram'),
            self.tr('Some Chatting Apps'),
            self.commonGroup
        )
        self.vlcCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.MEDIA,
            self.tr('VLC'),
            self.tr('Some Multimedia Apps'),
            self.commonGroup
        )
        self.cdemuCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.PIE_SINGLE,
            self.tr('WinCDEmu'),
            self.tr('Some Mounting Apps'),
            self.commonGroup
        )
        self.rarCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.BOOK_SHELF,
            self.tr('WinRAR'),
            self.tr('Some Archiving Apps'),
            self.commonGroup
        )
        self.zoomCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.PEOPLE,
            self.tr('Zoom'),
            self.tr('A Video Conference Apps'),
            self.commonGroup
        )

        # IDM Activator
        self.extraGroup = SettingCardGroup(self.tr('Extra Apps'), self.scrollWidget)
        self.idmCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.DOWNLOAD,
            self.tr('Internet Download Manager'),
            self.tr('Some Downloader App'),
            self.commonGroup
        )
        self.spotxCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.MUSIC,
            self.tr('SpotX (Spotify)'),
            self.tr('Some Online Music Player'),
            self.commonGroup
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
        self.essentialGroup.addSettingCard(self.dx11Card)
        self.essentialGroup.addSettingCard(self.dx12Card)
        self.essentialGroup.addSettingCard(self.vcrCard)
        self.essentialGroup.addSettingCard(self.webviewCard)
        
        self.commonGroup.addSettingCard(self.aimpCard)
        self.commonGroup.addSettingCard(self.canvaCard)
        self.commonGroup.addSettingCard(self.capcutCard)
        self.commonGroup.addSettingCard(self.chromeCard)
        self.commonGroup.addSettingCard(self.firefoxCard)
        self.commonGroup.addSettingCard(self.nitroCard)
        self.commonGroup.addSettingCard(self.telegramCard)
        self.commonGroup.addSettingCard(self.vlcCard)
        self.commonGroup.addSettingCard(self.cdemuCard)
        self.commonGroup.addSettingCard(self.rarCard)
        self.commonGroup.addSettingCard(self.zoomCard)
        
        self.extraGroup.addSettingCard(self.idmCard)
        self.extraGroup.addSettingCard(self.spotxCard)

        # add activator card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.essentialGroup)
        self.expandLayout.addWidget(self.commonGroup)
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