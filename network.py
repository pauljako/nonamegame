import dill
import socket
import pygame


class Network:
    def __init__(self, username: str, player: pygame.Rect, color, scene: int = 0):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "node2.craftsblock.eu"
        self.server = "127.0.0.1"
        self.port = 25565
        self.buffersize = 4096
        self.address = (self.server, self.port)
        self.username = username
        self.player = player
        self.color = color
        self.scene = scene

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.send(["game", self.username, self.player, self.color, self.scene])
        except:
            print("Connection Error")
            return ""

    def send(self, data):
        try:
            self.client.send(dill.dumps(data))
            return dill.loads(self.client.recv(self.buffersize))
        except socket.error as error:
            print(f"Error: {error}")
            return ""
