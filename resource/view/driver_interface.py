# coding:utf-8
from config import cfg
from qfluentwidgets import (SettingCardGroup, PrimaryPushSettingCard, ScrollArea, ExpandLayout, Theme, setTheme, isDarkTheme, FluentIcon as FIF)
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

class DriverInterface(ScrollArea):
    """ Driver interface """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # Label
        self.settingLabel = QLabel(self.tr("Driver & Update"), self)
        
        # Windows Update Group
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
        
        # Driver Update Group
        self.driverGroup = SettingCardGroup(self.tr('Driver Update'), self.scrollWidget)
        self.drvboosterCard = PrimaryPushSettingCard(
            self.tr('Run'),
            FIF.UPDATE,
            self.tr('Driver Booster (Recommended)'),
            self.tr('Need to install Visual C++ if its not opening'),
            self.driverGroup
        )
        
        # Extra Driver Group
        self.extraGroup = SettingCardGroup(self.tr('Extra Driver'), self.scrollWidget)
        self.hpfnCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.UPDATE,
            self.tr('HP Fn Key Driver'),
            self.tr('Enable Function key for some HP laptops'),
            self.driverGroup
        )
        self.t440Card = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.UPDATE,
            self.tr('T440p Camera Driver'),
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

        # add card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.winupdateGroup)
        self.expandLayout.addWidget(self.driverGroup)
        self.expandLayout.addWidget(self.extraGroup)
       
    # Button Action Goes Here
    def run_wumgr(self):
        exe_path = get_resource_path('resource/update-driver/wumgr/wumgr.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_wumt(self):
        exe_path = get_resource_path('resource/update-driver/wumt/wumt_x64.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_drvbooster(self):
        exe_path = get_resource_path('resource/update-driver/DriverBoosterPortable/DriverBoosterPortable.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_hpfnkey(self):
        exe_path = get_resource_path('resource/update-driver/hp_fn_key.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
        
    def run_t440drv(self):
        exe_path = get_resource_path('resource/update-driver/t440p_camera.exe')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', exe_path], check=True)
    
    # Button Slot Goes Here    
    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.themeChanged.connect(self.__onThemeChanged)
        
        self.wumgrCard.clicked.connect(self.run_wumgr)
        self.wumtCard.clicked.connect(self.run_wumt)
        
        self.drvboosterCard.clicked.connect(self.run_drvbooster)
        
        self.hpfnCard.clicked.connect(self.run_hpfnkey)
        self.t440Card.clicked.connect(self.run_t440drv)