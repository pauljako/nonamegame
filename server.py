import dill
import socket
from threading import Thread
import sys
import pygame

SERVER = ""
PORT = 25565

players = {}


def threaded_client(connection: socket.socket, username: str, player: pygame.Rect, color, scene):
    global players
    players[username] = player
    players[username + ".color"] = color
    players[username + ".scene"] = scene
    connection.send(dill.dumps(players))
    reply = ""

    while True:
        try:
            data = dill.loads(connection.recv(4096))

            if not data:
                print("Disconnected")
                break
            elif data[0] == "color":
                players[username + ".color"] = data[1]
                connection.sendall(dill.dumps(players))
            elif data[0] == "scene":
                players[username + ".scene"] = data[1]
                connection.sendall(dill.dumps(players))
            else:
                players[username] = data
                connection.sendall(dill.dumps(players))
        except:
            print("Error")
            break

    print(f"Lost Connection to: {username}")
    players.pop(username)
    players.pop(username + ".color")
    players.pop(username + ".scene")
    connection.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((SERVER, PORT))
    except socket.error as error:
        print(f"Error {error}")

    s.listen(2)
    print("Waiting for Connection")

    while True:
        connection, address = s.accept()
        try:
            connection_data = dill.loads(connection.recv(4096))
        except dill.UnpicklingError:
            print(f"Failed Connection to: {address}")
            connection_data = ["error"]
        if connection_data[0] == "game":
            username = connection_data[1]
            player = connection_data[2]
            color = connection_data[3]
            scene = connection_data[4]
            print(f"Connected to: {address} Username: {username} Color: {color}")
            Thread(target=threaded_client, args=(connection, username, player, color, scene)).start()
        else:
            print(f"Cannot connect to: {address}")


if __name__ == "__main__":
    main()
