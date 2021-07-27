import pygame
from lib.gameObject import gameObject

class textObject(gameObject):
    def __init__(self, text, font, screen, place):
        gameObject.__init__(self, place[0], place[1])
        self.text = text
        self.font = font
        self.screen = screen
        self._circle_cache = {}

    def _circlepoints(self, r):
        r = int(round(r))
        if r in self._circle_cache:
            return self._circle_cache[r]
        x, y, e = r, 0, 1 - r
        self._circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    def update(self):
        opx = 2
        text = self.font.render(self.text, True, (0, 0, 0))
        text_bg = self.font.render(self.text, True, (255, 255, 255))
        w = text.get_width() + 2 * opx
        h = text.get_height()

        osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(text_bg, (0, 0))

        for dx, dy in self._circlepoints(opx):
            surf.blit(osurf, (dx + opx, dy + opx))

        surf.blit(text, (opx, opx))

        self.screen.blit(surf, (self.x, self.y))