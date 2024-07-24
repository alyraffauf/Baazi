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

import os
import pygame
from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    fullname = os.path.realpath(fullname)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Entity(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(1, 1, 32, 32)
        self.position = [1,1]
        self.x_speed = 0
        self.y_speed = 0

    def vertical_move(self, speed):
        self.y_speed = speed

    def horizontal_move(self, speed):
        self.x_speed = speed

    def horizontal_stop(self):
        self.x_speed = 0

    def vertical_stop(self):
        self.y_speed = 0

    def stop(self):
        self.vertical_stop()
        self.horizontal_stop()

    def update(self, obstacles, portals):
        self.rect.left += self.x_speed
        self.rect.top += self.y_speed
        self.position = (self.position[0] + self.x_speed, self.position[1] + self.y_speed)
        # If colliding, go back
        # if pygame.sprite.spritecollide(self,obstacles,False):
        #     self.position = self.position[0], self.position[1] - self.y_speed

        # if pygame.sprite.spritecollide(self,obstacles,False): 
        #     self.position = self.position[0] - self.x_speed, self.position[1]

        #if pygame.sprite.spritecollide(self, portals, False):
        #    print "test"

        self.rect.left = self.position[0]
        self.rect.top = self.position[1]

class StationaryEntity(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self, obstacles):
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]

class House(StationaryEntity):

    def __init__(self):
        StationaryEntity.__init__(self)
        self.image = pygame.image.load("images/house2.png")
        self.rect = self.image.get_rect()
        self.image.convert()

class Door(StationaryEntity):

    def __init__(self):
        StationaryEntity.__init__(self)
        self.image = pygame.image.load("images/door1.png")
        self.rect = self.image.get_rect()
        self.image.convert()

class Rock(StationaryEntity):

    def __init__(self):
        StationaryEntity.__init__(self)
        self.image = pygame.image.load("images/sprite2.png")
        self.rect = self.image.get_rect()
        self.image.convert()

class Hero(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.health = 100
        self.life = 5
        self.inventory = []

    def shoot(self):
        print("shoot!")

    def decrease_health(self, amount):
        self.health = self.health - amount
        if self.health <= 0:
            print("dead!")

    def increase_health(self, amount):
        self.health += amount
