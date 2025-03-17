from settings import *
from timer import Timer
from random import choice
from sys import exit
from os.path import join

class Game:
	def __init__(self, get_next_shape, update_score):

		# general
		self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
		self.display_surface = pygame.display.get_surface() # get a reference to the currently set display surface
		self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
		self.sprites = pygame.sprite.Group()

		# game connection
		self.get_next_shape = get_next_shape
		self.update_score = update_score

		# lines
		self.lines_surface = self.surface.copy() # create a new copy of a Surface
		self.lines_surface.fill((0,255,0))
		self.lines_surface.set_colorkey((0,255,0)) # set the transparent colorkey
		self.lines_surface.set_alpha(120)

		# tetromino
		self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)] # storing data of the blocks in a list of list
		self.tetromino = Tetromino(choice(list(TETROMINOS.keys())), self.sprites, self.create_new_tetromino, self.field_data)

		# timer
		self.down_speed = UPDATE_START_SPEED
		self.down_speed_faster = self.down_speed * 0.3
		self.down_pressed = False 
		self.timers = {
			'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
			'horizontal move': Timer(MOVE_WAIT_TIME),
			'rotate move': Timer(ROTATE_WAIT_TIME)
		}
		self.timers['vertical move'].activate()

		# score
		self.current_level = 1
		self.current_score = 0
		self.current_lines = 0

	def calculate_score(self, num_lines):
		self.current_lines += num_lines
		self.current_score += SCORE_DATA[num_lines] * self.current_level

		if self.current_lines / 10 > self.current_level: # if 20 / 10 = 2 > 1: level += 1 
			self.current_level += 1
			self.down_speed *= 0.75
			self.down_speed_faster = self.down_speed * 0.3
			self.timers['vertical move'].duration = self.down_speed

		self.update_score(self.current_lines, self.current_score, self.current_level)

	def check_game_over(self):
		for block in self.tetromino.blocks:
			if block.pos.y < 0:
				exit()

	def create_new_tetromino(self):
		self.check_game_over()
		self.check_finished_rows()
		self.tetromino = Tetromino(self.get_next_shape(), self.sprites, self.create_new_tetromino, self.field_data)

	def timer_update(self):
		for timer in self.timers.values():
			timer.update() # updating the timer values 

	def move_down(self):
		self.tetromino.move_down()

	def draw_grid(self):
		for col in range(1, COLUMNS):
			x = col * CELL_SIZE
			pygame.draw.line(self.lines_surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1) # get_height is a method that returns the height of the surface
		
		for row in range(1, ROWS):
			y = row * CELL_SIZE
			pygame.draw.line(self.lines_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)

		self.surface.blit(self.lines_surface, (0,0)) # placing the line surface on top of the game surface

	def input(self):
		key = pygame.key.get_pressed()

		# check horizontal movement
		if not self.timers['horizontal move'].active: # only when not active
			if key[pygame.K_LEFT]:
				self.tetromino.move_horizontal(-1)
				self.timers['horizontal move'].activate() # triggers timer
			if key[pygame.K_RIGHT]:
				self.tetromino.move_horizontal(1)
				self.timers['horizontal move'].activate()
		
		# check for rotation
		if not self.timers['rotate move'].active:
			if key[pygame.K_UP]:
				self.tetromino.rotate()
				self.timers['rotate move'].activate()

		# down speedup
		if not self.down_pressed and key[pygame.K_DOWN]: # pressing key
			self.down_pressed = True
			self.timers['vertical move'].duration = self.down_speed_faster

		if self.down_pressed and not key[pygame.K_DOWN]: # releasing key
			self.down_pressed = False
			self.timers['vertical move'].duration = self.down_speed

	def check_finished_rows(self):
		deleted_rows = []

		# get the full row indexes
		for i, row in enumerate(self.field_data):
			if all(row): # if the row evaluate true
				deleted_rows.append(i)
		
		if deleted_rows:
			for deleted_row in deleted_rows:
				
				# delete full rows
				for block in self.field_data[deleted_row]:
					block.kill()
				
				# move down blocks
				for row in self.field_data:
					for block in row:
						if block and block.pos.y < deleted_row:
							block.pos.y += 1
				
				# rebuild the field data
				self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
				for block in self.sprites:
					self.field_data[int(block.pos.y)][int(block.pos.x)] = block

			# update score
			self.calculate_score(len(deleted_rows))

	def run(self):
		
		# update
		self.input()
		self.timer_update()
		self.sprites.update() # updating the blocks
		
		# drawing
		self.surface.fill('#6A5ACD') # set background of the surface GRAY 
		self.sprites.draw(self.surface)

		self.draw_grid()
		self.display_surface.blit(self.surface, (PADDING,PADDING))
		pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
	# We have 2 surfaces on top of each other overlaping to give an effect on the lines and the outline

