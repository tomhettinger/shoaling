import itertools

from pygame.sprite import collide_circle, collide_circle_ratio
import numpy as np

def fish_collision(sprite1, sprite2):
    """Algorithm for determining if there is a collision between the sprites."""
    if sprite1 == sprite2:
        return False
    else:
        return collide_circle(sprite1, sprite2)

def orientation_from_components(dx, dy):
        """Triangulation to return angle of orientation."""
        if float(dx) == 0:
            if float(dy) >= 0:
                orientation = np.pi / 2.
            else:
                orientation = 3.*np.pi / 2.
        else:                
            arctan = np.arctan(float(dy) / float(dx))
            if dx >= 0 and dy >= 0:
                orientation = arctan
            elif dx < 0 and dy >= 0:
                orientation = arctan + np.pi
            elif dx < 0 and dy < 0:
                orientation = arctan + np.pi
            elif dx >= 0 and dy < 0:
                orientation = arctan + 2.0*np.pi
        return orientation