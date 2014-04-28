import pygame
import numpy as np

from Fish import Fish


ZONE_OF_REPULSION = 20
ZONE_OF_ALIGNMENT = 30
ZONE_OF_ATTRACTION = 40
PREDATOR_FEAR = 60
MAX_SPEED = 15

class Prey(Fish):
    """This is the Fish Sprite that will move around the aquarium. y-axis points DOWN"""
    count = 0

    def __init__(self, rect=None, color=pygame.Color(255, 255, 255)):
        Fish.__init__(self, rect, color)
        Prey.count += 1
        self.preyID = Prey.count
        self.speed = 10


    def run_from_predators(self, predatorList):
        """Run away from the closest predator if it is very close."""
        predatorDistances = [self.distance_to(p) for p in predatorList]
        predatorTuples = zip(predatorList, predatorDistances)
        if not predatorTuples:
            return
        sortedTuples = sorted(predatorTuples, key=lambda x: x[1])
        closestPredator, dist = sortedTuples[0]
        if dist < PREDATOR_FEAR:
            self.speed = MAX_SPEED
            self.run_away(closestPredator)


    def school(self, preyList):
        """If too far from another fish, move towards closest fish."""
        if len(preyList) < 2:
            return

        distances = [self.distance_to(p) for p in preyList]
        preyTuples = zip(preyList, distances)
        sortedTuples = sorted(preyTuples, key=lambda x: x[1])[1:]

        attractiveFish = [fish for fish in sortedTuples if fish[1] < ZONE_OF_ATTRACTION]
        aligningFish = [fish for fish in sortedTuples if fish[1] < ZONE_OF_ALIGNMENT]
        repulsiveFish = [fish for fish in sortedTuples if fish[1] < ZONE_OF_REPULSION]

        # Less neighbors means speed up.
        self.speed = MAX_SPEED / (len(attractiveFish) + 1.)

        # If alone, run towards closest fish.
        if len(sortedTuples):
            closestPrey, dist = sortedTuples[0]
            if dist > ZONE_OF_ATTRACTION:
                self.run_towards(closestPrey)

        # If not align yourself like your buddies.
        if len(aligningFish):
            directions = [f[0].direction for f in aligningFish if f[1] > 0]
            weights = [1. / f[1] for f in aligningFish if f[1] > 0]
            if len(directions):
                self.direction = np.average(directions, weights=weights)


    def update(self, aquarium):
        """Update the fishes position."""
        # Stay near other fish
        preyList = aquarium.prey_group.sprites()
        self.school(preyList)

        # If a predator is within 20 pixels, run away
        predatorList = aquarium.predator_group.sprites()
        self.run_from_predators(predatorList)

        # Check the walls.
        self.check_walls(aquarium.width, aquarium.height)

        # Move the fish.
        self.rect.move_ip(self.xVel(), self.yVel())