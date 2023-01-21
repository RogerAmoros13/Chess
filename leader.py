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
        self.assets = import_assets()

    def draw(self, vals):
        self.draw_players()
        self.draw_logs(vals)
        self.draw_undo_button(vals)

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
            "Blancas: " + self.playerW.name, True, WHITE
        )
        self.screen.blit(white_player, (810, 10))
        white_player = self.font_large.render(
            "Negras: " + self.playerB.name, True, BLACK
        )
        self.screen.blit(white_player, (810, 55))

    def draw_logs(self, vals):
        log_text = self.font_large.render("Logs", True, GREY)
        self.screen.blit(log_text, (810, 360))
        logs = vals.get("logs")
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

    def draw_undo_button(self, vals):
        undo = vals.get("undo")
        # text = self.font_medium.render("Undo", True, GREY)
        if undo:
            pygame.draw.rect(self.screen, GREEN, (815, 105, 40, 40), 0, 3)
        else:
            pygame.draw.rect(self.screen, GREY2, (815, 105, 40, 40), 0, 3)
        self.screen.blit(self.assets["undo"], (815, 105))

