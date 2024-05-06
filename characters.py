import pygame
from pygame import Vector2 as vec

import globals as glb
from collidables import Collidable


class Character(Collidable):
  def __init__(self, position, velocity,
               acceleration, size, color, health):
    super().__init__(position, velocity, acceleration, size, color)
    self.max_health = health
    self.health = health
    self.dead = False

  @property
  def health(self):
    return self._health

  @health.setter
  def health(self, value):
    self._health = value
    if self._health <= 0:
      self.dead = True

  def draw(self, surface):
    pygame.draw.circle(surface, self._color, self.position,
                       self.size[0] // 2, width=1)
    pygame.draw.circle(surface, self._color, self.position,
                       (self.size[0] // 2)*(self.health/self.max_health))


class Player(Character):

  def __init__(self, position, velocity, acceleration, size):
    super().__init__(position, velocity, acceleration, size, glb.GREEN, glb.PLAYER_HEALTH)
    self.movement = {'left': False, 'right': False, 'up': False, 'down': False}

  def update(self):
    acceleration_val = vec(0, 0)
    if self.movement['left']:
      acceleration_val.x -= 1
    if self.movement['right']:
      acceleration_val.x += 1
    if self.movement['up']:
      acceleration_val.y -= 1
    if self.movement['down']:
      acceleration_val.y += 1

    if acceleration_val.length() > 0:
      acceleration_val = acceleration_val.normalize() * glb.PLAYER_ACCELERATION

    self.acceleration = acceleration_val

    # HANDLE VELOCITY NOT SKYROCKETING / VELOCITY CEILING
    self.velocity += self.acceleration
    if self.velocity.length() > glb.MAX_PLAYER_SPEED:
      self.velocity.scale_to_length(glb.MAX_PLAYER_SPEED)
    self.position += self.velocity

  def draw(self, surface):
    super().draw(surface)
    pygame.draw.rect(surface, glb.WHITE, self.rect, width=1)


class Enemy(Character):

  def __init__(self, position, velocity,
               acceleration, size, player, moving=True):
    super().__init__(position, velocity, acceleration, size, glb.RED, 20)
    self.pathfinding = 0
    self.player = player
    self.moving = moving


  def update(self):
    if self.moving:
      direction_to_player = (self.player.position - self.position)
      if direction_to_player.length() > 0:
        direction_to_player = direction_to_player.normalize()
      self.velocity = direction_to_player * glb.ENEMY_SPEED #scaletolength?
      self.position += self.velocity


class Ally(Character):
  pass
