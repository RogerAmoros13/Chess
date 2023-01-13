"""
Clase para la gestión de los Jugadores
"""


class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.get_all_moves = False
        self.moved_pawns = []

    def get_available_moves(self, position):
        piece_code = self.board[position[0]][position[1]]
        if not piece_code:
            return []
        if piece_code[1] != self.color:
            return []
        # Movimientos disponibles para el peón seleccionado
        if piece_code[-1] == "P":
            return self.get_pawn_moves(position, piece_code)
        return

    def get_all_available_moves(self):
        pass

    def get_pawn_moves(self, position, piece_code):
        # Dirección de avance del peón
        sign = 1 if piece_code[1] == "b" else -1
        moves = []
        # Avanzar una casilla
        if self._check_available_square([position[0] + sign, position[1]]):
            moves.append([position[0] + sign, position[1]])
        # Avanzar dos casillas
        if (
            self._check_available_square([position[0] + sign * 2, position[1]])
            and piece_code not in self.moved_pawns
        ):
            moves.append([position[0] + sign * 2, position[1]])
        return moves

    def _check_available_square(self, pos):
        # Comprueba si la casilla esta vacia o esta ocupada por una pieza contraria
        if not self.board[pos[0]][pos[1]]:
            return True
        return self.board[pos[0]][pos[1]][1] != self.color 