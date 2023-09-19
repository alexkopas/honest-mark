import sys
from PyQt5 import QtWidgets, QtGui
from app import HonestMarkApp
import logging
import ctypes

myappid = 'kopas.utils.honestmark.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

logging.basicConfig(level=logging.WARNING)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("xml.ico"))
    window = HonestMarkApp()
    window.show()
    app.exec()

