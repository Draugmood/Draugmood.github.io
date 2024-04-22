import globals as glb
from collidables import Collidable


class Projectile(Collidable):

  def __init__(self, position, velocity, acceleration, size, damage, color):
    self.color = color
    super().__init__(position, velocity, acceleration, size, self.color)
    self.damage = damage


class FrozenOrb(Projectile):

  def __init__(self, position, velocity, acceleration, size, damage):
    self.color = glb.BLUE
    super().__init__(position, velocity, acceleration, size, damage, self.color)


class IceBolt(Projectile):

  def __init__(self, position, velocity, acceleration, size, damage):
    self.color = glb.LIGHT_BLUE
    super().__init__(position, velocity, acceleration, size, damage, self.color)
