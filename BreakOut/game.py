import pygame, sys
from paddle import Paddle
from settings import *
from random import choice, randint

class Game():
    def __init__(self, surface):
        self.display_surface = surface
        self.font = pygame.font.Font('../Space Invaders/font/Pixeled.ttf', 25)

        # player
        self.player = pygame.sprite.Group()
        self.paddle = Paddle(230, 600, 'player', 'grey', 133, 30)
        self.player.add(self.paddle)

        # paddles
        self.paddles = pygame.sprite.Group()
        self.paddles_setup(rows = 6, cols = 4)

        # ball
        self.speed_x = 6
        self.speed_y = 8
        self.direction_x = 0
        self.moving_ball = pygame.Rect((screen_width / 2) - 15, (screen_height / 2) + 100, 25, 25)
    
        #score
        self.score = 0
        
        # lives
        self.live = 3

    def paddles_setup(self, rows, cols, x_distance = 140, y_distance = 37, x_offset = 25, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                
                paddle_tile = Paddle(x, y, 'pointer', choice(['blue','pink','red','white','yellow','green','purple','orange','white','pink']), 133, 30)
                self.paddles.add(paddle_tile)

    def draw_ball(self):
        pygame.draw.rect(self.display_surface, (255 ,255 ,255), self.moving_ball, 0, -1, 15, 15, 15, 15)

    def move_ball(self):
        self.moving_ball.y += self.speed_y
        self.moving_ball.x += self.speed_x * self.direction_x

    def ball_collision(self):
        # bottom border & top border
        if self.moving_ball.y >= screen_height:
            self.moving_ball.y = ((screen_height / 2) + 100)
            self.moving_ball.x = ((screen_width / 2) - 15)
            self.direction_x = 0
            self.live -= 1
        elif self.moving_ball.y <= 0:
            self.speed_y *= -1
        
        # left border & right border
        if self.moving_ball.x >= screen_width:
            self.speed_x *= -1
        elif self.moving_ball.x <= 0:
            self.speed_x *= -1

        # player
        if self.paddle.rect.colliderect(self.moving_ball):
            if self.moving_ball.y < 610 and self.moving_ball.y > 600:
                self.speed_y *= -1
                self.direction_x = -1

        if self.paddles:
            for sprite in self.paddles.sprites():
                if sprite.rect.colliderect(self.moving_ball):
                    sprite.kill()
                    self.score += 50
                    self.speed_y *= -1

    def game_end(self):
        if not self.paddles.sprites():
            self.moving_ball.y = ((screen_height / 2) + 100)
            self.moving_ball.x = ((screen_width / 2) - 15)
            self.direction_x = 0
            self.speed_y = 0

            win_surf = self.font.render('You Won', False, 'white')
            win_rect = win_surf.get_rect(topleft = ((screen_width / 2) - 90, (screen_height / 2) ))
            self.display_surface.blit(win_surf, win_rect)
        
        elif self.live <= 0:
            self.moving_ball.y = ((screen_height / 2) + 100)
            self.moving_ball.x = ((screen_width / 2) - 15)
            self.direction_x = 0
            self.speed_y = 0

            lose_surf = self.font.render('You lose', False, 'red')
            lose_rect = lose_surf.get_rect(topleft = ((screen_width / 2) - 90, (screen_height / 2) ))
            self.display_surface.blit(lose_surf, lose_rect)
    
    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = ((screen_width / 2) - 90, 10))
        self.display_surface.blit(score_surf, score_rect)

    def display_lives(self):
        ball = pygame.Rect((screen_width - 45), 39, 25, 25)
        pygame.draw.rect(self.display_surface, (255 ,255 ,255), ball, 0, -1, 15, 15, 15, 15)
        live_surf = self.font.render(f'{self.live}x', False, 'white')
        live_rect = live_surf.get_rect(topleft = ((screen_width - 100), 10))
        self.display_surface.blit(live_surf, live_rect)


    def run(self):
        self.player.update()
        self.player.draw(self.display_surface)

        self.paddles.draw(self.display_surface)
        self.draw_ball()
        self.move_ball()
        self.ball_collision()

        self.display_score()
        self.display_lives()
        self.game_end()

class CRT():
    def __init__(self, surface):
        self.display_surface = surface
        self.tv = pygame.image.load('../Space Invaders/graphics/tv.png')
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    def create_crt_line(self):
        self.line_height = 3
        self.line_amount = int(screen_height / self.line_height)
        for line in range(self.line_amount):
            y_pos = line * self.line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos))
    
    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_line()
        self.display_surface.blit(self.tv, (0,0))
        
