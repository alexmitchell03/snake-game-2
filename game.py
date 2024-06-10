import pygame
import random

pygame.init()

# screen dimensions
WIDTH = 640
HEIGHT = 480
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

def initialize_snake():
	snake = {
		# initial position center of screen
		"body": [(WIDTH // 2, HEIGHT // 2)],
		# initial direction is right
		"direction": pygame.K_RIGHT,
		"new_direction": pygame.K_RIGHT
	}
	return snake

def new_apple_position():
	return (random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE, 
					random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE)

def move_snake(snake):
	head_x, head_y = snake["body"][0]
	if snake["new_direction"] in [pygame.K_UP, pygame.K_w]:
		head_y -= BLOCK_SIZE
	elif snake["new_direction"] in [pygame.K_DOWN, pygame.K_s]:
		head_y += BLOCK_SIZE
	elif snake["new_direction"] in [pygame.K_LEFT, pygame.K_a]:
		head_x -= BLOCK_SIZE
	elif snake["new_direction"] in [pygame.K_RIGHT, pygame.K_d]:
		head_x += BLOCK_SIZE
	new_head = (head_x, head_y)
	# move the snake by adding new head to front and removing last segment
	snake["body"] = [new_head] + snake["body"][:-1]
	# updates direction
	snake["direction"] = snake["new_direction"]

def grow_snake(snake):
	tail = snake["body"][-1]
	tail_x, tail_y = tail
	if snake["direction"] in [pygame.K_UP, pygame.K_w]:
		new_tail = (tail_x, tail_y + BLOCK_SIZE)
	elif snake["direction"] in [pygame.K_DOWN, pygame.K_s]:
		new_tail = (tail_x, tail_y - BLOCK_SIZE)
	elif snake["direction"] in [pygame.K_LEFT, pygame.K_a]:
		new_tail = (tail_x + BLOCK_SIZE, tail_y)
	elif snake["direction"] in [pygame.K_RIGHT, pygame.K_d]:
		new_tail = (tail_x - BLOCK_SIZE, tail_y)
	snake["body"].append(new_tail)

def check_collision(snake):
	# returns True if collision is detected
	head = snake["body"][0]
	# if snake head hits window edge or collides with itself, end game
	if (head[0] < 0 or head[0] >= WIDTH or 
		head[1] < 0 or head[1] >= HEIGHT or 
		head in snake["body"][1:]):
			return True
	return False

def game_loop():
	snake = initialize_snake()
	apple = new_apple_position()
	running = True

	while running:
		for event in pygame.event.get():
			# if user closes window
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
						# prevent snake from reversing directly
						if ((event.key in [pygame.K_UP, pygame.K_w] and snake["direction"] not in [pygame.K_DOWN, pygame.K_s]) or
							(event.key in [pygame.K_DOWN, pygame.K_s] and snake["direction"] not in [pygame.K_UP, pygame.K_w]) or
							(event.key in [pygame.K_LEFT, pygame.K_a] and snake["direction"] not in [pygame.K_RIGHT, pygame.K_d]) or
							(event.key in [pygame.K_RIGHT, pygame.K_d] and snake["direction"] not in [pygame.K_LEFT, pygame.K_a])):
							snake["new_direction"] = event.key

		move_snake(snake)
		print("Snake head position:", snake["body"][0])

		# if snake head is at the same position as an apple
		if snake["body"][0] == apple:
			grow_snake(snake)
			apple = new_apple_position()
			print("Apple eaten! New position:", apple)

		if check_collision(snake):
			print("Collision detected! Game over.")
			running = False

		# draws game
		screen.fill(BLACK)
		for segment in snake["body"]:
			pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))
		pygame.draw.rect(screen, RED, (*apple, BLOCK_SIZE, BLOCK_SIZE))

		# updates full display surface to screen, showing the new frame
		pygame.display.flip()
		# limits frame rate of game loop to 10 fps
		clock.tick(10)

	pygame.quit()
	print("Game has ended.")

if __name__ == "__main__":
	game_loop()
