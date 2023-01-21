import pygame
from tools import *
from player import *
from board import Board
from leader import Leader
from chessEngine import ChessEngine
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Chess:
    def __init__(self):
        # Pygame screen
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Chess")
        self.surface = pygame.Surface(SIZE)
        self.clock = pygame.time.Clock()
        self.surface.set_colorkey((0, 0, 0))
        self.surface.set_alpha(100)

        # Data
        self.pieces = import_images()
        self.board = Board()
        self.chess = ChessEngine(self.board)
        self.players = {
            0: JoeBiden(self.chess, "w"),
            1: Human(self.chess, "b"),
        }
        self.count = 0

        # Leader
        self.leader = Leader(
            self.screen,
            self.players[0],
            self.players[1],
        )

        # Variables de estado
        self.mouse_pos = None
        self.start_square = None
        self.end_square = None
        self.pressed = False
        self.current_player = self.players.get(0)
        self.chess.color = self.current_player.color
        self.old_player = self.players.get(1)

    # Función para ejecutar el juego
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(GREY)
            self.surface.fill(BLACK)
            if not self.chess.check_mate:
                self.event_manager()
            self.draw()
            self.update()

    def get_mouse_events(self):
        mouse_buttons = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        curr_pos = [pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE]
        self.mouse_pos = curr_pos
        if self.chess.is_inside_board(curr_pos):
            if mouse_buttons[0] and not self.pressed:
                self.pressed = True
                if self.start_square:
                    available_moves = self.chess.get_available_moves(
                        self.start_square
                    )
                    if curr_pos == self.start_square:
                        self.start_square = None
                    elif curr_pos in available_moves and not self.current_player.is_ia:
                        self.end_square = curr_pos
                    elif not self.board.are_enemy_pieces(
                        self.start_square, curr_pos
                    ):
                        self.start_square = curr_pos
                    else:
                        self.start_square = None
                elif self.board.is_color(curr_pos, self.current_player.color):
                    self.start_square = curr_pos
            elif not mouse_buttons[0] and self.pressed:
                self.pressed = False

    def event_manager(self):
        self.get_mouse_events()
        if self.current_player.is_ia:
            move = self.current_player.play()
            if move:
                self.start_square = move["start"]
                self.end_square = move["end"]
        if self.end_square:
            self.chess.do_move(
                self.start_square,
                self.end_square,
                True,
            )
            self.update_game_flags()

    def update_game_flags(self):
        self.count += 1
        self.start_square = False
        self.end_square = False
        self.old_player = self.current_player
        self.current_player = self.get_current_player()

    def get_current_player(self):
        return self.players.get(self.count % 2)

    def draw(self):
        self.board.draw_board(
            {
                "screen": self.screen,
                "pieces": self.pieces,
                "pressed_piece": self.start_square,
                "surface": self.surface,
                "player": self.current_player,
            }
        )
        if self.chess.end_game:
            self.draw_end_screen()

    def draw_end_screen(self):
        font_title = pygame.font.SysFont("didot.ttc", 80)
        if self.chess.check_mate:
            log_text = font_title.render(
                "{} ganan!".format(
                    self.old_player.color_name
                ),
                True,
                BLUE
            )
        else:
            log_text = font_title.render(
                "Tablas!", True, BLUE
            )
        self.screen.blit(log_text, (230, 350))

    def update(self):
        pygame.draw.rect(self.screen, BROWN, (800, 0, 400, 800))
        self.screen.blit(self.surface, (0, 0))
        # self.leader.draw_pieces(self.start_square, self.mouse_pos)
        self.leader.draw(self.chess.logs)
        pygame.display.update()
        self.clock.tick(10)
        # time.sleep(.3)


if __name__ == "__main__":
    chess = Chess()
    chess.run()
