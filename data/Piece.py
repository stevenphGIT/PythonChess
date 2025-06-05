class Piece:
    def __init__(self, color, coords, board):
        self.x = coords[0]
        self.y = coords[1]
        self.color = color
        self.ever_moved = False
        self.piece_id = '!'
        self.piece_value = -1

    def get_all_moves(self, board):
        print("invalid piece")

    def get_legal_moves(self, board):
        print("invalid piece")

    def show_legal_moves(self, board):
        print("invalid piece")

    def cull_self_checking_moves(self, board, moves, color):
        output = []
        for move in moves:
            if board.check_for_check(color, (board.get_tile(self.x, self.y),move)) is False:
                output.append(move)
        return output