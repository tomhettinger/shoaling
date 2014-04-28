import itertools
from pygame.sprite import collide_circle, collide_circle_ratio

def fish_collision(sprite1, sprite2):
    """Algorithm for determining if there is a collision between the sprites."""
    if sprite1 == sprite2:
        return False
    else:
        return collide_circle(sprite1, sprite2)

def predator_collision(sprite1, sprite2):
    """Algorithm for determining if there is a collision between the sprites."""
    if sprite1 == sprite2:
        return False
    else:
        collide_func = collide_circle_ratio(5.0)
        return collide_func(sprite1, sprite2)