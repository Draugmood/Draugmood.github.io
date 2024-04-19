import pygame
from pygame import Vector2 as vec

import globals as glb


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
    self._rect.center = (position.x, position.y)

  # PROPERTIES AND SETTERS
  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, value: vec):
    self._position.update(value)
    self._rect.center = (value.x, value.y)

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

    if self._acceleration.x == 0:
      self._velocity.x *= glb.FRICTION_COEFFICIENT

      # Make sure we eventually full stop
      if abs(self._velocity.x) < glb.PLAYER_FULLSTOP_THRESHOLD:
        self._velocity.x = 0

    if self._acceleration.y == 0:
      self._velocity.y *= glb.FRICTION_COEFFICIENT

      # Make sure we eventually full stop
      if abs(self._velocity.y) < glb.PLAYER_FULLSTOP_THRESHOLD:
        self._velocity.y = 0

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
    pygame.draw.circle(surface, glb.RED, self._position, self._size[0] // 2)
    pygame.draw.rect(surface, glb.WHITE, self._rect, width=1)

  def collides_with(self, other: 'Collidable') -> bool:
    if not isinstance(other, Collidable):
      return False
    return self.rect().colliderect(other.rect())
