import pygame

import config as cf
from collidables import Collidable


class Projectile(Collidable):

  def __init__(self, position, velocity, size, damage):
    super().__init__(position, velocity, size)
    self.damage = damage
    self.color = cf.WHITE

  def draw(self, surface):
    pygame.draw.circle(surface, self.color, self.position, self.size // 2)


class FrozenOrb(Projectile):

  def __init__(self, position, velocity, size, damage):
    super().__init__(position, velocity, size, damage)
    self.color = cf.BLUE


class IceBolt(Projectile):

  def __init__(self, position, velocity, size, damage):
    super().__init__(position, velocity, size, damage)
    self.color = cf.LIGHT_BLUE


# READY TO TRY AND PUT EVERYTHING INTO MAIN GAME LOOP