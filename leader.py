import pygame
from tools import *


class Leader:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()

    def draw(self):
        pass

    def draw_pieces(self, pos, pos2):
        font = pygame.font.SysFont("didot.ttc", 22)
        if pos:
            text = font.render("Pos: ({}, {})".format(
                pos[0], pos[1]), True, WHITE
            )
            self.screen.blit(text, (820, 20))
        if pos2:
            text2 = font.render("Mouse Pos: ({}, {})".format(
                pos2[0], pos2[1]), True, WHITE
            )
            self.screen.blit(text2, (820, 50))
