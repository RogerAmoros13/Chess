from tools import *
"""
    Definición de la clase Board para la gestión de
    las pizas en el tablero.
"""


class Board:
    def __init__(self):
        self.board = BOARD_BASIC
        self.registry = []
        self.dims = 8

    def get_piece(self, pos):
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
            return False
        return self.board[pos[0]][pos[1]]

    def get_color(self, pos):
        piece = self.get_piece(pos)
        if piece:
            return piece[0]
        return ""

    def is_color(self, pos, color):
        piece = self.get_piece(pos)
        if piece:
            return piece[0] == color
        return False

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
                return piece[1] == code and piece[0] == color
            return piece[1] == code
        return False

    def are_enemy_pieces(self, pos1, pos2):
        # Son colores distintos --> True
        # Son colores iguales --> False
        piece1 = self.get_piece(pos1)
        piece2 = self.get_piece(pos2)
        if piece1 and piece2:
            return piece1[0] != piece2[0]
        return True

    def set_position(self, pos, value):
        self.board[pos[0]][pos[1]] = value

    def move_piece(self, vals):
        start = vals.get("start_square")
        end = vals.get("end_square")
        moved_piece = vals.get("moved_piece")
        if vals["castling"]:
            self.castling_move(vals["color"], vals["castling"])
        else:
            self.set_position(start, "")
            self.set_position(end, moved_piece)
            if vals["en_passant"]:
                self.set_position(
                    lst_sum(start, [0, end[1] - start[1]]),
                    ""
                )
            elif vals["promotion"]:
                self.set_position(end, "{}Q".format(vals["color"]))

    def undo_move(self, vals):
        start = vals.get("start_square")
        end = vals.get("end_square")
        moved_piece = vals.get("moved_piece")
        if vals["castling"]:
            self.undo_castling_move(vals["color"], vals["castling"])
        else:
            self.set_position(start, moved_piece)
            if vals["en_passant"]:
                self.set_position(
                    lst_sum(start, [0, end[1] - start[1]]),
                    vals["eaten_piece"]
                )
                self.set_position(end, "")
            else:
                self.set_position(end, vals["eaten_piece"])

    def get_copy(self):
        return self.board.copy()

    def castling_move(self, color, side):
        row = 7 if color == "w" else 0
        if side == "short":
            self.set_position([row, 4], "")
            self.set_position([row, 5], "{}R".format(color))
            self.set_position([row, 6], "{}K".format(color))
            self.set_position([row, 7], "")
        else:
            self.set_position([row, 0], "")
            self.set_position([row, 2], "{}K".format(color))
            self.set_position([row, 3], "{}R".format(color))
            self.set_position([row, 4], "")

    def undo_castling_move(self, color, side):
        row = 7 if color == "w" else 0
        if side == "short":
            self.set_position([row, 4], "{}K".format(color))
            self.set_position([row, 5], "")
            self.set_position([row, 6], "")
            self.set_position([row, 7], "{}R".format(color))
        else:
            self.set_position([row, 0], "{}R".format(color))
            self.set_position([row, 2], "")
            self.set_position([row, 3], "")
            self.set_position([row, 4], "{}K".format(color))

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
                    screen.blit(pieces[col], (x + 5, y + 5))
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
