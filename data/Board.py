from data.Tile import Tile
from data.piece_types.Pawn import Pawn
from data.piece_types.Knight import Knight
from data.piece_types.Bishop import Bishop
from data.piece_types.Rook import Rook
from data.piece_types.Queen import Queen
from data.piece_types.King import King


class Board:
  def __init__(self, width, height):
    self.in_check = None
    self.winner = None
    self.width = width
    self.height = height
    self.tile_width = width / 8
    self.tile_height = height / 8
    self.turn = 'w'
    self.white_score = 0
    self.black_score = 0
    self.clicked_piece = None
    self.tiles = self.populate_tile_array()
    self.set_pieces()
    self.signal_turn_end = False

  def populate_tile_array(self):
    tile_array = []
    row = []
    for i in range(8):
      row.clear()
      for j in range(8):
        if (i + j) % 2 == 0:
          tile_color = 'tan'
        else:
          tile_color = 'brown'
        row.append(
          Tile(i, j, self.tile_width, self.tile_height, tile_color)
        )
      tile_array.append(row.copy())

    return tile_array

  def set_pieces(self):
    piece_array = [
      ['bR', 'bK', 'bB', 'bQ', 'bX', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['', '', '', '', '', '', '', ''],
      ['', '', '', '', '', '', '', ''],
      ['', '', '', '', '', '', '', ''],
      ['', '', '', '', '', '', '', ''],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'wX', 'wB', 'wK', 'wR'],
    ]
    for i in range(8):
      for j in range(8):
        if piece_array[i][j] == '':
          self.tiles[j][i].piece = None
        else:
          if piece_array[i][j][0] == 'w':
            piece_color = 'white'
          else:
            piece_color = 'black'
          if piece_array[i][j][1] == 'P':
            self.tiles[j][i].piece = Pawn(piece_color, (j, i), self)
          if piece_array[i][j][1] == 'K':
            self.tiles[j][i].piece = Knight(piece_color, (j, i), self)
          if piece_array[i][j][1] == 'B':
            self.tiles[j][i].piece = Bishop(piece_color, (j, i), self)
          if piece_array[i][j][1] == 'R':
            self.tiles[j][i].piece = Rook(piece_color, (j, i), self)
          if piece_array[i][j][1] == 'Q':
            self.tiles[j][i].piece = Queen(piece_color, (j, i), self)
          if piece_array[i][j][1] == 'X':
            self.tiles[j][i].piece = King(piece_color, (j, i), self)

  def draw(self, screen):
    for row in self.tiles:
      for tile in row:
        tile.draw(screen)

  def get_tile(self, x, y):
    x = int(x)
    y = int(y)
    if 0 <= x < len(self.tiles) and 0 <= y < len(self.tiles[x]):
      return self.tiles[x][y]
    else:
      return None

  def tile_click(self, x_pos, y_pos):
    x = x_pos // self.tile_width
    y = y_pos // self.tile_height
    c_tile = self.get_tile(x, y)
    if self.turn == 'w':
      if self.clicked_piece is not None and c_tile.moveable:
        self.clear_yellow_tiles()
        self.move_piece(self.clicked_piece, c_tile)
        self.clear_piece_variables('black')
        self.clear_highlighted_tiles()
        self.signal_turn_end = True
      if c_tile.piece is not None and c_tile.piece.color == 'white':
        self.clicked_piece = c_tile.piece
        self.clicked_piece.show_legal_moves(self, True)

  def end_turn(self):
    if self.turn == 'b':
      self.turn = 'w'
    else:
      self.turn = 'b'

  def clear_highlighted_tiles(self):
    for row in self.tiles:
      for tile in row:
        tile.moveable = False

  def clear_yellow_tiles(self):
    for row in self.tiles:
      for tile in row:
        tile.show_moved = False

  def move_piece(self, moved_piece, to_tile):
    captured_piece = None
    if to_tile.piece is not None:
      captured_piece = to_tile.piece
    old_tile = self.get_tile(moved_piece.x, moved_piece.y)
    moved_piece.coords = (to_tile.x_coord, to_tile.y_coord)
    moved_piece.x = to_tile.x_coord
    moved_piece.y = to_tile.y_coord
    to_tile.piece = moved_piece
    old_tile.piece = None
    self.clicked_piece = None
    moved_piece.ever_moved = True

    to_tile.show_moved = True
    old_tile.show_moved = True

    if moved_piece.piece_id == 'X':
      if old_tile.x_coord - moved_piece.x == -2:
        rook_tile = self.get_tile(7, moved_piece.y)
        rook = rook_tile.piece
        new_tile = self.get_tile(5, moved_piece.y)
        new_tile.piece = rook
        rook_tile.piece = None
        rook.x = new_tile.x_coord
        rook.y = new_tile.y_coord
      if old_tile.x_coord - moved_piece.x == 2:
        rook_tile = self.get_tile(0, moved_piece.y)
        rook = rook_tile.piece
        new_tile = self.get_tile(3, moved_piece.y)
        new_tile.piece = rook
        rook_tile.piece = None
        rook.x = new_tile.x_coord
        rook.y = new_tile.y_coord
    if moved_piece.piece_id == 'P':
      if abs(old_tile.y_coord - moved_piece.y) == 2:
        moved_piece.passantable = True
        self.piece_can_passant = True
      else:
        self.piece_can_passant = False
      if abs(old_tile.y_coord - moved_piece.y) == 1 and abs(old_tile.x_coord - moved_piece.x) == 1:
        deltaY = old_tile.y_coord - moved_piece.y
        if captured_piece is None:
          if moved_piece.color == 'white':
            passanted_tile = self.get_tile(moved_piece.x, moved_piece.y + deltaY)
            captured_piece = passanted_tile.piece
            passanted_tile.piece = None
      if moved_piece.color == 'white':
        if moved_piece.y == 0:
          self.get_tile(moved_piece.x, moved_piece.y).piece = Queen('white', (moved_piece.x, moved_piece.y), self)
      if moved_piece.color == 'black':
        if moved_piece.y == 7:
          self.get_tile(moved_piece.x, moved_piece.y).piece = Queen('black', (moved_piece.x, moved_piece.y), self)
    if captured_piece is not None:
      if isinstance(captured_piece, King):
        print("King was captured, error in move calculation.")
      moved_piece.bounty = captured_piece.piece_value
      if moved_piece.color == 'white':
        self.white_score += captured_piece.piece_value
      else:
        self.black_score += captured_piece.piece_value
    self.last_captured_piece = captured_piece
    if captured_piece is not None:
      self.captured_tile = self.get_tile(captured_piece.x, captured_piece.y)
    else:
      self.captured_tile = None
    return captured_piece

  def clear_piece_variables(self, color):
    for row in self.tiles:
      for tile in row:
        if tile.piece is not None:
          if tile.piece.color == color:
            tile.piece.bounty = 0
            if isinstance(tile.piece, Pawn):
              tile.piece.passantable = False

  def find_piece_of_type(self, piece_id):
    pieces = []
    for row in self.tiles:
      for tile in row:
        if tile.piece is not None and tile.piece.piece_id == piece_id:
          pieces.append(tile.piece)
    return pieces

  def find_piece_of_color(self, color):
    pieces = []
    for row in self.tiles:
      for tile in row:
        if tile.piece is not None:
          if tile.piece.color is color:
            pieces.append(tile.piece)
    return pieces

  def find_piece_tiles_of_color(self, color):
    tiles = []
    for row in self.tiles:
      for tile in row:
        if tile.piece is not None:
          if tile.piece.color is color:
            tiles.append(tile)
    return tiles


  def find_moveable_piece(self, color):
    pieces = []
    pieces_with_captures = []
    self.check_for_check(color)
    for row in self.tiles:
      for tile in row:
        if tile.piece is not None:
          if tile.piece.color is color:
            piece_moves = tile.piece.get_legal_moves(self, True)
            if len(piece_moves) > 0:
              pieces.append(tile)
              for move in piece_moves:
                if move.piece is not None:
                  if move.piece.color is not color:
                    pieces_with_captures.append(tile)
    if len(pieces_with_captures) > 0:
      return pieces_with_captures
    return pieces

  def find_moves_of_color(self, color, debug = False):
    moves = []
    for row in self.tiles:
      for piece_tile in row:
        if piece_tile.piece is not None:
          if piece_tile.piece.color is color:
            for to_tile in piece_tile.piece.get_legal_moves(self, True):
              moves.append((piece_tile, to_tile))
    return moves

  def to_coord_from_coord(self, color):
    converted_moves = []
    moves = self.find_moves_of_color(color)
    for move in moves:
      new_move = ((move[0].x_coord, move[0].y_coord), (move[1].x_coord, move[1].y_coord))
      converted_moves.append(new_move)
    return converted_moves

  def check_for_check(self, king_color, from_to = None):
    old_tile = None
    delta_tile = None
    moved_piece = None
    delta_tile_previous_piece = None
    passanted_tile = None
    passanted_tile_piece = None
    rook_tile = None
    new_tile = None
    rook = None
    flag = False
    king_tile = None

    if from_to is not None:
      for row in self.tiles:
        for tile in row:
          if tile is from_to[0]:
            moved_piece = tile.piece
            old_tile = tile
            old_tile.piece = None
      for row in self.tiles:
        for tile in row:
          if tile is from_to[1]:
            delta_tile = tile
            delta_tile_previous_piece = delta_tile.piece
            delta_tile.piece = moved_piece
            if isinstance(moved_piece, Pawn):
              if abs(delta_tile.y_coord - moved_piece.y) == 1 and abs(delta_tile.x_coord - moved_piece.x) == 1:
                deltaY = delta_tile.y_coord - moved_piece.y
                passanted_tile = self.get_tile(moved_piece.x, moved_piece.y + deltaY)
                passanted_tile_piece = passanted_tile.piece
                passanted_tile.piece = None
            if isinstance(moved_piece, King):
              if old_tile.x_coord - moved_piece.x == -2:
                rook_tile = self.get_tile(7, moved_piece.y)
                rook = rook_tile.piece
                new_tile = self.get_tile(5, moved_piece.y)
                new_tile.piece = rook
                rook_tile.piece = None
                rook.x = new_tile.x_coord
                rook.y = new_tile.y_coord
              if old_tile.x_coord - moved_piece.x == 2:
                rook_tile = self.get_tile(0, moved_piece.y)
                rook = rook_tile.piece
                new_tile = self.get_tile(3, moved_piece.y)
                new_tile.piece = rook
                rook_tile.piece = None
                rook.x = new_tile.x_coord
                rook.y = new_tile.y_coord
    for row in self.tiles:
      for tile in row:
        if tile.piece and tile.piece.piece_id == 'X':
          if king_color == tile.piece.color:
            king_tile = tile
    for row in self.tiles:
      for tile in row:
        if tile.piece is not None:
          if tile.piece.color is not king_color:
            piece_moves = tile.piece.get_legal_moves(self, False)
            for move in piece_moves:
              if move is king_tile:
                flag = True
    if from_to is None:
      if flag:
        self.in_check = king_color
      else:
        self.in_check = None
    if from_to is not None:
      old_tile.piece = moved_piece
      delta_tile.piece = delta_tile_previous_piece
      if passanted_tile is not None:
        passanted_tile.piece = passanted_tile_piece
      if rook_tile is not None:
        rook_tile.piece = rook
        new_tile.piece = None
    return flag

  def checkmated(self):
    self.check_for_check('white')
    self.check_for_check('black')
    if self.in_check is None:
      self.winner = None
    else:
      if self.find_moveable_piece('white') is None:
        if self.in_check == 'white':
          self.winner = 'black'
        else:
          self.winner = 'nobody'
      if self.find_moveable_piece('black') is None:
        if self.in_check == 'black':
          self.winner = 'white'
        else:
          self.winner = 'nobody'


  def ToString(self):
    string = ""
    for row in self.tiles:
      for tile in row:
        if tile.piece is not None:
          string += tile.piece.color[0] + tile.piece.piece_id
        else:
          string += ' '
        string += ", "
      string += "\n"
    return string

  def reset(self):
    self.in_check = None
    self.winner = None
    self.turn = 'w'
    self.white_score = 0
    self.black_score = 0
    self.clicked_piece = None
    self.piece_array = [
      ['bR', 'bK', 'bB', 'bQ', 'bX', 'bB', 'bK', 'bR'],
      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
      ['', '', '', '', '', '', '', ''],
      ['', '', '', '', '', '', '', ''],
      ['', '', '', '', '', '', '', ''],
      ['', '', '', '', '', '', '', ''],
      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
      ['wR', 'wK', 'wB', 'wQ', 'wX', 'wB', 'wK', 'wR'],
    ]
    self.set_pieces()