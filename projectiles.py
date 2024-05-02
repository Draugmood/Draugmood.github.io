import time

import globals as glb
from collidables import Collidable


class Projectile(Collidable):

  def __init__(self, owner, position, velocity, acceleration, size, damage, color):
    self.color = color
    super().__init__(position, velocity, acceleration, size, self.color)
    self.owner = owner
    self.damage = damage


class FrozenOrb(Projectile):
  last_cast_time = {}
  cooldown = 3
  
  def __init__(self, owner, position, velocity, acceleration, size):
    self.viable = handle_cooldown(owner, FrozenOrb.last_cast_time, FrozenOrb.cooldown)
    self.color = glb.BLUE
    self.damage = 4
    super().__init__(owner, position, velocity,
                     acceleration, size, self.damage, self.color)


class IceBolt(Projectile):

  def __init__(self, owner, position, velocity, acceleration, size):
    self.color = glb.LIGHT_BLUE
    self.damage = 2
    super().__init__(owner, position, velocity,
                     acceleration, size, self.damage, self.color)


def handle_cooldown(owner, casted_dict, cooldown):
  current_time = time.time()
  if (owner in casted_dict
      and current_time < casted_dict[owner] + cooldown):
    return False
  else:
    casted_dict[owner] = current_time
    return True