import pygame

import globals as glb
from collidables import Collidable


class Projectile(Collidable):

  def __init__(self, position, velocity, acceleration, size, damage):
    self.color = glb.WHITE #default
    super().__init__(position, velocity, acceleration, size, self.color)
    self.damage = damage


class FrozenOrb(Projectile):

  def __init__(self, position, velocity, acceleration, size, damage):
    super().__init__(position, velocity, acceleration, size, damage)
    self.color = glb.BLUE


class IceBolt(Projectile):

  def __init__(self, position, velocity, acceleration, size, damage):
    super().__init__(position, velocity, acceleration, size, damage)
    self.color = glb.LIGHT_BLUE

