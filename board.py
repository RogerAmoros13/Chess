from tools import *
"""
    Definición de la clase Board para la gestión de
    las pizas en el tablero.
"""


class Board:
    def __init__(self):
        self.board = [
            ["1bR", "1bN", "1bB", "1bQ", "1bK", "1bB", "1bN", "1bR"],
            ["1bP", "2bP", "3bP", "4bP", "5bP", "6bP", "7bP", "8bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["1wP", "2wP", "3wP", "4wP", "5wP", "6wP", "7wP", "8wP"],
            ["1wR", "1wN", "1wB", "0wQ", "0wK", "2wB", "2wN", "2wR"],
        ]

    def get_piece(self, pos):
        return self.board[pos[0]][pos[1]]

    def get_color(self, pos):
        piece = self.get_piece(pos)
        if piece:
            return piece[1]
        return ""

    def is_pawn(self, pos):
        piece = self.get_piece(pos)
        if piece:
            return piece[2] == "P"
        return False

    def is_king(self, pos):
        piece = self.get_piece()
        if piece:
            return piece[2] == "K"
        return False

    def are_enemy_pieces(self, pos1, pos2):
        # Son colores distintos --> True
        # Son colores iguales --> False
        piece1 = self.get_piece(pos1)
        piece2 = self.get_piece(pos2)
        if piece1 and piece2:
            return piece1[1] != piece2[1]
        return True

    def set_position(self, pos, value):
        self.board[pos[0]][pos[1]] = value

    def move_piece(self, pos1, pos2):
        # Mover pieza de pos1 a pos2
        piece = self.get_piece(pos1)
        self.set_position(pos1, "")
        self.set_position(pos2, piece)

    def draw_board(self, vals):
        screen = vals.get("screen")
        pieces = vals.get("pieces")
        x = 0
        y = 0
        switch = True  # Variable para alternar el color de las casillas.
        for row in self.board:
            for col in row:
                color = WHITE_SQUARE if switch else GREEN
                pygame.draw.rect(
                    screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                if col:
                    screen.blit(pieces[col[1:3]], (x + 5, y + 5))
                # Si hay alguna pieza seleccionada se muestran los movimientos disponibles
                press = vals.get("pressed_piece")
                if press:
                    player = vals.get("player")
                    if self.square_in_available_moves(x, y, player, press):
                        pygame.draw.circle(
                            vals.get("surface"),
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

    def square_in_available_moves(self, x, y, player, press):
        _x = x // SQUARE_SIZE
        _y = y // SQUARE_SIZE
        moves = player.get_available_moves(press)
        return any(_x == r[0] and _y == r[1] for r in moves)
