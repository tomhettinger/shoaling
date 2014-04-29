from math import sqrt

from Fish import Fish

VISION = 500
ZONE_OF_WALL = 5
ZONE_OF_REPULSION = 100

HUNGER_CONST = -10.0
WALL_CONST = 2.0
REPULSIVE_CONST = 40.0


class Predator(Fish):
    """This is the Predator that will move around the aquarium. y-axis points DOWN"""
    count = 0

    def __init__(self, rect=None, color=None, deathSound=None):
        Fish.__init__(self, rect, color, deathSound)
        Predator.count += 1
        self.predatorID = Predator.count
        self.MAX_SPEED_X = 4.0
        self.MAX_SPEED_Y = 4.0

    def calc_prey_forces(self, preyList):
        """Calculate the force of running away from predators."""
        F_x, F_y = 0, 0
        if not preyList:
            return F_x, F_y
        distances = [self.distance_to(f) for f in preyList]
        sortedPrey = sorted(zip(preyList, distances), key=lambda x: x[1])
        for fish,dist in sortedPrey:
            if self.behind_me(fish):
                continue
            dx = self.rect[0] - fish.rect[0]
            dy = self.rect[1] - fish.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r > VISION or r == 0:
                continue
            else:
                F_x += HUNGER_CONST * (dx / r)
                F_y += HUNGER_CONST * (dy / r)
                break # after we find the closest fish
        return F_x, F_y


    def calc_predator_forces(self, predatorList):
        """Predator-Predator repulsion."""
        F_x, F_y = 0, 0
        if not predatorList:
            return F_x, F_y
        for fish in predatorList:
            if self.behind_me(fish):
                continue
            dx = self.rect[0] - fish.rect[0]
            dy = self.rect[1] - fish.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r > ZONE_OF_REPULSION:
                continue
            if r == 0:
                F_x += (REPULSIVE_CONST / 1.) * (dx / 1.)
                F_y += (REPULSIVE_CONST / 1.) * (dy / 1.)    
            else:
                F_x += (REPULSIVE_CONST / r) * (dx / r)
                F_y += (REPULSIVE_CONST / r) * (dy / r)
        return F_x, F_y  


    def calc_wall_forces(self, width, height):
        """Calculate the inward force of a wall, which is very short range. Either 0 or CONST."""
        F_x, F_y = 0, 0
        if self.rect[0] < ZONE_OF_WALL:
            F_x += WALL_CONST
        elif self.rect[0]+self.rect[2] > (width - ZONE_OF_WALL):
            F_x -= WALL_CONST
        if self.rect[1] < ZONE_OF_WALL:
            F_y += WALL_CONST
        elif self.rect[1]+self.rect[3] > (height - ZONE_OF_WALL):
            F_y -= WALL_CONST
        return F_x, F_y


    def update_velocity(self, aquarium):
        """Update the fishes position."""
        ## If a predator is within 20 pixels, run away
        preyList = aquarium.prey_group.sprites()
        preyForces = self.calc_prey_forces(preyList)

        # Check neighboring predators
        predatorList = aquarium.predator_group.sprites()
        predatorList.remove(self)
        predatorForces = self.calc_predator_forces(predatorList)

        # Check the walls.
        wallForces = self.calc_wall_forces(aquarium.width, aquarium.height)

        # Calculate final speed for this step.
        allForces = [preyForces, wallForces, predatorForces]
        for force in allForces:
            self.xVel += force[0]
            self.yVel += force[1]

        # Ensure fish doesn't swim too fast.
        if self.xVel >= 0:
            self.xVel = min(self.MAX_SPEED_X, self.xVel)
        else:
            self.xVel = max(-self.MAX_SPEED_X, self.xVel)
        if self.yVel >= 0:
            self.yVel = min(self.MAX_SPEED_Y, self.yVel)
        else:
            self.yVel = max(-self.MAX_SPEED_Y, self.yVel)


    def swim(self, aquarium):
        """Using my xVel and yVel values, take a step, so long as we don't swim out of bounds."""
        # Keep fish in the window
        if self.rect[0]+self.xVel <= 0 or self.rect[0]+self.xVel >= aquarium.width:
            dx = 0
        else:
            dx = self.xVel
        if self.rect[1]+self.yVel <= 0 or self.rect[1]+self.yVel >= aquarium.height:
            dy = 0
        else:
            dy = self.yVel

        self.rect.move_ip(dx, dy)