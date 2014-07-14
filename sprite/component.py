from PIL import Image
from contextlib import contextmanager


class SpriteComponent(object):

    def __init__(self, name, filepath=None, x=None, y=None, image=None, width=None,
                 height=None, extra_meta=None):
        self.component_name = name
        self.filepath = filepath
        self.x = x
        self.y = y
        self._width = width
        self._height = height
        if image:
            self._calc_dimensions(image)
        self.extra_meta = extra_meta or {}

    def __unicode__(self):
        return self.component_name

    @property
    def width(self):
        if not hasattr(self, "_width") or not self._width:
            with self.image as i:
                if i:
                    self._calc_dimensions(i)
        return self._width

    @property
    def height(self):
        if not hasattr(self, "_height") or not self._height:
            with self.image as i:
                if i:
                    self._calc_dimensions(i)
        return self._height

    @property
    def size(self):
        return (self.width, self.height)

    def _calc_dimensions(self, image):
        self._width, self._height = image.size

    @property
    @contextmanager
    def image(self):
        if not self.filepath:
            yield None
        else:
            try:
                f = open(self.filepath)
                value = Image.open(f)
                try:
                    value = value.__enter__()
                    yield value
                finally:
                    value.__exit__()
            except IOError:
                yield None
