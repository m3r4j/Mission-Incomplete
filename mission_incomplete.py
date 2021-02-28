import pygame
import sys
import os
import random

# THIS CHECKS IF ANY DATA FILES EXIST OR NOT
def check_files():
	# CHECK IF THE DATA FOLDER EXISTS
	if not os.path.exists('data'):
		os.mkdir('data')

	# CHECK IF THE 'bestscore.cfg' FILE EXISTS
	if not os.path.exists('data/bestscore.log'):
		with open('data/bestscore.log', 'a', encoding='utf-8', errors='ignore') as file : file.write('0')

# THIS LOADS THE BEST HIGH SCORE THE USER HAS GOTTEN
def load_high_score():
	check_files()

	with open('data/bestscore.log', 'r', encoding='utf-8', errors='ignore') as file:
		data = file.readlines()

		for score in data:
			return int(score)

# THIS FUNCTION SAVES THE NEW SCORE THAT THE USER GOT
def save_new_score(score):
	check_files()

	with open('data/bestscore.log', 'w', encoding='utf-8', errors='ignore') as file:
		file.write(str(score))


# PYGAME FUNCTIONS
pygame.init()
pygame.font.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 30)

# RGB COLOURS
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

width, height = 600, 385

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('Mission Incomplete')

# THE ICON FOR THE GAME (ON LINUX IT MIGHT NOT WORK)
game_icon = pygame.image.load('icon.png')
pygame.display.set_icon(game_icon)

# THE FRAME RATE AND THE CLOCK
fps = 60
clock = pygame.time.Clock()

# LOAD IN SOME IMAGES
background = pygame.image.load('sprites/background.png')
ball = pygame.image.load('sprites/ball.png')

# THE BALLS WIDTH AND HEIGHT
ball_width = 50
ball_height = 50


ball = pygame.transform.scale(ball, (ball_width, ball_height))

def generate_ball():
	global ball_x, ball_direction

	ball_direction = random.choice([-1, 1]) # RIGHT OR LEFT

	if ball_direction == 1: # GOING RIGHT
		ball_x = -100

	if ball_direction == -1: # GOING LEFT
		ball_x = width + 100

floor = 268

player_width = 30
player_height = 60
player_speed = 5

player_vel_reset = 15.5



# THE CLASS FOR THE SOUND EFFECTS
class sounds:
	def jump():
		pygame.mixer.Channel(0).play(pygame.mixer.Sound('audio/jump.wav'))

	def game_over():
		pygame.mixer.Channel(1).play(pygame.mixer.Sound('audio/game_over.wav'))



def draw_score():
	text = font.render('SCORE: ' + str(score), True, red)
	window.blit(text, (115, 20))


def draw_highscore():
	text = font.render('BEST: ' + str(best_score), True, red)
	window.blit(text, (115, 40))	


def draw_background():
	window.blit(background, (0, 0))

def handle_falling():
	global player_y, falling

	if player_y < floor:
		player_y += 4

	else:
		falling = False








def handle_jumping():
	global player_y, player_jumped, player_vel, falling

	if player_jumped and player_vel >= 0:
		player_y -= player_vel
		player_vel -= gravity

	else:
		player_vel = player_vel_reset
		player_jumped = False
		falling = True




def handle_keys(keys):
	global player_x, player_y, counter, direction, index, player_jumped

	if keys[pygame.K_a] and keys[pygame.K_d]:
		pass

	else:
		if keys[pygame.K_d] and player_x + player_speed < width - player_width: # IF THE PLAYER WANTS TO GO RIGHT
			player_x += player_speed
			counter += 1
			direction = 1

		if keys[pygame.K_a] and player_x - player_speed > 0: # IF THE PLAYER WANTS TO GO LEFT
			player_x -= player_speed
			counter += 1
			direction = -1

		if keys[pygame.K_a] == False and keys[pygame.K_d] == False or player_y < floor: # IF THE PLAYER IS NOT HOLDING ANYTHING
			index = 0

# RIGHT AND LEFT CHARACTER SPRITES WHICH ARE STORED IN THESE ARRAYS
right = []
left = []

for i in range(1, 3):
	img_right = pygame.image.load(f'sprites/character_{i}.png')
	img_right = pygame.transform.scale(img_right, (player_width, player_height))

	img_left = pygame.transform.flip(img_right, True, False)

	right.append(img_right)
	left.append(img_left)

# COOLDOWNS FOR SOME ANIMATIONS
walk_cooldown = 5
ball_cooldown = 5

