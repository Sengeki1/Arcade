import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.Surface((4, 20)) # Empty surface (width, height)
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

        # Audio
        sound = pygame.mixer.Sound('audio/laser.wav')
        sound.set_volume(0.2)
        sound.play()

    def move(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
        elif self.rect.bottom > 600:
            self.kill()
    
    def update(self):
        self.move()