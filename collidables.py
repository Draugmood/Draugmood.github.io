import pygame


class Collidable:
  """
  Base class for all collidable game objects. Handles position, velocity, and size,
  with automatic updates to bounding rectangle for collision detection.
  """
  def __init__(self, position, velocity, size):
    self._position = position
    self._velocity = velocity
    self._size = size
    self._rect = pygame.Rect(*position, size, size)

  # PROPERTIES AND SETTERS
  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, value):
    self._position = value
    self._rect.topleft = value

  @property
  def velocity(self):
    return self._velocity

  @velocity.setter
  def velocity(self, value):
    self._velocity = value
    #nothing more here?

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

  def collides_with(self, other: 'Collidable') -> bool:
    if not isinstance(other, Collidable):
      return False
    return self.rect().colliderect(other.rect())


class Character(Collidable):
  pass


class Player(Character):
  pass


class Enemy(Character):
  pass


class Ally(Character):
  pass
