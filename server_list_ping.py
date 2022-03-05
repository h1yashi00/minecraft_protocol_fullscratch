import util
import socket
import time
import json

class ServerData():
    def __init__(self, server_list):
        decoded_json  = json.loads(server_list)
        self._version = decoded_json['version']['name']
        self._online_players = decoded_json['players']['online']
        self._max_players = decoded_json['players']['max']

        try :
            self._favicon = decoded_json['favicon']
        except KeyError as error:
            self._favicon = "default"

        try :
            self._name    = decoded_json['description']['text']
        except TypeError as error:
            self._name    = decoded_json['description']

    def name(self):
        return self._name
    def online_players(self):
        return self._online_players
    def max_players(self):
        return self._max_players
    def version(self):
        return self._version
    def favicon(self):
        return self._favicon

class ServerListPing:
    def __init__(self, hostname='localhost', port=25565):
        self._hostname = hostname
        self._port     = port

    def _pong(self, connection):
        pass

    def _ping(self, connection):
        packet_id = b'\x01'
        millionseconds = util.writeFloat(time.time()*1000)
        data = packet_id + millionseconds
        util.sendData(connection, data)

    def _response(self, connection):
        packet_length = util.readVarInt(connection)
        packet_id     = util.readVarInt(connection)
        if packet_id != 0:
            Exception('fatal error occured packet id is not 0')
        string_length = util.readVarInt(connection)
        json_server = b''
        while True:
            json_server += connection.recv(1024)
            if len(json_server) >= string_length:
                break

        return ServerData(json_server)

    def _request(self, connection):
        util.sendData(connection, b'\x00')

    def _handshake(self, connection):
        data = b''
        data += util.writeVarInt(0) # packet ID
        data += util.writeVarInt(757) # version already writeVarInt()
        data += util.writeString(self._hostname) # hostname
        data += util.writeUnsignedShort(self._port) # port
        data += util.writeVarInt(1)                 # status
        util.sendData(connection, data)

    def get_list(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((self._hostname, self._port))
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._handshake(connection)
        self._request(connection)
        server = self._response(connection)
        self._ping(connection)
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()

        return server