# A FUNCTION TO DRAW THE PLAYER
def draw_player():
	if direction == 1:
		window.blit(right[index], (player_x, player_y))

	if direction == -1:
		window.blit(left[index], (player_x, player_y))

def game_loop():
	global player_jumped, player_y, direction, player_x, score, best_score, ball_x, ball, ball_speed, counter, gravity, index, falling

	counter_ball = 0
	counter = 0
	direction = 1
	index = 0

	player_jumped = False
	player_vel = player_vel_reset
	gravity = 0.50
	falling = False

	score = 0
	best_score = load_high_score() # LOADS THE USERS BEST SCORE BY READING INTO A FILE

	player_x = width // 2
	player_y = 268

	show_stats = True
	ball_y = 275

	ball_speed = 2
	scores = []

	generate_ball() # GENERATE A RANDOM BALL COMING FROM LEFT OR RIGHT

	while True:
		clock.tick(fps)

		for event in pygame.event.get():
			if event.type == pygame.QUIT: # CHECK FOR THE QUIT EVENT
				pygame.quit() # QUIT PYGAME
				sys.exit() # TERMINATE THE PROGRAM

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1: # THIS HIDES OR SHOWS THE STATS (SHOWS GAME SCORE AND BEST SCORE)
					show_stats = not show_stats # SHOW OR DON'T SHOW IT

				if event.key == pygame.K_SPACE and falling == False: # ALLOW THE USER TO JUMP BUT NOT JUMP MORE THAN ONCE IN THE AIR
					if player_jumped == False: # CHECK IF THE PLAYER HASN'T JUMPED YET
						sounds.jump() # MAKE THE JUMP SOUND EFFECT
					player_jumped = True # TELL THE PROGRAM THAT THE PLAYER HAS JUMPED
					


		keys = pygame.key.get_pressed() # GET EVERY KEY THAT HAS BEEN PRESSED
		window.fill(black) 

		draw_background() # DRAW THE BACKGROUND IMAGE
		handle_jumping() # HANDLE THE JUMPS d
		handle_falling() # HANDLE THE FALLING (THE USER GETTING PULLED BACK DOWN TO THE FLOOR)
		handle_keys(keys) # HANDLE ALL THE KEYS THAT ARE BEING PRESSED BY THE USER
		draw_player() # DRAW THE PLAYER

		# THE STATS FOR THE GAME
		if show_stats:	
			draw_score()
			draw_highscore()

		# THE WALKING ANIMATIONS COOLDOWN
		if counter > walk_cooldown:
			counter = 0
			index += 1

			if index >= len(right): # RESET THE INDEX
				index = 0

		# RECT OBJECTS WHICH CHECK IF THEY COLLIDED WITH EACHOTHER (GAME OVER)
		ball_rect = pygame.Rect(ball_x, ball_y, ball_width, ball_height)
		player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

		window.blit(ball, (ball_x, ball_y)) # DISPLAY THE BALL ONTO THE SCREEN

		# CHECK IF THE BALL HAS GONE OFF THE SCREEN
		if ball_x > width + 100 or ball_x < -100:
			generate_ball() # GENERATE A NEW BALL
			ball_speed += 0.25 # INCREASE DIFFICULTY
			score += 1 # INCREASE THE SCORE

		# FIND OUT WHICH DIRECTION THE BALL IS HEADING
		if ball_direction == 1:
			ball_x += ball_speed # GO RIGHT

		if ball_direction == -1:
			ball_x -= ball_speed # GO LEFT

		# CHECK THE COOLDOWN FOR THE BALLS ROTATION (SPINNING BALL)
		counter_ball += 1
		if counter_ball > ball_cooldown:
			counter_ball = 0
			ball = pygame.transform.rotate(ball, 90) # ROTATE THE BALL SO IT LOOKS LIKE IT'S SPINNING


		# CHECK IF THE SCORE IS EQUAL TO THE BEST SCORE
		if score == best_score and score not in scores:
			scores.append(score)

		# CHECK IF THE SCORE IS GREATER THAN THE BEST SCORE
		if score > best_score and score not in scores:
			save_new_score(score) # SAVE THE NEW SCORE
			best_score = score
			scores.append(score)


		# CHECK IF THE PLAYER HAS COLLIDED WITH THE BALL
		if player_rect.colliderect(ball_rect):
			sounds.game_over() # MAKE THE GAME OVER SOUND EFFECT
			game_loop() # RE-RUN THE MAIN LOOP


		pygame.display.update() # KEEP ON UPDATING THE SCREEN

game_loop()
