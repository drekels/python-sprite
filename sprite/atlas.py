from PIL import Image, ImageDraw
from sprite.component import SpriteComponent


MIN_SIZE = (1024, 1024)
DEFAULT_HEADER_COLOR = (0, 102, 136, 255)
DEFAULT_HEADER_INDENT = (10, 10)
DEFAULT_HEADER_LINE_SPACING = 0
HEADER_IMAGE_NAME = "ATLAS_HEADER"
NAME_KEY = "name"
RECT_KEY = "rect"


class Rect(object):

    def __init__(self, x, y, width, height):
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


class _ImageContainer(object):

    def __init__(self, rect):
        self.children = None
        self.rect = rect

    def add_to_child(self, child_index, component):
        added = False
        try:
            added = self.children[0].add_component(component)
        except AttributeError as e:
            if "add_component" not in str(e):
                raise
        return added

    def add_component(self, component):
        if self.children:
            return self.add_to_child(0, component) or self.add_to_child(1, component)
        extra_width = self.rect.width - component.width
        extra_height = self.rect.height - component.height
        if extra_width < 0 or extra_height < 0:
            return False
        if extra_width > extra_height:
            rect1 = Rect(self.rect.x, self.rect.y, component.size[0], self.rect.height)
            rect2 = Rect(self.rect.x + component.size[0], self.rect.y, extra_width, self.rect.height)
        else:
            rect1 = Rect(self.rect.x, self.rect.y, self.rect.width, component.height)
            rect2 = Rect(self.rect.x, self.rect.y + component.height, self.rect.width, extra_height)
        if rect1.size == component.size:
            self.children = (component, _ImageContainer(rect2))
            component.set_atlas_position(rect1.position)
            return True
        else:
            self.children = (_ImageContainer(rect1), _ImageContainer(rect2))
            return self.children[0].add_component(component)


class Atlas(object):

    def __init__(self, header="", min_size=MIN_SIZE):
        self.components = {}
        self._header = header
        self.size = min_size
        self._reset()

    def _reset(self):
        self.root_container = _ImageContainer(Rect(0, 0, *self.size))
        oldcomponents = self.components
        oldcomponents.pop(HEADER_IMAGE_NAME, None)
        self.components = {}
        if self._header:
            self._add_header()
        for name, info in oldcomponents.items():
            self.add(name, info.img, extra_meta=info.extra_meta)

    def _add_header(self):
        header = self._header.format(size="{0}x{1}".format(*self.size))
        lines = header.split("\n")
        dummydraw = ImageDraw.Draw(Image.new('RGBA', (1024, 1024)))
        width = (
            max([dummydraw.textsize(line)[0] for line in lines]) +
            2 * DEFAULT_HEADER_INDENT[0]
        )
        lineheight = dummydraw.textsize("K1")[1] + DEFAULT_HEADER_LINE_SPACING
        height = lineheight * (len(lines)) + 2 * DEFAULT_HEADER_INDENT[1]
        img = Image.new('RGBA', (width, height))
        draw = ImageDraw.Draw(img)
        position = DEFAULT_HEADER_INDENT
        for s in lines:
            draw.text(position, s, fill=DEFAULT_HEADER_COLOR)
            position = (position[0], position[1] + lineheight)
        self.add(SpriteComponent(HEADER_IMAGE_NAME, img))

    def _double_size(self):
        self.size = (self.size[0] * 2, self.size[1] * 2)

    def add_component(self, component):
        if component.name in self.components:
            raise KeyError("Atlas component with name '{0}' already exists".format(component.name))
        c = self.root_container.add_img(component)
        if not c:
            self._double_size()
            self._reset()
            self.add(component)
        else:
            self.components[component.name] = component

    def get_meta(self):
        data = [component.get_meta() for component in self.components.values()]
        return data

    def dump_atlas(self, filepath):
        a = Image.new("RGBA", self.size)
        for component in self.component.values():
            a.paste(component.img, (component.rect.x, component.rect.y))
        a.save(filepath, format="PNG")
