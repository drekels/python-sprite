#!/usr/bin/env python


ERRORTEXT = (
    "Sorry, this script can only be run if pygame is installed. Please run using a python "
    "instance with pygame installed, or download pygame from "
    "'http://www.pygame.org/download.shtml' and try again."
)


import sys
import os
import datetime as dt
from contextlib import contextmanager


try:
    import pygame
    from pygame.locals import QUIT
except ImportError:
    print ERRORTEXT
    sys.exit()


DIRECTORY = os.path.dirname(__file__)
PARENT_DIRECTORY = os.path.dirname(DIRECTORY)


if (DIRECTORY.endswith("samples")):
    sys.path.append(PARENT_DIRECTORY)


from sprite.animation import (
    SpriteAnimationStage, SpriteAnimationPlayer, SpriteAnimation, ZERO_TIME
)
from sprite.component import SpriteComponent


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (100, 100, 100)



IMG_DIR = os.path.join(os.path.dirname(__file__), "img")
FRONT1 = os.path.join(IMG_DIR, "front1.png")
FRONT2 = os.path.join(IMG_DIR, "front2.png")
FRONT3 = os.path.join(IMG_DIR, "front3.png")

class PygameSpriteComponent(SpriteComponent):

    @property
    def image(self):
        if not hasattr(self, "_image"):
            self._image = pygame.image.load(self.filepath)
            rect = self._image.get_rect()
            width, height = rect.width, rect.height
            self._image = pygame.transform.scale(self._image, (width*3, height*3))
        return self._image

    def calc_dimensions(self):
        rect = self.image.get_rect()
        self._width, self._height = rect.size


class PygameSpriteRenderer(pygame.sprite.Sprite):

    def __init__(self, components, starting_component=None, position=None, multiplier=1):
        super(PygameSpriteRenderer, self).__init__()
        self.components = dict([(component.name, component) for component in components])
        self.position_x, self.position_y = position or (0, 0)
        self.displacement_x, self.displacement_y = (0, 0)
        self.multiplier = multiplier
        self.component = None
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        if starting_component:
            self.set_component(starting_component)

    @property
    def position(self):
        return (self.position_x, self.position_y)

    @property
    def size(self):
        return self.width, self.height

    @property
    def displacement(self):
        return self.displacement_x, self.displacement_y

    @property
    def top_left_x(self):
        return self.position_x - self.width / 2 + self.displacement_x

    @property
    def top_left_y(self):
        return self.position_y - self.height / 2 + self.displacement_y

    @property
    def top_left(self):
        return self.top_left_x, self.top_left_y

    def set_component(self, component, **params):
        self.component = self.components.get(component, False) or component
        self.image = self.component.image
        self.width, self.height = self.component.size
        self.displacement_x, self.displacement_y = params.get("displacement", (0, 0))
        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.top_left, self.size)

    def set_position(self, x, y=None):
        if y is None:
            x, y = x
        self.position_x, self.position_y = x, y
        self.update_rect()


class SampleGame(object):

    @classmethod
    def start(cls):
        game = cls()
        game.run()

    def run(self):
        self.create_sprite()
        self.initialize_pygame()
        self.start_animation()
        self.start_timer()
        self.run_game_loop()

    def start_timer(self):
        self.last_time = dt.datetime.now()

    def check_time(self):
        now = dt.datetime.now()
        self.time_passed = now - self.last_time
        self.last_time = now

    def create_sprite(self):
        components = []
        for name, filepath in [("front1", FRONT1), ("front2", FRONT2), ("front3", FRONT3)]:
            components.append(PygameSpriteComponent(name, filepath=filepath))
        self.sprite = PygameSpriteRenderer(components, starting_component="front1")
        stages = [
            SpriteAnimationStage(components[0], 0.2, displacement_y=-3),
            SpriteAnimationStage(components[1], 0.4),
            SpriteAnimationStage(components[0], 0.2, displacement_y=-3),
            SpriteAnimationStage(components[2], 0.4),
        ]
        self.animation = SpriteAnimation("walk_front", stages)

    def start_animation(self, extra_time=ZERO_TIME):
        self.player = SpriteAnimationPlayer(self.sprite, self.animation)
        self.player.add_end_callback(self.start_animation)
        self.player.start_animation()

    def initialize_pygame(self):
        pygame.init()
        pygame.display.set_caption('Pygame Animation Sample')

        self.window = pygame.display.set_mode((500, 400), 0, 32)

        center = self.window.get_rect().center
        self.sprite.set_position(center)

        self.group = pygame.sprite.Group()
        self.group.add(self.sprite)

    def pass_animation_time(self, time):
        self.player.pass_animation_time(time)

    def draw(self):
        self.window.fill(GREY)
        self.group.draw(self.window)
        pygame.display.update()

    def run_game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.check_time()
            self.pass_animation_time(self.time_passed)
            self.draw()


if __name__ == "__main__":
    SampleGame.start()
