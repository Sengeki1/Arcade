import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((30, 110))
        self.image.fill(color)
        self.type = color
        self.rect = self.image.get_rect(topleft = pos)

        # speed
        self.speed = 8
        
    def move(self):
        key = pygame.key.get_pressed()

        if self.type == 'red':
            if key[pygame.K_w] and self.rect.y > 10:
                self.rect.y -= self.speed
            elif key[pygame.K_s]and self.rect.y < 480:
                self.rect.y += self.speed
    
    def update(self):
        self.move()
        