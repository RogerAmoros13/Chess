import pygame
import os

PATH_TO_PIECES = os.getcwd() + "\\files\\pieces"

# Parametros del display.
SIZE = (1200, 800)
SQUARE_SIZE = 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITE_SQUARE = (255, 255, 220)
GREEN = (76, 150, 85)
GREY  = (32, 32, 32)
GREY2 = (160, 160, 160)

# Definición y estado inicial del tablero
BOARD = [
    ["1bR", "1bN", "1bB", "1bQ", "1bK", "1bB", "1bN", "1bR"],
    ["1bP", "2bP", "3bP", "4bP", "5bP", "6bP", "7bP", "8bP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["1wP", "2wP", "3wP", "4wP", "5wP", "6wP", "7wP", "8wP"],
    ["1wR", "1wN", "1wB", "0wQ", "0wK", "2wB", "2wN", "2wR"],
]

def import_images():
    # Función para importar las imagenes de las piezas.
    dir_list = os.listdir(PATH_TO_PIECES)
    piece_vals = {}
    for piece in dir_list:
        name = piece[:2]
        final_path = PATH_TO_PIECES + "\\" + piece
        file = pygame.image.load(final_path)
        file = pygame.transform.scale(file, (90, 90))
        piece_vals[name] = file
    return piece_vals
