import random

import pygame

pygame.init()

window = pygame.display.set_mode((1920, 1080))

pygame.display.set_caption("Mriya Game")

plane_image = [pygame.image.load("plane_image/plane_1.png"), pygame.image.load("plane_image/plane_2.png"),
               pygame.image.load("plane_image/plane_3.png"),
               pygame.image.load("plane_image/plane_4.png"), pygame.image.load("plane_image/plane_5.png")]
plane_image_back = [pygame.image.load("plane_image/plane_5.png"), pygame.image.load("plane_image/plane_4.png"),
                    pygame.image.load("plane_image/plane_3.png"),
                    pygame.image.load("plane_image/plane_2.png"), pygame.image.load("plane_image/plane_1.png")]
fire = pygame.image.load("fire_image/fire.png")
enemy_image = [pygame.image.load("enemies_images/helic1.png"), pygame.image.load("enemies_images/helic2.png"),
               pygame.image.load("enemies_images/helic3.png"), pygame.image.load("enemies_images/helic4.png"),
               pygame.image.load("enemies_images/helic5.png"), pygame.image.load("enemies_images/helic6.png"),
               pygame.image.load("enemies_images/helic7.png"), pygame.image.load("enemies_images/helic6.png"),
               pygame.image.load("enemies_images/helic5.png"), pygame.image.load("enemies_images/helic4.png"),
               pygame.image.load("enemies_images/helic3.png"), pygame.image.load("enemies_images/helic2.png"),
               ]
enemy_soldier_image = pygame.image.load("enemies_images/kacap.png")
rocket_image = pygame.image.load("enemies_images/rocket.png")
background = pygame.image.load("sky.jpg")
background1 = pygame.image.load("start_window/front.jpg")
game_over = pygame.image.load("sad_game_over/geroyamslava.png")
winner_screen = pygame.image.load("happy_game_over/slavaukraine.png")
game_font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()
game_state = "start_menu"
color_spd = 8
color_dir = [1, 1, 1]
def_color = [254, 254, 254]


def draw_start_menu():
    window.blit(background1, (0, 0))
    draw_text("Press S to start game", 'arial', 40, def_color, window.get_width() / 2, window.get_height() / 2)
    change_color(def_color, color_dir)
    pygame.display.update()


def draw_text(text, font, size, color, x, y):
    font = pygame.font.SysFont(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)


def change_color(color, dir):
    for i in range(3):
        color[i] += color_spd * dir[i]
        if color[i] >= 255:
            color[i] = 0
        elif color[i] <= 0:
            color[i] = 255


def game_over_screen(image):
    window.blit(background, (0, 0))
    window.blit(image, (window.get_width() / 2 - image.get_width() / 2, window.get_height() / 2 - image.get_height() / 2))
    draw_text("R - Restart", 'arial', 40, def_color, window.get_width() / 2, window.get_height() - 400)
    draw_text("Q - Quit", 'arial', 40, def_color, window.get_width() / 2, window.get_height() - 300)
    change_color(def_color, color_dir)
    pygame.display.update()


