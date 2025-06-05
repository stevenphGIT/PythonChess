from operator import truediv

import pygame
from data.Piece import Piece


class Knight(Piece):
    def __init__(self, color, coords, board):
        super().__init__(color, coords, board)

        self.piece_id = 'K'
        self.piece_value = 3

    def get_all_moves(self, board):
        real_moves = []
        moves = []

        moves.append((2, -1))
        moves.append((2, 1))
        moves.append((-2, 1))
        moves.append((-2, -1))

        moves.append((-1, 2))
        moves.append((-1, -2))
        moves.append((1, 2))
        moves.append((1, -2))

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if 8 > new_pos[0] >= 0 and 8 > new_pos[1] >= 0:
                real_moves.append(
                    board.get_tile(new_pos[0], new_pos[1])
                )
        return real_moves

    def get_legal_moves(self, board, cull_moves = False):
        output = []
        for tile in self.get_all_moves(board):
            if tile.piece is None:
                output.append(tile)
            elif tile.piece.color is not self.color:
                output.append(tile)
        if cull_moves:
            final_moves = self.cull_self_checking_moves(board, output, self.color)
            return final_moves
        return output

    def show_legal_moves(self, board, cull_moves = False):
        legal_moves = []
        legal_moves = self.get_legal_moves(board, cull_moves)

        board.clear_highlighted_tiles()

        for tile in legal_moves:
            tile.moveable = True