class Tetromino:
	def __init__(self, shape, group, create_new_tetromino, field_data):
		
		# setup
		self.shape = shape
		self.block_positions = TETROMINOS[shape]['shape']
		self.color = TETROMINOS[shape]['color']
		self.create_new_tetromino = create_new_tetromino
		self.field_data = field_data

		# create blocks
		self.blocks = [Block(group, pos, self.color) for pos in self.block_positions] # self.block_positions list is represented as a tuple (x, y)

		# audio
		self.audio = pygame.mixer.Sound(join('sound', 'landing.wav'))
		self.audio.set_volume(0.05)

	# collision
	def next_move_horizontal_collide(self, amount):
		collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
		return True if any(collision_list) else False # Return True if collide
	
	def next_move_vertical_collide(self):
		collision_list = [block.vertical_collide(int(block.pos.y + 1), self.field_data) for block in self.blocks]
		return True if any(collision_list) else False
	
	# movement
	def move_horizontal(self, amount):
		if not self.next_move_horizontal_collide(amount): # only when not colliding
			for block in self.blocks:
					block.pos.x += amount

	def move_down(self):
		if not self.next_move_vertical_collide():
			for block in self.blocks:
				block.pos.y += 1 # incrementing the y position for each block created
		else:
			for block in self.blocks:
				self.field_data[int(block.pos.y)][int(block.pos.x)] = block # field_data[row/y][col/x]
				# we are change the values of the field_data to block as we occupie it with a block sprite at a certain position
				# self.audio.play()
			self.create_new_tetromino()
	
	# rotate
	def rotate(self):
		if self.shape != 'O':

			# 1. pivot point
			pivot_pos = self.blocks[0].pos

			# 2. new block positions
			new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

			# 3. Collision check
			for pos in new_block_positions:
				# horizontal
				if pos.x < 0 or pos.x >= COLUMNS:
					return # doesnt rotate if the block reach the edges 

				# field check -> collision with other pieces
				if self.field_data[int(pos.y)][int(pos.x)]:
					return

				# vertical check
				if pos.y > ROWS:
					return 

			# 4. implement new positions
			for i, block in enumerate(self.blocks):
				block.pos = new_block_positions[i]

class Block(pygame.sprite.Sprite):
	def __init__(self, group, pos, color):
		super().__init__(group) # it allows to place the sprite into a group
		self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
		self.image.fill(color)

		# position
		self.pos = pygame.math.Vector2(pos) + BLOCK_OFFSET
		self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

	def rotate(self, pivot_pos):
		return pivot_pos - (self.pos - pivot_pos).rotate(90)

	def horizontal_collide(self, x, field_data):
		if not 0 <= x < COLUMNS:
			return True

		if field_data[int(self.pos.y)][x]: # position of the block after placing it
			return True

	def vertical_collide(self, y, field_data):
		if y >= ROWS:
			return True
		
		if y >= 0 and field_data[y][int(self.pos.x)]: # execute 
			return True
	
	def update(self):
		self.rect.topleft = self.pos * CELL_SIZE # updating the visual representation of the block on the screen
		