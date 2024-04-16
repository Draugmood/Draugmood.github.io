#!/user/bin/env python3
"""Game objects and game loop"""
import sys

import pygame

import config as cf
from characters import Ally, Enemy, Player
from projectiles import FrozenOrb, IceBolt


def print_debug(player):
  print("Movement:", player.movement)
  print("Acceleration:", player.acceleration)
  print("Velocity:", player.velocity)
  print("Position:", player.position)

def handle_events(player, collidables):
  for event in pygame.event.get():
    match event.type:
    
      case pygame.QUIT:
        pygame.quit()
        sys.exit()
        
      case pygame.KEYDOWN:
        match event.key:
          case pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
          case pygame.K_LEFT:
            player.movement['left'] = True
          case pygame.K_RIGHT:
            player.movement['right'] = True
          case pygame.K_UP:
            player.movement['up'] = True
          case pygame.K_DOWN:
            player.movement['down'] = True
          
      case pygame.KEYUP:
        match event.key:
          case pygame.K_LEFT:
            player.movement['left'] = False
          case pygame.K_RIGHT:
            player.movement['right'] = False
          case pygame.K_UP:
            player.movement['up'] = False
          case pygame.K_DOWN:
            player.movement['down'] = False

      case pygame.MOUSEBUTTONDOWN:
        match event.button:
          case 1:
            ice_bolt = IceBolt((100, 200), (1, 3), (0, 0), (5, 5), 2)
            collidables.append(ice_bolt)
          case 3:
            frozen_orb = FrozenOrb((200, 100), (5, 0), (0, 0), (20, 20), 10)
            collidables.append(frozen_orb)




def main():

  background = pygame.Surface(cf.SCREEN.get_size()).convert()
  background.fill(cf.BLACK)

  player = Player((100, 100), (0, 0), (0, 0), (50, 50))

  collidables = [player]
  
  running = True

  while running:
    cf.CLOCK.tick(30)
    handle_events(player, collidables)


    cf.SCREEN.blit(background, (0, 0))

    for collidable in collidables:
      collidable.draw(cf.SCREEN)
      collidable.update()

    pygame.display.flip()

if __name__ == "__main__":
  main()
