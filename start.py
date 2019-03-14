#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 09:11:06 2018

@author: oem
"""
import math
import pygame, sys
from pygame.locals import *




FPS = 30

SCREENWIDTH = 1024
SCREENHEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


all_sprites = pygame.sprite.Group()


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    pygame.mixer.quit()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Neras First')

    background = pygame.image.load('testing/stars.png').convert()
    background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
    background_rect = background.get_rect()


    player = Player()
    mob = Mob()
    '''player2 = Player()
    player_sprite = pygame.image.load('testing/circle.png').convert_alpha()
    player_ship = pygame.transform.scale(player_sprite, (70, 70))
    player2.image = player_ship
    player2.x -= 75
    player2.y += 80'''

    while True:
        #event = Event()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                player.shoot()

        SCREEN.blit(background, background_rect)

        player.draw(SCREEN)
        player.onKeyPress(SCREEN)
        all_sprites.add(mob)
        all_sprites.update()
        all_sprites.draw(SCREEN)

        updateRotation(player)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def updateRotation(player):
    x, y = pygame.mouse.get_pos()

    rel_x, rel_y = x - player.rect.centerx, y - player.rect.centery
    angle = math.atan2(rel_y, rel_x)

    angle = ((180 / math.pi) * -math.atan2(rel_y, rel_x)) + 90



    rot = player.rotation# = player.rotation % 360
    db = rot - angle #degrees difference between player rotation and mouse
    if db == 180 or db == -180:
        return
    elif db > 182 and db < 360 or db > -178 and db < 0:
        player.rotation -= 2 #rotate right
    elif db < -182 and db > -360 or db > 0 and db < 178:
        player.rotation += 2 #left
    else:
        player.rotation = angle + 180
    #player.rotation = angle

    player.rotatedImage = pygame.transform.rotate(player.image, player.rotation)
    player.rotated_image_rect = player.rotatedImage.get_rect()

    player.rotated_image_rect.centerx = player.rect.centerx = player.x - player.x_len//2
    player.rotated_image_rect.centery = player.rect.centery = player.y - player.y_len//2



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rotation = 0.0
        player_sprite = pygame.image.load('testing/ship.png').convert_alpha()
        player_ship = pygame.transform.scale(player_sprite, (40, 70))
        self.image = player_ship
        self.rotatedImage = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.x = int(SCREENWIDTH * 0.5 - 25)
        self.y = int(SCREENHEIGHT * .7)
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.shoot_delay = 80
        self.last_shot = pygame.time.get_ticks()
        self.rotated_image_rect = self.rect
        bx, by = self.rect.bottomright
        self.x_len = bx - self.x
        self.y_len = by - self.y
    def draw(self,surface):
        surface.blit(self.rotatedImage, self.rotated_image_rect)

    def onKeyPress(self,surface):
        key = pygame.key.get_pressed()
        distance = 5
        if key[ord('s')] or key[pygame.K_DOWN]: #down
            self.y += distance
        elif key[ord('w')] or key[pygame.K_UP]: #up
            self.y -= distance
        if key[ord('d')] or key[pygame.K_RIGHT]: #right
            self.x += distance
        elif key[ord('a')] or key[pygame.K_LEFT]: #left
            self.x -= distance

        if key[ord('e')] or key[ord('q')]:
            if key[ord('e')]:
                self.rotation -= 3
            if key[ord('q')]:
                self.rotation += 3

            self.rotatedImage = pygame.transform.rotate(self.image, self.rotation)
            self.rotated_image_rect = self.rotatedImage.get_rect()

        self.rotated_image_rect.centerx = self.rect.centerx = self.x - self.x_len//2
        self.rotated_image_rect.centery = self.rect.centery = self.y - self.y_len//2

    def update(self):
        pass

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            laser = Laser(self.rect.centerx, self.rect.centery, self.rotation)
            all_sprites.add(laser)


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation):
        pygame.sprite.Sprite.__init__(self)
        print(rotation)
        self.image = pygame.image.load('testing/laser.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (5,9))
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image, self.rotation)

#        self.image.set_colorkey(BLACK) this would make black background not
#       show if i wasnt using conver alpha? test it

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10

    def update(self):
        #self.rect.y = math.cos(self.rotation/57.3)*self.rect.y
        self.rect.centery -= math.cos(self.rotation/57.2958)*self.speed
        self.rect.centerx -= math.sin(self.rotation/57.2958)*self.speed
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > SCREENHEIGHT:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rotation = 0 #pointAtPlayer() later
        player_sprite = pygame.image.load('testing/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(player_sprite, (50, 70))
      #  self.rotatedImage = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.x = int(SCREENWIDTH * 0.5 - 25)
        self.y = 70
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.shoot_delay = 80
        self.last_shot = pygame.time.get_ticks()
        #self.rotated_image_rect = self.rect
        bx, by = self.rect.bottomright
        self.x_len = bx - self.x
        self.y_len = by - self.y

    def update(self):
        pass



'''
class Event(object):
    def __init__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
           elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:

'''






if __name__ == '__main__':
    main()
