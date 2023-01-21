from tools import lst_sum, lst_diff, num2let


class ChessEngine:
    def __init__(self, board):
        self.board = board
        self.kings_moved = {"w": False, "b": False}
        self.kings_position = self.get_initial_king_position()
        self.color = None
        self.en_passant = None
        self.check = False
        self.check_mate = False
        self.stalemate = False
        self.end_game = False
        self.round = 1
        self.logs = []

    def get_initial_king_position(self):
        kings_pos = {}
        for i in range(self.board.dims):
            for j in range(self.board.dims):
                if self.board.is_king([i, j]):
                    kings_pos.update(
                        {self.board.get_color([i, j]): (i, j)}
                    )
        return kings_pos

    def get_pawn_moves(self, pos):
        # Dirección de avance del peón
        sign = 1 if self.color == "b" else -1
        moves = []
        # Avanzar una casilla
        if (
            self._check_available_square_pawn(
                lst_sum(pos, [sign, 0]))
        ):
            moves.append(lst_sum(pos, [sign, 0]))
            # Avanzar dos casillas
            start_file = 6 if self.color == "w" else 1
            if (
                self._check_available_square_pawn(
                    lst_sum(pos, [2 * sign, 0])
                ) and pos[0] == start_file
            ):
                moves.append(lst_sum(pos, [2 * sign, 0]))
        # Comer una ficha en diagonal
        for i in [1, -1]:
            if self._check_available_square_pawn(lst_sum(pos, [sign, i]), True):
                moves.append(lst_sum(pos, [sign, i]))
            # Comer al paso
            if self.en_passant or self.en_passant == 0:
                passant_row = 3 if self.color == "w" else 4
                if pos[0] == passant_row and pos[1] + i == self.en_passant:
                    moves.append(lst_sum(pos, [sign, i]))
        return self.check_is_valid_move(pos, moves)

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
        if self.board.is_king(start):
            king_pos = end
        else:
            king_pos = self.kings_position.get(self.color)
        vals = self.do_move(start, end, False)
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
        self.board.undo_move(vals)
        if len(check_squares):
            return True
        return False

    def is_castling(self, pos):
        row = 7 if self.color == "w" else 0
        if (
            self.kings_moved.get(self.color)
            or self.kings_position["w"] != (7, 4)
            or self.kings_position["b"] != (0, 4)
        ):
            return ""
        if pos == [row, 6]:
            return "short"
        if pos == [row, 2]:
            return "long"
        return ""

    def is_en_passant(self, start, end):
        if (
            (self.en_passant or self.en_passant == 0)
            and abs(start[1] - end[1]) == 1
            and self.board.is_pawn(lst_sum(start, [0, end[1] - start[1]]))
        ):
            return True
        return False

    def get_available_moves(self, position):
        # Movimientos disponibles para el peón seleccionado
        if self.board.is_pawn(position):
            return self.get_pawn_moves(position)
        elif self.board.is_knight(position):
            return self.get_knight_moves(position)
        elif self.board.is_bishop(position):
            return self.get_bishop_moves(position)
        elif self.board.is_rook(position):
            return self.get_rook_moves(position)
        elif self.board.is_queen(position):
            return self.get_queen_moves(position)
        elif self.board.is_king(position):
            return self.get_king_moves(position)
        return []

    def get_all_moves(self, check_one=True):
        moves = []
        for i in range(self.board.dims):
            for j in range(self.board.dims):
                if self.board.is_color([i, j], self.color):
                    av_moves = self.get_available_moves([i, j])
                    if check_one and av_moves:
                        return True
                    elif av_moves:
                        for move in av_moves:
                            moves.append(
                                {
                                    "start": [i, j],
                                    "end": move,
                                }
                            )
        if check_one:
            return False
        return moves

    def update_variables(self, color, en_passant):
        self.en_passant = en_passant
        self.color = color

    def do_move(self, start, end, real=True):
        """
        Inputs: 
            start [x, y]: Posición de partida.
            end [x, y]: Posición de llegada.
            real bool: Para comprovar si un movimiento provoca o no jaque
                       se actualiza el tablero a través de esta función y se comprueba 
                       si hay jaque. Como no queremos que actualice las 
                       variables de estado diferenciamos entre un movimiento 
                       'real' o 'no real'.

        Outputs:
            vals dict: Diccionario con la información del movimiento: 
                vals = {
                    "round": ronda,
                    "start_square": posición de partida,
                    "end_square": posición de llegada,
                    "moved_piece": pieza que se mueve,
                    "eaten_piece": si en la posición de llagada hay una pieza,
                    "castling": si se ha enrocado,
                    "promotion": si se ha promocionado un peón,
                    "en_passant": si se ha comido al paso,
                    "check": si hay jaque,
                    "check_mate": si hay jaque mate,
                    "stalemate": si hay tablas,
                    "color": color del que mueve,
                }

        """

        next_move_color = "b" if self.color == "w" else "w"
        is_en_passant = False
        castle = ""
        is_promotion = False
        is_en_passant = False
        moved_piece = self.board.get_piece(start)

        vals = {
            "round": self.round,
            "start_square": start,
            "end_square": end,
            "moved_piece": moved_piece,
            "color": self.color,
        }
        # Se come pieza?
        eat = ""
        if self.board.get_piece(end):
            eat = self.board.get_piece(end)
        # Posibilidades de mover el rey
        if self.board.is_king(start):
            if real:
                self.kings_moved.update({self.color: True})
                self.kings_position.update(
                    {self.color: (end[0], end[1])}
                )
            castle = self.is_castling(end)
        # Gestión de comer al paso
        if self.is_en_passant(start, end):
            is_en_passant = True
            eat = self.board.get_piece(lst_sum(start, [0, end[1] - start[1]]))
        if self.board.is_pawn(start):
            if abs(start[0] - end[0]) == 2:
                self.en_passant = start[1]
            if end[0] in [0, 7]:
                is_promotion = True
        # Promoción de peón y variable en_passant
        vals.update(
            {
                "eaten_piece": eat,
                "castling": castle,
                "promotion": is_promotion,
                "en_passant": is_en_passant,
            }
        )
        self.board.move_piece(vals)
        if real:
            self.color = next_move_color
            self.round += 1
            vals.update(self.check_endgame(real))
            vals = self.log_move(vals)
        return vals

    def check_endgame(self, real_move=False):
        check = self.is_check([0, 0], [0, 0])
        end_game = False
        check_mate = False
        stalemate = False
        if not self.get_all_moves():
            end_game = True
            if check:
                check_mate = True
            else:
                stalemate = True
        if real_move:
            self.check = check
            self.stalemate = stalemate
            self.check_mate = check_mate
            self.end_game = end_game
        return {
            "check": check,
            "check_mate": check_mate,
            "stalemate": stalemate,
        }

    def log_move(self, vals):
        start = vals.get("start_square")
        end = vals.get("end_square")
        count = vals.get("round")
        moved_piece = vals.get("moved_piece")
        eaten_piece = vals.get("eaten_piece")
        if vals["castling"]:
            log = "{}. O-O".format(count)
            if vals["castling"] == "long":
                log += "-O".format(count)
        else:
            log = "{}. {}{}{}  {}{}".format(
                count,
                moved_piece[1],
                num2let[start[1]],
                8 - start[0],
                num2let[end[1]],
                8 - end[0],
            )
        if eaten_piece:
            log += "x" + eaten_piece[1]
        if vals["check"]:
            log += "+"
        if vals["check_mate"]:
            log += "+"
        if vals["stalemate"]:
            log += " 1/2 - 1/2"
            
        vals.update({"log": log})
        self.logs.append(vals)
        return vals
