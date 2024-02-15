import pygame


def draw(players: dict, ground, scene: int, window: pygame.Surface, offline: bool, font: pygame.font, assets: dict):
    window.fill("white")
    rects = {}
    colors = {}
    if offline:
        loading_txt = font.render("Offline", 1, "black")
        window.blit(loading_txt, (0, 0))
    GROUND_X_SIZE, GROUND_Y_SIZE = assets["ground"].get_size()
    for i in ground:
        for d in range(int(i.size[0] / GROUND_X_SIZE)):
            f = d * GROUND_X_SIZE
            # window.blit(pygame.transform.scale(assets["ground"], (i.size[0] + f, i.size[1])), i)
            window.blit(assets["ground"], (i.x + f, i.y))
        # pygame.draw.rect(window, "green", i)
    for n, p in players.items():
        if isinstance(p, pygame.Rect):
            rects[n] = p
        else:
            na = n.split(".")[0]
            colors[na] = p
    for n, p in rects.items():
        pygame.draw.rect(window, colors[n], p)
    pygame.display.update()


if __name__ == "__main__":
    print("Cannot be run like this LOL")
