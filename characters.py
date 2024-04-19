from pygame import Vector2 as vec

import globals as glb
from collidables import Collidable


class Character(Collidable):
  pass


class Player(Character):

  def __init__(self, position, velocity, acceleration, size):
    super().__init__(position, velocity, acceleration, size)
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
    self._velocity += self._acceleration
    if self._velocity.length() > glb.MAX_PLAYER_SPEED:
      self._velocity.scale_to_length(glb.MAX_PLAYER_SPEED)
    self._position += self._velocity


class Enemy(Character):
  pass


class Ally(Character):
  pass
