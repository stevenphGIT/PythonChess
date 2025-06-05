import pygame

from data.Board import Board
from data.AI import bot_turn

pygame.init()

screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
board = Board(screen_size[0], screen_size[1])

def draw(display):
    display.fill('white')
    board.draw(display)
    pygame.display.update()

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if len(board.find_moveable_piece('white')) == 0:
        board.check_for_check('white')
        if board.in_check == 'white':
            board.winner = 'black'
        else:
            board.winner = 'nobody'
    if board.winner is not None:
        if board.winner == 'nobody':
            print("Stalemate! It's a tie.")
        elif board.winner == 'white':
            print("White wins with a point differential of " + str(board.white_score - board.black_score) + ".")
        else:
            print("Black wins with a point differential of " + str(board.black_score - board.white_score) + ".")
        running = False
    if board.turn == 'b':
        bot_turn(board, screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.tile_click(mouse_x, mouse_y)
    draw(screen)
    if board.signal_turn_end:
        board.end_turn()
        board.signal_turn_end = False