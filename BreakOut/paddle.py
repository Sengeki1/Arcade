import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, type, color, size_x, size_y):
        super().__init__()
        self.image = pygame.Surface((size_x, size_y))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.type = type
        self.speed = 8
    
    def move(self):
        if self.type == 'player':
            key = pygame.key.get_pressed()
            if key[pygame.K_a] and self.rect.x > 0:
                self.rect.x -= self.speed
            elif key[pygame.K_d] and self.rect.x < 470:
                self.rect.x += self.speed

    def update(self):
        self.move()
