# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QEventLoop, QTimer, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            SubtitleLabel, setFont)
from qfluentwidgets import (FluentIcon as FIF, SplashScreen)
from resource.view.setting_interface import SettingInterface
from resource.view.activator_interface import ActivatorInterface

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
        self.checkingInterface = Widget('Checking', self)
        self.standardInterface = Widget('Standard', self)
        self.driverInterface = Widget('Driver Install', self)
        self.storeInterface = Widget('MS Store', self)
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

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Setting', FIF.SETTING, NavigationItemPosition.BOTTOM)
        self.navigationInterface.setCurrentItem(self.activatorInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/icon2.ico'))
        self.setWindowTitle('PLNGRT Toolkit R')

        # create splash screen and show window
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.show()
        self.createSubInterface()
        self.splashScreen.finish()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)
        loop.exec()

    def showMessageBox(self):
        w = MessageBox(
            'About',
            'This app is a remake from old toolkit which using Tkinter as its GUI, now this app is made with PyQt5 and QFluentWidgets',
            self
        )
        w.yesButton.setText('Github Page')
        w.cancelButton.setText('Back')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/Aditya-fmh"))


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
