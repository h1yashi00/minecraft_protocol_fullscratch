#! /bin/python3
import struct

def sendData(connection, data):
    connection.send(writeVarInt(len(data)) + data)

def readVarInt(sock):
    value = 0
    length = 0
    currentByte = b''
    while True:
        currentByte = int.from_bytes(sock.recv(1), 'big')
        value |= (currentByte & 0x7F) << (length * 7)

        length += 1
        if length > 5:
            Exception("VarInt is too big")
        if (currentByte & 0x80) != 0x80:
            break
    return value

def writeVarInt(value):
    if value < 0:
        raise Exception("value is too small")
    data = b''
    while True:
        if ((value & ~0x7F) == 0):
            data += struct.pack('B', value)
            return data
        data += struct.pack('B', ((value & 0x7f) | 0x80))
        value >>= 7

def writeFloat(data):
    return struct.pack('L', int(data))

def writeString(text):
    encoded_text = text.encode('ASCII')
    return writeVarInt(len(encoded_text)) + encoded_text

def writeUnsignedShort(value):
    if (0 > value and value < 65535):
        raise Exception("value is out of range!")
    return struct.pack('>H', value)
