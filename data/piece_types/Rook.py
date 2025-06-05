from data.Piece import Piece


class Rook(Piece):
    def __init__(self, color, coords, board):
        super().__init__(color, coords, board)

        self.piece_id = 'R'
        self.piece_value = 5

    def get_all_moves(self, board):
        moves = []

        up = []
        for y in range(self.y)[::-1]:
            up.append(board.get_tile(
                self.x, y
            ))
        moves.append(up)

        down = []
        for y in range(self.y + 1, 8):
            down.append(board.get_tile(
                self.x, y
            ))
        moves.append(down)

        left = []
        for x in range(self.x + 1, 8):
            left.append(board.get_tile(
                x, self.y
            ))
        moves.append(left)

        right = []
        for x in range(self.x)[::-1]:
            right.append(board.get_tile(
                x, self.y
            ))
        moves.append(right)

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