import unittest2
from sprite.component import SpriteComponent, Rect
import logging
import os


LOG = logging.getLogger(__name__)


IMG_DIR = os.path.join(os.path.dirname(__file__), "img")
FRONT1 = os.path.join(IMG_DIR, "front1.png")


class TestRect(unittest2.TestCase):

    def test_equal(self):
        rects = [
            Rect(1, 1, 1, 1),
            Rect(1, 1, 1, 1),
            Rect(2, 1, 1, 1),
            Rect(2, 1, 1, 1),
            Rect(2, 2, 1, 1),
            Rect(2, 2, 1, 1),
            Rect(2, 2, 2, 1),
            Rect(2, 2, 2, 1),
            Rect(2, 2, 2, 2),
            Rect(2, 2, 2, 2),
        ]
        for i in range(len(rects) / 2):
            primary_a, primary_b = rects[i*2], rects[i*2+1]
            self.assertEqual(primary_a, primary_b)
            self.assertTrue(primary_a == primary_b)
            LOG.debug("{}, {}".format(primary_a, primary_b))
            self.assertFalse(primary_a != primary_b)
            for j in range(len(rects) / 2):
                if j == i:
                    continue
                secondary = rects[j*2]
                self.assertNotEqual(primary_a, secondary)
                self.assertFalse(primary_a == secondary)
                self.assertTrue(primary_a != secondary)


class TestSpriteComponent(unittest2.TestCase):

    def setUp(self):
        self.img1 = SpriteComponent("img1", filepath=FRONT1)
        self.img2 = SpriteComponent("img2", rect=Rect(1, 2, 3, 4))
        self.noimg = SpriteComponent("noimg")

    def test_rect_set(self):
        self.assertEqual(Rect(1, 2, 3, 4), self.img2.rect)
        self.assertEqual((3, 4), self.img2.size)
        self.assertEqual(3, self.img2.width)
        self.assertEqual(4, self.img2.height)

    def test_width_height(self):
        self.assertIsNotNone(self.img1.width)
        self.assertIsNotNone(self.img1.height)
        self.assertEqual(self.img1.width, 17)
        self.assertEqual(self.img1.height, 21)

    def test_width_height_none(self):
        self.assertIsNone(self.noimg.width)
        self.assertIsNone(self.noimg.height)

    def test_rect_none(self):
        self.assertIsNone(self.img1.rect)

    def test_rect_is_private(self):
        self.assertRaises(AttributeError, setattr, self.img1, "rect", Rect(1, 2, 3, 4))
