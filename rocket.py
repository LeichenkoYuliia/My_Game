from game_objects_models import rocket_image


class Rocket(object):
    model = rocket_image

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.step = 10
        self.hit_box = (self.x, self.y + 100, 70, 150)

    def draw(self, window):
        window.blit(rocket_image, (self.x, self.y))
        self.hit_box = (self.x, self.y + 100, 70, 150)
        # pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)
