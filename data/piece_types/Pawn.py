from data.Piece import Piece


class Pawn(Piece):
    def __init__(self, color, coords, board):
        super().__init__(color, coords, board)

        self.piece_id = 'P'
        self.piece_value = 1
        self.passantable = False

    def get_all_moves(self, board):
        real_moves = []
        moves = []

        if self.color == 'white':
            moves.append((0, -1))
            if not self.ever_moved:
                moves.append((0, -2))

        elif self.color == 'black':
            moves.append((0, 1))
            if not self.ever_moved:
                moves.append((0, 2))

        for move in moves:
            new_pos = (self.x, self.y + move[1])
            if 8 > new_pos[1] >= 0:
                real_moves.append(
                    board.get_tile(new_pos[0], new_pos[1])
                )

        return real_moves

    def get_legal_moves(self, board, cull_moves = False):
        output = []
        final_moves = []
        for tile in self.get_all_moves(board):
            if tile.piece is not None:
                break
            else:
                output.append(tile)

        if self.color == 'white':
            if self.x + 1 < 8 and self.y - 1 >= 0:
                tile = board.get_tile(
                    self.x + 1, self.y - 1
                )
                right_tile = board.get_tile(
                    self.x + 1, self.y
                )

                if tile.piece is not None:
                    if tile.piece.color != self.color:
                        output.append(tile)
                if isinstance(right_tile.piece, Pawn) and right_tile.piece.passantable and right_tile.piece.color != self.color:
                    output.append(tile)
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                tile = board.get_tile(
                    self.x - 1, self.y - 1
                )
                left_tile = board.get_tile(
                    self.x - 1, self.y
                )
                if tile.piece is not None:
                    if tile.piece.color != self.color:
                        output.append(tile)
                if isinstance(left_tile.piece, Pawn) and left_tile.piece.passantable and left_tile.piece.color != self.color:
                    output.append(tile)

        elif self.color == 'black':
            if self.x + 1 < 8 and self.y + 1 < 8:
                tile = board.get_tile(
                    self.x + 1, self.y + 1
                )
                right_tile = board.get_tile(
                    self.x + 1, self.y
                )
                if tile.piece is not None:
                    if tile.piece.color != self.color:
                        output.append(tile)
                if isinstance(right_tile.piece, Pawn) and right_tile.piece.passantable and right_tile.piece.color != self.color:
                    output.append(tile)
            if self.x - 1 >= 0 and self.y + 1 < 8:
                tile = board.get_tile(
                    self.x - 1, self.y + 1
                )
                left_tile = board.get_tile(
                    self.x - 1, self.y
                )
                if tile.piece is not None:
                    if tile.piece.color != self.color:
                        output.append(tile)
                if isinstance(left_tile.piece, Pawn) and left_tile.piece.passantable and left_tile.piece.color != self.color:
                    output.append(tile)

        if cull_moves:
            final_moves = self.cull_self_checking_moves(board, output, self.color)
            return final_moves
        return output

    def show_legal_moves(self, board, cull_moves = False):
        legal_moves = []
        legal_moves = self.get_legal_moves(board, True)

        board.clear_highlighted_tiles()

        for tile in legal_moves:
            tile.moveable = True