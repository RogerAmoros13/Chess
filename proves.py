
BOARD_BASIC = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
]

def print_board(board):
    for i in range(8):
        print(board[i])

new_board = []
for i in range(8):
    row = []
    for j in range(8):
        row.append(BOARD_BASIC[7-i][7-j])
    new_board.append(row)

BOARD_BASIC = new_board

print_board(BOARD_BASIC)