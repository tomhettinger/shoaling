from math import sqrt

from Fish import Fish

ZONE_OF_REPULSION = 50
ZONE_OF_ALIGNMENT = 100
ZONE_OF_ATTRACTION = 400
ZONE_OF_WALL = 30
ZONE_OF_FEAR = 80

ATTRACTIVE_CONST = -11.0
REPULSIVE_CONST = 12.0
ALIGNMENT_CONST = 0.5
WALL_CONST = 2.0
FEAR_CONST = 4.0


class Prey(Fish):
    """This is the Fish Sprite that will move around the aquarium. y-axis points DOWN"""
    count = 0

    def __init__(self, rect=None, color=None, deathSound=None):
        Fish.__init__(self, rect, color, deathSound)
        Prey.count += 1
        self.preyID = Prey.count
        self.MAX_SPEED_X = 9.0
        self.MAX_SPEED_Y = 9.0


    def calc_predator_forces(self, predatorList):
        """Calculate the force of running away from predators."""
        F_x, F_y = 0, 0
        if not predatorList:
            return F_x, F_y
        for predator in predatorList:
            if self.behind_me(predator):
                continue
            dx = self.rect[0] - predator.rect[0]
            dy = self.rect[1] - predator.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r > ZONE_OF_FEAR or r == 0:
                continue
            F_x += FEAR_CONST * (dx / r)
            F_y += FEAR_CONST * (dy / r)
        return F_x, F_y


    def calc_attractive_forces(self, preyList):
        """Calculate the attractive forces due to every other fish.
        Return the force in the (x,y) directions."""
        F_x, F_y = 0, 0
        if not preyList:
            return F_x, F_y
        for fish in preyList:
            if fish.color != self.color:
                continue
            if self.behind_me(fish):
                continue
            dx = self.rect[0] - fish.rect[0]
            dy = self.rect[1] - fish.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r > ZONE_OF_ATTRACTION or r <= ZONE_OF_REPULSION:
                continue
            F_x += (ATTRACTIVE_CONST / r) * (dx / r)
            F_y += (ATTRACTIVE_CONST / r) * (dy / r)
        return F_x, F_y


    def calc_repulsive_forces(self, preyList):
        """Calculate the repulsive force due to close by fish.
        Return the force in (x,y) directions."""
        F_x, F_y = 0, 0
        if not preyList:
            return F_x, F_y
        for fish in preyList:
            if self.behind_me(fish):
                continue
            dx = self.rect[0] - fish.rect[0]
            dy = self.rect[1] - fish.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r == 0 or r > ZONE_OF_REPULSION:
                continue
            F_x += (REPULSIVE_CONST / r) * (dx / r)
            F_y += (REPULSIVE_CONST / r) * (dy / r)
        return F_x, F_y        


    def calc_alignment_forces(self, preyList):
        """Calculate the alignment force due to other close fish. Fish like to
        swim in the same direction as other fish. Return the force in (x,y) directions."""
        F_x, F_y = 0, 0
        if not preyList:
            return F_x, F_y
        for fish in preyList:
            if fish.color != self.color:
                continue
            if self.behind_me(fish):
                continue
            dx = self.rect[0] - fish.rect[0]
            dy = self.rect[1] - fish.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r < ZONE_OF_REPULSION or r > ZONE_OF_ALIGNMENT:
                continue
            F_x += fish.xVel * (ALIGNMENT_CONST / r)
            F_y += fish.yVel * (ALIGNMENT_CONST / r)
        return F_x, F_y                


    def calc_wall_forces(self, width, height):
        """Calculate the inward force of a wall, which is very short range. Either 0 or CONST."""
        F_x, F_y = 0, 0
        if self.rect[0] < ZONE_OF_WALL:
            F_x += WALL_CONST
        elif (self.rect[0]+self.rect[2]) > (width-ZONE_OF_WALL):
            F_x -= WALL_CONST
        if self.rect[1] < ZONE_OF_WALL:
            F_y += WALL_CONST
        elif (self.rect[1]+self.rect[3]) > (height-ZONE_OF_WALL):
            F_y -= WALL_CONST
        return F_x, F_y


    def update_velocity(self, aquarium):
        """Update the fishes velocity based on forces from other fish."""
        # Stay near other fish, but not too close, and swim in same direction.
        preyList = aquarium.prey_group.sprites()
        preyList.remove(self)
        attractiveForces = self.calc_attractive_forces(preyList)
        repulsiveForces = self.calc_repulsive_forces(preyList)
        alignmentForces = self.calc_alignment_forces(preyList)

        # If a predator is within 20 pixels, run away
        predatorList = aquarium.predator_group.sprites()
        predatorForces = self.calc_predator_forces(predatorList)

        # Check the walls.
        wallForces = self.calc_wall_forces(aquarium.width, aquarium.height)

        # Calculate final speed for this step.
        allForces = [repulsiveForces, attractiveForces, alignmentForces, wallForces, predatorForces]
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