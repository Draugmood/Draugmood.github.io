from pygame import Vector2 as vec

from collidables import Collidable

import globals as glb


class Character(Collidable):
  pass


class Player(Character):

  def __init__(self, position, velocity, acceleration, size):
    super().__init__(position, velocity, acceleration, size)
    self.movement = {'left': False, 'right': False, 'up': False, 'down': False}

  def update(self):
    acceleration_val = vec(0, 0)
    if self.movement['left']:
      acceleration_val.x -= glb.PLAYER_ACCELERATION
    if self.movement['right']:
      acceleration_val.x += glb.PLAYER_ACCELERATION
    if self.movement['up']:
      acceleration_val.y -= glb.PLAYER_ACCELERATION
    if self.movement['down']:
      acceleration_val.y += glb.PLAYER_ACCELERATION

    if acceleration_val.length() > 0:
      acceleration_val.normalize()

    self.acceleration = acceleration_val

    # HANDLE VELOCITY NOT SKYROCKETING / VELOCITY CEILING
    if self._velocity.length() <= glb.MAX_PLAYER_SPEED:
      self._velocity += self._acceleration
    self._position += self._velocity


class Enemy(Character):
  pass


class Ally(Character):
  pass
