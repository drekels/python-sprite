""" The animations module contains functions for creating and reading animations """


import datetime as dt
import logging


LOG = logging.getLogger(__name__)
ZERO_TIME = dt.timedelta()


# ANIMATION HOOKS
ON_ANIMATION_END = "ON_ANIMATION_END"


class SpriteAnimationStage(object):
    params = [
        {"name": "component_name"},
        {"name": "duration"},
        {"name": "displacement_x", "default": 0},
        {"name": "displacement_y", "default": 0},
    ]

    def __init__(self, component, duration, displacement_x=0, displacement_y=0):
        self.component = component
        self.duration = duration
        self.displacement_x = displacement_x
        self.displacement_y = displacement_y

    def get_params(self):
        return self.__getstate__()

    def update_renderer(self, renderer):
        renderer.set_component(**self.__getstate__())

    def __getstate__(self):
        state = {}
        for param in self.params:
            name = param["name"]
            state[name] = getattr(self, name)
        return state

    def __setstate__(self, state):
        for param in self.params:
            if param["name"] in state:
                value = state[param["name"]]
            else:
                if "default" not in param:
                    raise AttributeError(
                        "SpriteAnimationStage requires value for {0}".format(param["name"])
                    )
                value = param["default"]
            setattr(self, param["name"], value)


def get_animation_state(animation, secondary_values=True):
    """ Return a dictionary containing all the animation data """
    stages = list(animation.get_stages())
    stages.sort(key=lambda x: x.order)
    state = {}
    state["stages"] = [stage.__getstate__() for stage in stages]
    state["name"] = animation.name
    if secondary_values:
        state["min_x"] = animation.min_x
        state["max_x"] = animation.max_x
        state["min_y"] = animation.min_y
        state["max_y"] = animation.max_y
        state["width"] = animation.width
        state["height"] = animation.height
        state["offset_x"] = animation.offset_x
        state["offset_y"] = animation.offset_y
    return state


def get_min_x(animation):
    stages = animation.get_stages()
    if not stages:
        return 0
    return min([stage.displacement_x - stage.component.width / 2.0 for stage in stages])


def get_max_x(animation):
    stages = animation.get_stages()
    if not stages:
        return 0
    return max([stage.displacement_x + stage.component.width / 2.0 for stage in stages])


def get_min_y(animation):
    stages = animation.get_stages()
    if not stages:
        return 0
    return min([stage.displacement_y - stage.component.height / 2.0 for stage in stages])


def get_max_y(animation):
    stages = animation.get_stages()
    if not stages:
        return 0
    return max([stage.displacement_y + stage.component.height / 2.0 for stage in stages])


def get_offset(animation):
    """ Get the offset to render each sprite with in order to keep the sprite within its
    height/width.  When rendering a sprite, the center of each component should be rendered at
    (BOX_CENTER + DISPLACEMENT + OFFSET).  The top left of the component should be rendered at
    [BOX_TOP_LEFT + DISPLACEMENT + OFFSET + (BOX_DIMENSIONS - SPRITE_DIMENSIONS) / 2]
    """
    return (get_offset_x(animation), get_offset_y(animation))


def get_offset_x(animation):
    return -(animation.min_x + animation.max_x) / 2.0


def get_offset_y(animation):
    return -(animation.min_y + animation.max_y) / 2.0


def get_width(animation):
    """ Get the width of the animation.  This is the horizontal space that the animation will take
    up throughout the animation.  This value can be used to create a box that keeps the animation
    from overlapping with other elements at any time during the animation.
    """
    return animation.max_x - animation.min_x


def get_height(animation):
    """ Get the height of the animation.  This is the vertical space that the animation will take
    up throughout the animation.  This value can be used to create a box that keeps the animation
    from overlapping with other elements at any time during the animation.
    """
    return animation.max_y - animation.min_y


class SpriteAnimation(object):
    __getstate__ = get_animation_state
    min_x = property(get_min_x)
    max_x = property(get_max_x)
    min_y = property(get_min_y)
    max_y = property(get_max_y)
    offset_x = property(get_offset_x)
    offset_y = property(get_offset_y)
    offset = property(get_offset)
    width = property(get_width)
    height = property(get_height)
    stage_class = SpriteAnimationStage

    @classmethod
    def load(cls, state):
        a = cls.__new__(cls)
        a.__setstate__(state)
        return a

    def __init__(self, name, stages=None):
        self.name = name
        self._stages = stages or []
        self.displacement = 0.0

    def __unicode__(self):
        return self.name

    def __setstate__(self, state):
        self.name = state["name"]
        self._stages = []
        for stage in state["stages"]:
            s = self.stage_class.__new__(self.stage_class)
            s.__setstate__(stage)
            self._stages.append(s)

    @property
    def stages(self):
        return self._stages

    def get_stages(self):
        return self.stages


class SpriteAnimationPlayer(object):

    def __init__(self, renderer, animation):
        self.renderer = renderer
        self.animation = animation
        self.stage_index = 0
        self.callbacks = {}

    def start_animation(self, extra_time=ZERO_TIME):
        self.stage_index = 0
        self.start_next_stage(extra_time=extra_time)

    def start_next_stage(self, extra_time=ZERO_TIME):
        try:
            self.stage = self.animation.stages[self.stage_index]
        except IndexError:
            self.end_animation(extra_time=extra_time)
        else:
            self.stage.update_renderer(self.renderer)
            self.stage_time_remaining = dt.timedelta(seconds=self.stage.duration)
            self.pass_animation_time(extra_time)

    def pass_animation_time(self, time):
        if self.iscomplete():
            return
        self.stage_time_remaining -= time
        if self.stage_time_remaining <= dt.timedelta():
            self.stage_index += 1
            self.start_next_stage(extra_time=-self.stage_time_remaining)

    def end_animation(self, extra_time=ZERO_TIME):
        self.execute_hook(ON_ANIMATION_END)

    def iscomplete(self):
        return self.stage_index == len(self.animation.stages)

    def add_end_callback(self, callback):
        self.add_callback(ON_ANIMATION_END, callback)

    def add_callback(self, hook, callback):
        self.callbacks.setdefault(hook, [])
        self.callbacks[hook].append(callback)

    def execute_hook(self, hook, extra_time=ZERO_TIME):
        callbacks = self.callbacks.pop(hook, [])
        for callback in callbacks:
            callback(extra_time=extra_time)
