import pygame
from tools import *


class Leader:
    def __init__(self, screen, player1, player2):
        self.screen = screen
        pygame.font.init()
        self.font_large = pygame.font.SysFont("didot.ttc", 60)
        self.font_big = pygame.font.SysFont("didot.ttc", 40)
        self.font_medium = pygame.font.SysFont("didot.ttc", 30)
        self.font_small = pygame.font.SysFont("didot.ttc", 20)
        self.font_tiny = pygame.font.SysFont("didot.ttc", 14)
        self.playerW = player1
        self.playerB = player2

    def draw(self, logs):
        self.draw_players()
        self.draw_logs(logs)

    def draw_pieces(self, pos, pos2):
        if pos:
            text = self.font_medium.render("Pos: ({}, {})".format(
                pos[0], pos[1]), True, WHITE
            )
            self.screen.blit(text, (820, 20))
        if pos2:
            text2 = self.font_medium.render("Mouse Pos: ({}, {})".format(
                pos2[0], pos2[1]), True, WHITE
            )
            self.screen.blit(text2, (820, 50))

    def draw_players(self):
        white_player = self.font_large.render(
            self.playerW.display_brain, True, WHITE)
        self.screen.blit(white_player, (810, 10))
        vs = self.font_big.render("vs", True, GREY)
        self.screen.blit(vs, (985, 20))
        white_player = self.font_large.render(
            self.playerB.display_brain, True, BLACK)
        self.screen.blit(white_player, (1020, 10))

    def draw_logs(self, logs):
        log_text = self.font_large.render("Logs", True, GREY)
        self.screen.blit(log_text, (810, 360))
        y = 410
        delay = 26
        start_iter = len(logs) - delay
        start_iter = start_iter + 1 if start_iter % 2 else start_iter
        for i, log in enumerate(logs):
            if i < start_iter:
                continue
            x = 820
            increment = 0
            if not log["round"] % 2:
                x = 960
                increment = 30
            msg = self.font_medium.render(log["log"], True, GREY)
            self.screen.blit(msg, (x, y))
            y += increment
            if y > 790:
                break
