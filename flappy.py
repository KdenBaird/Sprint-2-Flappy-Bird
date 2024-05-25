""" A majority of the built-in pygame fucntions I used chat GPT 
to tell me where I need to use them as well as what they did. I 
did not copy paste from chat gpt, however, there were some functions
where I needed assistance. I typed what was in ChatGPT and ensured that 
I understood what the code was doing."""

import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 650

# Setting the parameters for the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Game')

# Define Variables
font = pygame.font.SysFont('Bauhaus 93', 50)
black = (0, 0, 0)
flying = False
game_over = False
ground_scroll = 0
scroll_speed = 5
fps = 60
flower_gap = 250
flower_freq = 1500  # ms
last_flower = pygame.time.get_ticks()
score = 0
pass_flower = False
# Load pics
background = pygame.image.load("finaltest.png")
ground_img = pygame.image.load("scrollp2.png")


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.counter = 0
        self.index = 0
        self.image = pygame.image.load("pngwing.com.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.gravity = 0
        self.clicked = False

    def update(self):
        if flying or game_over:
            # Falling
            self.gravity += 0.5
            if self.gravity > 7:
                self.gravity = 7

            # If the bottom of the bird touches the ground, don't go below.
            if self.rect.bottom < 580:
                self.rect.y += int(self.gravity)
            else:
                self.rect.bottom = 580
                self.gravity = 0

            # Jumping (0 index means mouse left click. 1 is true or it's clicked.)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and not game_over:
                self.clicked = True
                self.gravity = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('flowertest1.png')
        self.rect = self.image.get_rect()

        # Position 1 is the top, Position -1 is from the bottom
        if position == 1:
            # This code takes the sunflower and flips it by the y axis (True)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(flower_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(flower_gap / 2)]

    def update(self):
        if not game_over:
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

    def draw_border(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

bird_group = pygame.sprite.Group()
flower_group = pygame.sprite.Group()

# Instance of the bird class is set to the middle of the screen.
flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)

sentinel = True
while sentinel:

    clock.tick(fps)

    screen.blit(background, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    flower_group.draw(screen)
    if flying:
        flower_group.update()

    for flower in flower_group:
        flower.draw_border(screen)
    # Create the ground
    screen.blit(ground_img, (ground_scroll, 580))

    # Check score
    if len(flower_group) > 0:
        if bird_group.sprites()[0].rect.left > flower_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < flower_group.sprites()[0].rect.right \
                and pass_flower == False:
            pass_flower = True
        if pass_flower == True:
            if bird_group.sprites()[0].rect.left > flower_group.sprites()[0].rect.right:
                score += 1
                pass_flower = False

    draw_text(str(score), font, black, int(SCREEN_WIDTH / 2), 15)

    # Check for collision If I set the falses to trues, it would kill that group once they collide
    if pygame.sprite.groupcollide(bird_group, flower_group, False, False) or flappy.rect.top < 0:
        game_over = True
        flying = False

    # See if bird hits ground
    if flappy.rect.bottom >= 580:
        game_over = True
        flying = False

    if not game_over and flying:
        # generate flowers
        time_now = pygame.time.get_ticks()
        if time_now - last_flower > flower_freq:

            flower_height = random.randint(-100, 100)
            bot_flower = Flower(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + flower_height, -1)
            top_flower = Flower(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + flower_height, 1)
            flower_group.add(bot_flower)
            flower_group.add(top_flower)
            last_flower = time_now

        # Draw and Move ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    for event in pygame.event.get():
        # Here if the user clicks the "X" in the game will stop.
        if event.type == pygame.QUIT:
            sentinel = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()
pygame.quit()
