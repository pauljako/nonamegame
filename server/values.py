import pygame

TILE_SIZE = 64
PLAYER_VELOCITY = 0.2
PLAYER_JUMP_PER_TICK = 0.1
PLAYER_JUMP_TICKS = 30
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 32


def get_values() -> dict:
    global PLAYER_VELOCITY, PLAYER_JUMP_PER_TICK, PLAYER_JUMP_TICKS, PLAYER_WIDTH, PLAYER_HEIGHT
    return {
        "player_velocity": PLAYER_VELOCITY,
        "player_jump_per_tick": PLAYER_JUMP_PER_TICK,
        "player_jump_ticks": PLAYER_JUMP_TICKS,
        "player_width": PLAYER_WIDTH,
        "player_height": PLAYER_HEIGHT,
    }


def set_values(data: dict):
    global PLAYER_VELOCITY, PLAYER_JUMP_PER_TICK, PLAYER_JUMP_TICKS, PLAYER_WIDTH, PLAYER_HEIGHT
    PLAYER_VELOCITY = data["player_velocity"]
    PLAYER_JUMP_PER_TICK = data["player_jump_per_tick"]
    PLAYER_JUMP_TICKS = data["player_jump_ticks"]
    PLAYER_WIDTH = data["player_width"]
    PLAYER_HEIGHT = data["player_height"]
