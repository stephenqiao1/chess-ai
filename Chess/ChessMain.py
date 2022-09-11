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

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = ChessEngine.ChessState()
    pieces = ['wP', 'wR', 'wN', 'wK', 'wB', 'wQ', 'bP', 'bR', 'bN', 'bK', 'bB', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    running = True
    while running:
        for e in p.event.get(): #Loops through every event in the queue
            if e.type == p.QUIT:
                running = False
            drawBoard(screen, gs.board)
            clock.tick(MAX_FPS)
            p.display.flip() #updates the display

def drawBoard(screen, board):
    colors = [p.Color("antiquewhite"), p.Color("bisque4")] #antiquewhite will act as the white square, and bisque4 as black
    for rank in range(DIMENSION):
        for file in range(DIMENSION):
            if (rank + file) % 2 == 0:
                color = colors[0]
            else:
                color = colors[1]
            p.draw.rect(screen, color, p.Rect(file*SQ_SIZE, rank*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board[rank][file]
            if piece != "/":
                screen.blit(IMAGES[piece], p.Rect(file*SQ_SIZE, rank*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()





