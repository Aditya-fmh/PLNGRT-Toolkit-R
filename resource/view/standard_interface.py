# coding:utf-8
from config import cfg, KEYTEST_URL, LCDTEST_URL, MICTEST_URL, SPEAKERTEST_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, PrimaryPushSettingCard, ScrollArea, ExpandLayout, Theme,
                            setTheme, isDarkTheme, FluentIcon as FIF)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel
import os, sys, subprocess

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
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

        # Standard Apps label
        self.settingLabel = QLabel(self.tr("Standard Apps"), self)
        
        # Essential Software Group
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
        
        # Common Apps Group
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
            self.tr('Capcut (Online Installer)'),
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

        # Extra Apps Group
        self.extraGroup = SettingCardGroup(self.tr('Extra Apps'), self.scrollWidget)
        self.idmCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.DOWNLOAD,
            self.tr('Internet Download Manager'),
            self.tr('Some Downloader App'),
            self.commonGroup
        )
        self.qcpuCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.SPEED_HIGH,
            self.tr('QuickCPU'),
            self.tr('Use this to fix CPU throttling'),
            self.commonGroup
        )
        self.spotxCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.MUSIC,
            self.tr('SpotX (Spotify) Online Installer'),
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
        self.extraGroup.addSettingCard(self.qcpuCard)
        self.extraGroup.addSettingCard(self.spotxCard)

        # add card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.essentialGroup)
        self.expandLayout.addWidget(self.commonGroup)
        self.expandLayout.addWidget(self.extraGroup)
       
    # Button Action Goes Here
    def run_dx11(self):
        exe_path = get_resource_path('resource/standard/dx11.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_dx12(self):
        exe_path = get_resource_path('resource/standard/DX12/DXSETUP.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_vcr(self):
        exe_path = get_resource_path('resource/standard/vcpp.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_webview(self):
        exe_path = get_resource_path('resource/standard/webview2.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_aimp(self):
        exe_path = get_resource_path('resource/standard/aimp.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_canva(self):
        exe_path = get_resource_path('resource/standard/canva.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_capcut(self):
        exe_path = get_resource_path('resource/standard/capcut.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_chrome(self):
        exe_path = get_resource_path('resource/standard/chrome.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_firefox(self):
        exe_path = get_resource_path('resource/standard/firefox.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_nitro(self):
        exe_path = get_resource_path('resource/standard/nitro.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_telegram(self):
        exe_path = get_resource_path('resource/standard/telegram.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_vlc(self):
        exe_path = get_resource_path('resource/standard/vlc.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_wincd(self):
        exe_path = get_resource_path('resource/standard/wincdemu.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_winrar(self):
        exe_path = get_resource_path('resource/standard/winrar.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_zoom(self):
        exe_path = get_resource_path('resource/standard/zoom.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_idm(self):
        exe_path = get_resource_path('resource/standard/idm.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_qcpu(self):
        exe_path = get_resource_path('resource/standard/quickcpu.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_spotx(self):
        script_path = get_resource_path('resource/standard/spotx.bat')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
    
    # Button Slot Goes Here    
    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.themeChanged.connect(self.__onThemeChanged)
        
        self.dx11Card.clicked.connect(self.run_dx11)
        self.dx12Card.clicked.connect(self.run_dx12)
        self.vcrCard.clicked.connect(self.run_vcr)
        self.webviewCard.clicked.connect(self.run_webview)
        
        self.aimpCard.clicked.connect(self.run_aimp)
        self.canvaCard.clicked.connect(self.run_canva)
        self.capcutCard.clicked.connect(self.run_capcut)
        self.chromeCard.clicked.connect(self.run_chrome)
        self.firefoxCard.clicked.connect(self.run_firefox)
        self.nitroCard.clicked.connect(self.run_nitro)
        self.telegramCard.clicked.connect(self.run_telegram)
        self.vlcCard.clicked.connect(self.run_vlc)
        self.cdemuCard.clicked.connect(self.run_wincd)
        self.rarCard.clicked.connect(self.run_winrar)
        self.zoomCard.clicked.connect(self.run_zoom)
        
        self.idmCard.clicked.connect(self.run_idm)
        self.qcpuCard.clicked.connect(self.run_qcpu)
        self.spotxCard.clicked.connect(self.run_spotx)