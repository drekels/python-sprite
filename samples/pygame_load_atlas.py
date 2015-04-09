#!/usr/bin/env python
""" PYGAME SAMPLE SPRITE

This script creates an instance of pygame with a single window.  Inside the
window, 2 sprites are rendered of a spearman from the front and the back.

The atlas that is loaded is the product of the 'make_atlas.py' sample script.

The `PygameSprite` takes care of drawing the sprite.  It does so at 3x the size
of the original images.
"""


import sys
import os
import datetime as dt
import pygame
import json
from pygame.locals import QUIT
from pygame import Rect


DIRECTORY = os.path.dirname(__file__)
PARENT_DIRECTORY = os.path.dirname(DIRECTORY)


if (DIRECTORY.endswith("samples")):
    sys.path.append(PARENT_DIRECTORY)


from sprite.component import SpriteComponent


GREY = (100, 100, 100)


ATLAS_IMAGE = 'sample_atlas.png'
ATLAS_META = 'sample_atlas.json'
IMG_DIR = os.path.join(os.path.dirname(__file__), "img")
ANIMATION_META = os.path.join(os.path.dirname(__file__), "animation_sample.yaml")


class PygameAtlasSprite(pygame.sprite.Sprite):

    def __init__(self, atlas, component_name, position=None, multiplier=1):
        super(PygameAtlasSprite, self).__init__()
        self.atlas = atlas
        self.multiplier = multiplier
        self.component = self.atlas.components[component_name]
        self.image = pygame.Surface(self.component.size)
        self.image.blit(atlas.image, (0, 0), Rect(*self.component.rect))
        self.image = pygame.transform.scale(self.image, [a * multiplier for a in self.component.size])
        self.multiplier = multiplier
        self.component = atlas.components[component_name]

    @property
    def position(self):
        return (self.position_x, self.position_y)

    @property
    def size(self):
        return self.width, self.height

    @property
    def displacement(self):
        return self.displacement_x, self.displacement_y


class PygameAtlas(object):

    def __init__(self, image, meta):
        self.image = pygame.image.load(image)
        self.components = {}
        with open(meta) as f:
            meta_dict = json.load(f)
        for component_meta in meta_dict:
            component = SpriteComponent.from_meta(component_meta)
            self.components[component.name] = component


class SampleGame(object):

    @classmethod
    def start(cls):
        game = cls()
        game.run()

    def run(self):
        self.load_atlas()
        self.create_sprites()
        self.initialize_pygame()
        self.run_game_loop()

    def start_timer(self):
        self.last_time = dt.datetime.now()

    def check_time(self):
        now = dt.datetime.now()
        self.time_passed = now - self.last_time
        self.last_time = now

    def create_sprites(self):
        self.front_sprite = PygameAtlasSprite(self.atlas, "front1", multiplier=3)
        self.left_sprite = PygameAtlasSprite(self.atlas, "left1", multiplier=3)

    def load_atlas(self):
        self.atlas = PygameAtlas("samples/sample_atlas.png", "samples/sample_atlas.json")


    def initialize_pygame(self):
        pygame.init()
        pygame.display.set_caption('Pygame Animation Sample')

        self.window = pygame.display.set_mode((500, 400), 0, 32)
        self.left_sprite.rect = pygame.Rect(20, 50, 0, 0)
        self.front_sprite.rect = pygame.Rect(270, 50, 0, 0)

        self.group = pygame.sprite.Group()
        self.group.add(self.left_sprite)
        self.group.add(self.front_sprite)

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
            self.draw()


if __name__ == "__main__":
    SampleGame.start()
