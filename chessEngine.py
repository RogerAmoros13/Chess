from tools import lst_sum, lst_diff


class ChessEngine:
    def __init__(self, board):
        self.board = board
        self.kings_moved = {"w": False, "b": False}
        self.kings_position = {"w": (7, 4), "b": (0, 4)}
        self.color = None

    def get_pawn_moves(self, position):
        # Dirección de avance del peón
        color = self.board.get_color(position)
        sign = 1 if color == "b" else -1
        moves = []
        # Avanzar una casilla
        if (
            self._check_available_square_pawn(
                lst_sum(position, [sign, 0]), color)
        ):
            moves.append(lst_sum(position, [sign, 0]))
            # Avanzar dos casillas
            start_file = 6 if color == "w" else 1
            if (
                self._check_available_square_pawn(
                    lst_sum(position, [2 * sign, 0]), color
                ) and position[0] == start_file
            ):
                moves.append(lst_sum(position, [2 * sign, 0]))
        # Comer una ficha en diagonal
        for i in [1, -1]:
            if self._check_available_square_pawn(lst_sum(position, [sign, i]), color, True):
                moves.append(lst_sum(position, [sign, i]))
        return self.check_is_valid_move(position, moves, color)

    def _get_knight_moves(self, pos, color):
        moves = []
        for i in [-2, 2]:
            for j in [-1, 1]:
                if self._check_available_square(lst_sum(pos, [i, j]), color):
                    moves.append(lst_sum(pos, [i, j]))
                if self._check_available_square(lst_sum(pos, [j, i]), color):
                    moves.append(lst_sum(pos, [j, i]))
        return moves

    def get_knight_moves(self, pos, _color=None):
        color = _color or self.board.get_color(pos)
        moves = self._get_knight_moves(pos, color)
        return self.check_is_valid_move(pos, moves, color)

    def get_directional_moves(self, pos, dir, color):
        fw = 1
        square = lst_sum(pos, dir)
        collide = False  # Flag para ver si choca contra una pieza
        moves = []
        while self.is_inside_board(square) and not collide:
            if (
                self._check_available_square(square, color)
            ):
                moves.append(square)
            if self.board.get_piece(square):
                collide = True
            fw += 1
            square = lst_sum(pos, [dir[0] * fw, dir[1] * fw])
        return moves

    def _get_bishop_moves(self, pos, color):
        moves = self.get_directional_moves(pos, [1, 1], color)
        moves += self.get_directional_moves(pos, [-1, 1], color)
        moves += self.get_directional_moves(pos, [1, -1], color)
        moves += self.get_directional_moves(pos, [-1, -1], color)
        return moves

    def get_bishop_moves(self, pos, _color=None):
        color = _color or self.board.get_color(pos)
        moves = self._get_bishop_moves(pos, color)
        return self.check_is_valid_move(pos, moves, color)

    def _get_rook_moves(self, pos, color):
        moves = self.get_directional_moves(pos, [1, 0], color)
        moves += self.get_directional_moves(pos, [-1, 0], color)
        moves += self.get_directional_moves(pos, [0, -1], color)
        moves += self.get_directional_moves(pos, [0, 1], color)
        return moves

    def get_rook_moves(self, pos, _color=None):
        color = _color or self.board.get_color(pos)
        moves = self._get_rook_moves(pos, color)
        return self.check_is_valid_move(pos, moves, color)

    def check_is_valid_move(self, pos, moves, color):
        valid_moves = []
        for move in moves:
            if self.is_check(pos, move, color):
                continue
            valid_moves.append(move)
        return valid_moves

    def get_queen_moves(self, pos):
        moves = self.get_rook_moves(pos)
        moves += self.get_bishop_moves(pos)
        return moves

    def _get_surrounding_moves(self, pos, color):
        moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == pos[0] and j == pos[1]:
                    continue
                if self._check_available_square(lst_sum(pos, [i, j]), color):
                    moves.append(lst_sum(pos, [i, j]))
        return moves

    def get_king_moves(self, pos):
        color = self.board.get_color(pos)
        moves = self._get_surrounding_moves(pos, color)
        sign = 7 if color == "w" else 0
        if not self.kings_moved.get(color) and not self.is_check(pos, pos, color):
            # Enroque corto
            if (
                self.board.is_rook([sign, 7], color)
                and not self.board.get_piece([sign, 6])
                and not self.board.get_piece([sign, 5])
                and not self.is_check(pos, [sign, 5], color)
            ):
                moves.append([sign, 6])
            if (
                self.board.is_rook([sign, 0], color)
                and not self.board.get_piece([sign, 1])
                and not self.board.get_piece([sign, 2])
                and not self.board.get_piece([sign, 3])
                and not self.is_check(pos, [sign, 3], color)
            ):
                moves.append([sign, 2])
        return self.check_is_valid_move(pos, moves, color)

    def _check_available_square_pawn(self, pos, color, eating=False):
        if not self.is_inside_board(pos):
            return False
        if self.board.get_piece(pos):
            if eating:
                return self.board.get_color(pos) != color
            return False
        if not eating:
            return True
        return False

    def _check_available_square(self, pos, color):
        # Comprobar que esta dentro del tablero
        if not self.is_inside_board(pos):
            return False
        if self.board.get_piece(pos):
            return self.board.get_color(pos) != color
        return True

    def is_inside_board(self, pos):
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
            return False
        return True

    def is_check(self, start, end, color):
        piece1 = self.board.get_piece(start)
        piece2 = self.board.get_piece(end)
        if self.board.is_king(start):
            king_pos = end
        else:
            king_pos = self.kings_position.get(color)
        self.board.move_piece(start, end, False)
        bishop_moves = self._get_bishop_moves(king_pos, color)
        rook_moves = self._get_rook_moves(king_pos, color)
        knight_moves = self._get_knight_moves(king_pos, color)
        king_moves = self._get_surrounding_moves(king_pos, color)
        check_squares = []
        for move in bishop_moves:
            if self.board.is_bishop(move) or self.board.is_queen(move):
                check_squares.append(move)
        for move in rook_moves:
            if self.board.is_rook(move) or self.board.is_queen(move):
                check_squares.append(move)
        for move in knight_moves:
            if self.board.is_knight(move):
                check_squares.append(move)
        for move in king_moves:
            if self.board.is_king(move):
                check_squares.append(move)
                continue
            diff = lst_diff(king_pos, move)
            if color == "w" and diff == [-1, -1] or diff == [-1, 1]:
                if self.board.is_pawn(move):
                    check_squares.append(move)
                    continue
            elif diff == [1, -1] or diff == [1, 1]:
                if self.board.is_pawn(move):
                    check_squares.append(move)
        self.board.undo_move(
            {
                "position": start,
                "piece": piece1,
            },
            {
                "position": end,
                "piece": piece2,
            }
        )
        if len(check_squares):
            return True
        return False

    def is_castling(self, pos, color):
        row = 7 if color == "w" else 0
        if self.kings_moved.get(color):
            return ""
        if pos == [row, 6]:
            return "short"
        if pos == [row, 2]:
            return "long"
        return ""

    def get_all_moves(self, player, check_one=True):
        moves = []
        for i in range(self.board.dims):
            for j in range(self.board.dims):
                if self.board.get_color([i, j]) == player.color:
                    moves += player.get_available_moves([i, j])
                    if check_one and moves:
                        return True
        return False
