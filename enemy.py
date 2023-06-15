from pygame import draw

from game_objects_models import enemy_image


class Enemy(object):
    model = enemy_image

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.step = 7
        self.fly_count = 0
        self.hit_box = (self.x + 75, self.y, 150, 100)
        self.health = 100
        self.visible = True

    def move(self):
        if self.step > 0:  # right
            if self.x < self.path[1] + self.step:
                self.x += self.step
                self.fly_count += 1
            else:
                self.step = self.step * -1
                self.x += self.step

        else:  # left
            if self.x > self.path[0] - self.step:
                self.x += self.step
                self.fly_count += 1
            else:
                self.step = self.step * -1
                self.x += self.step

    def draw(self, window):
        self.move()
        if self.visible:
            if 0 < self.fly_count >= 60:
                self.fly_count = 0
            window.blit(self.model[self.fly_count // 5], (self.x, self.y))
            self.hit_box = (self.x + 75, self.y, 150, 100)
            draw.rect(window, (255, 0, 0), (self.hit_box[0] - 50, self.hit_box[1] - 10, 250, 10))
            draw.rect(window, (57, 255, 20),
                      (self.hit_box[0] - 50, self.hit_box[1] - 10, 250 - (2.5 * (100 - self.health)), 10))
            # pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)

    def hit(self):
        if self.health > 0:
            self.health -= 5

