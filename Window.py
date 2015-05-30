__author__ = 'пк'
from PyQt4 import QtGui, QtCore
import sys


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(500, 300, 500, 300)
        self.setWindowTitle("Генерация пароля")
        self.grid = QtGui.QGridLayout()

        self.generate = QtGui.QPushButton("Сгенерировать", self)
        self.generate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.generate, QtCore.SIGNAL('clicked()'), self.prnt)
        self.setFocus()

        self.titlePrompting = QtGui.QLabel("Подсказка:")
        self.labelPrompting = QtGui.QLabel("")  # setText()
        self.labelPrompting.setAlignment(QtCore.Qt.AlignHCenter)
        self.labelPrompting.setStyleSheet('background-color: #FFFAFA; font-size: 14px;')
        self.titlePassword = QtGui.QLabel("Пароль:")
        self.labelPassword = QtGui.QLabel("")
        self.labelPassword.setAlignment(QtCore.Qt.AlignHCenter)
        self.labelPassword.setStyleSheet('background-color: #FFFAFA; font-size: 14px;')

        self.checkDigits = QtGui.QCheckBox()
        self.titleDigits = QtGui.QLabel("с цифрами")
        self.checkSymbols = QtGui.QCheckBox()
        self.titleSymbols = QtGui.QLabel("с символами:")
        self.inputSymbols = QtGui.QLineEdit(self)
        self.inputSymbols.setToolTip('Введите символы через пробел')
        self.checkMin = QtGui.QCheckBox()
        self.titleMin = QtGui.QLabel("минимальная длина:")
        self.inputMin = QtGui.QLineEdit(self)
        self.textMin = QtGui.QLabel("символов")
        self.checkMax = QtGui.QCheckBox()
        self.titleMax = QtGui.QLabel("максимальная длина:")
        self.inputMax = QtGui.QLineEdit(self)
        self.textMax = QtGui.QLabel("символов")

        self.grid.addWidget(self.titlePrompting, 0, 1)
        self.grid.addWidget(self.labelPrompting, 1, 0, 1, 3)
        self.grid.addWidget(self.titlePassword, 2, 1)
        self.grid.addWidget(self.labelPassword, 3, 0, 1, 3)

        self.grid.addWidget(self.checkDigits, 4, 0)
        self.grid.addWidget(self.titleDigits, 4, 1)
        self.grid.addWidget(self.checkSymbols, 5, 0)
        self.grid.addWidget(self.titleSymbols, 5, 1)
        self.grid.addWidget(self.inputSymbols, 5, 2)
        self.grid.addWidget(self.checkMin, 6, 0)
        self.grid.addWidget(self.titleMin, 6, 1)
        self.grid.addWidget(self.inputMin, 6, 2)
        self.grid.addWidget(self.textMin, 6, 3)
        self.grid.addWidget(self.checkMax, 7, 0)
        self.grid.addWidget(self.titleMax, 7, 1)
        self.grid.addWidget(self.inputMax, 7, 2)
        self.grid.addWidget(self.textMax, 7, 3)

        self.grid.addWidget(self.generate, 8, 1, 1, 2)
        self.setLayout(self.grid)

    def prnt(self):
        self.labelPrompting.setText("У попа была собака, он её любил")
        self.labelPassword.setText("U popa byla sobaka, on eyo lyubil")
        print("Генерирую!")


def main():
    pass

app = QtGui.QApplication(sys.argv)
win = Window()
win.show()

app.exec()