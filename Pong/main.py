import pygame, sys
from settings import *
from game import Game, CRT

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

game = Game(screen)
crt = CRT(screen)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    game.run()
    crt.draw()

    pygame.display.flip()
    clock.tick(60)