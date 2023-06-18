from game_objects_models import plane_image
import pygame

class Plane(object):
    model = plane_image
    model_reverse = plane_image[::-1]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.step = 35
        self.fly_count = 0
        self.super_fly = False
        self.hit_box = (self.x, self.y, 220, 220)
        self.hit_box_super_fly = (self.x + 80, self.y, 60, 220)
        self.health = True

    def draw(self, window):
        if self.health:
            if 0 < self.fly_count + 1 >= 25:
                self.fly_count = 24

            if self.super_fly:
                window.blit(self.model[self.fly_count // 5], (self.x, self.y))
                self.fly_count += 1
                self.hit_box_super_fly = (self.x + 80, self.y, 60, 220)
                # pygame.draw.rect(window, (255, 0, 0), self.hit_box_super_fly, 2)

            if not self.super_fly:
                window.blit(self.model_reverse[self.fly_count // 5], (self.x, self.y))
                self.fly_count += 1
                self.hit_box = (self.x, self.y, 220, 220)
                # pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)
