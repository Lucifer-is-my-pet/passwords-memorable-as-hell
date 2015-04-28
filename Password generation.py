from unittest import TestCase
from PasswordGeneration import Password
import re

__author__ = 'пк'


class TestPassword(TestCase):
    def test_find_new(self):
        newPassword = Password()
        cyr = newPassword.find_new()
        p = re.compile('[а-яА-я -:,]')
        self.assertEqual(len(p.findall(cyr)), len(cyr))
        # print(cyr)

    def test_cut(self):
        newPassword = Password()

    def test_transform(self):
        newPassword = Password()
        cyr = newPassword.find_new()
        tr = newPassword.transform(cyr)
        # print(tr)
        p = re.compile('[^а-яА-я]')
        self.assertEqual(len(p.findall(tr)), len(tr))

    def test_number_of_spaces(self):
        newPassword = Password()
        newPassword.transform("Кабы я была царица")
        self.assertEqual(newPassword.number_of_spaces(), 3)

    def test_add_digits(self):
        pass

    def test_up(self):
        newPassword = Password()

    def test_add_symbols(self):
        newPassword = Password()

    def test_clear(self):
        newPassword = Password()
        cyr = newPassword.find_new()
        newPassword.transform(cyr)
        newPassword.length = 20
        newPassword.withDigits = True
        newPassword.withSymbols = True
        newPassword.symbolsToUse = [',', '!', '@', '#', '$']
        newPassword.clear()
        self.assertEqual(newPassword.cyrillic, '')
        self.assertEqual(newPassword.translit, '')
        self.assertEqual(newPassword.length, 0)
        self.assertEqual(newPassword.withSymbols, False)
        self.assertEqual(newPassword.withDigits, False)
        self.assertEqual(newPassword.symbolsToUse, [])
        self.assertEqual(newPassword.thatOneLine, -1)