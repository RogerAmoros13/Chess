"""
Clase para la gestión de los Jugadores
"""


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
        return []

    def get_all_available_moves(self):
        pass

    def get_pawn_moves(self, position):
        # Dirección de avance del peón
        sign = 1 if self.board.get_color(position) == "b" else -1
        moves = []
        # Avanzar una casilla
        if self._check_available_square([position[0] + sign, position[1]]):
            moves.append([position[0] + sign, position[1]])
            # Avanzar dos casillas
            if (
                self._check_available_square([position[0] + sign * 2, position[1]])
                and self.board.get_piece(position) not in self.moved_pawns
            ):
                moves.append([position[0] + sign * 2, position[1]])
        # Comer una ficha en diagonal
        if self._check_available_square([position[0] + sign, position[1] + 1], True):
            moves.append([position[0] + sign, position[1] + 1])
        if self._check_available_square([position[0] + sign, position[1] - 1], True):
            moves.append([position[0] + sign, position[1] - 1])
        return moves

    def _check_available_square(self, pos, is_pawn_eating=False):
        # Si esta vacia:
            # Si es un peón comiendo --> False
            # Otro caso --> True
        if not self.board.get_piece(pos):
            if is_pawn_eating:
                return False
            return True
        # Si no esta vacia:
            # Si es un peón no comiendo --> False
            # Otro caso: color de la casilla que se quiere ocupar vs self.color
        if not is_pawn_eating:
            return False
        return self.board.get_color(pos) != self.color 
