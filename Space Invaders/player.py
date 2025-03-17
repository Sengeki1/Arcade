import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 5

        # lazer
        self.ready = True
        self.lazer_time = 0
        self.lazer_cooldown = 600

        self.lasers = pygame.sprite.Group() # define sprite Group

    def shoot_lazer(self):
        self.lasers.add(Laser(self.rect.center, 8)) # create Laser at the center of the player

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.x < 540:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_lazer() # run sprite
            self.ready = False
            self.lazer_time = pygame.time.get_ticks() # when player last time shooted

    def recharge(self):
        if self.ready == False:
            current_time = pygame.time.get_ticks() # cooldown while the player isnt shooting
            if current_time - self.lazer_time >= self.lazer_cooldown: # calculate cooldown
                self.ready = True
    
    def update(self):
        self.get_input()
        self.lasers.update()
        self.recharge()