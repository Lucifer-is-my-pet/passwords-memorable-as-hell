__author__ = 'Гуральник'
import random
import re


def read_file(fname):  # выкачиваем один раз в main и обращаемся уже к массиву
        with open(fname, 'r', encoding="utf-8") as fl:
            return fl.readlines()


class Password:
    dictionary = {' ': ' ', '-': '-', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
                  'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
                  'щ': 'shch', 'ъ': "'", 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya', ',': ',', ':': ':',
                  '(': '(', ')': ')'}

    def __init__(self):
        self.cyrillic = str()
        self.translit = str()
        self.length = 0  # требуемая длина пароля
        self.withDigits = False
        self.withSymbols = False
        self.symbolsToUse = []
        self.proverbs = read_file("proverbs.txt")
        self.numOfLines = len(self.proverbs)
        self.thatOneLine = -1  # номер строки, откуда получили пословицу
        self.usedNumbers = set()

    def find_new(self):  # заполни-метод
        """
        получает в генераторе случайных чисел номер строки и извлекает соответсвующую строку из файла, помещая в
        поле cyrillic
        номера, полученные в предыдущих попытках, фиксируются, чтобы не было повторов
        :return: str
        """
        for i in range(self.numOfLines):
            num = random.randint(0, self.numOfLines)
            if num not in self.usedNumbers:
                self.thatOneLine = num
                self.cyrillic = self.proverbs[num]
                self.usedNumbers.add(num)
                return self.cyrillic

    def cut(self):  # преобразуй-метод
        """
        вырезает первые буквы слов из кириллического варианта
        :return: list
        """
        splitted = self.cyrillic.split(' ')
        p = re.compile("[,;\-:]")
        fixed = list()
        for i in splitted:
            if p.search(i) is None:
                fixed.append(i)
            elif not p.match(i):
                fixed.append(i[:p.search(i).start()])

        cutted = list()
        for i in fixed:
            cutted.append(i[0])
        return cutted

    def transform(self, string):  # преобразуй-заполни-метод
        """
        создаёт транслитерованный вариант, помещает его в поле translit, если там пусто
        :string: str, list
        :return: str
        """
        result = str()
        for letter in string:
            if letter == '\n':
                break
            result += self.dictionary[letter.lower()]
        if not len(self.translit):
            self.translit = result
        return result

    def number_of_spaces(self):
        """
        :return: int
        """
        result = 0
        for i in self.translit:
            if i == ' ':
                result += 1
        return result

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
        if amazingNumber <= 10:
            amazingNumber *= self.number_of_spaces()
        elif amazingNumber > 100:
            amazingNumber //= self.number_of_spaces()
            if amazingNumber > 100:
                amazingNumber //= self.number_of_spaces()
        if len(str(amazingNumber)) != 2:
            raise BaseException("There are no 2 digits to insert!")
        if self.length == 0:  # если органичения нет
            result += str(amazingNumber // 10) + self.translit
            for i in range(len(result)):
                if result[i] == ' ' and i >= len(result) // 2:
                    result = result[:i] + str(amazingNumber % 10) + result[i + 1:]
                    break
        else:
            result += str(amazingNumber // 10) + self.translit
            num = self.length // 2 + round(random.random())
            result = result[0:num] + str(amazingNumber % 10) + result[num:]

        return result

    def up(self):  # TODO преобразуй-метод КОСЯЧИТ, ЕСЛИ ЕСТЬ СИМВОЛЫ В КОНЦЕ СЛОВА
        """
        работает с транслитерованным вариантом
        в полном варианте увеличивает последнюю букву каждого слова
        в обрезанном - первую, последнюю и примерно в середине
        :return: str
        """
        if self.length == 0:
            temp = self.translit.split(' ')
            for i in range(len(temp)):
                temp[i] = temp[i][:len(temp[i]) - 1] + temp[i][-1].upper()
            result = ' '.join(temp)
        else:
            result = self.translit[0].upper() + self.translit[1:-1] + self.translit[-1].upper()
            result = result[:len(result) // 2] + result[len(result) // 2].upper() + result[(len(result) // 2) + 1:]

        return result

    def add_symbols(self, string, num):  # TODO преобразуй-метод
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
        self.length = 0
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

    newPassword = Password()
    cyrillic = newPassword.find_new()  # "Сгенерировать"
    translit = newPassword.transform(cyrillic)
    if newPassword.length != 0:
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
            for i in found:
                splitted = translit.split(i)
                translit = ''.join(splitted)
    print(cyrillic)
    print(translit)
    print(uppered)
    print(withDigits)


if __name__ == '__main__':
    main()