import pygame
import os
import platform

if platform.system() == "Windows":
    bar = "\\"
else:
    bar = "/"

PATH_TO_PIECES = os.getcwd() + bar + "files" + bar + "pieces"

# Parametros del display.
SIZE = (1200, 800)
SQUARE_SIZE = 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITE_SQUARE = (255, 255, 220)
GREEN = (76, 150, 85)
GREY = (32, 32, 32)
GREY2 = (160, 160, 160)
YELLOW = (255, 255, 102)
BLUE = (0, 102, 255)
BROWN = (125, 100, 75)


def import_images():
    # Función para importar las imagenes de las piezas.
    dir_list = os.listdir(PATH_TO_PIECES)
    piece_vals = {}
    for piece in dir_list:
        name = piece[:2]
        final_path = PATH_TO_PIECES + bar + piece
        file = pygame.image.load(final_path)
        file = pygame.transform.scale(file, (90, 90))
        piece_vals[name] = file
    return piece_vals


def lst_sum(l1, l2):
    # Retorna la suma de dos listas. (Acción recurente)
    return [l1[0] + l2[0], l1[1] + l2[1]]


def lst_diff(l1, l2):
    return [l1[0] - l2[0], l1[1] - l2[1]]


num2let = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
}

# BOARDS

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

BOARD_ONLY_KINGS = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "bK", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "wK", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
]

BOARD_QUEEN = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "bK", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "wQ", "", "", "", "", ""],
    ["", "", "", "wK", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
]
