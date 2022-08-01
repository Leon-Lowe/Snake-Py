from curses import window
import pygame
from pygame.locals import *
import time

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 500))
        self.surface.fill((110,110,5))
        self.snake = Snake(self.surface)
        self.snake.draw()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
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

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.move_speed = 10
        self.block = pygame.image.load("Resources/Images/block.jpg").convert()
        self.x = 100
        self.y = 100

    def draw(self):
        self.parent_screen.fill((110,110,5))
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.update()

    def move_left(self):
        self.x -= self.move_speed
        self.draw()

    def move_right(self):
        self.x += self.move_speed
        self.draw()

    def move_down(self):
        self.y += self.move_speed
        self.draw()

    def move_up(self):
        self.y -= self.move_speed
        self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()

