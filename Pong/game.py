import pygame
from paddle import Paddle
from random import randint
from settings import *

class Game():
    def __init__(self, surface):
        # paddle
        self.display_surface = surface
        self.paddle = pygame.sprite.Group()
        self.add_paddle()

        # line
        self.rect_size = 5
        self.line_amount = 6
        self.rect_y_position = [num * (600 / self.line_amount) for num in range(self.line_amount)]
        
        # ball
        self.speed_x = 6
        self.speed_y = 8
        self.x_pos = 437
        self.y_pos = 290
        self.moving_ball = pygame.Rect(self.x_pos, self.y_pos, 25, 25)

        # score
        self.scoreA = 0
        self.scoreB = 0

    def create_line(self, *offset, x_start, y_start):
        for offset_y in offset:
            pygame.draw.rect(self.display_surface, (64, 64, 64), pygame.Rect(x_start, offset_y + y_start ,self.rect_size, 50))

    def add_paddle(self):
        self.paddleA = Paddle((80, 250), 'red')
        self.paddleB = Paddle((820, 250), 'blue')
        self.paddle.add(self.paddleA)
        self.paddle.add(self.paddleB)
    
    def draw_ball(self):
        pygame.draw.rect(self.display_surface, (255, 255, 255), self.moving_ball, 0, -1, 15, 15, 15, 15)

    def move_ball(self):
        self.moving_ball.x += self.speed_x
        self.moving_ball.y += self.speed_y
        
    def ball_collision(self):
        # bottom border & top border
        if self.moving_ball.y >= screen_height:
            self.speed_y *= -1
        elif self.moving_ball.y <= 0:
            self.speed_y *= -1

        # right border & left border
        if self.moving_ball.x >= screen_width:
            self.moving_ball.y = self.y_pos
            self.moving_ball.x = self.x_pos
            self.speed_x *= -1
            self.scoreA += 1
        elif self.moving_ball.x <= 0:
            self.moving_ball.y = self.y_pos
            self.moving_ball.x = self.x_pos
            self.speed_x *= -1
            self.scoreB += 1

        # paddleA
        if self.paddleA.rect.colliderect(self.moving_ball):
            if self.moving_ball.x > 90 and self.moving_ball.x < 100:
                self.speed_x *= -1
        
        # paddleB
        if self.paddleB.rect.colliderect(self.moving_ball):
            if self.moving_ball.x < 820 and self.moving_ball.x > 800:
                self.speed_x *= -1

    def ai_move(self):
        y_pos = self.moving_ball.y
        if y_pos > self.paddleB.rect.y:
            self.paddleB.rect.y += 7
        else:
            self.paddleB.rect.y -= 7
    
    def display_score(self):
        self.font = pygame.font.Font('../Space Invaders/font/Pixeled.ttf',25)
        score_surf_a = self.font.render(f'Player A: {self.scoreA}', False, (64, 64, 64))
        score_rect_a = score_surf_a.get_rect(topleft = (200, 100))
        self.display_surface.blit(score_surf_a, score_rect_a)

        score_surf_b = self.font.render(f'Player B: {self.scoreB}', False, (64, 64, 64))
        score_rect_b = score_surf_a.get_rect(topleft = (490, 100))
        self.display_surface.blit(score_surf_b, score_rect_b)
    
    def display_game_end(self):
        if self.scoreA == 10:
            self.moving_ball.x = self.x_pos
            self.moving_ball.y = self.y_pos
            self.speed_x = 0
            self.speed_y = 0
            self.paddleB.rect.y = 250

            win_surface = self.font.render(f'You won!', False, (255, 255, 255))
            win_surface_rect = win_surface.get_rect(topleft = (365, 240))
            self.display_surface.blit(win_surface, win_surface_rect)
        elif self.scoreB == 10:
            self.moving_ball.x = self.x_pos
            self.moving_ball.y = self.y_pos
            self.speed_x = 0
            self.speed_y = 0
            self.paddleB.rect.y = 250

            win_surface = self.font.render(f'You lose!', False, (235, 0, 0))
            win_surface_rect = win_surface.get_rect(topleft = (365, 240))
            self.display_surface.blit(win_surface, win_surface_rect)
        
    def run(self):
        # paddle
        self.paddle.update()
        self.paddle.draw(self.display_surface)

        # line
        self.create_line(*self.rect_y_position, x_start = 448, y_start = 25)

        # ball
        self.draw_ball()
        self.move_ball()
        self.ball_collision()

        # ai
        self.ai_move()

        # score & game end
        self.display_score()
        self.display_game_end()

class CRT():
    def __init__(self, surface):
        self.tv = pygame.image.load('../Space Invaders/graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))
        self.display_surface = surface
    
    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        self.display_surface.blit(self.tv, (0, 0))
        