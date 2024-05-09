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
  speed = 5
  cooldown = 2
  last_cast_time = {}
  spawn_cd = 0.1
  last_bolt_spawn = {}
  
  def __init__(self, owner, position, direction, acceleration, size):
    self.viable = handle_cooldown(owner, FrozenOrb.last_cast_time, FrozenOrb.cooldown)
    self.color = glb.BLUE
    self.damage = 4
    super().__init__(owner, position, direction * FrozenOrb.speed,
                     acceleration, size, self.damage, self.color)
    if self.velocity.length() > 0:
      self.bolt_direction = self.velocity.normalize().rotate(20)

  def update(self):
    super().update()
    if self.velocity.length() > 0:
      self.bolt_direction.rotate_ip(glb.SPAWNSPINNER_ROTATION)

  def spawn_bolts(self):
    if handle_cooldown(self, FrozenOrb.last_bolt_spawn, FrozenOrb.spawn_cd):
      return IceBolt(self.owner, self.position, self.bolt_direction, (0, 0), (5, 5))
    return None


class IceBolt(Projectile):
  speed = 10
  
  def __init__(self, owner, position, direction, acceleration, size):
    self.color = glb.LIGHT_BLUE
    self.damage = 2
    super().__init__(owner, position, direction * IceBolt.speed,
                     acceleration, size, self.damage, self.color)


def handle_cooldown(owner, casted_dict, cooldown):
  current_time = time.time()
  if (owner in casted_dict
      and current_time < casted_dict[owner] + cooldown):
    return False
  else:
    casted_dict[owner] = current_time
    return True