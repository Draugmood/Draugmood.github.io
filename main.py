#!/user/bin/env python3
"""Game objects and game loop"""
import asyncio
import sys
import random
import math

import pygame
from pygame import Vector2 as vec

import globals as glb

from characters import Ally, Enemy, Player
from projectiles import FrozenOrb, IceBolt


def aim(position):
  mouse_pos = vec(pygame.mouse.get_pos())
  return (mouse_pos - position).normalize()


def handle_collisions(player, all_collidables, projectiles):
  for projectile in projectiles:
    for collidable in all_collidables:
      if collidable == projectile.owner:
        continue
      if projectile.rect.colliderect(collidable.rect):
        collidable.health -= projectile.damage

  for enemy in all_collidables:
    if player == enemy:
      continue
    if player.rect.colliderect(enemy.rect):
      player.health -= 2


def handle_events(player, projectile_list):

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
            ice_bolt = IceBolt(player,
                               player.position,
                               aim(player.position)*glb.PROJECTILE_SPEED,
                               (0, 0),
                               (5, 5))
            projectile_list.append(ice_bolt)
            
          case 3:
            frozen_orb = FrozenOrb(player,
                                   player.position,
                                   aim(player.position)*glb.PROJECTILE_SPEED,
                                   (0, 0),
                                   (20, 20))
            if frozen_orb is not None:
              projectile_list.append(frozen_orb)

def get_enemy_position_around_player(player_position, distance):
  # Generate a random angle in radians
  angle = random.uniform(0, 2 * math.pi)

  # Calculate the offset from the player based on the angle and distance
  dx = math.cos(angle) * distance
  dy = math.sin(angle) * distance

  # Calculate the new enemy position
  enemy_position = player_position + pygame.Vector2(dx, dy)

  return enemy_position

async def main():

  background = pygame.Surface(glb.SCREEN.get_size()).convert()
  background.fill(glb.BLACK)

  screen_center = vec(glb.SCREEN.get_size()) / 2

  player = Player(screen_center, (0, 0), (0, 0), (50, 50))
  enemy = Enemy((200, 200), (0, 0), (0, 0), (50, 50), player)

  collidables = [player, enemy]
  projectiles = []

  num_kills = 0
  
  running = True

  while running:
    glb.CLOCK.tick(30)

    handle_events(player, projectiles)

    glb.SCREEN.blit(background,(0, 0))
    pygame.draw.circle(glb.SCREEN, glb.GREEN,
                       player.position, glb.ENEMY_SPAWN_RANGE, width=1)
    # just drew this circle, enemies are spawning around player at this rad

    for projectile in projectiles:
      projectile.update()
      projectile.draw(glb.SCREEN)

    for collidable in collidables:
      collidable.update()
      collidable.draw(glb.SCREEN)

    handle_collisions(player, collidables, projectiles)


    collidables = [collidable for collidable in collidables 
                   if not (hasattr(collidable, 'dead') and collidable.dead)]

    if len(collidables) < 2:
      num_kills += 1
      new_enemy_pos = get_enemy_position_around_player(player.position,
                                                       glb.ENEMY_SPAWN_RANGE)
      enemy = Enemy(new_enemy_pos, (0, 0), (0, 0), (50, 50), player)
      collidables.append(enemy)

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
      
    glb.print_text(f"Kills: {num_kills}", glb.WHITE, glb.NORMAL_FONT,
                   glb.SCREEN, (10, 10), "topleft")

    pygame.display.flip()
    await asyncio.sleep(0)

if __name__ == "__main__":
  asyncio.run(main())
