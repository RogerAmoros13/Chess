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
        # Comer una ficha 
        if self._check_available_square([position[0] + sign, position[1] + 1], True):
            moves.append([position[0] + sign, position[1] + 1])
        if self._check_available_square([position[0] + sign, position[1] - 1], True):
            moves.append([position[0] + sign, position[1] - 1])
        return moves

    def _check_available_square(self, pos, is_pawn_eating=False):
        # Si esta vacia:
            # Si es un peón comiendo --> False
            # Otro caso --> True
        if not self.board[pos[0]][pos[1]]:
            if is_pawn_eating:
                return False
            return True
        # Si no esta vacia:
            # Si es un peón no comiendo --> False
            # Otro caso: color de la casilla que se quiere ocupar vs self.color
        return self.board[pos[0]][pos[1]][1] != self.color 
