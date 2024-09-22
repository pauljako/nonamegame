import pygame
from server import values


def draw(
        players: dict,
        ground,
        dirt,
        scene: int,
        window: pygame.Surface,
        offline: bool,
        font: pygame.font,
        assets: dict,
        x_offset: float,
        y_offset: float
):
    window.fill("white")
    rects = {}
    colors = {}
    for i in ground:
        window.blit(pygame.transform.scale(assets["ground"], (i.width, i.height)), (i.x - x_offset, i.y - y_offset))
    for i in dirt:
        window.blit(pygame.transform.scale(assets["dirt"], (i.width, i.height)), (i.x - x_offset, i.y - y_offset))
    for n, p in players.items():
        if isinstance(p, pygame.Rect):
            rects[n] = p
        elif n.split(".")[1] == "color":
            na = n.split(".")[0]
            colors[na] = p
    for n, p in rects.items():
        window.blit(pygame.transform.scale(assets["player"], (values.PLAYER_WIDTH, values.PLAYER_HEIGHT)), (p.x - x_offset, p.y - y_offset))
    if offline:
        loading_txt = font.render("Offline", 1, "black")
        window.blit(loading_txt, (0, 0))
    pygame.display.update()


if __name__ == "__main__":
    print("Cannot be run like this LOL")
