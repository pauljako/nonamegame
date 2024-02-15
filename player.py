import pygame


class Player(pygame.Rect):
    def __init__(self, color, a=0, b=0, c=0):
        player_width = 40
        player_height = 80
        win_width = 1080
        win_height = 800
        super().__init__(win_width / 2 - player_width, win_height - player_height - 20, player_width, player_height)
        self.color = color
