import random

piece_scores = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

"""
Random Move Algorithm 
"""
def find_random_move(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


"""
Best move based on material
"""
def find_best_move(gs, validMoves):
    turn_multipler = 1 if gs.whiteTurn else -1
    opponent_minmax_score = CHECKMATE
    best_move = None
    random.shuffle(validMoves)
    for player_move in validMoves:
        gs.make_move(player_move)
        opponents_moves = gs.get_valid_moves()
        if gs.staleMate:
            opponents_max_score = STALEMATE
        elif gs.checkMate:
            opponents_max_score = -CHECKMATE
        else:
            opponents_max_score = -CHECKMATE
            for opponents_move in opponents_moves:
                gs.make_move(opponents_move)
                gs.get_valid_moves
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turn_multipler * material_score(gs.board)
                if score > opponents_max_score:
                    opponents_max_score = score
                gs.undo_move()
            if opponent_minmax_score > opponents_max_score:
                opponent_minmax_score = opponents_max_score
                best_move = player_move
            gs.undo_move()
        return best_move

'''
Helper method for recursive call
'''
def find_best_move_minmax(gs, validMoves):
    global next_move
    next_move = None
    find_minmax_move(gs, validMoves, DEPTH, gs.whiteTurn)
    return next_move
def find_minmax_move(gs, validMoves, depth, whiteTurn):
    global next_move
    if depth == 0:
        return material_score(gs.board)

    if whiteTurn:
        max_score = -CHECKMATE
        for move in validMoves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_minmax_move(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score
    else:
        min_score = CHECKMATE
        for move in validMoves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_minmax_move(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score

def score_board(gs):
    if gs.checkMate:
        if gs.whiteTurn:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += piece_scores[square[1]]
            elif square[0] == 'b':
                score -= piece_scores[square[1]]

    return score


'''
Score the board based on material
'''
def material_score(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_scores[square[1]]
            elif square[0] == 'b':
                score -= piece_scores[square[1]]

    return score