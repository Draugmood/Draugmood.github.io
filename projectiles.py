import math
import time

from pygame import Vector2 as vec

import globals as glb
from characters import Character
from collidables import Collidable


class Projectile(Collidable):
  lifespan = 2

  def __init__(self, owner, position, velocity, acceleration, size, damage,
               color):
    self.color = color
    super().__init__(position, velocity, acceleration, size, self.color)
    self.owner = owner
    self.damage = damage
    self.dead = False
    self.birth = time.time()

  def update(self):
    super().update()
    if (time.time() - self.birth) > self.lifespan:
      self.dead = True

  def hit(self, other: Collidable):
    other.health -= self.damage

  def draw(self, surface):
    super().draw(surface)


class Grenade(Projectile):
  speed = 6

  def __init__(self, owner, position, target, acceleration, size):
    self.color = glb.WHITE
    self.damage = 20
    self.angle = math.atan2(target.y - position.y, target.x - position.x)
    self.direction = vec(1, 0).rotate_rad(self.angle)
    self.speed_decay = 0
    self.gravity = acceleration[1]

    self.travel_distance = position.distance_to(target)
    self.travel_time = self.travel_distance / Grenade.speed

    self.v_speed = self.travel_time * self.gravity / 2
    velocity = self.direction * Grenade.speed
    velocity.y += self.v_speed

    super().__init__(owner, position, velocity, acceleration, size,
                     self.damage, self.color)


class FrozenOrb(Projectile):
  speed = 5
  cooldown = 2
  last_cast_time = {}
  spawn_cd = 0.1
  last_bolt_spawn = {}
  explode_bolts = 10

  def __init__(self, owner, position, direction, acceleration, size):
    self.viable = handle_cooldown(owner, FrozenOrb.last_cast_time,
                                  FrozenOrb.cooldown)
    self.color = glb.BLUE
    self.damage = 1
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
      return IceBolt(self.owner, self.position, self.bolt_direction, (0, 0),
                     (5, 5))
    return None

  def explode(self, projectile_list):
    for i in range(FrozenOrb.explode_bolts):
      direction = self.bolt_direction.rotate(36 * i)
      ice_bolt = IceBolt(self.owner, self.position, direction, (0, 0), (5, 5))
      projectile_list.append(ice_bolt)


class IceBolt(Projectile):
  speed = 10
  slow_effect = 0.5
  slow_duration = 1

  def __init__(self, owner, position, direction, acceleration, size):
    self.color = glb.LIGHT_BLUE
    self.damage = 2
    if not direction.is_normalized():
      direction = direction.normalize()
    super().__init__(owner, position, direction * IceBolt.speed, acceleration,
                     size, self.damage, self.color)

  def hit(self, other: Collidable):
    super().hit(other)
    if isinstance(other, Character):
      self.inflict_cold(other)
    self.dead = True

  def inflict_cold(self, other: Character):
    other.apply_cold(IceBolt.slow_duration, IceBolt.slow_effect)


def handle_cooldown(owner, casted_dict, cooldown):
  current_time = time.time()
  if (owner in casted_dict and current_time < casted_dict[owner] + cooldown):
    return False
  else:
    casted_dict[owner] = current_time
    return True
