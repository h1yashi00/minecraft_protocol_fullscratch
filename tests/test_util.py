from unittest import TestCase
import util

class Test_readVarInt(TestCase):
    pass
    # def test_x00(self):
    #     self.assertEqual(util.readVarInt(b'\x00'), 0)
    # def test_x01(self):
    #     self.assertEqual(util.readVarInt(b'\x01'), 1)
    # def test_x02(self):
    #     self.assertEqual(util.readVarInt(b'\x02'), 2)
    # def test_x7f(self):
    #     self.assertEqual(util.readVarInt(b'\x7f'), 127)
    # def test_x80x01(self):
    #     self.assertEqual(util.readVarInt(b'\x80\x01'), 128)
    # def test_xffx01(self):
    #     self.assertEqual(util.readVarInt(b'\xff\x01'), 255)

class Test_writeVarInt(TestCase):

    def test_0(self):
        self.assertEqual(util.writeVarInt(0), b'\x00')
    def test_1(self):
        self.assertEqual(util.writeVarInt(1), b'\x01')
    def test_2(self):
        self.assertEqual(util.writeVarInt(2), b'\x02')
    def test_127(self):
        self.assertEqual(util.writeVarInt(127), b'\x7f')
    def test_128(self):
        self.assertEqual(util.writeVarInt(128), b'\x80\x01')
    def test_2147483647(self):
        self.assertEqual(util.writeVarInt(2147483647), b'\xff\xff\xff\xff\x07')

class Test_writeString(TestCase):
    def test_localhost(self):
        packed_length = util.writeVarInt(len('localhost'))
        self.assertEqual(util.writeString('localhost'), packed_length + b'localhost')

class Test_writeUnsignedShort(TestCase):
    def test_0(self):
        self.assertEqual(util.writeUnsignedShort(0), b'\x00\x00')
    def test_25565(self):
        self.assertEqual(util.writeUnsignedShort(25565), b'\x63\xdd')
    def test_65535(self):
        self.assertEqual(util.writeUnsignedShort(65535), b'\xff\xff')
    def test_65536(self):
        self.assertRaises(Exception, util.writeUnsignedShort, 65536)

