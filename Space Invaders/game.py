import pygame, sys
from player import Player
import obstacle
import alien
from laser import Laser
from random import choice, randint

class Game:
    def __init__(self):
        # Player setup
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player((screen_width / 2, screen_height - 10)))

        # Health and score setup
        self.lives = 2
        self.live_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)

        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_position = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_position, x_start = 50, y_start = 480)
        # (*) unpacking operator so we can work the values from the list  

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_laser = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        # Extra Setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_timer = randint(40, 80)

        # Audio
        music = pygame.mixer.Sound('audio/music.wav')
        music.set_volume(0.2)
        music.play(loops = -1)

        self.explosion = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion.set_volume(0.2)

    def create_multiple_obstacle(self, *offset, x_start, y_start): # offset sets them arguments as tuple
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape): # returns an index on which row of the list
            for col_index, col in enumerate(row): # returns the index of the row as tuple
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x # multiply the index for the block size
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset # x_distance is the distance between the aliens
                y = row_index * y_distance + y_offset # y_distance is the distance between the aliens
                
                if row_index == 0: alien_sprite = alien.Alien('yellow', x, y)
                elif 1 <= row_index <= 2: alien_sprite = alien.Alien('green', x, y)
                else: alien_sprite = alien.Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_move_down(self, distance):
        if self.aliens: # if there are aliens if the screen
            for aliens in self.aliens.sprites():
                aliens.rect.y += distance 
    
    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)
    
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites()) # chose a random sprite
            laser_sprite = Laser(random_alien.rect.center, -6)
            self.alien_laser.add(laser_sprite)

    def extra_timer(self):
        self.extra_spawn_timer -= 1
        if self.extra_spawn_timer <= 0:
            self.extra.add(alien.Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_timer = randint(400, 800)

    def collision_checks(self):
        # player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                
                # alien collision
                alien_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                for alien in alien_hit:
                    self.score += alien.value
                    self.explosion.play()
                    laser.kill()

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    self.explosion.play()
                    laser.kill()
        
        # alien laser
        if self.alien_laser:
            for laser in self.alien_laser:
                # obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                
                # player collision
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.explosion.play()
                    self.lives -= 1
                    if self.lives < 0:
                        pygame.quit()
                        sys.exit()
        
        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', False, ('white'))
        score_rect = score_surf.get_rect(topleft = (10, -10))
        screen.blit(score_surf, score_rect)

    def display_victory(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You Won', False, 'white')
            victory_rect =  victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

    def run(self):
        self.player.update()
        self.alien_laser.update()
        self.extra.update()
        self.aliens.update(self.alien_direction)

        self.alien_position_checker()
        self.extra_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen) # drawing sprite from the class
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_laser.draw(screen)
        self.extra.draw(screen)

        self.display_lives()
        self.display_score()
        self.display_victory()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))
    
    def creat_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90)) # transparacy
        self.creat_crt_lines()
        screen.blit(self.tv, (0, 0))

if __name__ == '__main__': # used to execute some code only if the file was run directly, and not imported
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock =  pygame.time.Clock()
    game = Game()
    crt = CRT()
    game_active = True

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == ALIENLASER:
                game.alien_shoot()
        
        screen.fill((30, 30, 30))
        game.run()
        crt.draw()

        pygame.display.flip() # updates everything that is on the display surface
        clock.tick(60)