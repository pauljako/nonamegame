#!/usr/bin/env python3

import dill
import socket
from threading import Thread
import sys
import pygame

rooms = {}


def threaded_client(connection: socket.socket, username: str, player: pygame.Rect, color, scene, room_code: str):
    global rooms
    if room_code not in rooms:
        print(f"Creating new Room with Code: {room_code}")
        rooms[room_code] = {}
    players = rooms[room_code]
    players[username] = player
    players[username + ".color"] = color
    players[username + ".scene"] = scene
    connection.send(dill.dumps(values.get_values()))
    connection.send(dill.dumps(players))

    while True:
        try:
            data = dill.loads(connection.recv(4096))

            if not data:
                print(f" {username} Disconnected")
                break
            elif data[0] == "color":
                players[username + ".color"] = data[1]
                rooms[room_code] = players
                connection.sendall(dill.dumps(players))
            elif data[0] == "scene":
                players[username + ".scene"] = data[1]
                rooms[room_code] = players
                connection.sendall(dill.dumps(players))
            else:
                players[username] = data
                rooms[room_code] = players
                connection.sendall(dill.dumps(players))
        except:
            print("Error")
            break

    print(f"Lost Connection to: {username}")
    players.pop(username)
    players.pop(username + ".color")
    players.pop(username + ".scene")
    if len(players) == 0:
        print(f"Closing Room {room_code}")
        rooms.pop(room_code)
    else:
        rooms[room_code] = players
    connection.close()


def main(address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((address, port))
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
            room_code = connection_data[5]
            print(f"Connected to: {address} Username: {username}, Color: {color}, Scene: {scene}, Room Code: {room_code}")
            Thread(
                target=threaded_client,
                args=(connection, username, player, color, scene, room_code),
                name=f"NoGameName Server {address}",
                daemon=True
            ).start()
        else:
            print(f"Cannot connect to: {address}")


if __name__ == "__main__":
    import values
    main("127.0.0.1", 25565)
else:
    from server import values
