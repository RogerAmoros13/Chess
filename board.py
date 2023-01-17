from tools import *
"""
    Definición de la clase Board para la gestión de
    las pizas en el tablero.
"""


class Board:
    def __init__(self, board=False):
        self.board = [
            ["1bR", "1bN", "1bB", "1bQ", "1bK", "1bB", "1bN", "1bR"],
            ["1bP", "2bP", "2bP", "4bP", "5bP", "6bP", "7bP", "8bP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["1wP", "2wP", "3wP", "4wP", "5wP", "6wP", "7wP", "8wP"],
            ["1wR", "1wN", "1wB", "0wQ", "0wK", "1wB", "1wN", "2wR"],
        ]
        self.registry = []
        self.dims = 8

    def get_piece(self, pos):
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
            return False
        return self.board[pos[0]][pos[1]]

    def get_color(self, pos):
        # TODO: get_color(self, pos, color) --> bool
        piece = self.get_piece(pos)
        if piece:
            return piece[1]
        return ""

    def is_pawn(self, pos, color=None):
        return self.is_piece(pos, "P", color)

    def is_king(self, pos, color=None):
        return self.is_piece(pos, "K", color)

    def is_knight(self, pos, color=None):
        return self.is_piece(pos, "N", color)

    def is_bishop(self, pos, color=None):
        return self.is_piece(pos, "B", color)

    def is_rook(self, pos, color=None):
        return self.is_piece(pos, "R", color)

    def is_queen(self, pos, color=None):
        return self.is_piece(pos, "Q", color)

    def is_king(self, pos, color=None):
        return self.is_piece(pos, "K", color)

    def is_piece(self, pos, code, color):
        piece = self.get_piece(pos)
        if piece:
            if color:
                return piece[2] == code and piece[1] == color
            return piece[2] == code
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

    def move_piece(self, pos1, pos2, register=True):
        # Mover pieza de pos1 a pos2
        piece1 = self.get_piece(pos1)
        piece2 = self.get_piece(pos2)
        self.set_position(pos1, "")
        self.set_position(pos2, piece1)
        vals = {
            piece1: pos1,
        }
        if register:
            if piece2:
                vals.update({piece2: pos2})
            self.registry.append(vals)

    def undo_move(self, square1=None, square2=None, castling=False):
        if castling:
            return True
        piece1 = square1.get("piece")
        pos1 = square1.get("position")
        piece2 = square2.get("piece")
        pos2 = square2.get("position")
        self.set_position(pos1, piece1)
        self.set_position(pos2, piece2)

    def get_copy(self):
        return self.board.copy()

    def castling_move(self, color, side):
        row = 7 if color == "w" else 0
        king = self.get_piece([row, 4])
        if side == "short":
            rook = self.get_piece([row, 7])
            self.set_position([row, 4], "")
            self.set_position([row, 5], rook)
            self.set_position([row, 6], king)
            self.set_position([row, 7], "")
            self.registry.append(
                {
                    king: [row, 4],
                    rook: [row, 7],
                }
            )
        else:
            rook = self.get_piece([row, 0])
            self.set_position([row, 0], "")
            self.set_position([row, 2], king)
            self.set_position([row, 3], rook)
            self.set_position([row, 4], "")
            self.registry.append(
                {
                    rook: [row, 0],
                    king: [row, 4],
                }
            )

    def draw_board(self, vals):
        screen = vals.get("screen")
        pieces = vals.get("pieces")
        press = vals.get("pressed_piece")
        player = vals.get("player")
        x = 0
        y = 0
        switch = True  # Variable para alternar el color de las casillas.
        for row in self.board:
            for col in row:
                color = WHITE_SQUARE if switch else GREEN
                pygame.draw.rect(
                    screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE)
                )
                if col:
                    if (
                        press == [y // SQUARE_SIZE, x // SQUARE_SIZE]
                    ):
                        pygame.draw.rect(
                            screen, YELLOW, (x, y, SQUARE_SIZE, SQUARE_SIZE)
                        )
                    screen.blit(pieces[col[1:3]], (x + 5, y + 5))
                # Si hay alguna pieza seleccionada se muestran los movimientos disponibles
                if press and self.square_in_available_moves(x, y, player, press):
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
