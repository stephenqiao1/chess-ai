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
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '/'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteTurn = not self.whiteTurn

class Move():
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSqr, endSqr, board):
        self.startRow = startSqr[0]
        self.startCol = startSqr[1]
        self.endRow = endSqr[0]
        self.endCol = endSqr[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]


    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)


    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]