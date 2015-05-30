__author__ = 'Гуральник'
import random
import re


def read_file(fname):  # выкачиваем один раз в main и обращаемся уже к массиву
    with open(fname, 'r', encoding="utf-8") as fl:
        return fl.readlines()


def number_of_words(string):
    splitted = string.split(' ')
    while splitted.find('-') > 0:
        splitted.remove('-')
    return len(splitted)


class Password:
    dictionary = {' ': ' ', '-': '-', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
                  'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
                  'щ': 'shch', 'ъ': "'", 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya', ',': ',', ':': ':',
                  '(': '(', ')': ')', '?': '?'}

    def __init__(self):
        self.cyrillic = str()
        self.translit = str()
        self.min = -1
        self.max = -1
        self.withDigits = False
        self.withSymbols = False
        self.symbolsToUse = []
        self.proverbs = read_file("proverbs.txt")
        self.numOfLines = len(self.proverbs)
        self.thatOneLine = -1  # номер строки, откуда получили пословицу
        self.usedNumbers = set()

    def __len__(self):
        return len(self.translit)

    def find_new(self):  # заполни-метод
        """
        получает в генераторе случайных чисел номер строки и извлекает соответсвующую строку из файла, помещая в
        поле cyrillic
        номера, полученные в предыдущих попытках, фиксируются, чтобы не было повторов
        прежде чем добавить пословицу, метод проверяет, соответствует ли она ограничениям
        :return: str
        """
        if len(self.usedNumbers) == self.numOfLines:
            raise BaseException("Все попытки получить пароль исчерпаны! Вы король кликанья!")
        for i in range(self.numOfLines):
            num = round(random.uniform(0, self.numOfLines))
            if num not in self.usedNumbers:
                temp = self.proverbs[num]
                ind = temp.find('\n')
                if ind > 0:
                    temp = temp[:ind]
                if (self.max != -1) and (number_of_words(temp) > self.max) and (not self.withDigits) and (not self.withSymbols):
                    continue
                elif (self.max != -1) and ((number_of_words(temp) + 4) > self.max) and self.withDigits and self.withSymbols:
                    continue
                elif (self.max != -1) and ((number_of_words(temp) + 2) > self.max) and (self.withDigits or self.withSymbols):
                    continue
                if (self.min != -1) and (number_of_words(temp) < self.max) and (not self.withDigits) and (not self.withSymbols):
                    continue
                elif (self.min != -1) and ((number_of_words(temp) - 4) < self.max) and self.withDigits and self.withSymbols:
                    continue
                elif (self.min != -1) and ((number_of_words(temp) - 2) < self.max) and (self.withDigits or self.withSymbols):
                    continue
                self.cyrillic = temp
                self.usedNumbers.add(num)
                self.thatOneLine = num + 1
                return self.cyrillic

    def cut(self):  # преобразуй-метод
        """
        вырезает первые буквы слов из кириллического варианта
        :return: list
        """
        p = re.compile('\W+')
        splitted = p.split(self.cyrillic)
        # print(self.cyrillic, splitted)

        cutted = list()
        for i in splitted:
            cutted.append(i[0])
        return cutted

    def transform(self, string):  # преобразуй-заполни-метод
        """
        создаёт транслитерованный вариант, помещает его в поле translit, если там пусто
        :string: str, list
        :return: str
        """
        temp = str()
        for letter in string:
            if letter == '\n':
                break
            temp += self.dictionary[letter.lower()]
        if not len(self):
            self.translit = temp

        result = str()
        for i in temp:
            if i in self.symbolsToUse or i.isalpha() or i == ' ':
                result += i
        return result

    def number_of_spaces(self):
        """
        :return: int
        """
        p = re.compile('[ ]')
        result = len(p.findall(self.translit))
        return result

    def last_match(self, string):
        """
        возвращает индекс последнего вхождения букв в строке
        :param string: слово пословицы
        :return: int
        """
        p = re.compile("[a-zA-Z]")
        return [m.start() for m in p.finditer(string)][-1]

    def add_digits(self):  # преобразуй-метод
        """
        работает с транслитeрованным вариантом, добавляет цифры
        если нет ограничения на длину, вставляет в начало и примерно в середину вместо какого-то из пробелов,
        если есть - в начало и примерно в середину
        две цифры получаем из манипуляций с номером строки, откуда была вытянута пословица и числом пробелов
        (если число строк файла с пословицами перевалит за тысячу - придётся переделывать)
        :return: str
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
                amazingNumber //= spaces
                if count > 5:
                    raise BaseException("Я зациклился. Номер сейчас:" + str(amazingNumber) + "пробелов:" + str(spaces))
        if self.max == -1:  # если органичения нет
            result += str(amazingNumber // 10) + self.translit
            for i in range(len(result)):
                if result[i] == ' ' and i >= len(result) // 2:
                    result = result[:i] + str(amazingNumber % 10) + result[i + 1:]
                    break
        else:
            result += str(amazingNumber // 10) + self.translit
            num = len(self) // 2 + round(random.random())
            result = result[0:num] + str(amazingNumber % 10) + result[num:]

        return result

    def up(self):  # преобразуй-метод
        """
        работает с транслитерованным вариантом
        в полном варианте увеличивает последнюю букву каждого слова
        в обрезанном - первую, последнюю и примерно в середине
        :return: str
        """
        if self.max == -1:
            splitted = self.translit.split(' ')
            temp = list()
            p = re.compile('[a-zA-Z]')
            for i in range(len(splitted)):
                if p.search(splitted[i]):  # попалось не тире
                    ind = self.last_match(splitted[i])
                    # if ind == 0 or len(splitted[i]) == 1:
                    #     print("Одно слово!", splitted[i][:ind] + splitted[i][ind].upper())
                    temp.append(splitted[i][:ind] + splitted[i][ind].upper())
                    if ind != len(splitted[i]) - 1:  # в конце слова есть другие символы
                        temp[i] += splitted[i][ind + 1:]
                else:
                    temp.append(splitted[i])
            result = ' '.join(temp)
        else:
            result = self.translit[0].upper() + self.translit[1:-1] + self.translit[-1].upper()
            result = result[:len(result) // 2] + result[len(result) // 2].upper() + result[(len(result) // 2) + 1:]

        return result

    def add_symbols(self, string, num):  # преобразуй-метод TODO
        """
        :num: int, номер группы, если пользователь выбрал из предложенных, а не указал конкретные. 0 - не указал
        (проверять полную пословицу на наличие символов и соответствие их допустимому набору
        возможно, добавлять нужно будет меньше или придётся что-то удалить)
        :string: str, строка, с которой работаем
        :return: str
        """
        pass

    def clear(self):
        """
        сбрасывает часть настроек после повторного нажатия "Сгенерировать"
        :return: None
        """
        self.cyrillic = str()
        self.translit = str()
        self.min = -1
        self.max = -1
        self.withDigits = False
        self.withSymbols = False
        self.symbolsToUse = []
        self.thatOneLine = -1


def main():
    # при старте программы генерируется объект Password, который будет меняться после ходу изменения параметров и/или
    # повторного нажатия на кнопку "Сгенерировать"
    # вытягиваем пословицу, помещая в поле кириллицы
    # транслитеруем, помещаем в поле транслита
    # добавляем заглавные буквы, работаем с преобразованной строкой
    # если есть ограничение на длину, обрезаем кириллический вариант и транслитеруем (добавляем заглавные буквы)
    # если нужны цифры, добавляются, с учётом предыдущего параметра
    # то же с символами
    # при выводе пробелы "съедаются", впароле их быть не должно

    newPassword = Password()
    cyrillic = newPassword.find_new()  # "Сгенерировать"
    translit = newPassword.transform(cyrillic)
    if len(newPassword) != 0:
        translit = newPassword.transform(newPassword.cut())  # поле translit обновилось
        uppered = newPassword.up()
    uppered = newPassword.up()
    withDig = input("С циферками? ")
    if withDig == "да":
        newPassword.withDigits = True
    if newPassword.withDigits:
        withDigits = newPassword.add_digits()
    if newPassword.withSymbols:
        pass
    else:  # избавляемся от символов
        splitted = translit.split(' ')
        translit = ''.join(splitted)
        p = re.compile("[^A-Za-z0-9]")
        if len(p.findall(translit)):
            found = set(p.findall(translit))
            # print("i found", found)
            for i in found:
                splitted = translit.split(i)
                translit = ''.join(splitted)

    print(cyrillic)
    print(translit)
    spl = uppered.split(' ')
    print(''.join(spl))
    if withDig == "да":
        spl = withDigits.split(' ')
        print(''.join(spl))


if __name__ == '__main__':
    main()