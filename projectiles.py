import pygame

import config as cf
from collidables import Collidable


class Projectile(Collidable):

  def __init__(self, position, velocity, acceleration, size, damage):
    super().__init__(position, velocity, acceleration, size)
    self.damage = damage
    self.color = cf.WHITE

  def draw(self, surface):
    # temporary implementation
    pygame.draw.circle(surface, self.color, self.position, self.size[0] // 2)


class FrozenOrb(Projectile):

  def __init__(self, position, velocity, acceleration, size, damage):
    super().__init__(position, velocity, acceleration, size, damage)
    self.color = cf.BLUE


class IceBolt(Projectile):

  def __init__(self, position, velocity, acceleration, size, damage):
    super().__init__(position, velocity, acceleration, size, damage)
    self.color = cf.LIGHT_BLUE


# READY TO TRY AND PUT EVERYTHING INTO MAIN GAME LOOP