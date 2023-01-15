"""
Clase para la gestión de los Jugadores
"""

from tools import lst_sum


class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.get_all_moves = False
        self.moved_pawns = []
        self.won_pieces = []

    def get_available_moves(self, position):
        if not self.board.get_piece(position):
            return []
        if self.board.get_color(position) != self.color:
            return []
        # Movimientos disponibles para el peón seleccionado
        if self.board.is_pawn(position):
            return self.get_pawn_moves(position)
        if self.board.is_knight(position):
            return self.get_knight_moves(position)
        if self.board.is_bishop(position):
            return self.get_bishop_moves(position)
        if self.board.is_rock(position):
            return self.get_rock_moves(position)
        if self.board.is_queen(position):
            return self.get_queen_moves(position)
        if self.board.is_king(position):
            return self.get_king_moves(position)
        return []

    def get_all_available_moves(self):
        pass

    def get_pawn_moves(self, position):
        # Dirección de avance del peón
        sign = 1 if self.board.get_color(position) == "b" else -1
        moves = []
        # Avanzar una casilla
        if self._check_available_square_pawn(lst_sum(position, [sign, 0])):
            moves.append(lst_sum(position, [sign, 0]))
            # Avanzar dos casillas
            if (
                self._check_available_square_pawn(
                    lst_sum(position, [2 * sign, 0])
                ) and self.board.get_piece(position) not in self.moved_pawns
            ):
                moves.append(lst_sum(position, [2 * sign, 0]))
        # Comer una ficha en diagonal
        for i in [1, -1]:
            if self._check_available_square_pawn(lst_sum(position, [sign, i]), True):
                moves.append(lst_sum(position, [sign, i]))
        return moves

    def get_knight_moves(self, pos):
        moves = []
        for i in [-2, 2]:
            for j in [-1, 1]:
                if self._check_available_square(lst_sum(pos, [i, j])):
                    moves.append(lst_sum(pos, [i, j]))
                if self._check_available_square(lst_sum(pos, [j, i])):
                    moves.append(lst_sum(pos, [j, i]))
        return moves

    def get_directional_moves(self, pos, dir):
        fw = 1
        square = lst_sum(pos, dir)
        collide = False  # Flag para ver si choca contra una pieza
        moves = []
        while self.is_inside_board(square) and not collide:
            if self._check_available_square(square):
                moves.append(square)
            if self.board.get_piece(square):
                collide = True
            fw += 1
            square = lst_sum(pos, [dir[0] * fw, dir[1] * fw])
        return moves

    def get_bishop_moves(self, pos):
        moves = self.get_directional_moves(pos, [1, 1])
        moves += self.get_directional_moves(pos, [-1, 1])
        moves += self.get_directional_moves(pos, [1, -1])
        moves += self.get_directional_moves(pos, [-1, -1])
        return moves

    def get_rock_moves(self, pos):
        moves = self.get_directional_moves(pos, [1, 0])
        moves += self.get_directional_moves(pos, [-1, 0])
        moves += self.get_directional_moves(pos, [0, -1])
        moves += self.get_directional_moves(pos, [0, 1])
        return moves

    def get_queen_moves(self, pos):
        moves = self.get_rock_moves(pos)
        moves += self.get_rock_moves(pos)
        return moves
    
    def get_king_moves(self, pos):
        moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == pos[0] and j == pos[1]:
                    continue
                if self._check_available_square(lst_sum(pos, [i, j])):
                    moves.append(lst_sum(pos, [i, j]))
        return moves


    def _check_available_square_pawn(self, pos, eating=False):
        if not self.is_inside_board(pos):
            return False
        if self.board.get_piece(pos):
            if eating:
                return self.board.get_color(pos) != self.color
            return False
        if not eating:
            return True
        return False

    def _check_available_square(self, pos):
        # Comprobar que esta dentro del tablero
        if not self.is_inside_board(pos):
            return False
        if self.board.get_piece(pos):
            return self.board.get_color(pos) != self.color
        return True

    def is_inside_board(self, pos):
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
            return False
        return True
