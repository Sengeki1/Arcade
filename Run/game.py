import pygame, os
from sys import exit
from random import choice

#os.chdir('/home/marco/Documentos/Game_Development/Run')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # calling the super class first
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0

        #sound
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    # instead of calling all the methods individualy
    def update(self): # update all of the sprites
        self.player_input()
        self.apply_gravity()
        self.player_animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'Fly':
            fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (900, y_pos))
        self.difficulty = 15
        self.obstacle_speed = 6

    def obstacle_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill() # kill the sprite obstacle each time it reaches the end of the screen

    def speed(self, score): # updates the score
        if self.difficulty <= score:
            self.obstacle_speed += 1
            self.difficulty += 16
        else: self.rect.x -= self.obstacle_speed

    def update(self, score):
        self.obstacle_animation()
        self.speed(score)
        self.destroy()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time # counts time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    display_surface.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty() # clears the sprites from the group
        return False
    return True

pygame.init()
display_surface = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock() # Clock Object
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # Font Object
game_active = False
start_time = 0
score = 0

# Background Music
bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.set_volume(0.3)
bg_Music.play(loops = -1) # playing sound forever

player = pygame.sprite.GroupSingle() # Creating a singleGroup sprite
player.add(Player()) # using method from the super class add to add the class Player as a single group sprite

obstacle = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert() # convert function is for pygame to work better with image (faster fps)
ground_surface = pygame.image.load('graphics/ground.png').convert()
restart_surf = test_font.render('Restart', False, (64, 64, 64))
restart_rect = restart_surf.get_rect(center = (400, 200))

# Intro Screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) # Zoom the image
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 320))

#  Timer
# Costume User Event
obstacle_timer = pygame.USEREVENT + 1 # the plus one is to avoid a conflict on each event we add
pygame.time.set_timer(obstacle_timer, 1100) # Triggers Event

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and restart_rect.collidepoint(event.pos):
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
            if event.type == pygame.MOUSEMOTION and restart_rect.collidepoint(event.pos):
                restart_surf = test_font.render('Restart', False, (255, 255, 255))
            else: restart_surf
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle.add(Obstacle(choice(['Fly', 'Snail', 'Snail', 'Snail'])))

    if game_active:
        # Surfaces
        display_surface.blit(sky_surface, (0, 0)) # draw surface in our display surface
        display_surface.blit(ground_surface, (0, 300))
        
        # Score
        score = display_score()
        
        # Draw & Update the Sprites
        player.draw(display_surface)
        player.update()
        obstacle.draw(display_surface)
        obstacle.update(score)

        # Collision
        game_active = collision_sprite()

    else:
        if score == 0:
            display_surface.fill((94, 129, 162))
            display_surface.blit(player_stand, player_stand_rect)
            display_surface.blit(game_name, game_name_rect)
            display_surface.blit(game_message, game_message_rect) 
        else:
            display_surface.fill((0, 0, 0))
            display_surface.blit(restart_surf, restart_rect)

            # score display
            score_message = test_font.render(f'Your score: {score}', False, (64, 64, 64))
            score_message_rect = score_message.get_rect(center = (400, 330))
            display_surface.blit(score_message, score_message_rect)
        
    pygame.display.update()
    clock.tick(60) # Game shouldn't run past 60 frames p/second