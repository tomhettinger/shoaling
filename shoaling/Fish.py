"""Consider using cartesian vectors only, and ditching the polar.  (self.vector = x, y for direction)"""
import pygame
from pygame.locals import *

import numpy as np


class Fish(pygame.sprite.Sprite):
    """This is the Fish Sprite that will move around the aquarium. y-axis points DOWN"""
    count = 0

    def __init__(self, rect=None, color=None):
        pygame.sprite.Sprite.__init__(self)
        
        Fish.count += 1
        self.fishID = Fish.count

        if color is not None:
            self.color = color
        else:
            self.color = pygame.Color(255, 0, 0)

        if rect is not None:
            self.image = pygame.Surface([rect[2], rect[3]])
            self.image.fill(self.color)
            self.rect = rect
        else:
            self.image = pygame.Surface([20, 20])
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
        
        self.speed = 10
        self.direction = np.random.random()*2.0*np.pi


    def xVel(self):
        """Compute the velocity in the x-axis"""
        return self.speed*np.cos(self.direction)


    def yVel(self):
        """Compute the velocity in the y-axis"""
        return self.speed*np.sin(self.direction)


    def update_direction(self, xDir, yDir):
        if float(xDir) == 0:
            if float(yDir) >= 0:
                newDirection = np.pi / 2.
            else:
                newDirection = 3.*np.pi / 2.

        else:                
            arctan = np.arctan(float(yDir) / float(xDir))
            if xDir >= 0 and yDir >= 0:
                newDirection = arctan
            elif xDir < 0 and yDir >= 0:
                newDirection = arctan + np.pi
            elif xDir < 0 and yDir < 0:
                newDirection = arctan + np.pi
            elif xDir >= 0 and yDir < 0:
                newDirection = arctan + 2.0*np.pi

        try:
            self.direction = newDirection
        except:
            print xDir, yDir


    def reflect(self, otherFish):
        """Due to a collision, this fish needs to change direction."""
        xDir = np.cos(self.direction)
        yDir = np.sin(self.direction)
        myX, myY = self.rect[0], self.rect[1]
        otherX, otherY = otherFish.rect[0], otherFish.rect[1]
        deltaX = myX - otherX
        deltaY = myY - otherY
        if abs(deltaX) >= abs(deltaY):
            xDir = np.cos(self.direction)
            if deltaX >= 0:
                xDir = abs(xDir)
            else:
                xDir = -1.0*abs(xDir)
        else:
            yDir = np.sin(self.direction)
            if deltaY >= 0:
                yDir = abs(yDir)
            else:
                yDir = -1.0*abs(yDir)
        self.update_direction(xDir, yDir)


    def check_walls(self, width, height):
        """If I reach an edge, reflect off of it."""
        xDir = np.cos(self.direction)
        yDir = np.sin(self.direction)
        leftEdge = self.rect[0]
        rightEdge = self.rect[0] + self.rect[2]
        topEdge = self.rect[1]
        bottomEdge = self.rect[1] + self.rect[3]
        if leftEdge < 0:
            xDir = abs(xDir)
        if rightEdge > width:
            xDir = -1.0*abs(xDir)
        if topEdge < 0:
            yDir = abs(yDir)
        if bottomEdge > height:
            yDir = -1.0*abs(yDir)
        self.update_direction(xDir, yDir)


    def run_away(self, otherFish):
        """Run in opposite direction as otherFish."""
        myX, myY = self.rect[0], self.rect[1]
        otherX, otherY = otherFish.rect[0], otherFish.rect[1]
        deltaX = myX - otherX
        deltaY = myY - otherY
        self.update_direction(deltaX, deltaY)


    def run_towards(self, otherFish):
        """Run towards otherFish."""
        myX, myY = self.rect[0], self.rect[1]
        otherX, otherY = otherFish.rect[0], otherFish.rect[1]
        deltaX = myX - otherX
        deltaY = myY - otherY
        self.update_direction(-deltaX, -deltaY)


    def distance_to(self, otherFish):
        """Calculate the distance to another fish."""
        myX, myY = self.rect[0], self.rect[1]
        otherX, otherY = otherFish.rect[0], otherFish.rect[1]
        return np.sqrt((myX-otherX)**2 + (myY-otherY)**2)


    def update(self, aquarium):
        """Update the fishes position."""
        # Check the walls.
        self.check_walls(aquarium.width, aquarium.height)

        # Move the fish.
        self.rect.move_ip(self.xVel(), self.yVel())