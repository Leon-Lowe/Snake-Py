from curses import window
import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOUR = (110, 110, 5)
MAIN_FONT_COLOUR = (237, 237, 237)
SECONDARY_FONT_COLOUR = (156, 156, 156)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(BACKGROUND_COLOUR)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_colliding(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False 

    def play_background_music(self):
        pygame.mixer.music.load("Resources/Sfx/bg_music_1.mp3")
        pygame.mixer.music.play()
    
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"Resources/Sfx/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("Resources/Images/background.jpg")
        self.surface.blit(bg, (0, 0))
    
    def draw_call(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        #Snake colliding with apple
        if self.is_colliding(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            self.play_sound("ding")
            

        #Snake colliding with self
        for i in range(1, self.snake.length):
            if self.is_colliding(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont("arial", 30, True)
        score = font.render(f"Score: {self.snake.length - 1}", True, MAIN_FONT_COLOUR)
        self.surface.blit(score, (0, 0))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOUR)
        line1_font = pygame.font.SysFont("arial", 60, True)
        line2_font = pygame.font.SysFont("arial", 45, False, False)
        line3_font = pygame.font.SysFont("arial", 30, False, True)
        line1 = line1_font.render(f"Game Over", True, MAIN_FONT_COLOUR)
        line2 = line2_font.render(f"Your score was {self.snake.length - 1}", True, MAIN_FONT_COLOUR)
        line3 = line3_font.render(f"Press 'Enter' to play again", True, SECONDARY_FONT_COLOUR)

        self.surface.blit(line1, (200, 300))
        self.surface.blit(line2, (200, 400))
        self.surface.blit(line3, (200, 450))

        pygame.display.update()

        pygame.mixer.music.pause()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if pause:
                        if event.key == K_RETURN:
                            pause = False
                            pygame.mixer.music.unpause()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.draw_call()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.3)

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("Resources/Images/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "down"

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        self.draw()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_down(self):
        self.direction = "down"

    def move_up(self):
        self.direction = "up"

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("Resources/Images/apple.jpg")
        self.parent_screen = parent_screen
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE

if __name__ == "__main__":
    game = Game()
    game.run()

