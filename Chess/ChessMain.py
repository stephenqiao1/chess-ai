"""
Displays the board
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}
currMoves = ()

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = ChessEngine.ChessState()
    sqrSelected = ()  # keep track of the last click of the user (tuple: (rank, file))
    playerClicks = [] # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    pieces = ['wP', 'wR', 'wN', 'wK', 'wB', 'wQ', 'bP', 'bR', 'bN', 'bK', 'bB', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    running = True
    while running:
        for e in p.event.get():  # Loops through every event in the queue
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqrSelected == (row, col):
                    sqrSelected = ()
                    playerClicks = []
                else:
                    sqrSelected = (row, col)
                    playerClicks.append(sqrSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.makeMove(move)
                    sqrSelected = ()
                    playerClicks = []

            draw_board(screen, gs.board)
            clock.tick(MAX_FPS)
            p.display.flip()  # updates the display

def draw_board(screen, board):
    colors = [p.Color("antiquewhite"), p.Color("bisque4")]  # antiquewhite will act as the white square, and bisque4
                                                            # as black
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if (row + col) % 2 == 0:
                color = colors[0]
            else:
                color = colors[1]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board[row][col]
            if piece != "/":
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
