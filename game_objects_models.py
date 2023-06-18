from pygame import image

SPRITES_DIR = "sprites/"

plane_image = [image.load(SPRITES_DIR + f"player/model/plane_{n}.png") for n in list(range(1, 6))]
plane_image_back = [image.load(SPRITES_DIR + f"player/model/plane_{n}.png") for n in list(range(5, 0, -1))]
enemy_image = [image.load(SPRITES_DIR + f"helicopter/model/helic{n}.png") for n in
               list(range(1, 8)) + list(range(7, 0, -1))]
keyboard = image.load(SPRITES_DIR + f"keys/key.png")
explosion_models = {}
explosion_models["soldier"] = [image.load(SPRITES_DIR + f"kacap/explosion/blood_{n}.png") for n in range(1, 5)]
explosion_models["helicopter"] = [image.load(SPRITES_DIR + f"helicopter/explosion/fire{n}.png") for n in range(1, 5)]
explosion_models["plane"] = [image.load(SPRITES_DIR + f"player/explosion/end{n}.png") for n in range(1, 5)]

fire = image.load(SPRITES_DIR + "fire/fire.png")

enemy_soldier_image = image.load(SPRITES_DIR + "kacap/model/kacap.png")
rocket_image = image.load(SPRITES_DIR + "rocket/rocket.png")
background = image.load(SPRITES_DIR + "background/sky.jpg")
sad_background = image.load(SPRITES_DIR + "background/sky2.jpg")
background1 = image.load(SPRITES_DIR + "background/main_screen/front.jpg")
game_over = image.load(SPRITES_DIR + "background/geroyamslava.png")
winner_screen = image.load(SPRITES_DIR + "background/slavaukraine2.png")
