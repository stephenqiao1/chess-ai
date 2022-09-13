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
        self.moveFunctions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                              'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
    def make_move(self, move):
        self.board[move.startRow][move.startCol] = '/'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteTurn = not self.whiteTurn


    """
    Undo move
    """
    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteTurn = not self.whiteTurn


    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteTurn) or (turn == 'b' and not self.whiteTurn):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)
        return moves


    """
    Get all the pawn moves for the pawn located at row col, and add to the list
    """
    def get_pawn_moves(self, row, col, moves):
        if self.whiteTurn:  # white pawn's turn
            if self.board[row - 1][col] == '/':  # pawn advances one square
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '/':  # pawn advances two squares
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col - 1 >= 0:  # capturing a piece on the left
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col + 1 <= 7:  # capturing a piece on the right
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))

        else:  # black pawn's turn
            if self.board[row+1][col] == '/':
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '/':
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col - 1 >= 0:  # capturing a piece on the left
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))


    """
    Get all the rook moves for the rook located at row col, and add to the list
    """
    def get_rook_moves(self, row, col, moves):
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        enemy_color = "b" if self.whiteTurn else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '/':  # empty space
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # enemy piece
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:  # friendly piece
                        break
                else:
                    break

    """
    Get all the knight moves for the rook located at row col, and add to the list
    """
    def get_knight_moves(self, row, col, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = "w" if self.whiteTurn else "b"
        for m in directions:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    """
    Get all the bishop moves for the rook located at row col, and add to the list
    """
    def get_bishop_moves(self, row, col, moves):
        directions = ((-1, 1), (1, 1), (1, -1), (-1, -1))
        enemy_color = "b" if self.whiteTurn else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '/':
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    """
    Get all the queen moves for the rook located at row col, and add to the list
    """
    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    """
    Get all the king moves for the rook located at row col, and add to the list
    """
    def get_king_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.whiteTurn else "b"
        for i in range(8):
            end_row = row + directions[i][0]
            end_col = col + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

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
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)


    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]