import util
import socket
import time

class Login:
    def __init__(self, hostname='localhost', port=25565):
        self._hostname = hostname
        self._port = port

    def _keepAlive(self, connection):
        while True:
            connection.recv(1024)

    def _joinGamePacket(self, connection):
        packet_length = util.readVarInt(connection)
        data          = util.readVarInt(connection)
        print(packet_length)
        print(data)

    def _loginSuccess(self, connection):
        packet_length = util.readVarInt(connection)
        divade        = util.readVarInt(connection)
        packet_id     = util.readVarInt(connection)
        uuid          = connection.recv(16)
        name_length   = util.readVarInt(connection)
        name          = connection.recv(name_length).decode('utf-8')
        print('packet length %s' % packet_length)
        print('packet ID %s' % packet_id)
        print('uuid %s' % uuid)
        print('name_length %s' % name_length)
        print('name %s' % name)

    def _setCompression(self, connection):
        packet_length = util.readVarInt(connection)
        packet_id     = util.readVarInt(connection)
        maximum_size_packet = util.readVarInt(connection)
        print('packet length %s' % packet_length)
        print('packet ID %s' % packet_id)
        print('maximum_size_packet %s' % maximum_size_packet)

    def _encryptionResponse(self, connection):
        packet_lenght = util.readVarInt(connection)
        packet_id     = util.readVarInt(connection)
        server_id_length = util.readVarInt(connection)
        public_key_length = util.readVarInt(connection)
        print('packet_length %s' % packet_lenght)
        print('packet_id %s' % packet_id)
        print('server_id_length %s' % server_id_length)
        print(public_key_length)
        public_key = connection.recv(public_key_length)
        print(public_key)
        print(public_key[0])
        verify_token_length = util.readVarInt(connection)
        print(verify_token_length)
        verify_token        = connection.recv(verify_token_length)
        print(verify_token)

    def _loginStart(self, connection):
        data = b''
        data += util.writeVarInt(0)
        data += util.writeString('Narikak')
        util.sendData(connection, data)

    def _handshake(self, connection):
        data = b''
        data += util.writeVarInt(0) # packet ID
        data += util.writeVarInt(757) # version
        data += util.writeString(self._hostname) # hostname
        data += util.writeUnsignedShort(self._port)   # port
        data += util.writeVarInt(2)              # login
        util.sendData(connection, data)

    def go(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((self._hostname, self._port))
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._handshake(connection)
        self._loginStart(connection)
        self._setCompression(connection)
        self._loginSuccess(connection)
        self._joinGamePacket(connection)
        self._keepAlive(connection)
        connection.close()
