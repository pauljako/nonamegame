import pygame

PLAYER_VELOCITY = 0.2
PLAYER_JUMP_PER_TICK = 0.1
PLAYER_JUMP_TICKS = 30
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 80
WIDTH = 740
HEIGHT = 600
SCENES = [
    [
        pygame.Rect(0, HEIGHT - 20, 1000000, 20),
        pygame.Rect(20, HEIGHT - 60, 20, 20),
        pygame.Rect(600, HEIGHT - 60, 60, 20),
        pygame.Rect(100, HEIGHT - 140, 60, 20),
        pygame.Rect(680, HEIGHT - 120, 60, 20)],
    [
        pygame.Rect(0, HEIGHT - 20, 1000000, 40),
        pygame.Rect(20, HEIGHT - 60, 400, 20),
        pygame.Rect(600, HEIGHT - 60, 60, 20),
        pygame.Rect(100, HEIGHT - 140, 60, 20),
        pygame.Rect(680, HEIGHT - 120, 60, 20)
    ]
]


def get_values() -> dict:
    global PLAYER_VELOCITY, PLAYER_JUMP_PER_TICK, PLAYER_JUMP_TICKS, PLAYER_WIDTH, PLAYER_HEIGHT, WIDTH, HEIGHT, SCENES
    return {
        "player_velocity": PLAYER_VELOCITY,
        "player_jump_per_tick": PLAYER_JUMP_PER_TICK,
        "player_jump_ticks": PLAYER_JUMP_TICKS,
        "player_width": PLAYER_WIDTH,
        "player_height": PLAYER_HEIGHT,
        "width": WIDTH,
        "height": HEIGHT,
        "scenes": SCENES
    }


def set_values(data: dict):
    global PLAYER_VELOCITY, PLAYER_JUMP_PER_TICK, PLAYER_JUMP_TICKS, PLAYER_WIDTH, PLAYER_HEIGHT, WIDTH, HEIGHT, SCENES
    PLAYER_VELOCITY = data["player_velocity"]
    PLAYER_JUMP_PER_TICK = data["player_jump_per_tick"]
    PLAYER_JUMP_TICKS = data["player_jump_ticks"]
    PLAYER_WIDTH = data["player_width"]
    PLAYER_HEIGHT = data["player_height"]
    WIDTH = data["width"]
    HEIGHT = data["height"]
    SCENES = data["scenes"]
