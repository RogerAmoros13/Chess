from tools import lst_sum, lst_diff


class ChessEngine:
    def __init__(self, board):
        self.board = board
        self.kings_moved = {"w": False, "b": False}
        self.kings_position = {"w": (7, 4), "b": (0, 4)}
        self.color = None

    def get_pawn_moves(self, position):
        # Dirección de avance del peón
        sign = 1 if self.color == "b" else -1
        moves = []
        # Avanzar una casilla
        if (
            self._check_available_square_pawn(
                lst_sum(position, [sign, 0]))
        ):
            moves.append(lst_sum(position, [sign, 0]))
            # Avanzar dos casillas
            start_file = 6 if self.color == "w" else 1
            if (
                self._check_available_square_pawn(
                    lst_sum(position, [2 * sign, 0])
                ) and position[0] == start_file
            ):
                moves.append(lst_sum(position, [2 * sign, 0]))
        # Comer una ficha en diagonal
        for i in [1, -1]:
            if self._check_available_square_pawn(lst_sum(position, [sign, i]), True):
                moves.append(lst_sum(position, [sign, i]))
        return self.check_is_valid_move(position, moves)

    def _get_knight_moves(self, pos):
        moves = []
        for i in [-2, 2]:
            for j in [-1, 1]:
                if self._check_available_square(lst_sum(pos, [i, j])):
                    moves.append(lst_sum(pos, [i, j]))
                if self._check_available_square(lst_sum(pos, [j, i])):
                    moves.append(lst_sum(pos, [j, i]))
        return moves

    def get_knight_moves(self, pos):
        moves = self._get_knight_moves(pos)
        return self.check_is_valid_move(pos, moves)

    def get_directional_moves(self, pos, dir):
        fw = 1
        square = lst_sum(pos, dir)
        collide = False  # Flag para ver si choca contra una pieza
        moves = []
        while self.is_inside_board(square) and not collide:
            if (
                self._check_available_square(square)
            ):
                moves.append(square)
            if self.board.get_piece(square):
                collide = True
            fw += 1
            square = lst_sum(pos, [dir[0] * fw, dir[1] * fw])
        return moves

    def _get_bishop_moves(self, pos):
        moves = self.get_directional_moves(pos, [1, 1])
        moves += self.get_directional_moves(pos, [-1, 1])
        moves += self.get_directional_moves(pos, [1, -1])
        moves += self.get_directional_moves(pos, [-1, -1])
        return moves

    def get_bishop_moves(self, pos):
        moves = self._get_bishop_moves(pos)
        return self.check_is_valid_move(pos, moves)

    def _get_rook_moves(self, pos):
        moves = self.get_directional_moves(pos, [1, 0])
        moves += self.get_directional_moves(pos, [-1, 0])
        moves += self.get_directional_moves(pos, [0, -1])
        moves += self.get_directional_moves(pos, [0, 1])
        return moves

    def get_rook_moves(self, pos):
        moves = self._get_rook_moves(pos)
        return self.check_is_valid_move(pos, moves)

    def check_is_valid_move(self, pos, moves):
        valid_moves = []
        for move in moves:
            if self.is_check(pos, move):
                continue
            valid_moves.append(move)
        return valid_moves

    def get_queen_moves(self, pos):
        moves = self.get_rook_moves(pos)
        moves += self.get_bishop_moves(pos)
        return moves

    def _get_surrounding_moves(self, pos):
        moves = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == pos[0] and j == pos[1]:
                    continue
                if self._check_available_square(lst_sum(pos, [i, j])):
                    moves.append(lst_sum(pos, [i, j]))
        return moves

    def get_king_moves(self, pos):
        moves = self._get_surrounding_moves(pos)
        sign = 7 if self.color == "w" else 0
        if not self.kings_moved.get(self.color) and not self.is_check(pos, pos):
            # Enroque corto
            if (
                self.board.is_rook([sign, 7], self.color)
                and not self.board.get_piece([sign, 6])
                and not self.board.get_piece([sign, 5])
                and not self.is_check(pos, [sign, 5])
            ):
                moves.append([sign, 6])
            if (
                self.board.is_rook([sign, 0], self.color)
                and not self.board.get_piece([sign, 1])
                and not self.board.get_piece([sign, 2])
                and not self.board.get_piece([sign, 3])
                and not self.is_check(pos, [sign, 3])
            ):
                moves.append([sign, 2])
        return self.check_is_valid_move(pos, moves)

    def _check_available_square_pawn(self, pos, eating=False):
        if not self.is_inside_board(pos):
            return False
        if self.board.get_piece(pos):
            if eating:
                return not self.board.is_color(pos, self.color)
            return False
        if not eating:
            return True
        return False

    def _check_available_square(self, pos):
        # Comprobar que esta dentro del tablero
        if not self.is_inside_board(pos):
            return False
        if self.board.get_piece(pos):
            return not self.board.is_color(pos, self.color)
        return True

    def is_inside_board(self, pos):
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
            return False
        return True

    def is_check(self, start, end):
        piece1 = self.board.get_piece(start)
        piece2 = self.board.get_piece(end)
        if self.board.is_king(start):
            king_pos = end
        else:
            king_pos = self.kings_position.get(self.color)
        self.board.move_piece(start, end, False)
        bishop_moves = self._get_bishop_moves(king_pos)
        rook_moves = self._get_rook_moves(king_pos)
        knight_moves = self._get_knight_moves(king_pos)
        king_moves = self._get_surrounding_moves(king_pos)
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
            if self.color == "w" and diff == [-1, -1] or diff == [-1, 1]:
                if self.board.is_pawn(move):
                    check_squares.append(move)
                    continue
            elif diff == [1, -1] or diff == [-1, -1]:
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
                if self.board.is_color([i, j], player.color):
                    moves += player.get_available_moves([i, j])
                    if check_one and moves:
                        return True
        return False

    def change_color(self, color):
        self.color = color
