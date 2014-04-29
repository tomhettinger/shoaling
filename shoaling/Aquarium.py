#!/usr/bin/env python
import sys
from random import random

import pygame
from pygame.locals import *

import Prey, Predator
import physics

redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)

NUMBER_OF_PREY = 13
NUMBER_OF_PREDATORS = 1

class Aquarium:
    """This is the main class for creating the aquarium used for visualization of the fish."""

    def __init__(self, width=800, height=600):
        """Initialize pygame."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Aquarium')
        self.chewSound = pygame.mixer.Sound('./chew.wav')

    def draw_direction_line(self, fish):
        """Given a fish sprite, draw a line of motion using xVel and yVel."""
        startX = fish.rect[0]
        startY = fish.rect[1]
        endX = (fish.rect[0] + 2*fish.xVel)
        endY = (fish.rect[1] + 2*fish.yVel)
        pygame.draw.line(self.screen, blackColor, (startX, startY), (endX, endY), 3)


    def load_sprites(self):
        """Load all of the fish sprites."""
        self.predator_group = pygame.sprite.Group()
        for i in range(NUMBER_OF_PREDATORS):
            self.predator_group.add(Predator.Predator(rect=pygame.Rect(random()*self.width, random()*self.height, 30, 30), color=greenColor))
        
        self.prey_group = pygame.sprite.Group()
        for i in range(NUMBER_OF_PREY):
            self.prey_group.add(Prey.Prey(rect=pygame.Rect(random()*self.width, random()*self.height, 10, 10), deathSound=self.chewSound, color=whiteColor))
        for i in range(NUMBER_OF_PREY):
            self.prey_group.add(Prey.Prey(rect=pygame.Rect(random()*self.width, random()*self.height, 10, 10), deathSound=self.chewSound, color=redColor))

    def main_loop(self):
        """The main loop for drawing into the Aquarium."""
        fpsClock = pygame.time.Clock()
        self.load_sprites()

        while True:
            self.screen.fill(blueColor)
            self.predator_group.draw(self.screen)
            self.prey_group.draw(self.screen)

            # Update the fish velocities
            for predator in self.predator_group.sprites():
                predator.update_velocity(aquarium=self)
            for prey in self.prey_group.sprites():
                prey.update_velocity(aquarium=self)

            # Move fish                
            for predator in self.predator_group.sprites():
                predator.swim(aquarium=self)                
            for prey in self.prey_group.sprites():
                prey.swim(aquarium=self)

            # Draw direction arrows
            for predator in self.predator_group.sprites():
                self.draw_direction_line(predator)
            for fish in self.prey_group.sprites():
                self.draw_direction_line(fish)

            # Check for all colisions among predators and fish
            spriteHitList = pygame.sprite.groupcollide(self.predator_group, self.prey_group, False, True, collided=physics.fish_collision)

            # Go through a list of all Event objects that happened since the last get()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        Prey.ATTRACTIVE_CONST -= 1.0
                        Prey.ATTRACTIVE_CONST = min(0.0, Prey.ATTRACTIVE_CONST)
                        print 'ATTRACTIVE_CONST = %.1f' % Prey.ATTRACTIVE_CONST
                    if event.key == K_a:
                        Prey.ATTRACTIVE_CONST += 1.0
                        Prey.ATTRACTIVE_CONST = min(0.0, Prey.ATTRACTIVE_CONST)
                        print 'ATTRACTIVE_CONST = %.1f' % Prey.ATTRACTIVE_CONST
                    if event.key == K_w:
                        Prey.REPULSIVE_CONST += 1.0
                        Prey.REPULSIVE_CONST = max(0.0, Prey.REPULSIVE_CONST)
                        print 'REPULSIVE_CONST = %.1f' % Prey.REPULSIVE_CONST
                    if event.key == K_s:
                        Prey.REPULSIVE_CONST -= 1.0
                        Prey.REPULSIVE_CONST = max(0.0, Prey.REPULSIVE_CONST)
                        print 'REPULSIVE_CONST = %.1f' % Prey.REPULSIVE_CONST
                    if event.key == K_e:
                        Prey.ALIGNMENT_CONST += 0.1
                        Prey.ALIGNMENT_CONST = max(0.0, Prey.ALIGNMENT_CONST)
                        print 'ALIGNMENT_CONST = %.1f' % Prey.ALIGNMENT_CONST
                    if event.key == K_d:
                        Prey.ALIGNMENT_CONST -= 0.1
                        Prey.ALIGNMENT_CONST = max(0.0, Prey.ALIGNMENT_CONST)
                        print 'ALIGNMENT_CONST = %.1f' % Prey.ALIGNMENT_CONST
                    if event.key == K_r:
                        Prey.WALL_CONST += 1.0
                        Prey.WALL_CONST = max(0.0, Prey.WALL_CONST)
                        print 'WALL_CONST = %.1f' % Prey.WALL_CONST
                    if event.key == K_f:
                        Prey.WALL_CONST -= 1.0
                        Prey.WALL_CONST = max(0.0, Prey.WALL_CONST)
                        print 'WALL_CONST = %.1f' % Prey.WALL_CONST
                    if event.key == K_t:
                        Prey.FEAR_CONST += 1.0
                        Prey.FEAR_CONST = max(0.0, Prey.FEAR_CONST)
                        print 'FEAR_CONST = %.1f' % Prey.FEAR_CONST
                    if event.key == K_g:
                        Prey.FEAR_CONST -= 1.0
                        Prey.FEAR_CONST = max(0.0, Prey.FEAR_CONST)
                        print 'FEAR_CONST = %.1f' % Prey.FEAR_CONST

                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT)) # Create an event

            # Draw new window to the screen.
            pygame.display.update()
            fpsClock.tick(30)   # Wait long enough so fps <= 30.


def main():
    aquarium = Aquarium()
    aquarium.main_loop()

if __name__ == "__main__":
    main()