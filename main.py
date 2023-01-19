import pygame
from tools import *
from player import Player
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
        self.leader = Leader(self.screen)

        # Data
        self.pieces = import_images()
        self.board = Board()
        self.chess = ChessEngine(self.board)
        self.players = {
            0: Player(self.chess, "w"),
            1: Player(self.chess, "b"),
        }
        self.round = 0

        # Variables de estado
        self.pressed_piece = None
        self.pressed_square = None
        self.pressed = False
        self.check_mate = False
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

            self.screen.fill(BLACK)
            self.surface.fill(BLACK)
            if not self.check_mate:
                self.event_manager()
            self.draw()
            if not self.check_mate and not self.chess.get_all_moves(self.current_player):
                self.check_mate = True
            if self.check_mate:
                self.draw_win_screen()
            self.update()

    def event_manager(self):
        mouse_buttons = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        # Posición que se acaba de marcar
        curr_pos = [pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE]
        self.pressed_square = curr_pos

        # Comprueba si se está manteniendo pulsado el botón
        if mouse_buttons[0] and not self.pressed:

            # Existe una casilla previa pulsada?
            if self.pressed_piece:

                # Movimientos permitidos del jugador para la pieza seleccionada
                available_moves = self.current_player.get_available_moves(
                    self.pressed_piece
                )

                if (
                    self.chess.is_inside_board(curr_pos)
                    and not self.board.are_enemy_pieces(self.pressed_piece, curr_pos)
                ):
                    self.pressed_piece = curr_pos

                # Esta casilla es la misma que habia o no es valida?
                elif (
                    self.pressed_piece == curr_pos
                    or curr_pos not in available_moves
                ):
                    self.pressed_piece = None

                # Realizar el movimiento
                else:
                    self.end_move(self.pressed_piece, curr_pos)

            # Si la casilla está en blanco no se guarda la posición
            elif (
                not self.board.get_piece(curr_pos)
                or not self.board.is_color(curr_pos, self.current_player.color)
            ):
                self.pressed_piece = None
            else:
                self.pressed_piece = curr_pos
            self.pressed = True
        elif not mouse_buttons[0] and self.pressed:
            self.pressed = False

    def end_move(self, start, end):
        if self.board.get_piece(end):
            self.current_player.won_pieces.append(self.board.get_piece(end))
        if self.board.is_king(start):
            self.chess.kings_position.update(
                {self.current_player.color: (end[0], end[1])})
            castle = self.chess.is_castling(end, self.current_player.color)
            if castle:
                self.board.castling_move(self.current_player.color, castle)
            else:
                self.board.move_piece(start, end)
            self.chess.kings_moved.update({self.current_player.color: True})
        # Si el movimiento es valido se cambia la posición
        # Se termina la ronda y se despulsa la pieza
        else:
            if self.chess.is_en_passant(start, end):
                self.board.set_position(lst_sum(start, [0, end[1] - start[1]]), "")
            self.board.move_piece(start, end)
        self.pressed_piece = None
        self.round += 1
        self.old_player = self.current_player
        self.current_player = self.get_current_player()
        en_passant = None
        if self.board.is_pawn(end) and abs(start[0] - end[0]) == 2:
            en_passant = start[1]
        self.chess.update_variables(self.current_player.color, en_passant)

    def get_current_player(self):
        return self.players.get(self.round % 2)

    def draw(self):
        self.board.draw_board(
            {
                "screen": self.screen,
                "pieces": self.pieces,
                "pressed_piece": self.pressed_piece,
                "surface": self.surface,
                "player": self.current_player,
            }
        )

    def draw_win_screen(self):
        font_title = pygame.font.SysFont("didot.ttc", 80)
        log_text = font_title.render("{} ganan!".format(
            self.old_player.display_name), True, BLUE)
        self.screen.blit(log_text, (230, 350))

    def update(self):
        pygame.draw.rect(self.screen, GREY, (800, 0, 400, 800))
        self.screen.blit(self.surface, (0, 0))
        self.leader.draw_pieces(self.pressed_piece, self.pressed_square)
        self.leader.draw_logs(self.board.registry)
        pygame.display.update()
        self.clock.tick(30)
        # time.sleep(.4)


if __name__ == "__main__":
    chess = Chess()
    chess.run()
