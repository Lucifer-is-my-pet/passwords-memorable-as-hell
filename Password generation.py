__author__ = 'Гуральник'
import random
import re


def read_file(fname):  # выкачиваем один раз в main и обращаемся уже к массиву
        with open(fname, 'r', encoding="cp1251") as fl:
            return fl.readlines()


class Password:
    dictionary = {' ': ' ', '—': '—', '-': '-', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
                  'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
                  'щ': 'shch', 'ъ': "'", 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya', ',': ','}

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

    def find_new(self):
        """
        получает в генераторе случайных чисел номер строки и извлекает соответсвующую строку из файла, помещая в
        поле cyrillic
        номера, полученные в предыдущих попытках, фиксируются, чтобы не было повторов
        """
        for i in range(self.numOfLines):
            num = random.randint(0, self.numOfLines)
            if num not in self.usedNumbers:
                self.thatOneLine = num
                self.cyrillic = self.proverbs[num]
                self.usedNumbers.append(num)
                return self.cyrillic

    def cut(self):
        """
        вырезает первые буквы слов (из кириллического варианта)
        """
        splitted = self.cyrillic.split(' ')
        p = re.compile("[,;\-:]")
        for i in range(len(splitted)):
            if p.match(splitted[i]):
                splitted.pop(i)
        cutted = list()
        for i in splitted:
            cutted.append(i[0])
            if self.withSymbols and cutted[len(cutted) - 1] != ' ':  # если понадобится заполнять спецсимволами
                cutted.append(' ')
        return cutted

    def transform(self, string):
        """
        преобазует кириллицу в латиницу
        """
        result = str()
        for letter in string:
            result += self.dictionary[letter]

    def number_of_spaces(self):
        result = 0
        for i in self.translit:
            if i == ' ':
                result += 1
        return result

    def add_digits(self):
        """
        работает с транслитeрованным вариантом, добавляет цифры
        если нет ограничения на длину, вставляет в начало и примерно в середину вместо какого-то из пробелов,
        если есть - в начало и примерно в середину
        две цифры получаем из манипуляций с номером строки, откуда была вытянута пословица и числом пробелов
        ЕСЛИ ЧИСЛО СТРОК ПЕРЕВАЛИТ ЗА ТЫСЯЧУ - ПРИДЁТСЯ ПЕРЕДЕЛЫВАТЬ. ТОВАРИЩ, БУДЬ БДИТЕЛЕН
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
            raise BaseException("There are not 2 numbers to insert!")
        if self.length > 0:
            result += str(amazingNumber // 10) + self.translit
            for i in range(len(result)):
                if result[i] == ' ' and i >= len(result) // 2:
                    result[i] = str(amazingNumber % 10)
                    break
        else:
            result += str(amazingNumber // 10) + self.cut()
            num = self.length // 2 + round(random.random())
            result = result[0:num] + str(amazingNumber % 10) + result[num:]

        return result


def main():
    # при старте программы генерируется объект Password, который будет меняться по ходу изменения параметров и/или
    # повторного нажатия на кнопку "Сгенерировать"
    pass


if __name__ == '__main__':
    main()