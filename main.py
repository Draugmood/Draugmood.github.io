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
from projectiles import FrozenOrb, IceBolt, Grenade


def aim(position):
  mouse_pos = vec(pygame.mouse.get_pos())
  return (mouse_pos - position).normalize()


def handle_collisions(player, all_collidables, projectiles):
  for projectile in projectiles:
    for collidable in all_collidables:
      if collidable == projectile.owner:
        continue
      if projectile.rect.colliderect(collidable.rect):
        projectile.hit(collidable)

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
          case pygame.K_SPACE:
            grenade = Grenade(player, player.position,
                              vec(pygame.mouse.get_pos()),
                              (0, 0), (10, 10))
            projectile_list.append(grenade)

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
            ice_bolt = IceBolt(player, player.position, aim(player.position),
                               (0, 0), (5, 5))
            projectile_list.append(ice_bolt)


          case 3:
            frozen_orb = FrozenOrb(player, player.position,
                                   aim(player.position), (0, 0), (20, 20))
            if frozen_orb.viable:
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
  background.fill(glb.DARKSLATEGREY)

  screen_center = vec(glb.SCREEN.get_size()) / 2

  player = Player(screen_center, (0, 0), (0, 0), (50, 50))
  enemy1 = Enemy((200, 200), (0, 0), (0, 0), (50, 50), player, moving=False)
  enemy2 = Enemy((200, 400), (0, 0), (0, 0), (50, 50), player, moving=False)
  enemy3 = Enemy((200, 600), (0, 0), (0, 0), (50, 50), player, moving=False)

  collidables = [player, enemy1, enemy2, enemy3]
  projectiles = []

  num_kills = 0

  running = True

  while running:
    glb.CLOCK.tick(30)

    handle_events(player, projectiles)

    glb.SCREEN.blit(background, (0, 0))
    pygame.draw.circle(glb.SCREEN,
                       glb.GREEN,
                       player.position,
                       glb.ENEMY_SPAWN_RANGE,
                       width=1)
    # just drew this circle, enemies are spawning around player at this rad

    for projectile in projectiles:
      projectile.update()
      projectile.draw(glb.SCREEN)
      if hasattr(projectile, 'bolt_direction'):
        ice_bolt = projectile.spawn_bolts()
        if ice_bolt is not None:
          projectiles.append(ice_bolt)
        if projectile.dead:
          projectile.explode(projectiles)

    for collidable in collidables:
      collidable.update()
      collidable.draw(glb.SCREEN)

    glb.print_text(f"{pygame.mouse.get_pos()[0]}",
                   glb.WHITE,
                   glb.NORMAL_FONT,
                   glb.SCREEN,
                   (1600, 700),
                   align="topleft")

    """pygame.draw.circle(glb.SCREEN,
                       col1,
                       (player.position.x-100, player.position.y),
                       100)

    pygame.draw.circle(glb.SCREEN,
                      col2,
                      (player.position.x+100, player.position.y),
                      100)"""

    handle_collisions(player, collidables, projectiles)

    collidables = [
        collidable for collidable in collidables
        if not (hasattr(collidable, 'dead') and collidable.dead)
    ]

    projectiles = [
        projectile for projectile in projectiles if not projectile.dead
    ]

    if len(collidables) < 4:
      num_kills += 1
      new_enemy_pos = get_enemy_position_around_player(player.position,
                                                       glb.ENEMY_SPAWN_RANGE)
      enemy = Enemy(new_enemy_pos, (0, 0), (0, 0), (50, 50), player)
      collidables.append(enemy)

    texts = [
        f"Position: {player.position}", f"Acceleration: {player.acceleration}",
        f"Velocity: {player.velocity}",
        f"X Movement: {'Left' if player.movement['left'] else 'Right' if player.movement['right'] else 'None'}",
        f"Y Movement: {'Up' if player.movement['up'] else 'Down' if player.movement['down'] else 'None'}",
        f"Rect: {player.rect}", f"Projectiles: {len(projectiles)}"
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
