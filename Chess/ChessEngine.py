"""
Stores all the information about the current state of the chess game. Will also determine the valid moves at
the current state and include a move log.
"""

class ChessState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["/", "/", "/", "/", "/", "/", "/", "/"],
            ["/", "/", "/", "/", "/", "/", "/", "/"],
            ["/", "/", "/", "/", "/", "/", "/", "/"],
            ["/", "/", "/", "/", "/", "/", "/", "/"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        self.whiteTurn = True
        self.moveLog = []
