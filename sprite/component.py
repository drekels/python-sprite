class Rect(object):

    def __init__(self, x, y, width=None, height=None):
        if width is None:
            x, y = x
            width, height = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __getstate__(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }

    def __repr__(self):
        return "Rect({x}, {y}, {width}, {height})".format(**self.__dict__)

    def __unicode__(self):
        return "({x}, {y}, {width}, {height})".format(**self.__dict__)

    def __eq__(self, other):
        for param in ["x", "y", "width", "height"]:
            if getattr(self, param) != getattr(other, param):
                return False
        return True

    def __ne__(self, other):
        return not (self == other)

    @property
    def position(self):
        return self.x, self.y

    @property
    def size(self):
        return self.width, self.height

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.width
        yield self.height

    def get_tuple(self):
        return (x for x in self)


class SpriteComponent(object):

    @classmethod
    def from_meta(cls, meta):
        value = cls()
        value.__setstate__(meta)
        return value

    def __init__(self, name=None, filepath=None, rect=None, image=None, extra_meta=None):
        self.name = name
        self.filepath = filepath
        self._rect = rect
        self._width, self._height = None, None
        if rect:
            self._width, self._height = rect.width, rect.height
        self._image = image
        self.extra_meta = extra_meta or {}

    def __unicode__(self):
        return self.name

    def __getstate__(self):
        state = {"name": self.name}
        if self.rect:
            state["x"] = self.rect.x
            state["y"] = self.rect.y
        if self.width is not None:
            state["width"] = self.width
            state["height"] = self.height
        if self.extra_meta:
            state["extra_meta"] = self.extra_meta
        return state

    def __setstate__(self, state):
        self.name = state['name']
        self._width, self._height = state['width'], state['height']
        self.set_atlas_position(state['x'], state['y'])
        if "extra_meta" in state:
            self.extra_meta = state["extra_meta"]

    def get_meta(self):
        state = self.__getstate__()
        return state

    def set_atlas_position(self, x, y=None):
        if y is None:
            x, y = x
        self._rect = Rect(x, y, self.width, self.height)

    @property
    def rect(self):
        return self._rect

    @property
    def width(self):
        if not hasattr(self, "_width") or not self._width:
            self.calc_dimensions()
        return self._width

    @property
    def height(self):
        if not hasattr(self, "_height") or not self._height:
            self.calc_dimensions()
        return self._height

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def atlas_position(self):
        if self.x is None:
            return None
        return (self.x, self.y)

    @property
    def image(self):
        if not self._image and self.filepath:
            from PIL import Image
            self._image = Image.open(self.filepath)
        return self._image

    def calc_dimensions(self):
        if self.image:
            self._width, self._height = self.image.size
