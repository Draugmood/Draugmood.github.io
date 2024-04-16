#!/user/bin/env python3
"""Game objects and game loop"""
import random
import sys
import timeit

import pygame as pg
from pygame import Vector2 as vec

import config as cf
from projectiles import FrozenOrb, IceBolt

def handle_events(movement):
  for event in pg.event.get():
    match event.type:
      case pg.QUIT:
        pg.quit()
        sys.exit()
      case pg.KEYDOWN:
        match event.key:
          case pg.K_ESCAPE:
            pg.quit()
            sys.exit()
          case pg.K_LEFT:
            movement['left'] = True
          case pg.K_RIGHT:
            movement['right'] = True
          case pg.K_UP:
            movement['up'] = True
          case pg.K_DOWN:
            movement['down'] = True
          
      case pg.KEYUP:
        match event.key:
          case pg.K_LEFT:
            movement['left'] = False
          case pg.K_RIGHT:
            movement['right'] = False
          case pg.K_UP:
            movement['up'] = False
          case pg.K_DOWN:
            movement['down'] = False


def move_character(movement, position, speed):
  if movement['left']:
    position[0] -= speed
  if movement['right']:
    position[0] += speed
  if movement['up']:
    position[1] -= speed
  if movement['down']:
    position[1] += speed


def main():

  background = pg.Surface(cf.SCREEN.get_size()).convert()
  background.fill(cf.BLACK)

  character_position = [100, 100]
  character_speed = 10

  frozen_orb = FrozenOrb((200, 100), (0, 0), 20, 10)
  ice_bolt = IceBolt((100, 200), (0, 0), 5, 2)

  move_state = {
    'left': False,
    'right': False,
    'up': False,
    'down': False
  }
  
  running = True

  while running:
    cf.CLOCK.tick(30)
    handle_events(move_state)

    move_character(move_state, character_position, character_speed)

    cf.SCREEN.blit(background, (0, 0))
    pg.draw.circle(cf.SCREEN, cf.RED, character_position, 20)
    frozen_orb.draw(cf.SCREEN)
    ice_bolt.draw(cf.SCREEN)

    pg.display.flip()

if __name__ == "__main__":
  main()
