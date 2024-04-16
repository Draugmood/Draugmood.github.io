import pygame
from pygame import Vector2 as vec

import config as cf


class Collidable:
  """
  Base class for all collidable game objects. Handles position, velocity, and size,
  with automatic updates to bounding rectangle for collision detection.
  """

  def __init__(self, position, velocity, acceleration, size):
    self._position = vec(position)
    self._velocity = vec(velocity)
    self._acceleration = vec(acceleration)
    self._size = size
    self._rect = pygame.Rect(*position, *size)

  # PROPERTIES AND SETTERS
  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, value):
    self._position.update(value)
    self._rect.topleft = value

  @property
  def velocity(self):
    return self._velocity

  @velocity.setter
  def velocity(self, value):
    self._velocity = value
    #nothing more here?

  @property
  def acceleration(self):
    return self._acceleration

  @acceleration.setter
  def acceleration(self, value):
    self._acceleration = vec(value)

  @property
  def size(self):
    return self._size

  @size.setter
  def size(self, value):
    self._size = value
    self._rect.size = value

  # METHODS
  def rect(self) -> pygame.Rect:
    return self._rect

  def update(self):
    self._velocity += self._acceleration
    self._position += self._velocity

  def draw(self, surface):
    pygame.draw.circle(surface, cf.RED, self._position, self._size[0] // 2)

  def collides_with(self, other: 'Collidable') -> bool:
    if not isinstance(other, Collidable):
      return False
    return self.rect().colliderect(other.rect())
