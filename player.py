"""
Clase para la gestión de los Jugadores
"""

AI_dict = {
    "human": "Humano",
    "min_max": "Algoritmo Min Max",
    "dummy": "Joe Bidden",
}


class Player:
    def __init__(self, chess_engine, color, brain="human"):
        self.board = chess_engine.board
        self.chess = chess_engine
        self.color = color
        self.brain = brain
        self.won_pieces = []
        self.color_name = "Blancas" if color == "w" else "Negras"
        self.display_brain = AI_dict[brain]

    def get_available_moves(self, position):
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
