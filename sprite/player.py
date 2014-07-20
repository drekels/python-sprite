class SpriteAnimationPlayer(object):

    def __init__(self, renderer, animation):
        self.renderer = renderer
        self.animation = animation
        self.stage_index = 0

    def start_animation(self, extra_time=0):
        self.stage_index = 0
        self.start_next_stage(extra_time=extra_time)


    def start_next_stage(self, extra_time=0):
        try:
            self.stage = self.animation.stages[self.stage_index]
        except IndexError:
            self.end_animaiton()
        else:
            self.renderer.set_component(self.stage.component, **self.stage.get_params())
            self.stage_time_remaining = self.stage.duration
            self.pass_animation_time(extra_time)

    def pass_animation_time(self, time):
        self.stage_time_remaining -= time
        if self.stage_time_remaining <= 0:
            self.stage_index += 1
            self.start_next_stage(extra_time=-self.stage_time_remaining)

    def end_animation(self):
        self.complete = True

    def iscomplete(self):
        return self.stage_index == len(self.animation.stages)
