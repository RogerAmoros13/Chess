import pygame
from tools import *
from player import Player
from board import Board
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Chess:
    def __init__(self):
        # Pygame screen
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Chess")
        self.surface = pygame.Surface(SIZE)
        self.surface.set_colorkey((0, 0, 0))
        self.surface.set_alpha(100)

        # Data
        self.pieces = import_images()
        self.board = Board()
        self.players = {
            0: Player(self.board, "w"),
            1: Player(self.board, "b"),
        }
        self.round = 0

        # Variables de estado
        self.pressed_piece = None
        self.pressed = False
    
    # Función para ejecutar el juego
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    
            self.screen.fill(BLACK)
            self.surface.fill(BLACK)
            self.player_move_manager()
            self.draw()
            pygame.draw.rect(self.screen, GREY, (800, 0, 400, 800))
            self.screen.blit(self.surface, (0, 0))
            pygame.display.update()
            # time.sleep(.2)

    def player_move_manager(self):
        mouse_buttons = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        # Posición que se acaba de marcar
        curr_pos = [pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE]
        player = self.get_current_player()
        
        # Comprueba si se está manteniendo pulsado el botón
        if mouse_buttons[0] and not self.pressed:

            # Existe una casilla previa pulsada?
            if self.pressed_piece:
                
                # Movimientos permitidos del jugador para la pieza seleccionada
                available_moves = player.get_available_moves(self.pressed_piece)

                if not self.board.are_enemy_pieces(self.pressed_piece, curr_pos):
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
            ):
                self.pressed_piece = None
            else:
                self.pressed_piece = curr_pos
            self.pressed = True
        elif not mouse_buttons[0] and self.pressed:
            self.pressed = False 

    def end_move(self, start, end):
        player = self.get_current_player()
        if self.board.get_piece(end):
            player.won_pieces.append(self.board.get_piece(end))
        if self.board.is_pawn(start):
            player.moved_pawns.append(self.board.get_piece(start))

        # Si el movimiento es valido se cambia la posición
        # Se termina la ronda y se despulsa la pieza
        self.board.move_piece(start, end)
        self.pressed_piece = None
        self.round += 1

    def get_current_player(self):
        return self.players.get(self.round % 2)
        
    def is_change_piece(self, player, pos):
        piece_code = self.board[pos[0]][pos[1]]
        if not piece_code:
            return False
        return piece_code[1] == player.color

    def draw(self):
        self.board.draw_board(
            {
                "screen": self.screen,
                "pieces": self.pieces,
                "pressed_piece": self.pressed_piece,
                "surface": self.surface,
                "player": self.get_current_player(),
            }
        )
    
    def draw_valid_moves(self):
        pass
        

if __name__ == "__main__":
    chess = Chess()
    chess.run()