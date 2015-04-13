__author__ = 'Гуральник'
import random
import re


def read_file(fname):  # выкачиваем один раз в main и обращаемся уже к массиву
        with open(fname, 'r', encoding="cp1251") as fl:
            return fl.readlines()


class Password:
    dictionary = {' ': ' ', '-': '-', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
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

    def find_new(self):  # заполни-метод
        """
        получает в генераторе случайных чисел номер строки и извлекает соответсвующую строку из файла, помещая в
        поле cyrillic и возвращает её
        номера, полученные в предыдущих попытках, фиксируются, чтобы не было повторов
        """
        for i in range(self.numOfLines):
            num = random.randint(0, self.numOfLines)
            if num not in self.usedNumbers:
                self.thatOneLine = num
                self.cyrillic = self.proverbs[num]
                self.usedNumbers.append(num)
                return self.cyrillic

    def cut(self):  # преобразуй-метод
        """
        вырезает первые буквы слов (из кириллического варианта), возвращает список
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
        создаёт транслитерованный вариант, помещает его в поле translit, если там пусто, возвращает строку
        :string - str, list
        """
        result = str()
        for letter in string:
            result += self.dictionary[letter]
        if not len(self.translit):
            self.translit = result
        return result

    def number_of_spaces(self):
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
        ЕСЛИ ЧИСЛО СТРОК ФАЙЛА С ПОСЛОВИЦАМИ ПЕРЕВАЛИТ ЗА ТЫСЯЧУ - ПРИДЁТСЯ ПЕРЕДЕЛЫВАТЬ. ТОВАРИЩ, БУДЬ БДИТЕЛЕН
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
            result += str(amazingNumber // 10) + self.transform(self.cut())
            num = self.length // 2 + round(random.random())
            result = result[0:num] + str(amazingNumber % 10) + result[num:]

        return result

    def upper(self):  # преобразуй-метод
        """
        работает с транслитерованным вариантом, возвращает строку
        пока вариант для полной пословицы!
        """
        temp = self.translit.split(' ')
        for i in range(len(temp)):
            temp[i] = temp[i][:len(temp[i]) - 1] + temp[i][-1].upper()
        result = ' '.join(temp)
        return result

    def add_symbols(self, string, num):  # преобразуй-метод
        """
        могут быть: 1. скобки, 2. точки-зпт-воскл, 3. астериск, слэши, двоеточие, доллар, процент, кавычки
        :num - int, номер группы, если пользователь выбрал, а не указал конкретные. 0 - не указал
        :string - строка, с которой работаем
        ПРОВЕРЯТЬ ПОЛНУЮ ПОСЛОВИЦУ НА НАЛИЧИЕ СИМВОЛОВ И СООТВЕТСТВИЕ ИХ ДОПУСТИМОМУ НАБОРУ
        ВОЗМОЖНО, ДОБАВЛЯТЬ НУЖНО БУДЕТ МЕНЬШЕЮ ИЛИ ПРИДЁТСЯ ЧТО-ТО УДАЛИТЬ
        """
        result = str()
        if num == 0:
            pass  # работаем с заданным набором
        elif num == 1:
            brackets = ["()", "[]", "{}"]
            typeOfBrackets = random.randint(1, 3)
            result = brackets[typeOfBrackets][0] + string + brackets[typeOfBrackets][1]
        elif num == 2:
            punctuation = ['.', '!', "...", '?']
            typeOfPunctuation = random.randint(1, 4)
            result = string + punctuation[typeOfPunctuation]
        elif num == 3:
            symbols = ['*', '/', '\\', '+', '"', '$', '%', '-']
            typeOfSymbol = random.randint(1, 8)
            result = symbols[typeOfSymbol] + string + symbols[typeOfSymbol]

        return result


def main():
    # при старте программы генерируется объект Password, который будет меняться по ходу изменения параметров и/или
    # повторного нажатия на кнопку "Сгенерировать"
    # вытягиваем пословицу, помещая в поле кириллицы
    # транслитеруем, помещаем в поле транслита
    # добавляем заглавные буквы, работаем с преобразованной строкой
    # если есть ограничение на длину, обрезаем кириллический вариант и транслитеруем
    # если нужны цифры, добавляются, с учётом предыдущего параметра
    # то же с символами
    pass


if __name__ == '__main__':
    main()