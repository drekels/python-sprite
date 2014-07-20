import unittest2
from sprite.component import SpriteComponent
from sprite.animation import SpriteAnimation, SpriteAnimationStage
import logging
import os
from test.sprite import (
    FRONT1, FRONT2, FRONT3, EXPECTED_FRONT_SIZE
)


LOG = logging.getLogger(__name__)



def initialize_components(testcase):
    for name, filepath in [("front1", FRONT1), ("front2", FRONT2), ("front3", FRONT3)]:
        component = SpriteComponent(name, filepath=filepath)
        setattr(testcase, name, component)


class TestSpriteAnimationStage(unittest2.TestCase):

    def setUp(self):
        initialize_components(self)
        self.stage1 = SpriteAnimationStage(component=self.front1, duration=0.2)
        self.stage2 = SpriteAnimationStage(component=self.front2, duration=0.4)
        self.stage3 = SpriteAnimationStage(component=self.front3, duration=0.4, displacement_x=1,
            displacement_y=-2
        )

    def test_init(self):
        self.assertEqual(0.2, self.stage1.duration)
        self.assertEqual(self.front1, self.stage1.component)
        self.assertEqual(0, self.stage1.displacement_x)
        self.assertEqual(0, self.stage1.displacement_y)




class TestSpriteAnimation(unittest2.TestCase):

    def setUp(self):
        initialize_components(self)
        self.stages1 = [
            SpriteAnimationStage(component=self.front1, duration=0.2),
            SpriteAnimationStage(component=self.front2, duration=0.4),
            SpriteAnimationStage(component=self.front1, duration=0.2),
            SpriteAnimationStage(component=self.front3, duration=0.4),
        ]
        self.stages2 = [
            SpriteAnimationStage(
                component=self.front1, duration=0.2, displacement_x=10, displacement_y=1
            ),
            SpriteAnimationStage(
                component=self.front2, duration=0.4, displacement_x=-5, displacement_y=5
            ),
            SpriteAnimationStage(component=self.front1, duration=0.2, displacement_y=3),
            SpriteAnimationStage(component=self.front3, duration=0.4, displacement_y=1),
        ]
        self.animation1 = SpriteAnimation("TestAnimation1", self.stages1)
        self.animation2 = SpriteAnimation("TestAnimation2", self.stages2)
        self.animation3 = SpriteAnimation("TestAnimation3")

    def test_init(self):
        self.assertEqual("TestAnimation1", self.animation1.name)
        self.assertEqual(self.stages1, self.animation1.stages)
        self.assertEqual([], self.animation3.stages)

    def test_min_x(self):
        expected_width, _ = EXPECTED_FRONT_SIZE
        expected_min = -expected_width / 2.0
        self.assertEqual(expected_min, self.animation1.min_x)

    def test_max_x(self):
        expected_width, _ = EXPECTED_FRONT_SIZE
        expected_max = expected_width / 2.0
        self.assertEqual(expected_max, self.animation1.max_x)

    def test_min_y(self):
        _, expected_height = EXPECTED_FRONT_SIZE
        expected_min = -expected_height / 2.0
        self.assertEqual(expected_min, self.animation1.min_y)

    def test_max_y(self):
        _, expected_height = EXPECTED_FRONT_SIZE
        expected_max = expected_height / 2.0
        self.assertEqual(expected_max, self.animation1.max_y)

    def test_width(self):
        expected_width, _ = EXPECTED_FRONT_SIZE
        self.assertEqual(expected_width, self.animation1.width)

    def tets_height(self):
        _, expected_height = EXPECTED_FRONT_SIZE
        self.assertEqual(expected_height, self.animation1.height)

    def test_width_with_displacement(self):
        LOG.debug(self.animation2.min_x)
        expected_width, _ = EXPECTED_FRONT_SIZE
        expected_width += 15
        self.assertEqual(expected_width, self.animation2.width)

    def test_height_with_displacement(self):
        _, expected_height = EXPECTED_FRONT_SIZE
        expected_height += 4
        self.assertEqual(expected_height, self.animation2.height)

    def test_offset_trivial(self):
        self.assertEqual((0, 0), self.animation1.offset)

    def test_offset_complex(self):
        self.assertEqual(-2.5, self.animation2.offset_x)
        self.assertEqual(-3, self.animation2.offset_y)
