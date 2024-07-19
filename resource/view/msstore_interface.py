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

class StoreInterface(ScrollArea):
    """ MS Store interface """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # Label
        self.settingLabel = QLabel(self.tr("Microsoft Store Related App"), self)
        
        # MS Store Group
        self.mstoreGroup = SettingCardGroup(self.tr('Microsoft Store'), self.scrollWidget)
        self.mstoreCard = PrimaryPushSettingCard(
            self.tr('Install'),
            FIF.SHOPPING_CART,
            self.tr('Microsoft Store (Recommended)'),
            self.tr('This will install older version of microsoft store, need to update later'),
            self.mstoreGroup
        )
        
        # Standalone Group
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

        # add card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.mstoreGroup)
        self.expandLayout.addWidget(self.aloneGroup)
       
    # Button Action Goes Here
    def run_msstore(self):
        script_path = get_resource_path('resource/msstore/Store/Add-Store.cmd')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def run_requirement(self):
        script_path = get_resource_path('resource/msstore/requirement.ps1')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def run_calc(self):
        script_path = get_resource_path('resource/msstore/install-calculator.ps1')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def run_camera(self):
        script_path = get_resource_path('resource/msstore/install-camera.ps1')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def run_paint(self):
        script_path = get_resource_path('resource/msstore/install-paint.ps1')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def run_paint3d(self):
        script_path = get_resource_path('resource/msstore/install-paint3d.ps1')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def run_photos(self):
        script_path = get_resource_path('resource/msstore/install-photos.ps1')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
        
    def run_whatsapp(self):
        script_path = get_resource_path('resource/msstore/install-whatsapp.ps1')
        nircmd_path = get_resource_path('resource/tool/nircmd/nircmd.exe')
        subprocess.run([nircmd_path, 'elevate', 'cmd.exe', '/c', script_path], shell=True)
    
    # Button Slot Goes Here    
    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.themeChanged.connect(self.__onThemeChanged)
        
        self.mstoreCard.clicked.connect(self.run_msstore)
        
        self.reqCard.clicked.connect(self.run_requirement)
        self.calcCard.clicked.connect(self.run_calc)
        self.cameraCard.clicked.connect(self.run_camera)
        self.paintCard.clicked.connect(self.run_paint)
        self.paint3dCard.clicked.connect(self.run_paint3d)
        self.photosCard.clicked.connect(self.run_photos)
        self.whatsCard.clicked.connect(self.run_whatsapp)