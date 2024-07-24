#!/usr/bin/env python2
# Copyright (C) 2013 Alexandra Chace <marilyn@marilync.co>

# Baazi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Baazi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Baazi. If not, see <http://www.gnu.org/licenses/>.

import pygame
import sys
import os
import time
from pygame.locals import *
from characters import *

# Set the resolution in which the game runs.
WIN_WIDTH = 800
WIN_HEIGHT = 600
HALF_WIDTH = 400
HALF_HEIGHT = 300

def camera_func(camera, target_rect):
    """This is a really simple camera that never stops scrolling"""
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def camera_func(camera, target_rect):
    """This is a smart camera that respects boundaries"""
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # Stops scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   
    t = max(-(camera.height-WIN_HEIGHT), t) 
    t = min(0, t)                           # Stops scrolling at the top
    return Rect(l, t, w, h)

class Camera(object):
    def __init__(self):
        self.camera_func = camera_func
        self.state = Rect(0, 0, WIN_WIDTH*32, WIN_HEIGHT*32)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

class Baazi():
    def __init__(self):
        pygame.display.init()

        self.camera = Camera()

        self.load_map("map1.png")
        pygame.display.set_caption("Baazi")

        self.characters = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        
        self.town1() # Loads a demo level.

        # Now it's time to add our player to the map.
        self.player= Hero()
        self.player.image = pygame.image.load("images/player1.png")
        self.player.rect = pygame.Rect(320, 240, 16, 32)
        self.player.position = [320,240]
        self.player.image.convert()
        self.characters.add(self.player)

    def load_map(self, mapname):
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 0)
        self.screen = pygame.display.get_surface()
        fullname = os.path.join('images', mapname)
        fullname = os.path.realpath(fullname)

        self.background = pygame.image.load(fullname)
        self.background.convert()

    def town1(self):
        """Builds a simple town to explore."""
        town = [
        "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
        "RH   H                           HR",
        "R                                          R",
        "R                                          R",
        "R D      D                              D  R",
        "R                                          R",
        "R                                          R",
        "R                                          R",
        "R    RRRRRRRR                              R",
        "R                                          R",
        "R                              RRRRRRR     R",
        "R                   RRRRRR                 R",
        "R                                          R",
        "R         RRRRRRR                          R",
        "R                                          R",
        "R                     RRRRRR               R",
        "R                                          R",
        "R   RRRRRRRRRRR                            R",
        "R                                          R",
        "R                 RRRRRRRRRRR              R",
        "R                                          R",
        "R                                          R",
        "R                                          R",
        "R                                          R",
        "RRRRRRRRRRRRRRRRRRRRRRRRRRRRR      RRRRRRRRR",]

        x = y = 0

        for row in town:
            for col in row:
                if col == "R":
                    rock = Rock()
                    rock.position = (x,y)
                    self.obstacles.add(rock)
                    size_x = 16
                    size_y = 16
                elif col == "H":
                    house = House()
                    house.position = [x,y]
                    self.obstacles.add(house)
                    size_x = 64
                    size_y = 64
                elif col == "D":
                    door = Door()
                    door.position = [x,y]
                    self.portals.add(door)
                    size_x = 16
                    size_y = 16
                else:
                    size_x = 16
                    size_y = 16
                x += size_x
            y += size_y
            x = 0

    def load_house(self):
        for e in self.obstacles:
            e.kill()
        for e in self.portals:
            e.kill()
        self.load_map("map5.png")
    def show(self):
        self.event_input(pygame.event.get())
        
        self.screen = pygame.display.get_surface()
        self.screen.blit(self.background, (0, 0))

        self.camera.update(self.player)
        self.player.update(self.obstacles, self.portals)
        for e in self.characters:
            if pygame.sprite.spritecollide(self.player,self.obstacles,False):
                self.player.position = self.player.position[0] - self.player.x_speed, self.player.position[1] - self.player.y_speed
                self.player.y_speed = 0
                self.player.x_speed = 0
            if pygame.sprite.spritecollide(self.player, self.portals, False):
                self.load_house()
            e.update(self.obstacles, self.portals)
            self.screen.blit(e.image, self.camera.apply(e))

        for e in self.obstacles:
            e.update(self.obstacles)
            self.screen.blit(e.image, self.camera.apply(e))

        for e in self.portals:
            e.update(self.portals)
            self.screen.blit(e.image, self.camera.apply(e))


        
        pygame.display.update()

    def event_input(self, events):
        for event in events: 
            if event.type == QUIT: 
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.player.horizontal_move(-5)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.player.horizontal_move(5)
            elif event.type == KEYDOWN and event.key == K_UP:
                self.player.vertical_move(-5)
            elif event.type == KEYDOWN and event.key == K_DOWN:
                self.player.vertical_move(5)
            elif event.type == KEYUP and (event.key == K_LEFT or event.key == K_RIGHT):
                self.player.horizontal_stop()
            elif event.type == KEYUP and (event.key == K_UP or event.key == K_DOWN):
                self.player.vertical_stop()
            elif event.type == KEYUP and event.key == K_SPACE:
                self.player.shoot()
            else: 
                print(event)

if __name__ == '__main__':
    baazi = Baazi()
    while True:
        clock = pygame.time.Clock()
        clock.tick(60)
        baazi.show()
