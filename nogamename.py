import json
import os.path
import random
import sys
import threading
import time

try:
    import pygame
except ModuleNotFoundError:
    print("It looks like pygame is not installed")
try:
    from network import Network
    from network import check_port
    from draw import draw
    import ega
    from server import values
except ModuleNotFoundError as e:
    print(e)
    print("Required Files not Found. Exiting")
    sys.exit()

initialized: bool = False
WINDOW: pygame.Surface
GAME_NAME: str
MAX_FPS: int
FONT: pygame.font.Font
USERNAME: str
ASSETS: dict
INIT_COLOR: str
ROOM_CODE: str


def init(width: int, height: int, max_fps: int, username: str, color: str, room: str):
    global ROOM_CODE, FONT, MAX_FPS, WINDOW, ASSETS, INIT_COLOR, USERNAME, initialized
    title = f"NoGameName ({username})"
    print(f"Welcome to {title}")
    print(f"Initializing Game...")
    pygame.quit()
    pygame.init()
    pygame.font.quit()
    pygame.font.init()
    ROOM_CODE = room
    MAX_FPS = max_fps
    FONT = pygame.font.Font("assets/fonts/SupremeSpike.otf", 12)
    WINDOW = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption(title)
    ASSETS = {
        "ground": pygame.image.load(os.path.join("assets", "textures", "tiles", "ground.png")),
        "player": pygame.image.load(os.path.join("assets", "textures", "entities", "player.png")),
        "dirt": pygame.image.load(os.path.join("assets", "textures", "tiles", "ground2.png"))
    }
    pygame.display.set_icon(ASSETS["ground"])
    loading_txt = FONT.render("Loading...", 1, "white")
    WINDOW.blit(loading_txt, ((WINDOW.get_width() / 2) - (loading_txt.get_width() / 2), (WINDOW.get_height() / 2) - (loading_txt.get_height() / 2)))
    pygame.display.update()
    INIT_COLOR = color
    USERNAME = username
    pygame.display.update()
    print("Game Initialized")
    initialized = True


def main():
    global WINDOW
    color = INIT_COLOR
    scene = 1
    player = pygame.Rect(load_player_entry(scene), (values.PLAYER_WIDTH, values.PLAYER_HEIGHT))
    net = Network(username=USERNAME, player=player, color=color, room_code=ROOM_CODE, scene=scene, address="127.0.0.1", port=5467)
    new_values, players = net.connect()
    if players is None:
        print("Connection Error. Game will launch offline")
        offline = True
    elif players[USERNAME] != player:
        print("Error while verifying. Game will launch offline")
        offline = True
    else:
        offline = False

    if not offline:
        values.set_values(new_values)
        WINDOW = pygame.display.set_mode((WINDOW.get_width(), WINDOW.get_height()), pygame.RESIZABLE)
    else:
        try:
            from server import server as gameserver
        except ModuleNotFoundError as e:
            print(e)
            print("Failed to launch in offline mode. Exiting")
            sys.exit()
        while True:
            offline_port = random.randint(2500, 5500)
            if check_port(offline_port):
                break
        server_thread = threading.Thread(
            name="NoGameName Server",
            target=gameserver.main,
            args=("127.0.0.1", offline_port),
            daemon=True
        )
        print(f"Starting Integrated Server on Port {offline_port}")
        server_thread.start()
        net = Network(username=USERNAME, player=player, color=color, room_code=ROOM_CODE, scene=scene,
                      address="127.0.0.1", port=offline_port)
        new_values, players = net.connect()
        if players is None:
            print("Connection Error. Exiting")
            sys.exit()
        elif players[USERNAME] != player:
            print("Error while verifying. Exiting")
            sys.exit()
    try:
        ega_connection = ega.Connection(True)
    except ConnectionRefusedError:
        print("Connection to EGA failed. Game will launch without it.")
        ega_connection = None
    loop(offline, player, color, scene, net, ega_connection)
    print("Bye!")
    net.client.close()
    pygame.quit()


