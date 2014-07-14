import unittest2
from sprite.component import SpriteComponent
import logging
import os


LOG = logging.getLogger(__name__)


IMG_DIR = os.path.join(os.path.dirname(__file__), "img")
FRONT1 = os.path.join(IMG_DIR, "front1.png")


class TestSpriteComponent(unittest2.TestCase):

    def setUp(self):
        self.img1 = SpriteComponent("img1", filepath=FRONT1)
        self.noimg = SpriteComponent("noimg")

    def testWidthHeight(self):
        self.assertIsNotNone(self.img1.width)
        self.assertIsNotNone(self.img1.height)
        self.assertEqual(self.img1.width, 17)
        self.assertEqual(self.img1.height, 21)

    def testWidthHeightNone(self):
        self.assertIsNone(self.noimg.width)
        self.assertIsNone(self.noimg.height)

