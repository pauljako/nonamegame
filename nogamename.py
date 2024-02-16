import os.path
try:
    import pygame
except ModuleNotFoundError:
    print("It looks like pygame is not installed")
try:
    from network import Network
    from draw import draw
except ModuleNotFoundError:
    print("Required Files not Found")

WIDTH: int
HEIGHT: int
WIN: pygame.Surface
PLAYER_WIDTH: int
PLAYER_HEIGHT: int
PLAYER_VEL: float
GAME_NAME: str
PLAYER_JUMP_TICKS: int
PLAYER_JUMP_PER_TICK: float
MAX_FPS: int
FONT: pygame.font.Font
USERNAME: str
ASSETS: dict
SCENES: list


def init(WIN_SIZE: tuple, TITLE: str, FONT_NAME: str, FONT_SIZE: int, NAME: str):
    global WIDTH, HEIGHT, WIN, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL, GAME_NAME, PLAYER_JUMP_TICKS, PLAYER_JUMP_PER_TICK, MAX_FPS, FONT, USERNAME, ASSETS, SCENES
    print(f"Welcome to {TITLE}!")
    print("Initializing Game...")
    pygame.quit()
    pygame.init()
    pygame.font.quit()
    pygame.font.init()
    WIDTH = WIN_SIZE[0]
    HEIGHT = WIN_SIZE[1]
    GAME_NAME = TITLE
    FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    MAX_FPS = 120
    WIN = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption(GAME_NAME)
    ASSETS = {
        "ground": pygame.image.load(os.path.join(os.path.join("assets", "textures"), "ground.png"))
    }
    pygame.display.set_icon(ASSETS["ground"])
    loading_txt = FONT.render("Loading...", 1, "white")
    WIN.blit(loading_txt, (0, 0))
    PLAYER_VEL = 0.2
    PLAYER_JUMP_PER_TICK = 0.1
    PLAYER_JUMP_TICKS = 30
    PLAYER_WIDTH = 40
    PLAYER_HEIGHT = 80
    USERNAME = NAME
    SCENES = [
        [
            pygame.Rect(0, HEIGHT - 20, WIDTH, 20), pygame.Rect(20, HEIGHT - 60, 20, 20),
            pygame.Rect(600, HEIGHT - 60, 60, 20), pygame.Rect(100, HEIGHT - 140, 60, 20),
            pygame.Rect(680, HEIGHT - 120, 60, 20)
        ],
        [
            pygame.Rect(0, HEIGHT - 20, WIDTH, 20), pygame.Rect(20, HEIGHT - 60, 20, 20),
            pygame.Rect(600, HEIGHT - 60, 60, 20), pygame.Rect(100, HEIGHT - 140, 60, 20),
            pygame.Rect(680, HEIGHT - 120, 60, 20)
        ]
    ]
    pygame.display.update()
    print("Game Initialized")
    return True


def main():
    run = True
    color = "black"
    player = pygame.Rect(WIDTH / 2 - PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT - 20, PLAYER_WIDTH, PLAYER_HEIGHT)
    scene = 1
    clock = pygame.time.Clock()
    isJumping = False
    falling = False
    jumpCount = 10
    net = Network(USERNAME, player, color, scene)
    players = net.connect()
    if isinstance(players, str):
        print("Connection Error. Game will launch offline")
        offline = True
    elif players[USERNAME] != player:
        print("Error while verifying. Game will launch offline")
        offline = True
    else:
        offline = False
    while run:
        dt = clock.tick(MAX_FPS)
        if offline:
            players = {USERNAME: player, USERNAME + ".color": color, USERNAME + ".scene": scene}
        else:
            players = net.send(player)
            player = players[USERNAME]
            color = players[USERNAME + ".color"]
            scene = players[USERNAME + ".scene"]
        ground = SCENES[scene]
        draw(players, ground, scene, WIN, offline, FONT, ASSETS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.x += PLAYER_VEL * dt
            if player.collidelist(ground) != -1:
                player.x -= PLAYER_VEL * dt
        if keys[pygame.K_a]:
            player.x -= PLAYER_VEL * dt
            if player.collidelist(ground) != -1:
                player.x += PLAYER_VEL * dt
        if keys[pygame.K_SPACE] and not isJumping and not falling:
            isJumping = True
        if jumpCount >= 0 and isJumping:
            falling = True
            player.y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        elif isJumping:
            jumpCount = 10
            isJumping = False
        else:
            falling = True
            player.y += 10
            if player.collidelist(ground) != -1:
                falling = False
                player.y -= 10
        if keys[pygame.K_c] and not offline:
            if keys[pygame.K_y]:
                net.send(["color", "yellow"])
            elif keys[pygame.K_b]:
                net.send(["color", "blue"])
            elif keys[pygame.K_r]:
                net.send(["color", "red"])
            elif keys[pygame.K_n]:
                net.send(["color", "black"])
        elif keys[pygame.K_c] and offline:
            if keys[pygame.K_y]:
                color = "yellow"
            elif keys[pygame.K_b]:
                color = "blue"
            elif keys[pygame.K_r]:
                color = "red"
            elif keys[pygame.K_n]:
                color = "black"
    print("Bye!")
    net.client.close()
    pygame.quit()


if __name__ == '__main__':
    print("Warning: You are trying to launch the Game Directly. This is no longer supported. Starting launcher now.")
    try:
        import launcher
    except ModuleNotFoundError:
        print("Cannot Import Launcher: Module Not Found")
    launcher.main()
