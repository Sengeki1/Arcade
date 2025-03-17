import pygame, sys
from settings import *
from game import Game

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

game = Game(screen)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                game.sprite.move(1, 0)
            elif event.key == pygame.K_LEFT:
                game.sprite.move(-1, 0)
            elif event.key == pygame.K_DOWN:
                game.sprite.move(0, 1)
            elif event.key == pygame.K_UP:
                game.sprite.move(0, -1)


    screen.fill((34, 34, 34))
    game.run()
    
    pygame.display.flip()
    clock.tick(60)