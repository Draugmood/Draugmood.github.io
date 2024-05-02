"""Placeholder code rememberance boi for code that 'throws' a grenade in 2d top-down
space (or something like that). See https://youtu.be/rgAsqP6xdWk?t=667.
"""
class Grenade(Debris):
  def __init__(self, pos, target):
  super().__init__('grenade', pos)

  self.angle = math.atan2(target[1] - self.pos[1], target[0] - self.pos[0])
  self.speed = 120
  self.speed_decay = 0
  self.gravity = 450

  dis = pp.utils.game_math.distance(pos, target)
  travel_time = dis / self.speed

  self.v_speed = travel_time * self.gravity / 2