import os.path
import random
import sys
import threading


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


def init(max_fps: int, username: str, color: str, room: str):
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
    WINDOW = pygame.display.set_mode((values.WIDTH, values.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(title)
    ASSETS = {
                 "ground": pygame.image.load(os.path.join("assets", "textures", "ground.png"))
             }
    pygame.display.set_icon(ASSETS["ground"])
    loading_txt = FONT.render("Loading...", 1, "white")
    WINDOW.blit(loading_txt, ((values.WIDTH / 2) - (loading_txt.get_width() / 2), (values.HEIGHT / 2) - (loading_txt.get_height() / 2)))
    pygame.display.update()
    INIT_COLOR = color
    USERNAME = username
    pygame.display.update()
    print("Game Initialized")
    initialized = True


# def init(WIN_SIZE: tuple, TITLE: str, FONT_NAME: str, FONT_SIZE: int, NAME: str, COLOR: str, ROOM: str):
#     global WIDTH, HEIGHT, WIN, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL, GAME_NAME, PLAYER_JUMP_TICKS, PLAYER_JUMP_PER_TICK, MAX_FPS, FONT, USERNAME, ASSETS, SCENES, INIT_COLOR, ROOM_CODE
#     print(f"Welcome to {TITLE}!")
#     print("Initializing Game...")
#     pygame.quit()
#     pygame.init()
#     pygame.font.quit()
#     pygame.font.init()
#     WIDTH = WIN_SIZE[0]
#     HEIGHT = WIN_SIZE[1]
#     GAME_NAME = TITLE
#     ROOM_CODE = ROOM
#     FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
#     MAX_FPS = 120
#     WIN = pygame.display.set_mode(WIN_SIZE)
#     pygame.display.set_caption(GAME_NAME)
#     ASSETS = {
#         "ground": pygame.image.load(os.path.join(os.path.join("assets", "textures"), "ground.png"))
#     }
#     pygame.display.set_icon(ASSETS["ground"])
#     loading_txt = FONT.render("Loading...", 1, "white")
#     WIN.blit(loading_txt, (0, 0))
#     PLAYER_VEL = 0.2
#     PLAYER_JUMP_PER_TICK = 0.1
#     PLAYER_JUMP_TICKS = 30
#     PLAYER_WIDTH = 40
#     PLAYER_HEIGHT = 80
#     INIT_COLOR = COLOR
#     USERNAME = NAME
#     SCENES = [
#         [
#             pygame.Rect(0, HEIGHT - 20, WIDTH, 20), pygame.Rect(20, HEIGHT - 60, 20, 20),
#             pygame.Rect(600, HEIGHT - 60, 60, 20), pygame.Rect(100, HEIGHT - 140, 60, 20),
#             pygame.Rect(680, HEIGHT - 120, 60, 20)
#         ],
#         [
#             pygame.Rect(0, HEIGHT - 20, WIDTH, 20), pygame.Rect(20, HEIGHT - 60, 400, 20),
#             pygame.Rect(600, HEIGHT - 60, 60, 20), pygame.Rect(100, HEIGHT - 140, 60, 20),
#             pygame.Rect(680, HEIGHT - 120, 60, 20)
#         ]
#     ]
#     pygame.display.update()
#     print("Game Initialized")
#     return True


def main():
    global WINDOW
    color = INIT_COLOR
    player = pygame.Rect(values.WIDTH / 2 - values.PLAYER_WIDTH, values.HEIGHT - values.PLAYER_HEIGHT - 60, values.PLAYER_WIDTH, values.PLAYER_HEIGHT)
    scene = 1
    net = Network(username=USERNAME, player=player, color=color, room_code=ROOM_CODE, scene=scene, address="127.0.0.1", port=2531)
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
        WINDOW = pygame.display.set_mode((values.WIDTH, values.HEIGHT), pygame.RESIZABLE)
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


def loop(is_offline: bool, player: pygame.Rect, color: str, scene: int, net: Network, ega_connection: ega.Connection):
    run = True
    clock = pygame.time.Clock()
    is_jumping = False
    falling = False
    jump_count = 10
    x_offset: float = 0
    y_offset: float = 0
    while run:
        dt = clock.tick(MAX_FPS)
        players = net.send(player)
        player: pygame.Rect = players[USERNAME]
        color = players[USERNAME + ".color"]
        scene = players[USERNAME + ".scene"]
        ground = values.SCENES[scene]
        draw(players, ground, scene, WINDOW, is_offline, FONT, ASSETS, x_offset, y_offset)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.x += values.PLAYER_VELOCITY * dt
            x_offset -= values.PLAYER_VELOCITY * dt
            if player.collidelist(ground) != -1:
                player.x -= values.PLAYER_VELOCITY * dt
                x_offset += values.PLAYER_VELOCITY * dt
        if keys[pygame.K_a]:
            player.x -= values.PLAYER_VELOCITY * dt
            x_offset += values.PLAYER_VELOCITY * dt
            if player.collidelist(ground) != -1:
                player.x += values.PLAYER_VELOCITY * dt
                x_offset -= values.PLAYER_VELOCITY * dt
        if keys[pygame.K_SPACE] and not is_jumping and not falling:
            is_jumping = True
        if jump_count >= 0 and is_jumping:
            falling = True
            player.y -= (jump_count * abs(jump_count)) * 0.5
            y_offset += (jump_count * abs(jump_count)) * 0.5
            jump_count -= 1
        elif is_jumping:
            jump_count = 10
            is_jumping = False
        else:
            falling = True
            player.y += 10
            y_offset -= 10
            if player.collidelist(ground) != -1:
                falling = False
                player.y -= 10
                y_offset += 10
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


if __name__ == '__main__':
    #print("Warning: You are trying to launch the Game Directly. This is no longer supported. Starting launcher now.")
    #try:
    #    import launcher
    #except ModuleNotFoundError:
    #    print("Cannot Import Launcher: Module Not Found")
    #launcher.main()
    init(120, "Test", "blue", "1")
    main()
