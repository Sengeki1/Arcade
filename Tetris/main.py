from settings import *
import sys
from os.path import join

#components
from game import Game
from score import Score
from preview import Preview

from random import choice, randint

class CRT:
    def __init__(self):
        self.tv = pygame.image.load('../Space Invaders/graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def create_crt_lines(self):    
        self.line_height = 3
        self.line_amount = GAME_HEIGHT / self.line_height
        for y in range(int(self.line_amount)):
            y_pos = y * self.line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (WINDOW_WIDTH, y_pos), 1)
    
    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()


class Main:
    def __init__(self):

        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]  

        # components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()
    
        # audio
        self.music = pygame.mixer.Sound(join('sound', 'music.wav'))
        self.music.set_volume(0.2)
        self.music.play(loops= -1)

        # crt
        self.crt = CRT()

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0) # getting and removing the shape from the list
        self.next_shapes.append(choice(list(TETROMINOS.keys()))) # append a new shape into the list since we always want 3 shapes
        return next_shape # returning the shape
    
    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # display
            self.display_surface.fill('#3D59AB')
            self.crt.draw()
            self.display_surface.blit(self.crt.tv, (0, 0))
    
            # components
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)
            
            # updating the game
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    main = Main()
    main.run()
