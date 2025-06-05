import pygame
from data.Piece import Piece


class Bishop(Piece):
    def __init__(self, color, coords, board):
        super().__init__(color, coords, board)

        self.piece_id = 'B'
        self.piece_value = 3

    def get_all_moves(self, board):
        moves = []

        up_right = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            up_right.append(board.get_tile(
                self.x + i, self.y - i
            ))
        moves.append(up_right)

        down_right = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            down_right.append(board.get_tile(
                self.x + i, self.y + i
            ))
        moves.append(down_right)

        up_left = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            up_left.append(board.get_tile(
                self.x - i, self.y - i
            ))
        moves.append(up_left)

        down_left = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            down_left.append(board.get_tile(
                self.x - i, self.y + i
            ))
        moves.append(down_left)



        return moves

    def get_legal_moves(self, board, cull_moves = False):
        output = []
        for axis in self.get_all_moves(board):
            for tile in axis:
                if tile.piece is None:
                    output.append(tile)
                else:
                    if tile.piece.color is not self.color:
                        output.append(tile)
                        break
                    else:
                        break
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