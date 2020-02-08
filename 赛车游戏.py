import pygame
from pygame.locals import *
import sys
import time
import random

WINDOW_WIDTH = 486
WINDOW_HEIGHT = 757
DEFAULT_FPS = 60
DEFAULT_DELAY = 1.0 / DEFAULT_FPS - 0.002


class Car:
    def __init__(self, window):
        self.window = window
        self.img = pygame.image.load('img/car.png')
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = WINDOW_WIDTH / 6 - self.width / 2
        self.y = WINDOW_HEIGHT - 200

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move_left(self):
        sound = pygame.mixer.Sound('snd/car.wav')
        sound.play()
        if self.x < WINDOW_WIDTH / 6 - self.width / 2:
            self.x = WINDOW_WIDTH / 6 - self.width / 2
        else:
            self.position = [WINDOW_WIDTH / 6 - self.width / 2, WINDOW_WIDTH / 2 - self.width / 2,
                             WINDOW_WIDTH * 5 / 6 - self.width / 2]
            index = self.position.index(self.x)
            if 0 < index < len(self.position):
                index -= 1
                self.x = self.position[index]

    def move_right(self):
        sound = pygame.mixer.Sound('snd/car.wav')
        sound.play()
        if self.x > WINDOW_WIDTH - WINDOW_WIDTH / -self.width / 2:
            self.x = WINDOW_WIDTH - WINDOW_WIDTH / 6 - self.width / 2
        else:
            self.position = [WINDOW_WIDTH / 6 - self.width / 2, WINDOW_WIDTH / 2 - self.width / 2,
                             WINDOW_WIDTH * 5 / 6 - self.width / 2]
            index = self.position.index(self.x)
            if index < len(self.position) - 1:
                index += 1
                self.x = self.position[index]


class Stone:
    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):
        self.img = pygame.image.load('img/stone.png')
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        position = [WINDOW_WIDTH / 6 - self.width / 2, WINDOW_WIDTH / 2 - self.width / 2,
                    WINDOW_WIDTH * 5 / 6 - self.width / 2]
        self.x = position[random.randint(0, 2)]
        self.y = -self.height

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move(self, score):
        self.y += 10
        if self.y > WINDOW_HEIGHT:
            self.reset()


class Bomb:
    def __init__(self, window, x, y):
        self.window = window
        self.imgs = []
        for i in range(1, 14):
            self.imgs.append(pygame.image.load('img/image {}.png'.format(i)))
        self.index = 0
        self.img = self.imgs[self.index]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x - self.width / 2
        self.y = y - self.height / 2
        self.is_destroyed = False
        sound = pygame.mixer.Sound('snd/bomb.wav')
        sound.play()

    def display(self):
        if self.index >= len(self.imgs):
            self.is_destroyed = True
            return
        self.img = self.imgs[self.index]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.window.blit(self.img, (self.x, self.y))
        self.index += 1


def Conclusion():
    global finish_text, ft_x, ft_y, finish2_text, ft2_x, ft2_y
    font_text = pygame.font.Font('font/happy.ttf', 50)
    finish_text = font_text.render('游戏结束', True, (0xff, 0, 0))
    ft_width = finish_text.get_width()
    ft_height = finish_text.get_height()
    ft_x = (WINDOW_WIDTH - ft_width) / 2
    ft_y = (WINDOW_HEIGHT - ft_height) / 2 - 50
    finish2_text = font_text.render('最终得分:%d' % score, True, (0xff, 0, 0))
    ft2_width = finish2_text.get_width()
    ft2_height = finish2_text.get_height()
    ft2_x = (WINDOW_WIDTH - ft2_width) / 2
    ft2_y = (WINDOW_HEIGHT - ft2_height) / 2 + 30


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('赛车')
    pygame.display.set_icon(pygame.image.load('img/car_1.png'))
    fps = 0
    score = 0
    bg = pygame.image.load('img/Lane.PNG')
    # newImage = pygame.transform.scale(image, (w, h))
    font = pygame.font.Font('font/happy.ttf', 24)
    car = Car(window)
    is_over = False
    stones = []
    for i in range(2):
        stones.append(Stone(window))
    bombs = []
    pygame.mixer_music.load('snd/The Racer.mp3')
    pygame.mixer_music.play(-1)
    while True:
        start = time.time()
        window.blit(bg, (0, 0))
        fps_text = font.render('FPS: %d' % fps, True, (255, 0, 0))
        window.blit(fps_text, (370, 20))
        score_text = font.render('积分：%d' % score, True, (0x33, 0xCC, 0x33))
        window.blit(score_text, (10, 20))
        Conclusion()
        if is_over:
            window.blit(finish_text, (ft_x, ft_y))
            window.blit(finish2_text, (ft2_x, ft2_y))
        if not is_over:
            car.display()
            car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
            for stone in stones:
                stone_rect = pygame.Rect(stone.x, stone.y, stone.width, stone.height)
                stone.display()
                stone.move(score)
                events = pygame.event.get()
                for event in events:
                    if event.type == KEYDOWN:
                        if event.key == K_LEFT:
                            car.move_left()
                        if event.key == K_RIGHT:
                            car.move_right()
                if pygame.Rect.colliderect(stone_rect, car_rect):
                    bombs.append(Bomb(window, car.x + car.width / 2, car.y + car.height / 2))
                    is_over = True
                if stone.y > WINDOW_HEIGHT - 10:
                    score += 10
        for bomb in bombs:
            if bomb.is_destroyed:
                bombs.remove(bomb)
            bomb.display()
        pygame.display.flip()
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and is_over:
                    for stone in stones:
                        stone.reset()
                    score = 0
                    is_over = False
        key = pygame.key.get_pressed()
        if key[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        end = time.time()
        cost = end - start
        if cost < DEFAULT_DELAY:
            sleep = DEFAULT_DELAY - cost
        else:
            sleep = 0
        time.sleep(sleep)
        end = time.time()
        fps = 1.0 / (end - start)
