import pygame
from tools import *
from player import Player
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
        self.board = BOARD
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

                if self.is_change_piece(player, curr_pos):
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
                not self.board[curr_pos[0]][curr_pos[1]]
            ):
                self.pressed_piece = None
            else:
                self.pressed_piece = curr_pos
            self.pressed = True
        elif not mouse_buttons[0] and self.pressed:
            self.pressed = False 

    def end_move(self, start, end):
        # Si el movimiento es valido se cambia la posición
        # Se termina la ronda y se despulsa la pieza
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = ""
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
        self.draw_board()
            
    # Dibujar el fondo del tablero y las piezas.
    def draw_board(self):
        x = 0
        y = 0
        switch = True # Variable para alternar el color de las casillas.
        for row in self.board:
            for col in row:
                color = WHITE_SQUARE if switch else GREEN
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                if col:
                    self.screen.blit(self.pieces[col[1:3]], (x + 5, y + 5))
                # Si hay alguna pieza seleccionada se muestran los movimientos disponibles
                if self.pressed_piece:
                    player = self.get_current_player()
                    if [x // SQUARE_SIZE, y // SQUARE_SIZE] in player.get_available_moves(self.pressed_piece):
                        pygame.draw.circle(
                            self.surface, 
                            GREY2, 
                            (y + SQUARE_SIZE / 2, x + SQUARE_SIZE / 2), 
                            15
                        )
                x += SQUARE_SIZE
                switch = not switch
            # Al cambiar de fila se repite el color.
            switch = not switch
            x = 0
            y += SQUARE_SIZE
    
    def draw_valid_moves(self):
        pass
        

if __name__ == "__main__":
    chess = Chess()
    chess.run()