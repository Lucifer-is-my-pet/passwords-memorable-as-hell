__author__ = 'Гуральник'
import random
import re
from PyQt4 import QtGui, QtCore
import sys


class PasswordsError(Exception):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

dictionary = {' ': ' ', '-': '-', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
              'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
              'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
              'ъ': "'", 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya', ',': ',', ':': ':', '?': '?'}
w = re.compile('\W+')
sp = re.compile('[ ]')
alph = re.compile("[a-zA-Z]")


def read_file(fname):  # выкачиваем один раз в main и обращаемся уже к массиву
    with open(fname, 'r', encoding="utf-8") as fl:
        return fl.readlines()


def cut_first_letters(string):  # преобразуй-метод
    """
    вырезает первые буквы слов из кириллического варианта
    :return: list
    """
    splitted = w.split(string)
    # print(string, splitted)

    cutted = list()
    for i in splitted:
        cutted.append(i[0])
    return cutted


def transliterate(string, symbolsToUse):  # преобразуй-заполни-метод
    """
    создаёт транслитерованный вариант строки
    :string: str, list
    :return: str
    """
    temp = str()
    for letter in string:
        if letter == '\n':
            break
        temp += dictionary[letter.lower()]
    # print(self.translit, 'is not iterable', self.cyrillic)

    result = str()
    for i in temp:
        if i in symbolsToUse or i.isalpha() or i == ' ':
            result += i
    # if not len(self):
    # self.translit = result
    return result


def number_of_letters(string):
    """
    :param string:
    :return: int: число букв в транслитерованном варианте предполагаемой пословицы
    """
    splitted = cut_first_letters(string)
    translitted = transliterate(splitted, "")
    return len(translitted)


def critical_number_of_repetitions(string):
    """
    критичное число повторов: символ встречается больше 3-х раз или есть как минимум два различных повторяющихся символа
    :param string:
    :return: есть ли в предполагаемом пароле критичное число повторов
    """
    reps = {letter: 0 for letter in set(string)}
    for letter in string:
        reps[letter] += 1
    counter = 0
    for item in list(reps.values()):
        if item > 3:
            return True
        elif item > 2:
            counter += 1
    if counter > 1:
        return True
    return False


def once_true(lst):
    counter = 0
    for i in lst:
        if i is True:
            counter += 1
    if counter > 1:
        return False
    else:
        return True


class Password:
    def __init__(self):
        self.cyrillic = str()
        self.translit = str()
        self.min = -1
        self.max = -1
        self.withDigits = False
        self.withSymbols = False
        self.symbolsToUse = str()
        self.proverbs = read_file("proverbs.txt")
        self.numOfLines = len(self.proverbs)
        self.thatOneLine = -1  # номер строки, откуда получили пословицу
        self.usedNumbers = set()

    def __len__(self):
        return len(self.translit)

    def __str__(self):
        return self.translit

    def find_new(self):  # заполни-метод
        """
        получает в генераторе случайных чисел номер строки и извлекает соответсвующую строку из файла, помещая в
        поле cyrillic
        номера, полученные в предыдущих попытках, фиксируются, чтобы не было повторов
        прежде чем добавить пословицу, метод проверяет, соответствует ли она ограничениям
        :return: str
        """
        if len(self.usedNumbers) == self.numOfLines:
            raise PasswordsError("Все попытки получить пароль исчерпаны! Вы король кликанья!")
        for i in range(self.numOfLines):
            num = round(random.uniform(0, self.numOfLines - 1))
            if num not in self.usedNumbers:
                temp = self.proverbs[num]
                ind = temp.find('\n')
                if ind > 0:
                    temp = temp[:ind]

                if (self.max != -1) and self.max <= 12 and critical_number_of_repetitions(temp):
                    continue

                if (self.max != -1) and (number_of_letters(temp) > self.max) and (not self.withDigits) and \
                        (not self.withSymbols):
                    continue
                elif (self.max != -1) and ((number_of_letters(temp) + 4) > self.max) and self.withDigits and \
                        self.withSymbols:
                    continue
                elif (self.max != -1) and ((number_of_letters(temp) + 2) > self.max) and (self.withDigits or self.withSymbols):
                    continue
                if (self.min != -1) and (number_of_letters(temp) < self.min) and (not self.withDigits) and \
                        (not self.withSymbols):
                    continue
                elif (self.min != -1) and ((number_of_letters(temp) - 4) < self.min) and self.withDigits and \
                        self.withSymbols:
                    continue
                elif (self.min != -1) and ((number_of_letters(temp) - 2) < self.min) and (self.withDigits or self.withSymbols):
                    continue

                self.cyrillic = temp
                self.usedNumbers.add(num)
                self.thatOneLine = num + 1
                return self.cyrillic

    def number_of_spaces(self):
        """
        :return: int
        """
        temp = str()
        for letter in self.cyrillic:
            if letter in self.symbolsToUse or letter.isalpha() or letter == ' ':
                temp += letter

        result = len(sp.findall(temp))
        return result

    def last_match(self, string):
        """
        возвращает индекс последнего вхождения букв в строке
        :param string: слово пословицы
        :return: int
        """
        return [m.start() for m in alph.finditer(string)][-1]

    def add_digits(self):  # преобразуй-метод
        """
        работает с транслитeрованным вариантом, добавляет цифры в начало и в конец пароля
        две цифры получаем из манипуляций с номером строки, откуда была вытянута пословица и числом пробелов
        """
        result = str()
        amazingNumber = self.thatOneLine
        spaces = self.number_of_spaces()
        if amazingNumber < 10:
            amazingNumber *= spaces
            if len(str(amazingNumber)) != 2:
                amazingNumber //= 10
        elif amazingNumber >= 100:
            if spaces == 1:
                spaces += 1
            count = 0
            while len(str(amazingNumber)) != 2:
                count += 1
                if spaces == 0:
                    raise PasswordsError("В пароле нет пробелов: " + self.translit)
                amazingNumber //= spaces
                if count > 5:
                    raise PasswordsError(
                        "Я зациклился. Номер сейчас: " + str(amazingNumber) + ", пробелов: " + str(spaces))

        result += str(amazingNumber // 10) + self.translit + str(amazingNumber % 10)
        self.translit = result

    def up(self):  # преобразуй-метод
        """
        работает с транслитерованным вариантом (может содержать только буквы и пробелы, а может - тире, зпт и апострофы)
        в полном варианте увеличивает последнюю букву каждого слова
        в обрезанном - первую, последнюю и примерно в середине
        """
        if self.max == -1:
            splitted = self.translit.split(' ')
            temp = list()
            for i in range(len(splitted)):
                if alph.search(splitted[i]):  # попалось не тире
                    ind = self.last_match(splitted[i])
                    # if ind == 0 or len(splitted[i]) == 1:
                    # print("Одно слово!", splitted[i][:ind] + splitted[i][ind].upper())
                    temp.append(splitted[i][:ind] + splitted[i][ind].upper())
                    if ind != len(splitted[i]) - 1:  # в конце слова есть другие символы
                        temp[i] += splitted[i][ind + 1:]
                else:
                    temp.append(splitted[i])
            result = ' '.join(temp)
        else:
            result = self.translit[0].upper() + self.translit[1:-1] + self.translit[-1].upper()
            result = result[:len(result) // 2] + result[len(result) // 2].upper() + result[(len(result) // 2) + 1:]

        self.translit = result

    def add_symbols(self):  # преобразуй-метод
        """
        добавляет спец. символы в пароль
        :return: str
        """
        result = str()
        counter = 0
        for letter in self.translit:
            if letter in self.symbolsToUse:
                counter += 1
        if counter >= 2:  # символов уже достаточно
            return self.translit
        elif counter == 1 and len(self.symbolsToUse) > 1:
            # исключить уже использованный символ
            temp = list(self.symbolsToUse)
            thatSymbol = (set(temp) & set(self.translit)).pop()
            temp.remove(thatSymbol)
            temp = ''.join(temp)
            ind = round(random.uniform(0, len(temp) - 1))
            toUse = temp[ind]
            result = toUse.join(self.translit.split(' '))
        elif counter == 1 and len(self.symbolsToUse) == 1:
            return self.translit
        else:  # могут быть скобки, тогда лучше обрамить ими
            temp = list(self.symbolsToUse)
            ind1 = ind2 = ind3 = 0
            toUse2 = toUse3 = str()
            openBreaks = "([{<"
            openBreaksPresent = [False for x in range(4)]
            closeBreaks = ")]}>"
            closeBreaksPresent = [False for x in range(4)]
            for i in temp:
                if i in openBreaks:
                    openBreaksPresent[openBreaks.index(i)] = True
                elif i in closeBreaks:
                    closeBreaksPresent[closeBreaks.index(i)] = True
            if True in openBreaksPresent and True in closeBreaksPresent:
                if once_true(openBreaksPresent):  # если один вид скобок
                    toUse2 = openBreaks[openBreaksPresent.index(True)]
                    toUse3 = closeBreaks[closeBreaksPresent.index(True)]
                    temp.remove(toUse2)
                    temp.remove(toUse3)
                else:  # если несколько видов скобок
                    indexes = [x for x in range(4) if openBreaksPresent[x] is True]
                    ind = round(random.uniform(0, len(indexes) - 1))
                    toUse2 = openBreaks[indexes[ind]]
                    toUse3 = closeBreaks[indexes[ind]]
                    temp.remove(toUse2)
                    temp.remove(toUse3)
            else:
                ind2 = round(random.uniform(0, len(temp) - 1))
                toUse2 = temp[ind2]
                toUse3 = toUse2
            ind1 = round(random.uniform(0, len(temp) - 1))
            while temp[ind1] == toUse2 and len(temp) > 1:
                ind1 = round(random.uniform(0, len(temp) - 1))
            toUse1 = temp[ind1]
            result = toUse1.join(self.translit.split(' '))
            result = toUse2 + result + toUse3
        self.translit = result
        # return result


class Window(QtGui.QWidget):
    def __init__(self, passToGenerate, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.myPreciousPassword = passToGenerate
        self.setGeometry(600, 300, 450, 300)
        self.setWindowTitle("Генерация пароля")
        self.grid = QtGui.QGridLayout()

        self.generate = QtGui.QPushButton("Сгенерировать", self)
        self.generate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.generate, QtCore.SIGNAL('clicked()'), self.generation)
        self.setFocus()

        self.titlePrompting = QtGui.QLabel("Подсказка:")
        self.labelPrompting = QtGui.QLabel("")
        self.labelPrompting.setAlignment(QtCore.Qt.AlignHCenter)
        self.labelPrompting.setStyleSheet('background-color: #FFFAFA; font-size: 14px;')
        self.titlePassword = QtGui.QLabel("Пароль:")
        self.labelPassword = QtGui.QLineEdit("")
        self.labelPassword.setAlignment(QtCore.Qt.AlignHCenter)
        self.labelPassword.setStyleSheet('background-color: #FFFAFA; font-size: 14px;')

        self.checkUp = QtGui.QCheckBox()
        self.titleUp = QtGui.QLabel("с заглавными буквами")
        self.checkDigits = QtGui.QCheckBox()
        self.titleDigits = QtGui.QLabel("с цифрами")
        self.checkSymbols = QtGui.QCheckBox()
        self.titleSymbols = QtGui.QLabel("с символами:")
        self.titleSymbols.setToolTip('Введите символы, не разделяя их запятой или пробелом')
        self.inputSymbols = QtGui.QLineEdit(self)
        self.inputSymbols.setToolTip('Введите символы, не разделяя их запятой или пробелом')
        self.checkMin = QtGui.QCheckBox()
        self.titleMin = QtGui.QLabel("минимальная длина:")
        self.inputMin = QtGui.QLineEdit(self)
        self.textMin = QtGui.QLabel("символов")
        self.checkMax = QtGui.QCheckBox()
        self.titleMax = QtGui.QLabel("максимальная длина:")
        self.inputMax = QtGui.QLineEdit(self)
        self.textMax = QtGui.QLabel("символов")

        self.grid.addWidget(self.titlePrompting, 0, 1)
        self.grid.addWidget(self.labelPrompting, 1, 0, 1, 4)
        self.grid.addWidget(self.titlePassword, 2, 1)
        self.grid.addWidget(self.labelPassword, 3, 0, 1, 4)

        self.grid.addWidget(self.checkUp, 4, 0)
        self.grid.addWidget(self.titleUp, 4, 1)
        self.grid.addWidget(self.checkDigits, 5, 0)
        self.grid.addWidget(self.titleDigits, 5, 1)
        self.grid.addWidget(self.checkSymbols, 6, 0)
        self.grid.addWidget(self.titleSymbols, 6, 1)
        self.grid.addWidget(self.inputSymbols, 6, 2)
        self.grid.addWidget(self.checkMin, 7, 0)
        self.grid.addWidget(self.titleMin, 7, 1)
        self.grid.addWidget(self.inputMin, 7, 2)
        self.grid.addWidget(self.textMin, 7, 3)
        self.grid.addWidget(self.checkMax, 8, 0)
        self.grid.addWidget(self.titleMax, 8, 1)
        self.grid.addWidget(self.inputMax, 8, 2)
        self.grid.addWidget(self.textMax, 8, 3)

        self.grid.addWidget(self.generate, 9, 1, 1, 2)
        self.setLayout(self.grid)

    def generation(self):
        if (not self.checkMin.isChecked() and self.inputMin.text()) or \
                (not self.checkMax.isChecked() and self.inputMax.text()):
            QtGui.QMessageBox.critical(self, 'Ошибка', "Не отмечено, что в пароле есть ограничение на длину")
            return
        if (self.checkMin.isChecked() and not self.inputMin.text()) or \
                (self.checkMax.isChecked() and not self.inputMax.text()):
            QtGui.QMessageBox.critical(self, 'Ошибка', "Не указано значение ограничения на длину пароля")
            return
        if not self.checkSymbols.isChecked() and self.inputSymbols.text():
            QtGui.QMessageBox.critical(self, 'Ошибка', "Не отмечено, что в пароле должны содержаться спец. символы")
            return

        self.myPreciousPassword.withDigits = self.checkDigits.isChecked()
        self.myPreciousPassword.withSymbols = self.checkSymbols.isChecked()
        self.myPreciousPassword.symbolsToUse = self.inputSymbols.text()
        if self.checkMin.isChecked():
            self.myPreciousPassword.min = int(self.inputMin.text())
        else:
            self.myPreciousPassword.min = -1
        if self.checkMax.isChecked():
            self.myPreciousPassword.max = int(self.inputMax.text())
        else:
            self.myPreciousPassword.max = -1

        try:
            cyrillic = self.myPreciousPassword.find_new()
        except PasswordsError as nmpe:
            QtGui.QMessageBox.critical(self, 'Ошибка', str(nmpe))
            self.close()

        self.labelPrompting.setText(cyrillic)
        if self.myPreciousPassword.translit:
            self.myPreciousPassword.translit = str()
        self.myPreciousPassword.translit = transliterate(cyrillic, self.myPreciousPassword.symbolsToUse)
        if self.myPreciousPassword.max > 0:
            self.myPreciousPassword.translit = transliterate(cut_first_letters(self.myPreciousPassword.cyrillic),
                                                             self.myPreciousPassword.symbolsToUse)
        if self.checkUp.isChecked():
            self.myPreciousPassword.up()
        if self.myPreciousPassword.withDigits:
            self.myPreciousPassword.add_digits()
        if self.myPreciousPassword.withSymbols:
            self.myPreciousPassword.add_symbols()
        if not ' ' in self.myPreciousPassword.symbolsToUse:
            self.myPreciousPassword.translit = ''.join(self.myPreciousPassword.translit.split(' '))

        self.labelPassword.setText(str(self.myPreciousPassword))


def main():
    # при старте программы генерируется объект Password, который будет меняться после
    # повторного нажатия на кнопку "Сгенерировать"
    # вытягиваем пословицу, помещая в поле кириллицы
    # транслитеруем, помещаем в поле транслита
    # добавляем заглавные буквы, работаем с преобразованной строкой
    # если есть ограничение на длину, обрезаем кириллический вариант и транслитеруем (добавляем заглавные буквы)
    # если нужны цифры, добавляются, с учётом предыдущего параметра
    # то же с символами
    # при выводе пробелы "съедаются", если их нет в списке допустимых символов

    newPassword = Password()
    app = QtGui.QApplication(sys.argv)
    win = Window(newPassword)
    win.show()
    app.exec()

if __name__ == '__main__':
    main()