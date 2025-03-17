import pygame
from settings import *
from sprites import Shape

class Game:
    def __init__(self, surface):
        self.display_surface = surface
        pygame.key.set_repeat(500, 100) # delay after pressing the key and repeating it after milliseconds

        # sprite group
        self.all_sprites = pygame.sprite.Group()

        # player
        self.sprite = Shape(0, 10)
        self.all_sprites.add(self.sprite)

    def draw_grid(self):
        # vertical line
        for x in range(0, (screen_width - 99), block_size):
            pygame.draw.line(self.display_surface, 'grey', (x, 0), (x, (screen_height) - 125))
        # horizontal line
        for y in range(0, (screen_height - 99), block_size):
            pygame.draw.line(self.display_surface, 'grey', (0, y), ((screen_width - 120), y))

    def run(self):
        self.draw_grid()
        self.all_sprites.update()
        self.all_sprites.draw(self.display_surface)