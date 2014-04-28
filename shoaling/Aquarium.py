#!/usr/bin/env python
import sys

from numpy.random import random as random
import pygame
from pygame.locals import *

import Prey, Predator
import physics

redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)

NUMBER_OF_PREY = 30
NUMBER_OF_PREDATORS = 0

class Aquarium:
    """This is the main class for creating the aquarium used for visualization of the fish."""

    def __init__(self, width=640, height=480):
        """Initialize pygame."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Aquarium')


    def load_sprites(self):
        """Load all of the fish sprites."""
        self.predator_group = pygame.sprite.Group()
        for i in range(NUMBER_OF_PREDATORS):
            self.predator_group.add(Predator.Predator(rect=pygame.Rect(random()*self.width, random()*self.height, 30, 30)))
        
        self.prey_group = pygame.sprite.Group()
        for i in range(NUMBER_OF_PREY):
            self.prey_group.add(Prey.Prey(rect=pygame.Rect(random()*self.width, random()*self.height, 10, 10)))


    def main_loop(self):
        """The main loop for drawing into the Aquarium."""
        fpsClock = pygame.time.Clock()
        self.load_sprites()

        while True:
            self.screen.fill(blueColor)
            self.predator_group.draw(self.screen)
            self.prey_group.draw(self.screen)

            # Update the fish positions
            for predator in self.predator_group.sprites():
                predator.update(aquarium=self)
            for prey in self.prey_group.sprites():
                prey.update(aquarium=self)

            # Check for all colisions among predators and fish
            spriteHitList = pygame.sprite.groupcollide(self.predator_group, self.prey_group, False, True, collided=physics.fish_collision)
            
            # Check for predator-predator collisions
            spriteHitList = pygame.sprite.groupcollide(self.predator_group, self.predator_group, False, False, collided=physics.predator_collision)
            if len(spriteHitList):
                for me, others in spriteHitList.iteritems():
                    if len(others) > 1:
                        'I collided with more than one fish.'
                    else:
                        me.reflect(others[0])

            # Check for all colisions among fish and fish
            spriteHitList = pygame.sprite.groupcollide(self.prey_group, self.prey_group, False, False, collided=physics.fish_collision)
            if len(spriteHitList):
                for me, others in spriteHitList.iteritems():
                    if len(others) > 1:
                        'I collided with more than one fish.'
                    else:
                        me.reflect(others[0])            

            # Go through a list of all Event objects that happened since the last get()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_a:
                        print '"A" key pressed.'
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT)) # Create an event

            # Draw new window to the screen.
            pygame.display.update()
            fpsClock.tick(45)   # Wait long enough so fps <= 30.


if __name__ == "__main__":
    aquarium = Aquarium()
    aquarium.main_loop()