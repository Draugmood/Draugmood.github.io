import math
import time

import pygame
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
  speed = 10

  def __init__(self, owner, position, target, acceleration, size):
    self.color = glb.WHITE
    self.shadow_color = pygame.Color(glb.SHADOW)
    self.damage = 20
    self.speed_decay = 0
    self.z = 0
    self.gravity = 3
    self.true_position = vec(position)
    direction = target - position
    range = direction.length()
    self.velocity = vec(direction).normalize() * self.speed
    self.flight_time = range / self.velocity.length()
    self.lifespan = self.flight_time/32
    
    self.vz = 0.5 * self.gravity * self.flight_time
    
    super().__init__(owner, position, self.velocity, acceleration, size,
                     self.damage, self.color)

  def update(self):
    self.vz -= self.gravity
    self.z += self.vz
    scaled_z = self.z * glb.ISOMETRIC_SCALING
    self.velocity += self.acceleration
    self.true_position += self.velocity
    self.position = self.true_position
    self.position.y -= scaled_z
    Projectile.update(self)

  def draw(self, surface):
    super().draw(surface)
    shadow_rect = pygame.Rect(
      self.true_position.x - self.size[0]/2,
      self.true_position.y - (self.size[1])*glb.ISOMETRIC_SCALING,
      self.size[0],
      self.size[1]*glb.ISOMETRIC_SCALING
    )

    if 0 <= (self.z / 3) < 256:
      self.shadow_color.a = int(255-(self.z / 3))

    glb.print_text(f"{self.flight_time}",
                   glb.WHITE,
                   glb.NORMAL_FONT,
                   glb.SCREEN,
                   (1600, 740),
                   align="topleft")
    
    glb.print_text(f"{self.lifespan}",
                   glb.WHITE,
                   glb.NORMAL_FONT,
                   glb.SCREEN,
                   (1600, 720),
                   align="topleft")

    shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
    # pygame.draw.circle(shadow_surface,
    #                    self.shadow_color,
    #                    shadow_surface.get_rect().center,
    #                    self.size[0]/2)
    
    pygame.draw.ellipse(shadow_surface,
                        self.shadow_color,
                        shadow_surface.get_rect())

    glb.SCREEN.blit(shadow_surface, shadow_rect)
    

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
