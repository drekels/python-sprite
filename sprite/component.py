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


class SpriteComponent(object):

    def __init__(self, name, filepath=None, rect=None, image=None, extra_meta=None):
        self.name = name
        self.filepath = filepath
        self._rect = rect
        self._width, self._height = None, None
        if rect:
            self._width, self._height = rect.width, rect.height
        if image:
            self.calc_dimensions(image)
        self.extra_meta = extra_meta or {}

    def __unicode__(self):
        return self.component_name

    def set_atlas_position(self, x, y=None):
        if y is None:
            x, y = x
        self.rect = Rect(x, y, self.width, self.height)

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

    def calc_dimensions(self):
        if not self.filepath:
            return
        from PIL import Image
        image = Image.open(self.filepath)
        with Image.open(self.filepath) as image:
            if image:
                self._width, self._height = image.size