class Plane(object):
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
                window.blit(plane_image[self.fly_count // 5], (self.x, self.y))
                self.fly_count += 1
                self.hit_box_super_fly = (self.x + 80, self.y, 60, 220)
                # pygame.draw.rect(window, (255, 0, 0), self.hit_box_super_fly, 2)

            if not self.super_fly:
                window.blit(plane_image_back[self.fly_count // 5], (self.x, self.y))
                self.fly_count += 1
                self.hit_box = (self.x, self.y, 220, 220)
                # pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)
        else:
            global game_state
            game_state = "game_over"


class Fire(object):
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


class Enemy(object):
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
        if self.step > 0:    # right
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
            window.blit(enemy_image[self.fly_count // 5], (self.x, self.y))
            self.hit_box = (self.x + 75, self.y, 150, 100)
            pygame.draw.rect(window, (255, 0, 0), (self.hit_box[0] - 50, self.hit_box[1] - 10, 250, 10))
            pygame.draw.rect(window, (57, 255, 20),
                             (self.hit_box[0] - 50, self.hit_box[1] - 10, 250 - (2.5 * (100 - self.health)), 10))
            # pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)



    def hit(self):
        if self.health > 0:
            self.health -= 5
        else:
            global game_state
            game_state = "win_game_over"

class EnemySoldier(object):
    hit_point = 10

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.step = 7
        self.hit_box = (self.x + 35, self.y, 60, 150)

    def draw(self, window):
        window.blit(enemy_soldier_image, (self.x, self.y))
        self.hit_box = (self.x + 35, self.y, 60, 150)
        pygame.draw.rect(window, (255, 0, 0), (1900, 300, 20, 600))
        pygame.draw.rect(window, (57, 255, 20),
                         (1900, 300, 20, 600 - (60 * (10 - EnemySoldier.hit_point))))
        # pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)

    def hit(self):
        if EnemySoldier.hit_point > 0:
            EnemySoldier.hit_point -= 1
        else:
            global game_state
            game_state = "sad_game_over"


class Rocket(object):
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


def redraw_game_window():
    window.blit(background, (0, 0))
    enemy.draw(window)
    for soldier in soldiers:
        soldier.draw(window)
    mriya.draw(window)
    for rocket in rockets:
        rocket.draw(window)
    if not mriya.super_fly:
        for bullet in bullets:
            bullet.draw(window)
        for bullet in bullets2:
            bullet.draw(window)

    pygame.display.update()


def check_hit(projectiles, target):
    for projectile in projectiles.copy():
        if projectile.hit_box[1] - projectile.hit_box[3] / 2 < target.hit_box[1] + target.hit_box[3] and \
                projectile.hit_box[1] + projectile.hit_box[3] / 2 > target.hit_box[1]:
            if projectile.hit_box[0] + projectile.hit_box[2] / 2 > target.hit_box[0] and projectile.hit_box[0] - \
                    projectile.hit_box[2] / 2 < target.hit_box[0] + target.hit_box[2]:
                projectiles.remove(projectile)
                return True


def check_plane_hit(our_plane, enemy_rockets):
    if not our_plane.super_fly:
        for rocket in enemy_rockets.copy():
            if check_hit(enemy_rockets, our_plane):
                our_plane.health = False
            if 1080 > rocket.y > -260:
                rocket.y += rocket.step

    else:
        for rocket in enemy_rockets.copy():
            if rocket.hit_box[1] - rocket.hit_box[3] / 2 < our_plane.hit_box_super_fly[1] + \
                    our_plane.hit_box_super_fly[3] and rocket.hit_box[1] + rocket.hit_box[3] / 2 > \
                    our_plane.hit_box_super_fly[1]:
                if rocket.hit_box[0] + rocket.hit_box[2] / 2 > our_plane.hit_box_super_fly[0] and rocket.hit_box[0] - \
                        rocket.hit_box[2] / 2 < our_plane.hit_box_super_fly[0] + \
                        our_plane.hit_box_super_fly[2]:
                    our_plane.health = False
            if 1080 > rocket.y > -260:
                rocket.y += rocket.step


restart = True

while restart:
    mriya = Plane(820, 860, 220, 220)
    enemy = Enemy(0, 30, 300, 100, 1620)
    run = True
    bullets = []
    bullets2 = []
    soldiers = []
    rockets = []
    EnemySoldier.hit_point = 10
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

        if game_state == "start_menu":
            draw_start_menu()
            if keys[pygame.K_s]:
                game_state = "game"

        if game_state == "game":
            if keys[pygame.K_LEFT] and mriya.x > mriya.step:
                mriya.x -= mriya.step
            elif keys[pygame.K_RIGHT] and mriya.x < 1920 - mriya.width - mriya.step:
                mriya.x += mriya.step
            if keys[pygame.K_UP]:
                mriya.super_fly = True
                mriya.fly_count = 0
            if keys[pygame.K_DOWN]:
                mriya.super_fly = False
                mriya.fly_count = 0
            if keys[pygame.K_SPACE] and shoot_loop == 0:
                if len(bullets) < 4:
                    bullets.append(
                        Fire(round(mriya.x + mriya.width // 2) + 35, round(mriya.y + mriya.height // 2) - 35, 25, 25))
                shoot_loop = 1
                if len(bullets2) < 4:
                    bullets2.append(
                        Fire(round(mriya.x + mriya.width // 2) - 52, round(mriya.y + mriya.height // 2) - 35, 25, 25))
                shoot_loop = 1

            if len(soldiers) < 1:
                soldiers.append(
                    EnemySoldier(round(enemy.x + enemy.width // 2), round(enemy.y + enemy.height // 2), 150, 150))

            for soldier in soldiers.copy():
                if check_hit(bullets, soldier):
                    soldiers.remove(soldier)
                if check_hit(bullets2, soldier):
                    soldiers.remove(soldier)
                if 1080 > soldier.y > 0:
                    soldier.y += soldier.step
                else:
                    soldier.hit()
                    soldiers.remove(soldier)


            for bullet in bullets.copy():
                if check_hit(bullets, enemy):
                    enemy.hit()
                    # bullets.remove(bullet)
                if 1080 > bullet.y > 0:
                    bullet.y -= bullet.step
                else:
                    bullets.remove(bullet)


            for bullet in bullets2.copy():
                if check_hit(bullets2, enemy):
                    enemy.hit()
                    # bullets2.remove(bullet)
                if 1080 > bullet.y > 0:
                    bullet.y -= bullet.step
                else:
                    bullets2.remove(bullet)


            if enemy.health <= 75:
                if len(rockets) < 20:
                    rockets.append(
                        Rocket(random.randint(0, 1920), -250, 70, 250))
                check_plane_hit(mriya, rockets)


            if enemy.health <= 50:
                if len(rockets) < 40:
                    rockets.append(
                        Rocket(random.randint(0, 1920), -250, 70, 250))
                check_plane_hit(mriya, rockets)


            if enemy.health <= 25:
                if len(rockets) < 60:
                    rockets.append(
                        Rocket(random.randint(0, 1920), -250, 70, 250))
                check_plane_hit(mriya, rockets)
            redraw_game_window()

        if game_state == "game_over":
            game_over_screen(game_over)
            if keys[pygame.K_r]:
                game_state = "start_menu"
                run = False

            if keys[pygame.K_q]:
                pygame.quit()
                quit()
        if game_state == "win_game_over":
            game_over_screen(winner_screen)
            if keys[pygame.K_r]:
                game_state = "start_menu"
                run = False

            if keys[pygame.K_q]:
                pygame.quit()
                quit()

pygame.quit()
quit()
