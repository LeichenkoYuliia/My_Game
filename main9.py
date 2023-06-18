import random
import time

import pygame
from game_objects_models import background1, background, sad_background, winner_screen, game_over, keyboard
from player import Plane
from enemy import Enemy
from soldier import EnemySoldier
from rocket import Rocket
from fire import Fire
from explosion import Explosion
from utils import GameStates

pygame.init()
window = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Mriya Game")
game_font = pygame.font.Font(None, 30)
music1 = pygame.mixer.music.load("music/1.mp3")
pygame.mixer.music.play(-1)

fire_sound = pygame.mixer.Sound("music/fire/boom-4.mp3")
fire_sound.set_volume(1)
rockets_sound = pygame.mixer.Sound("music/rockets/1.mp3")
clock = pygame.time.Clock()

color_spd = 8
color_dir = [1, 1, 1]
def_color = [254, 254, 254]


class Game:
    def __init__(self):
        self.state = GameStates.START_MENU

    def draw_start_menu(self):
        window.blit(background1, (0, 0))
        self.draw_text("Press S to start game", 'arial', 40, def_color, window.get_width() / 2, window.get_height() / 2)
        self.change_color(def_color, color_dir)
        pygame.display.update()

    def draw_keyboard_menu(self):
        window.blit(background, (0, 0))
        window.blit(keyboard, (600, 550))
        self.draw_text("Press SPACE to start game", 'arial', 40, def_color, window.get_width() / 2, window.get_height() / 2)
        self.change_color(def_color, color_dir)
        pygame.display.update()

    def draw_text(self, text, font, size, color, x, y):
        font = pygame.font.SysFont(font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        window.blit(text_surface, text_rect)

    def change_color(self, color, dir):
        for i in range(3):
            color[i] += color_spd * dir[i]
            if color[i] >= 255:
                color[i] = 0
            elif color[i] <= 0:
                color[i] = 255

    def game_over_screen(self, background_screen, image):
        window.blit(background_screen, (0, 0))
        window.blit(image,
                    (window.get_width() / 2 - image.get_width() / 2, window.get_height() / 2 - image.get_height() / 2))
        self.draw_text("R - Restart", 'arial', 40, def_color, window.get_width() / 2, window.get_height() - 400)
        self.draw_text("Q - Quit", 'arial', 40, def_color, window.get_width() / 2, window.get_height() - 300)
        self.change_color(def_color, color_dir)
        pygame.display.update()

    def redraw_game_window(self):
        window.blit(background, (0, 0))

        for soldier in soldiers:
            soldier.draw(window)
        for explosion in Explosion.explosions.copy():
            explosion.draw_explosion(window)
        if not enemy.visible and len(Explosion.explosions) == 0:
            self.state = GameStates.WIN
        enemy.draw(window)
        if not mriya.health and len(Explosion.explosions) == 0:
            self.state = GameStates.GAME_OVER
        mriya.draw(window)
        for rocket in rockets:
            rocket.draw(window)
        if not mriya.super_fly:
            for bullet in bullets:
                bullet.draw(window)
            for bullet in bullets2:
                bullet.draw(window)

        pygame.display.update()

    def check_hit(self, projectiles, target):
        for projectile in projectiles.copy():
            if projectile.hit_box[1] - projectile.hit_box[3] / 2 < target.hit_box[1] + target.hit_box[3] and \
                    projectile.hit_box[1] + projectile.hit_box[3] / 2 > target.hit_box[1]:
                if projectile.hit_box[0] + projectile.hit_box[2] / 2 > target.hit_box[0] and projectile.hit_box[0] - \
                        projectile.hit_box[2] / 2 < target.hit_box[0] + target.hit_box[2]:
                    projectiles.remove(projectile)
                    return True

    def check_plane_hit(self, our_plane, enemy_rockets):
        if not our_plane.super_fly:
            for rocket in enemy_rockets.copy():
                if self.check_hit(enemy_rockets, our_plane):
                    our_plane.health = False
                    if len(Explosion.explosions) < 1:
                        Explosion.explosions.append(Explosion(mriya.x, mriya.y, 150, 150, "plane"))
                if 1080 > rocket.y > -260:
                    rocket.y += rocket.step
        else:
            for rocket in enemy_rockets.copy():
                if rocket.hit_box[1] - rocket.hit_box[3] / 2 < our_plane.hit_box_super_fly[1] + \
                        our_plane.hit_box_super_fly[3] and rocket.hit_box[1] + rocket.hit_box[3] / 2 > \
                        our_plane.hit_box_super_fly[1]:
                    if rocket.hit_box[0] + rocket.hit_box[2] / 2 > our_plane.hit_box_super_fly[0] and rocket.hit_box[
                        0] - \
                            rocket.hit_box[2] / 2 < our_plane.hit_box_super_fly[0] + \
                            our_plane.hit_box_super_fly[2]:
                        our_plane.health = False
                        if len(Explosion.explosions) < 1:
                            Explosion.explosions.append(Explosion(mriya.x, mriya.y, 150, 150, "plane"))
                if 1080 > rocket.y > -260:
                    rocket.y += rocket.step


if __name__ == "__main__":
    game = Game()
    restart = True

    while restart:
        mriya = Plane(820, 860, 220, 220)
        enemy = Enemy(0, 30, 300, 100, 1620)
        run = True
        bullets = []
        bullets2 = []
        soldiers = []
        rockets = []
        EnemySoldier.hit_point = 3
        shoot_loop = 0

        while run:
            clock.tick(27)

            if shoot_loop > 0:
                shoot_loop += 1
            if shoot_loop > 5:
                shoot_loop = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    restart = False

            keys = pygame.key.get_pressed()

            if game.state == GameStates.START_MENU:
                pygame.mixer.music.unpause()
                game.draw_start_menu()

                if keys[pygame.K_s]:
                    game.state = GameStates.KEYBOARD_MENU

            if game.state == GameStates.KEYBOARD_MENU:
                game.draw_keyboard_menu()

                if keys[pygame.K_SPACE]:
                    game.state = GameStates.GAME

            if game.state == GameStates.GAME:
                pygame.mixer.music.pause()
                if keys[pygame.K_q]:
                    pygame.quit()
                    quit()
                if keys[pygame.K_a] and mriya.x > mriya.step:
                    mriya.x -= mriya.step
                if keys[pygame.K_d] and mriya.x < 1920 - mriya.width - mriya.step:
                    mriya.x += mriya.step
                if keys[pygame.K_w] and not mriya.super_fly:
                    mriya.super_fly = True
                    mriya.fly_count = 0
                if keys[pygame.K_s] and mriya.super_fly:
                    mriya.super_fly = False
                    mriya.fly_count = 0
                if keys[pygame.K_SPACE] and shoot_loop == 0:
                    fire_sound.play()
                    if len(bullets) < 4:
                        bullets.append(
                            Fire(round(mriya.x + mriya.width // 2) + 35, round(mriya.y + mriya.height // 2) - 35, 25,
                                 25))
                    shoot_loop = 1
                    if len(bullets2) < 4:
                        bullets2.append(
                            Fire(round(mriya.x + mriya.width // 2) - 52, round(mriya.y + mriya.height // 2) - 35, 25,
                                 25))
                    shoot_loop = 1

                if len(soldiers) < 1:
                    soldiers.append(
                        EnemySoldier(round(enemy.x + enemy.width // 2), round(enemy.y + enemy.height // 2), 150, 150))

                for soldier in soldiers.copy():
                    if game.check_hit(bullets, soldier):
                        if len(Explosion.explosions) < 1:
                            Explosion.explosions.append(Explosion(soldier.x, soldier.y, 75, 75, "soldier"))
                        soldiers.remove(soldier)
                    if game.check_hit(bullets2, soldier):
                        if len(Explosion.explosions) < 1:
                            Explosion.explosions.append(Explosion(soldier.x, soldier.y, 75, 75, "soldier"))
                        soldiers.remove(soldier)
                    if 1080 > soldier.y > 0:
                        soldier.y += soldier.step
                    else:
                        soldier.hit()
                        if EnemySoldier.hit_point <= 0:
                            game.state = GameStates.GAME_OVER
                        soldiers.remove(soldier)

                for bullet in bullets.copy():
                    if game.check_hit(bullets, enemy):
                        enemy.hit()
                        if enemy.health <= 0:
                            if len(Explosion.explosions) < 1:
                                Explosion.explosions.append(Explosion(enemy.x, enemy.y - 75, 75, 75, "helicopter"))
                            enemy.visible = False
                    if 1080 > bullet.y > 0:
                        bullet.y -= bullet.step
                    else:
                        bullets.remove(bullet)

                for bullet in bullets2.copy():
                    if game.check_hit(bullets2, enemy):
                        enemy.hit()
                        if enemy.health <= 0:
                            if len(Explosion.explosions) < 1:
                                Explosion.explosions.append(Explosion(enemy.x, enemy.y - 75, 75, 75, "helicopter"))
                            enemy.visible = False
                    if 1080 > bullet.y > 0:
                        bullet.y -= bullet.step
                    else:
                        bullets2.remove(bullet)

                if enemy.health <= 100:
                    if len(rockets) < 20:
                        rockets.append(
                            Rocket(random.randint(0, 1920), -250, 70, 250))
                        rockets_sound.play()
                    game.check_plane_hit(mriya, rockets)

                if enemy.health <= 60:
                    if len(rockets) < 40:
                        rockets.append(
                            Rocket(random.randint(0, 1920), -250, 70, 250))
                        rockets_sound.play()
                    game.check_plane_hit(mriya, rockets)

                if enemy.health <= 30:
                    if len(rockets) < 60:
                        rockets.append(
                            Rocket(random.randint(0, 1920), -250, 70, 250))
                        rockets_sound.play()
                    game.check_plane_hit(mriya, rockets)
                game.redraw_game_window()

            if game.state == GameStates.GAME_OVER:
                game.game_over_screen(sad_background, game_over)
                if keys[pygame.K_r]:
                    game.state = GameStates.START_MENU
                    run = False
                if keys[pygame.K_q]:
                    pygame.quit()
                    quit()

            if game.state == GameStates.WIN:
                game.game_over_screen(background, winner_screen)
                if keys[pygame.K_r]:
                    game.state = GameStates.START_MENU
                    run = False
                if keys[pygame.K_q]:
                    pygame.quit()
                    quit()

    pygame.quit()
    quit()
