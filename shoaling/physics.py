from math import pi, atan2

from pygame.sprite import collide_circle


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
                orientation = pi / 2.
            else:
                orientation = 3.*pi / 2.
        else:
            orientation = atan2(float(dy), float(dx))
        return orientation