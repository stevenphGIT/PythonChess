from data.Piece import Piece


class King(Piece):
    def __init__(self, color, coords, board):
        super().__init__(color, coords, board)

        self.piece_id = 'X'
        self.piece_value = 100

    def get_all_moves(self, board):
        moves = []

        can_up = False
        can_down = False
        can_left = False
        can_right = False

        if self.x < 7:
            can_right = True
        if self.x > 0:
            can_left = True
        if self.y < 7:
            can_down = True
        if self.y > 0:
            can_up = True

        if can_right:
            moves.append(board.get_tile(
                self.x + 1, self.y
            ))
            if can_up:
                moves.append(board.get_tile(
                    self.x + 1, self.y - 1
                ))
            if can_down:
                moves.append(board.get_tile(
                    self.x + 1, self.y + 1
                ))

        if can_left:
            moves.append(board.get_tile(
                self.x - 1, self.y
            ))
            if can_up:
                moves.append(board.get_tile(
                    self.x - 1, self.y - 1
                ))
            if can_down:
                moves.append(board.get_tile(
                    self.x - 1, self.y + 1
                ))

        if can_up:
            moves.append(board.get_tile(
                self.x, self.y - 1
            ))

        if can_down:
            moves.append(board.get_tile(
                self.x, self.y + 1
            ))

        if not self.ever_moved:
            if board.get_tile(self.x + 1, self.y).piece is None and board.get_tile(self.x + 2, self.y).piece is None:
                if board.get_tile(7, self.y).piece is not None and not board.get_tile(7, self.y).piece.ever_moved:
                    moves.append(board.get_tile(
                        self.x + 2, self.y
                    ))
            if board.get_tile(self.x - 1, self.y).piece is None and board.get_tile(self.x - 2, self.y).piece is None and board.get_tile(self.x - 3, self.y).piece is None:
                if board.get_tile(0, self.y).piece is not None and not board.get_tile(0, self.y).piece.ever_moved:
                    moves.append(board.get_tile(
                        self.x - 2, self.y
                    ))

        return moves

    def get_legal_moves(self, board, cull_moves = False):
        output = []
        for tile in self.get_all_moves(board):
            if tile.piece is None:
                output.append(tile)
            else:
                if tile.piece.color is not self.color:
                    output.append(tile)
        if cull_moves:
            final_moves = self.cull_self_checking_moves(board, output, self.color)
            if board.get_tile(self.x + 1, self.y) not in final_moves:
                if board.get_tile(self.x + 2, self.y) in final_moves:
                    final_moves.remove(board.get_tile(self.x + 2, self.y))
            if board.get_tile(self.x - 1, self.y) not in final_moves:
                if board.get_tile(self.x - 2, self.y) in final_moves:
                    final_moves.remove(board.get_tile(self.x - 2, self.y))
            return final_moves
        return output

    def show_legal_moves(self, board, cull_moves = False):
        legal_moves = []
        legal_moves = self.get_legal_moves(board, cull_moves)

        board.clear_highlighted_tiles()

        for tile in legal_moves:
            tile.moveable = True