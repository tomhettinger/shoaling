import pygame

from Fish import Fish

VISION = 200

class Predator(Fish):
    """This is the Predator that will move around the aquarium. y-axis points DOWN"""
    count = 0

    def __init__(self, rect=None, color=pygame.Color(0, 255, 0)):
        Fish.__init__(self, rect, color)
        Predator.count += 1
        self.predatorID = Predator.count
        self.speed = 7


    def run_to_prey(self, preyList):
        """Run away from the closest predator if it is very close."""
        preyDistances = [self.distance_to(p) for p in preyList]
        preyTuples = zip(preyList, preyDistances)
        if not preyTuples:
            return
        sortedTuples = sorted(preyTuples, key=lambda x: x[1])
        closestPrey, dist = sortedTuples[0]
        if dist < VISION:
            self.run_towards(closestPrey)


    def update(self, aquarium):
        """Update the fishes position."""
        ## If a predator is within 20 pixels, run away
        preyList = aquarium.prey_group.sprites()
        self.run_to_prey(preyList)

        # Check the walls.
        self.check_walls(aquarium.width, aquarium.height)

        # Move the fish.
        self.rect.move_ip(self.xVel(), self.yVel())