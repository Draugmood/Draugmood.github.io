import pygame

import globals as glb
from collidables import Collidable


class Projectile(Collidable):

  def __init__(self, position, velocity, acceleration, size, damage):
    super().__init__(position, velocity, acceleration, size)
    self.damage = damage
    self.color = glb.WHITE

  def draw(self, surface):
    # temporary implementation
    pygame.draw.circle(surface, self.color, self.position, self.size[0] // 2)


class FrozenOrb(Projectile):

  def __init__(self, position, velocity, acceleration, size, damage):
    super().__init__(position, velocity, acceleration, size, damage)
    self.color = glb.BLUE


class IceBolt(Projectile):

  def __init__(self, position, velocity, acceleration, size, damage):
    super().__init__(position, velocity, acceleration, size, damage)
    self.color = glb.LIGHT_BLUE


# READY TO TRY AND PUT EVERYTHING INTO MAIN GAME LOOP