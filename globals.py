#!/user/bin/env python3
"""Config file for Mayhem clone"""
import os

import pygame as pg
from pygame import Vector2 as vec

pg.init()  # Initialize pygame

BLUE = pg.Color(0, 0, 104)
LIGHT_BLUE = pg.Color(135, 185, 250)
MAROON = pg.Color(136, 0, 21)
RED = pg.Color(255, 0, 0)
BLACK = pg.Color(0, 0, 0)
WHITE = pg.Color(255, 255, 255)


# Text rendering
def print_text(text, color, text_font, surface, pos, align="center"):
  rendered_text = text_font.render(text, True, color)
  text_rect = text.get_rect(center=pos)
  if align == "center":
    text_rect.center = pos
  elif align == "topright":
    text_rect.topright = pos
  surface.blit(text_rect, rendered_text)


NORMAL_FONT = pg.font.Font(None, 30)
TITLE_FONT = pg.font.Font(None, 300)
SUBTITLE_FONT = pg.font.Font(None, 100)
MENU_TITLE_FONT = pg.font.Font(None, 200)
MENU_BUTTON_FONT = pg.font.Font(None, 50)

# Stuff
CLOCK = pg.time.Clock()
INFO_OBJ = pg.display.Info()
SCREEN_RECT = pg.Rect(0, 0, INFO_OBJ.current_w, INFO_OBJ.current_h)
SCREEN = pg.display.set_mode((0, 0), pg.FULLSCREEN)
FRICTION_COEFFICIENT = 0.8  #lower number = more friction

# Player
MAX_PLAYER_SPEED = 12
PLAYER_FULLSTOP_THRESHOLD = 0.1
PLAYER_ACCELERATION = 3


def load_image(name):
  """Function for loading images from the 'resources' folder"""
  fullname = os.path.join("resources", name)
  try:
    image = pg.image.load(fullname)
  except pg.error as message:
    print("Cannot load image:", name)
    raise SystemExit(message)
  image = image.convert_alpha()

  return image


# Camera control
def center_camera(camera, target_rect):
  """
    Camera function used for moving the camera object from
    its current state (position) towards its target's position.
    """
  x = -target_rect.center[0] + SCREEN_RECT.width // 4
  y = -target_rect.center[1] + SCREEN_RECT.height // 2

  camera.topleft += ((pg.Vector2(
      (x, y)) - pg.Vector2(camera.left, camera.top)) * 0.2
                     )  # <- fancy camera tracking latency

  camera.x = max(-(camera.width - SCREEN_RECT.width // 2), min(0, camera.x))
  camera.y = max(-(camera.height - SCREEN_RECT.height), min(0, camera.y))

  return camera


class Camera():
  """
    Camera object that adds a positional offset to the game objects,
    creating the illusion of a moving screen as if by a top-down camera.
    The added offset is the position of the camera on the canvas.
    The camera's position is updated with the update method, taking
    in a target for the camera to follow; the player ships in this case.
    """

  def __init__(self, camera_func, width, height):
    self.camera_func = camera_func
    self.state = pg.Rect(0, 0, width, height)

  def apply(self, target):
    """Moves the target by an offset equal to the camera's position"""
    return target.rect.move(self.state.topleft)

  def update(self, target):
    """Updates the camera's position toward that of the target, using a camera function"""
    self.state = self.camera_func(self.state, target.rect)
