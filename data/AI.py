import _pickle as cPickle

import pygame


def evaluate_board(board):
    piece_values = {'P': 1, 'K': 3, 'B': 3, 'R': 5, 'Q': 9, 'X': 0}
    score = 0

    board.checkmated()

    if board.winner is not None:
        if board.winner == 'black':
            score += 100000
        elif board.winner == 'white':
            score -= 100000
        else:
            score -= 100

    if board.in_check == 'black':
        score -= 9
    elif board.in_check == 'white':
        score += 9

    for row in board.tiles:
        for tile in row:
            piece = tile.piece
            if piece is not None:
                value = piece_values.get(piece.piece_id.upper(), 0)
                if piece.color == 'black':
                    score += value * 10
                    if piece.piece_id != "P" and piece.piece_id != "X":
                        if piece.y < 2 and not piece.ever_moved:
                            score -= 3
                    elif piece.piece_id == "P":
                        pawn_values = {0:0, 1:0, 2:0, 3: 1, 4: 1, 5: 3, 6: 7}
                        score += pawn_values.get(piece.y)
                else:
                    score -= value * 10
                    if piece.piece_id != "P" and piece.piece_id != "X":
                        if piece.y > 5 and not piece.ever_moved:
                            score += 3
                    elif piece.piece_id == "P":
                        pawn_values = {1:7, 2:3, 3: 1, 4: 1, 5: 0, 6: 0}
                        score -= pawn_values.get(piece.y)
    center_bonus = {'P': 3, 'K': 2, 'B': 2, 'R': 1, 'Q': 0, 'X': -5}  # Scale bonuses
    center_tiles = [(3, 3), (3, 4), (4, 3), (4, 4)]

    for x, y in center_tiles:
        piece = board.tiles[x][y].piece
        if piece is not None:
            bonus = center_bonus.get(piece.piece_id.upper(), 0)
            score += bonus if piece.color == 'black' else -bonus
    return score

def should_extend_depth(board, depth,  from_tile, to_tile):
    if depth != 1:
        return False
    if to_tile.piece is not None:
        return True
    return False

def minimax(board, depth, alpha, beta, maximizing_player, extra_depth = 0):
    board.checkmated()
    if depth == 0 or extra_depth == 1 or board.winner is not None:
        return evaluate_board(board), None

    only_eval_captures = False

    if extra_depth > 0:
        only_eval_captures = True

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        moves = []
        for row in board.tiles:
            for piece_tile in row:
                if piece_tile.piece is not None:
                    if piece_tile.piece.color == 'black':
                        for to_tile in piece_tile.piece.get_legal_moves(board, True):
                            if only_eval_captures:
                                if to_tile.piece is not None:
                                    moves.append((piece_tile, to_tile))
                            else:
                                moves.append((piece_tile, to_tile))
        converted_moves = []
        for move in moves:
            new_move = ((move[0].x_coord, move[0].y_coord), (move[1].x_coord, move[1].y_coord))
            converted_moves.append(new_move)
        move_tiles = converted_moves
        if not move_tiles:
            return evaluate_board(board), None
        for move in move_tiles:
            new_board = cPickle.loads(cPickle.dumps(board, -1))
            from_coord, to_coord = move
            from_tile = new_board.get_tile(from_coord[0], from_coord[1])
            to_tile = new_board.get_tile(to_coord[0], to_coord[1])
            piece = from_tile.piece

            new_board.move_piece(piece, to_tile)

            if should_extend_depth(new_board, depth, from_tile, to_tile):
                eval_score, _ = minimax(new_board, depth, alpha, beta, False, extra_depth + 1)
            else:
                eval_score, _ = minimax(new_board, depth - 1, alpha, beta, False)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = ((from_tile.x_coord, from_tile.y_coord), (to_tile.x_coord, to_tile.y_coord))
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        moves = []
        for row in board.tiles:
            for piece_tile in row:
                if piece_tile.piece is not None:
                    if piece_tile.piece.color == 'white':
                        for to_tile in piece_tile.piece.get_legal_moves(board, True):
                            if only_eval_captures:
                                if to_tile.piece is not None:
                                    moves.append((piece_tile, to_tile))
                            else:
                                moves.append((piece_tile, to_tile))
        converted_moves = []
        for move in moves:
            new_move = ((move[0].x_coord, move[0].y_coord), (move[1].x_coord, move[1].y_coord))
            converted_moves.append(new_move)
        move_tiles = converted_moves
        if not move_tiles:
            return evaluate_board(board), None
        for move in move_tiles:
            new_board = cPickle.loads(cPickle.dumps(board, -1))
            from_coord, to_coord = move
            from_tile = new_board.get_tile(from_coord[0], from_coord[1])
            to_tile = new_board.get_tile(to_coord[0], to_coord[1])
            piece = from_tile.piece
            new_board.move_piece(piece, to_tile)

            if should_extend_depth(new_board, depth, from_tile, to_tile):
                eval_score, _ = minimax(new_board, depth, alpha, beta, True, extra_depth + 1)
            else:
                eval_score, _ = minimax(new_board, depth - 1, alpha, beta, True)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = ((from_tile.x_coord, from_tile.y_coord), (to_tile.x_coord, to_tile.y_coord))
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def bot_turn(board, screen, depth=3):
    if board.in_check == 'black' and not board.find_moveable_piece('black'):
        board.winner = 'white'
        return

    board.clear_highlighted_tiles()
    board.draw(screen)
    pygame.display.update()

    _, best_move = minimax(board, depth, float('-inf'), float('inf'), True)

    if best_move is not None:
        from_coord, to_coord = best_move
        from_tile = board.get_tile(from_coord[0], from_coord[1])
        to_tile = board.get_tile(to_coord[0], to_coord[1])
        piece = from_tile.piece
        board.clear_yellow_tiles()
        board.move_piece(piece, to_tile)
        board.clear_piece_variables('black')
        board.end_turn()
    else:
        if board.check_for_check('black'):
            board.winner = 'white'
        else:
            board.winner = 'nobody'
        return