from unittest import TestCase
import util
from unittest.mock import patch

class Test_readVarInt(TestCase):
    @patch("util._readByte")
    def test_x00(self, _readByte_patch):
        _readByte_patch.return_value = b'\x00'
        self.assertEqual(util.readVarInt(""), 0)

    @patch("util._readByte")
    def test_x01(self, _readByte_patch):
        _readByte_patch.return_value = b'\x01'
        self.assertEqual(util.readVarInt(""), 1)

    @patch("util._readByte")
    def test_x02(self, _readByte_patch):
        _readByte_patch.return_value = b'\x02'
        self.assertEqual(util.readVarInt(""), 2)

    @patch("util._readByte")
    def test_x7f(self, _readByte_patch):
        _readByte_patch.return_value = b'\x7f'
        self.assertEqual(util.readVarInt(""), 127)

    @patch("util._readByte")
    def test_x80x01(self, _readByte_patch):
        _readByte_patch.side_effect = [b'\x80', b'\x01']
        self.assertEqual(util.readVarInt(""), 128)

    @patch("util._readByte")
    def test_xffx01(self, _readByte_patch):
        _readByte_patch.side_effect = [b'\xff', b'\x01']
        self.assertEqual(util.readVarInt(""), 255)

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
    def test_129(self):
        self.assertEqual(util.writeVarInt(129), b'\x81\x01')
    def test_256(self):
        self.assertEqual(util.writeVarInt(256), b'\x80\x02')
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

