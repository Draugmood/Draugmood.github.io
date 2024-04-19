#!/user/bin/env python3
"""Game objects and game loop"""
import asyncio
import sys

import pygame
from pygame import Vector2 as vec

import globals as glb
from characters import Ally, Enemy, Player
from projectiles import FrozenOrb, IceBolt


def aim(position):
  mouse_pos = vec(pygame.mouse.get_pos())
  return (mouse_pos - position).normalize()
  

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
          case pygame.K_a:
            player.movement['left'] = True
          case pygame.K_d:
            player.movement['right'] = True
          case pygame.K_w:
            player.movement['up'] = True
          case pygame.K_s:
            player.movement['down'] = True
          
      case pygame.KEYUP:
        match event.key:
          case pygame.K_a:
            player.movement['left'] = False
          case pygame.K_d:
            player.movement['right'] = False
          case pygame.K_w:
            player.movement['up'] = False
          case pygame.K_s:
            player.movement['down'] = False

      case pygame.MOUSEBUTTONDOWN:
        match event.button:
          case 1:
            ice_bolt = IceBolt(player.position,
                               aim(player.position)*glb.PROJECTILE_SPEED,
                               (0, 0),
                               (5, 5),
                               2)
            collidables.append(ice_bolt)
            
          case 3:
            frozen_orb = FrozenOrb(player.position,
                                   aim(player.position)*glb.PROJECTILE_SPEED,
                                   (0, 0),
                                   (20, 20),
                                   10)

            collidables.append(frozen_orb)



async def main():

  background = pygame.Surface(glb.SCREEN.get_size()).convert()
  background.fill(glb.BLACK)

  player = Player((100, 100), (0, 0), (0, 0), (50, 50))

  collidables = [player]
  
  running = True

  while running:
    glb.CLOCK.tick(30)

    handle_events(player, collidables)


    glb.SCREEN.blit(background, (0, 0))

    for collidable in collidables:
      collidable.draw(glb.SCREEN)
      collidable.update()

    texts = [
        f"Position: {player.position}",
        f"Acceleration: {player.acceleration}",
        f"Velocity: {player.velocity}",
        f"X Movement: {'Left' if player.movement['left'] else 'Right' if player.movement['right'] else 'None'}",
        f"Y Movement: {'Up' if player.movement['up'] else 'Down' if player.movement['down'] else 'None'}",
        f"Rect: {player.rect}"
    ]

    for i, text in enumerate(texts):
      glb.print_text(text, glb.WHITE, glb.NORMAL_FONT, glb.SCREEN,
                 (glb.SCREEN_RECT.width - 10, 10 + i * 30), "topright")

    pygame.display.flip()
    await asyncio.sleep(0)

if __name__ == "__main__":
  asyncio.run(main())
