"""
Clase para la gestión de los Jugadores
"""

from tools import lst_sum


class Player:
    def __init__(self, chess_engine, color):
        self.board = chess_engine.board
        self.chess = chess_engine
        self.color = color
        self.won_pieces = []

    def get_available_moves(self, position):
        if not self.board.get_piece(position):
            return []
        if self.board.get_color(position) != self.color:
            return []
        # Movimientos disponibles para el peón seleccionado
        if self.board.is_pawn(position):
            return self.chess.get_pawn_moves(position)
        elif self.board.is_knight(position):
            return self.chess.get_knight_moves(position)
        elif self.board.is_bishop(position):
            return self.chess.get_bishop_moves(position)
        elif self.board.is_rook(position):
            return self.chess.get_rook_moves(position)
        elif self.board.is_queen(position):
            return self.chess.get_queen_moves(position)
        elif self.board.is_king(position):
            return self.chess.get_king_moves(position)
        return []

    def get_all_available_moves(self):
        pass
