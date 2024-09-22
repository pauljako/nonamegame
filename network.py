import dill
import socket
import pygame
import errno


class Network:
    def __init__(self, username: str, player: pygame.Rect, color, room_code: str, scene: int, address: str, port: int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "node2.craftsblock.eu"
        self.server = address
        self.port = port
        self.buffersize = 4096
        self.address = (self.server, self.port)
        self.username = username
        self.player = player
        self.color = color
        self.scene = scene
        self.room_code = room_code

    def connect(self):
        try:
            self.client.connect(self.address)
            new_values = self.send(["game", self.username, self.player, self.color, self.scene, self.room_code])
            new_players = dill.loads(self.client.recv(self.buffersize))
            return new_values, new_players
        except:
            print("Connection Error")
            return None, None

    def send(self, data):
        try:
            self.client.send(dill.dumps(data))
            return dill.loads(self.client.recv(self.buffersize))
        except socket.error as error:
            print(f"Error: {error}")
            return ""


def check_port(port) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            return False
        else:
            print(e)
            return False
    s.close()
    return True
