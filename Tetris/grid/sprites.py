import pygame
from settings import *

class Shape(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((block_size, block_size))
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def draw_square(self):
        self.image = pygame.Surface((block_size * 2, block_size * 2))
        self.image.fill('green')
    
    def draw_rectangle(self):
        self.image = pygame.Surface((block_size * 4, block_size))
        self.image.fill('green')
    
    def move(self, dir_x = 0, dir_y = 0):
        self.x += dir_x # each time we press a key we increment a value to the x, initially is 0
        self.y += dir_y

    def update(self):
        self.rect.x = self.x * block_size # multiply the direction by the block size to fit the grid
        self.rect.y = self.y * block_size
        self.draw_square()