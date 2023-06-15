from game_objects_models import fire


class Fire(object):
    model = fire

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.step = 20
        self.width = width
        self.height = height
        self.hit_box = (self.x, self.y, 25, 25)

    def draw(self, window):
        window.blit(fire, (self.x, self.y))
        self.hit_box = (self.x, self.y, 25, 25)
        # pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)
