import time

import pygame
from pygame import Vector2 as vec

import globals as glb
from collidables import Collidable


class Character(Collidable):
  def __init__(self, position, velocity,
               acceleration, size, color, health):
    super().__init__(position, velocity, acceleration, size, color)
    self.max_health = health
    self._health = health
    self.dead = False
    self._cold_coefficient = 0
    self.cold_expires = 0

  @property
  def health(self):
    return self._health

  @health.setter
  def health(self, value):
    self._health = value
    if self._health <= 0:
      self.dead = True

  def update(self):
    glb.print_text("Character update", glb.WHITE, glb.NORMAL_FONT,
       glb.SCREEN, (glb.SCREEN_RECT.width - 10, 10 + 590), "topright")
    super().update()
    if time.time() > self.cold_expires:
      self._cold_coefficient = 0
      # COLD STILL DONT WORK BRO
      # SEE RECENT ANSWER FROM GPT

  @property
  def is_cold(self):
    return self._cold_coefficient != 0

  def apply_cold(self, duration, slow_coefficient):
    current_time = time.time()
    if current_time > self.cold_expires or slow_coefficient > self._cold_coefficient:
      self._cold_coefficient = slow_coefficient
    self.cold_expires = max(self.cold_expires, current_time + duration)

  def move(self):
    glb.print_text("Character move", glb.WHITE, glb.NORMAL_FONT,
       glb.SCREEN, (glb.SCREEN_RECT.width - 10, 10 + 560), "topright")
    self.velocity += self.acceleration
    self.position -= self.velocity * (1 - self._cold_coefficient)

  def draw(self, surface):
    color = glb.MAROON if self.is_cold else self._color
    pygame.draw.circle(surface, color, self.position,
                       self.size[0] // 2, width=1)
    pygame.draw.circle(surface, color, self.position,
                       (self.size[0] // 2)*(self.health/self.max_health))
    glb.print_text(f"{self.health}", glb.WHITE, glb.NORMAL_FONT,
                   surface, self.rect.center, "center")


class Player(Character):
  max_speed = 12
  accel_magnitude = 3
  max_health = 100

  def __init__(self, position, velocity, acceleration, size):
    super().__init__(position, velocity, acceleration,
                     size, glb.GREEN, Player.max_health)
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
      acceleration_val = acceleration_val.normalize() * Player.accel_magnitude

    self.acceleration = acceleration_val

    # HANDLE VELOCITY NOT SKYROCKETING / VELOCITY CEILING
    self.velocity += self.acceleration
    if self.velocity.length() > Player.max_speed:
      self.velocity.scale_to_length(Player.max_speed)
    self.position += self.velocity

  def draw(self, surface):
    super().draw(surface)
    pygame.draw.rect(surface, glb.WHITE, self.rect, width=1)


class Enemy(Character):
  speed = 5
  max_health = 20

  def __init__(self, position, velocity,
               acceleration, size, player, moving=True):
    super().__init__(position, velocity, acceleration,
                     size, glb.RED, Enemy.max_health)
    self.pathfinding = 0
    self.player = player
    self.moving = moving


  def update(self):
    if self.moving:
      direction_to_player = (self.player.position - self.position)
      if direction_to_player.length() > 0:
        direction_to_player = direction_to_player.normalize()
      self.velocity = direction_to_player * Enemy.speed #scaletolength?
      self.position += self.velocity


class Ally(Character):
  pass
