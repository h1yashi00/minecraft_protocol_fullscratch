import unittest
from server_list_ping import ServerListPing

class Test_ServerListPing(unittest.TestCase):
    def test_Notchain(self):
        s = ServerListPing()
        server = s.get_list()
        self.assertEqual(server.name(), "A Minecraft Server")
        self.assertEqual(server.version(), "1.18.1")
        self.assertEqual(server.online_players(), 0)
        self.assertEqual(server.max_players(), 20)
        self.assertEqual(server.favicon(), 'default')

    def test_hypixel(self):
        s = ServerListPing('mc.hypixel.net')
        server = s.get_list()

    def test_shotbow(self):
        s = ServerListPing('us.shotbow.net')
        server = s.get_list()
