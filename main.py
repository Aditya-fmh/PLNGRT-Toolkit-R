# coding:utf-8
import sys
import os

# Redirect stdout and stderr to a log file
log_file_path = os.path.join(os.path.dirname(__file__), 'output.log')
log_file = open(log_file_path, 'w')
sys.stdout = log_file
sys.stderr = log_file

from PyQt5.QtCore import Qt, QUrl, QEventLoop, QTimer, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QDialog
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            SubtitleLabel, setFont)
from qfluentwidgets import (FluentIcon as FIF, SplashScreen)
from resource.view.setting_interface import SettingInterface
from resource.view.activator_interface import ActivatorInterface
from resource.view.checking_interface import CheckingInterface
from resource.view.standard_interface import StandardInterface
from resource.view.driver_interface import DriverInterface
from resource.view.msstore_interface import StoreInterface
from resource.view.extra_interface import ExtraInterface

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.activatorInterface = ActivatorInterface(self)
        self.activatorInterface.setObjectName('Activator')
        
        self.checkingInterface = CheckingInterface(self)
        self.checkingInterface.setObjectName('Checking')
        
        self.standardInterface = StandardInterface(self)
        self.standardInterface.setObjectName('Standard')
        
        self.driverInterface = DriverInterface(self)
        self.driverInterface.setObjectName('Driver Install')
        
        self.storeInterface = StoreInterface(self)
        self.storeInterface.setObjectName('MS Store')
        
        self.extraInterface = ExtraInterface(self)
        self.extraInterface.setObjectName('Extra Tweak')
        
        self.settingInterface = SettingInterface(self)
        self.settingInterface.setObjectName('Setting')

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.activatorInterface, FIF.COMMAND_PROMPT, 'Activator')
        self.addSubInterface(self.checkingInterface, FIF.SEARCH_MIRROR, 'Checking')
        self.addSubInterface(self.standardInterface, FIF.APPLICATION, 'Standard')
        self.addSubInterface(self.storeInterface, FIF.SHOPPING_CART, 'MS Store')
        self.addSubInterface(self.driverInterface, FIF.UPDATE, 'Driver Install')
        self.addSubInterface(self.extraInterface, FIF.DEVELOPER_TOOLS, 'Extra')

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Setting', FIF.SETTING, NavigationItemPosition.BOTTOM)
        self.navigationInterface.setCurrentItem(self.activatorInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'resource', 'icon2.ico')
        else:
            icon_path = os.path.join(os.path.dirname(__file__), 'resource', 'icon2.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle('PLNGRT Toolkit R')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)
        loop.exec()

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    setTheme(Theme.DARK)

    app = QApplication(sys.argv)

    # Directly instantiate the Window class
    w = Window()
    w.show()
    app.exec_()

    log_file.close()  # Ensure the log file is closed when the application exits