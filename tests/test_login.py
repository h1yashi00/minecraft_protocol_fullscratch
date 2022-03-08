import unittest
from login import Login

class TestLogin(unittest.TestCase):
    def test_login(self):
        login = Login()
        login.go()
