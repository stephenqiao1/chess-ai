"""
Displays the board
"""

import pygame as p
from Chess import ChessEngine, AIMoves

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
    validMoves = gs.get_valid_moves()
    moveMade = False  # set to true when a move is made
    sqrSelected = ()  # keep track of the last click of the user (tuple: (rank, file))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    player_one = False  # true if human is playing white, vice versa
    player_two = False
    pieces = ['wP', 'wR', 'wN', 'wK', 'wB', 'wQ', 'bP', 'bR', 'bN', 'bK', 'bB', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    running = True
    while running:
        humanTurn = (gs.whiteTurn and player_one) or (not gs.whiteTurn and player_two)
        for e in p.event.get():  # Loops through every event in the queue
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if humanTurn:
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
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.make_move(validMoves[i])
                                moveMade = True
                                sqrSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks= [sqrSelected]
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        gs.undo_move()
                        moveMade = True

            # AI Move
            if not humanTurn:
                ai_move = AIMoves.find_best_move_minmax(gs, validMoves)
                if ai_move is None:
                    ai_move = AIMoves.find_random_move(validMoves)
                gs.make_move(ai_move)
                moveMade = True

            if moveMade:
                validMoves = gs.get_valid_moves()
                moveMade = False

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