def load_scene(scene_number: int, item: str) -> list:
    file = os.path.join("assets", "scenes", f"{scene_number}.json")
    with open(file, "rb") as f:
        data: list = json.load(f)
    scene_height = len(data) - 1
    return_value = []
    current_row = 0
    for row in data:
        current_tile = 0
        for tile in row:
            if tile == item:
                return_value.append(pygame.Rect(float(current_tile * values.TILE_SIZE), float(current_row * values.TILE_SIZE), float(values.TILE_SIZE), float(values.TILE_SIZE)))
            current_tile += 1
        current_row += 1
    return return_value


def load_player_entry(scene_number) -> tuple[int, int]:
    scene = load_scene(scene_number, "p")
    return scene[0].x, scene[0].y


def loop(is_offline: bool, player: pygame.Rect, color: str, scene: int, net: Network, ega_connection: ega.Connection):
    run = True
    clock = pygame.time.Clock()
    is_jumping = False
    falling = False
    scene_changed = False
    jump_count = 10
    x_offset = 0
    y_offset = 0
    while run:
        dt = clock.tick(MAX_FPS)
        players = net.send(player)
        player: pygame.Rect = players[USERNAME]
        color = players[USERNAME + ".color"]
        scene = players[USERNAME + ".scene"]
        ground = load_scene(scene, "n")
        dirt = load_scene(scene, "d")
        player_entities = []
        for p in players.values():
            if isinstance(p, pygame.Rect) and not p == player:
                player_entities.append(p)
        collisions_entities: list = ground + player_entities + dirt
        x_offset = player.x - ((WINDOW.get_width() / 2) - (player.width / 2))
        y_offset = player.y - ((WINDOW.get_height() / 2) - (player.height / 2))
        draw(players, ground, dirt, scene, WINDOW, is_offline, FONT, ASSETS, x_offset, y_offset)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.x += values.PLAYER_VELOCITY * dt
            # x_offset -= values.PLAYER_VELOCITY * dt
            if player.collidelist(collisions_entities) != -1:
                player.x -= values.PLAYER_VELOCITY * dt
                # x_offset += values.PLAYER_VELOCITY * dt
        if keys[pygame.K_a]:
            player.x -= values.PLAYER_VELOCITY * dt
            # x_offset += values.PLAYER_VELOCITY * dt
            if player.collidelist(collisions_entities) != -1:
                player.x += values.PLAYER_VELOCITY * dt
                # x_offset -= values.PLAYER_VELOCITY * dt
        if keys[pygame.K_SPACE] and not is_jumping and not falling:
            is_jumping = True
        if jump_count >= 0 and is_jumping:
            falling = True
            player.y -= (jump_count * abs(jump_count)) * 0.5
            # y_offset += (jump_count * abs(jump_count)) * 0.5
            jump_count -= 1
        elif is_jumping:
            jump_count = 10
            is_jumping = False
        else:
            falling = True
            player.y += 5
            # y_offset -= 10
            if player.collidelist(collisions_entities) != -1:
                falling = False
                player.y -= 5
                # y_offset += 10
        if keys[pygame.K_c]:
            if ega_connection is not None:
                ega_connection.add_achievement("Color Guy", "Change the Color in game")
            if keys[pygame.K_y]:
                net.send(["color", "yellow"])
            elif keys[pygame.K_b]:
                net.send(["color", "blue"])
            elif keys[pygame.K_r]:
                net.send(["color", "red"])
            elif keys[pygame.K_n]:
                net.send(["color", "black"])

        if keys[pygame.K_RIGHT] and not scene_changed:
            net.send(["scene", scene + 1])
            scene_changed = True
        elif keys[pygame.K_LEFT] and not scene_changed:
            net.send(["scene", scene - 1])
            scene_changed = True

        if (not keys[pygame.K_RIGHT]) and (not keys[pygame.K_LEFT]):
            scene_changed = False



if __name__ == '__main__':
    #print("Warning: You are trying to launch the Game Directly. This is no longer supported. Starting launcher now.")
    #try:
    #    import launcher
    #except ModuleNotFoundError:
    #    print("Cannot Import Launcher: Module Not Found")
    #launcher.main()
    init(1024, 720, 120, "Test", "blue", "1")
    main()
