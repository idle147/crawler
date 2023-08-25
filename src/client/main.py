import sys

from core.main_win import MainWin
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWin()
    window.show()
    app.exec_()
