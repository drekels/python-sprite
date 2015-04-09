#!/usr/bin/env python
""" PYGAME SAMPLE SPRITE

This script creates an instance of pygame with a single window.  Inside the
window, 2 sprites are rendered of a spearman walking in the left direction and
the front direction.

The image are loaded from the `samples/img` directory and their names are
inferred from the filenames.  The animation details are stored in the
`samples/animation_sample.yaml` file, with the names of the components
corresponding to the file names.

The game loop creates animation players to play each animation, and keeps
track of time passing so that it can update them.  The animation players
are given a callback that restarts the animations, so the animations run
continuously.

The `PygameSpriteRenderer` takes care of drawing the animation.  It
does so at 3x the size of the original images.
"""


import sys
import os
import datetime as dt
import pygame
import yaml
from pygame.locals import QUIT


DIRECTORY = os.path.dirname(__file__)
PARENT_DIRECTORY = os.path.dirname(DIRECTORY)


if (DIRECTORY.endswith("samples")):
    sys.path.append(PARENT_DIRECTORY)


from sprite.animation import SpriteAnimationPlayer, SpriteAnimation, ZERO_TIME
from sprite.component import SpriteComponent


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (100, 100, 100)


IMG_DIR = os.path.join(os.path.dirname(__file__), "img")
ANIMATION_META = os.path.join(os.path.dirname(__file__), "animation_sample.yaml")


class PygameSpriteComponent(SpriteComponent):

    @property
    def image(self):
        if not self._image:
            self._image = pygame.image.load(self.filepath)
            rect = self._image.get_rect()
            width, height = rect.width, rect.height
            self._image = pygame.transform.scale(self._image, (width*3, height*3))
        return self._image

    def calc_dimensions(self):
        rect = self.image.get_rect()
        self._width, self._height = rect.size


class PygameSpriteRenderer(pygame.sprite.Sprite):

    @classmethod
    def load_components(cls):
        cls.components = {}
        for filename in os.listdir(IMG_DIR):
            component_name = filename.split(".")[0]
            filepath = os.path.join(IMG_DIR, filename)
            cls.components[component_name] = PygameSpriteComponent(
                component_name, filepath=filepath
            )


    @classmethod
    def get_component(cls, component_name):
        if not hasattr(cls, "components"):
            cls.load_components()
        return cls.components[component_name]

    def __init__(self, starting_component=None, position=None, multiplier=1):
        super(PygameSpriteRenderer, self).__init__()
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

    def set_component(self, component_name, **params):
        self.component = self.get_component(component_name)
        self.image = self.component.image
        self.width, self.height = self.component.size
        self.displacement_x = params.get("displacement_x", 0) * self.multiplier
        self.displacement_y = params.get("displacement_y", 0) * self.multiplier
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
        self.load_animations()
        self.create_sprites()
        self.initialize_pygame()
        self.start_animations()
        self.start_timer()
        self.run_game_loop()

    def start_timer(self):
        self.last_time = dt.datetime.now()

    def check_time(self):
        now = dt.datetime.now()
        self.time_passed = now - self.last_time
        self.last_time = now

    def create_sprites(self):
        self.front_sprite = PygameSpriteRenderer(starting_component="front1")
        self.left_sprite = PygameSpriteRenderer(starting_component="left1")

    def load_animations(self):
        with open(ANIMATION_META) as f:
            data = yaml.load(f)
        self.animations = {}
        for animation_data in data["animations"]:
            animation = SpriteAnimation.load(animation_data)
            self.animations[animation.name] = animation

    def start_animations(self):
        self.start_left_animation()
        self.start_front_animation()

    def start_front_animation(self, extra_time=ZERO_TIME):
        animation = self.animations["front-walk"]
        self.front_player = SpriteAnimationPlayer(self.front_sprite, animation)
        self.front_player.add_end_callback(self.start_front_animation)
        self.front_player.start_animation()

    def start_left_animation(self, extra_time=ZERO_TIME):
        animation = self.animations["left-walk"]
        self.left_player = SpriteAnimationPlayer(self.left_sprite, animation)
        self.left_player.add_end_callback(self.start_left_animation)
        self.left_player.start_animation()

    def initialize_pygame(self):
        pygame.init()
        pygame.display.set_caption('Pygame Animation Sample')

        self.window = pygame.display.set_mode((500, 400), 0, 32)
        window_rect = self.window.get_rect()
        halfwidth = window_rect.width / 2
        left_rect = pygame.Rect(
            window_rect.x, window_rect.y, halfwidth, window_rect.height)
        right_rect = pygame.Rect(
            window_rect.x + halfwidth, window_rect.y, halfwidth, window_rect.height
        )

        self.left_sprite.set_position(left_rect.center)
        self.front_sprite.set_position(right_rect.center)

        self.group = pygame.sprite.Group()
        self.group.add(self.left_sprite)
        self.group.add(self.front_sprite)

    def pass_animation_time(self, time):
        self.left_player.pass_animation_time(time)
        self.front_player.pass_animation_time(time)

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
