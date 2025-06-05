import pygame

class Tile:
    def __init__(self, x_coord, y_coord, width, height, color):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height

        self.final_x = x_coord * width
        self.final_y = y_coord * height
        self.abs_pos = (self.final_x, self.final_y)
        self.pos = (x_coord, y_coord)
        tan = (230, 200, 170)
        brown = (180, 100, 80)
        self.moved_color = (255, 255, 100)
        self.show_moved = False
        self.color = color

        if self.color == 'tan':
            self.draw_color = tan
        elif self.color == 'brown':
            self.draw_color = brown

        if self.color == 'tan':
            self.highlight_color = (150, 255, 100)
        elif self.color == 'brown':
            self.highlight_color = (50, 220, 0)
        self.piece = None
        self.location = self.get_location()
        self.moveable = False

        self.rect = pygame.Rect(
            self.final_x,
            self.final_y,
            self.width,
            self.height
        )

    def get_location(self):
        columns = 'abcdefgh'
        return columns[self.x_coord] + str(self.y_coord + 1)

    def draw(self, display):

        if self.moveable:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        elif self.show_moved:
            pygame.draw.rect(display, self.moved_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.piece is not None:
            id_to_fullname = {
                "P": "pawn",
                "K": "knight",
                "B": "bishop",
                "R": "rook",
                "Q": "queen",
                "X": "king"
            }
            img_path = 'images/' + self.piece.color + "_" + id_to_fullname.get(self.piece.piece_id) + '.png'
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (self.width - 20, self.height - 20))
            centering_rect = img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(img, centering_rect.topleft)