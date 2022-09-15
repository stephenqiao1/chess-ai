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
        self.whiteKingSquare = (7, 4)
        self.blackKingSquare = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()  # position for the where an enpassant capture possible
        self.current_castling_right = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_right.wks, self.current_castling_right.bks,
                                               self.current_castling_right.wqs, self.current_castling_right.bqs)]


    def make_move(self, move):
        self.board[move.startRow][move.startCol] = '/'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteTurn = not self.whiteTurn  # swap players
        if move.pieceMoved == 'wK':  # update the white king's position
            self.whiteKingSquare = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':  # update the black king's position
            self.blackKingSquare = (move.endRow, move.endCol)

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # enpassant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '/'

        # updating enpassantPossible
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        # castling
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # kingside
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '/'
            else:  # queenside
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '/'


        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_right.wks, self.current_castling_right.bks,
                                             self.current_castling_right.wqs, self.current_castling_right.bqs))

    """
    Undo move
    """
    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteTurn = not self.whiteTurn
            if move.pieceMoved == 'wK':  # update white king's position
                self.whiteKingSquare = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':  # update black king's position
                self.blackKingSquare = (move.startRow, move.startCol)
            if move.isEnpassantMove:  # undo en passant
                self.board[move.endRow][move.endCol] = '/'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # undo csatling rights
            self.castle_rights_log.pop()
            self.current_castling_right = self.castle_rights_log[-1]

            # undo castle
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: # kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '/'
                else: # queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '/'


    def update_castle_rights(self, move):  # update the castle rights given a move
        if move.pieceMoved == 'wK':
            self.current_castling_right.wks = False
            self.current_castling_right.wqs = False
        elif move.pieceMoved == 'bK':
            self.current_castling_right.bks = False
            self.current_castling_right.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.current_castling_right.wqs = False
                elif move.startCol == 7:  # right rook
                    self.current_castling_right.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.current_castling_right.bqs = False
                elif move.startCol == 7:  # right rook
                    self.current_castling_right.bks = False


    def get_valid_moves(self):
        tempEnpassantPossible = self.enpassantPossible
        temp_castle_rights = CastleRights(self.current_castling_right.wks, self.current_castling_right.bks,
                                          self.current_castling_right.wqs, self.current_castling_right.bqs)
        moves = self.get_all_possible_moves()  # generate all possible moves
        if self.whiteTurn:
            self.get_castle_moves(self.whiteKingSquare[0], self.whiteKingSquare[1], moves)
        else:
            self.get_castle_moves(self.blackKingSquare[0], self.blackKingSquare[1], moves)
        for i in range(len(moves)-1, -1, -1):  # for each move, make the move
            self.make_move(moves[i])
            self.whiteTurn = not self.whiteTurn  # generate all opponent moves, and determine if they check your king
            if self.in_check():  # if they do check your king, not a valid move
                moves.remove(moves[i])
            self.whiteTurn = not self.whiteTurn
            self.undo_move()
        if len(moves) == 0:  # checks if there is checkmate or stalemate
            if self.in_check():
                self.checkMate = True
            else:
                self.staleMate = True

        self.enpassantPossible = tempEnpassantPossible
        self.current_castling_right = temp_castle_rights
        return moves

    """
    Determine if the player is in check
    """
    def in_check(self):
        if self.whiteTurn:
            return self.square_under_attack(self.whiteKingSquare[0], self.whiteKingSquare[1])
        else:
            return self.square_under_attack(self.blackKingSquare[0], self.blackKingSquare[1])


    def square_under_attack(self, row, col):
        self.whiteTurn = not self.whiteTurn
        enemy_moves = self.get_all_possible_moves()
        self.whiteTurn = not self.whiteTurn
        for move in enemy_moves:
            if move.endRow == row and move.endCol == col:
                return True
        return False
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
                elif (row-1, col-1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row-1, col-1), self.board, isEnpassantMove=True))
            if col + 1 <= 7:  # capturing a piece on the right
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))
                elif (row - 1, col + 1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, isEnpassantMove=True))

        else:  # black pawn's turn
            if self.board[row+1][col] == '/':
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '/':
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col - 1 >= 0:  # capturing a piece on the left
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
                elif (row+1, col-1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row+1, col-1), self.board, isEnpassantMove=True))
            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))
                elif (row+1, col+1) == self.enpassantPossible:
                    moves.append(Move((row, col), (row+1, col+1), self.board, isEnpassantMove=True))


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


    def get_castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return
        if (self.whiteTurn and self.current_castling_right.wks) or (not self.whiteTurn and self.current_castling_right.bks):
            self.get_kingside_castle_moves(row, col, moves)
        if (self.whiteTurn and self.current_castling_right.wqs) or (not self.whiteTurn and self.current_castling_right.bqs):
            self.get_queenside_castle_moves(row, col, moves)


    def get_kingside_castle_moves(self, row, col, moves):
        if self.board[row][col+1] == '/' and self.board[row][col+2] == '/':
            if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, isCastleMove=True))

    def get_queenside_castle_moves(self, row, col, moves):
        if self.board[row][col-1] == '/' and self.board[row][col-2] == '/' and self.board[row][col-3]:
            if not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, isCastleMove=True))
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
class Move():
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSqr, endSqr, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSqr[0]
        self.startCol = startSqr[1]
        self.endRow = endSqr[0]
        self.endCol = endSqr[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        # en passant
        self.isEnpassantMove = isEnpassantMove
        self.isCastleMove = isCastleMove
        if self.isEnpassantMove:
            self.pieceCaptured == 'wP' if self.pieceMoved == 'bP' else 'bP'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)


    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]