import pygame
from pygame import Vector2 as vec

import globals as glb


class Collidable:
  """
  Base class for all collidable game objects. Handles position, velocity, and size,
  with automatic updates to bounding rectangle for collision detection.
  """

  def __init__(self, position, velocity, acceleration, size, color):
    self._position = vec(position)
    self._velocity = vec(velocity)
    self._acceleration = vec(acceleration)
    self._size = size
    self._rect = pygame.Rect(*position, *size)
    self._rect.center = (position[0], position[1])
    self._color = color

  # PROPERTIES AND SETTERS
  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, value: vec):
    self._position.update(value)
    self.rect.center = (value.x, value.y)

  @property
  def velocity(self):
    return self._velocity

  @velocity.setter
  def velocity(self, value):
    self._velocity = value

  @property
  def acceleration(self):
    return self._acceleration

  @acceleration.setter
  def acceleration(self, value):
    self._acceleration = vec(value)

    if self._acceleration.x == 0:
      self.velocity.x *= glb.FRICTION_COEFFICIENT

      # Make sure we eventually full stop
      if abs(self.velocity.x) < glb.FULLSTOP_THRESHOLD:
        self.velocity.x = 0

    if self._acceleration.y == 0:
      self.velocity.y *= glb.FRICTION_COEFFICIENT

      # Make sure we eventually full stop
      if abs(self._velocity.y) < glb.FULLSTOP_THRESHOLD:
        self.velocity.y = 0

  @property
  def size(self):
    return self._size

  @size.setter
  def size(self, value):
    self._size = value
    self._rect.size = value

  @property
  def rect(self) -> pygame.Rect:
    return self._rect
  
  @rect.setter
  def rect(self, value: pygame.Rect):
    self._rect = value

  def update(self):
    self.velocity += self.acceleration
    self.position += self.velocity

  def draw(self, surface):
    pygame.draw.circle(surface, self._color, self.position, self.size[0] // 2)

  def collides_with(self, other: 'Collidable') -> bool:
    return False # TODO: reassess need for this