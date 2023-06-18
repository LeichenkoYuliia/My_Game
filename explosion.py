import pygame
from game_objects_models import explosion_models


class Explosion(object):
    images = ""
    models = explosion_models
    explosions = []

    def __init__(self, x, y, width, height, name_of_target):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.next_frame_time = 0
        self.anim_index = -1
        self.name_of_target = name_of_target

    def draw_explosion(self, window):
        current_time = pygame.time.get_ticks()

        if current_time > self.next_frame_time:
            inter_frame_time = 150
            self.next_frame_time = current_time + inter_frame_time
            self.anim_index += 1
            if self.anim_index >= len(Explosion.models[self.name_of_target]):
                Explosion.explosions.clear()
                self.anim_index = -1
        explosion_image = Explosion.models[self.name_of_target][self.anim_index]
        window.blit(explosion_image, (self.x + 20, self.y + 90))
