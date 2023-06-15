from pygame import draw
from game_objects_models import enemy_soldier_image

class EnemySoldier(object):
    model = enemy_soldier_image
    hit_point = 10

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.step = 7
        self.hit_box = (self.x + 35, self.y, 60, 150)

    def draw(self, window):
        window.blit(self.model, (self.x, self.y))
        self.hit_box = (self.x + 35, self.y, 60, 150)
        draw.rect(window, (255, 0, 0), (1900, 300, 20, 600))
        draw.rect(window, (57, 255, 20),
                         (1900, 300, 20, 600 - (60 * (10 - EnemySoldier.hit_point))))
        # pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)

    def hit(self):
        if EnemySoldier.hit_point > 0:
            EnemySoldier.hit_point -= 1
        # else:
        #     global game_state
        #     game_state = "sad_game_over"