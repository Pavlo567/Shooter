from pygame import *
from random import randint
import pygame_menu
init()
import pickle
import os

font.init()

mixer.init()
mixer.music.load('musics.mp3')
mixer.music.set_volume(0.3)
mixer.music.play()
fire_sound = mixer.Sound('shot.wav')

WIDTH, HEIGHT = 900, 600
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Shooter")
#картинки для спрайтів
ufo_image = image.load("alien.png")
player_image = image.load("spaceship.png")
fire_image = image.load("lazer.png")
asteroid_image = image.load("stone.png")
ufo2_image = image.load("big_alien.png")

path = os.getcwd()
exp_images = os.listdir(path + "/explosion")
images_list = []
for img in exp_images:
    images_list.append(transform.scale(image.load("explosion/" + img), (80,80)))
# класи
class Explosion(sprite.Sprite):
    def __init__(self, x, y, images_list):
        super().__init__()
        self.images = images_list
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.k = 0
        self.frames = 0

    def update(self):
        window.blit(self.image, self.rect)
        self.frames +=1
        
        if self.frames == 3 :
            self.frames = 0
            self.k += 1
            self.image = self.images[self.k]
        if self.k == len(self.images) -1:
            self.kill()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.mask = mask.from_surface(self.image)

    
    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def update(self): #рух спрайту
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet( fire_image, 10, 20, self.rect.centerx - 5, self.rect.y)
        bullets.add(bullet)
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        global lost
        '''рух спрайту'''
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else: #якщо спрайт дійшов до нижнього краю
            lost += 1
            lost_text.set_text("Skipped:" + str(lost))
            self.rect.y = randint(-500, -100) #рандомні координати зверху екрану
            self.rect.x = randint(0, WIDTH - 70)
            self.speed = randint(2, 5) #рандомна швидкість

class Alien(GameSprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__(sprite_img, width, height, x, y, speed)
        self.hp = 5
    def update(self):
        global lost
        '''рух спрайту'''
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else: #якщо спрайт дійшов до нижнього краю
            lost += 1
            lost_text.set_text("Skipped:" + str(lost))
            self.rect.y = randint(-500, -100) #рандомні координати зверху екрану
            self.rect.x = randint(0, WIDTH - 70)
            self.speed = randint(2, 5) #рандомна швидкість

class Asteroid(GameSprite):
    def update(self):
        global lost
        '''рух спрайту'''
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else: #якщо спрайт дійшов до нижнього краю
            self.rect.y = randint(-500, -100) #рандомні координати зверху екрану
            self.rect.x = randint(0, WIDTH - 70)
            self.speed = randint(2, 5) #рандомна швидкість

class Bullet(GameSprite):
    def update(self):
        '''рух спрайту'''
        if self.rect.y > -20:
            self.rect.y -= self.speed
        else: #якщо спрайт дійшов до верхнього краю
            self.kill()


class Text(sprite.Sprite):
    def __init__(self, text, x, y, font_size=22, font_name="impact", color=(255,255,255)):
        self.font = font.SysFont(font_name, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
    
    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)

    def set_text(self, new_text): #змінюємо текст напису
        self.image = self.font.render(new_text, True, self.color)

lost_text = Text("Skipped: 0", 20, 20)
score_text = Text("Score: 0", 20, 50)

bg = transform.scale(image.load("game.jpg"), (WIDTH, HEIGHT))
bg2 = transform.scale(image.load("game.jpg"), (WIDTH, HEIGHT))
bg1_y = 0
bg2_y = -HEIGHT
# створення спрайтів
player = Player(player_image, width = 100, height = 100, x = 200, y = HEIGHT-150)

bullets = sprite.Group()
ufos = sprite.Group() #група спрайтів
for i in range(7):
    rand_y = randint(-500, -100)
    rand_x = randint(0, WIDTH - 70)
    rand_speed = randint(2, 4)
    ufos.add(Enemy(ufo_image, width = 80, height = 50, x = rand_x, y = rand_y, speed = rand_speed))
bullets = sprite.Group()
aliens = sprite.Group() #група спрайтів
for i in range(1):
    rand_y = randint(-500, -100)
    rand_x = randint(0, WIDTH - 70)
    rand_speed = randint(2, 4)
    aliens.add(Alien(ufo2_image, width = 130, height = 110, x = rand_x, y = rand_y, speed = rand_speed))
asteroids = sprite.Group()
for i in range(2):
    rand_y = randint(-500, -100)
    rand_x = randint(0, WIDTH - 70)
    rand_speed = randint(2, 4)
    asteroids.add(Asteroid(asteroid_image, width = 50, height = 50, x = rand_x, y = rand_y, speed = rand_speed))

run = True
finish = False
clock = time.Clock()
FPS = 60
step = 3
score = 0
lost = 0

result_text = Text("YOU WIN!", 350, 250, font_size = 50)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE: #якщо натиснуто пробіл
                player.fire()
    if not finish:
        player.update() #рух гравця
        bullets.update() # рух куль
        ufos.update()
        aliens.update()
        asteroids.update()
    #зіткнення куль та ворогів
        spritelist = sprite.groupcollide(ufos, bullets, True, True, sprite.collide_mask)
        for collide in spritelist:
            score += 1
            score_text.set_text("Score:" + str(score))
            rand_y = randint(-500, -100)
            rand_x = randint(0, WIDTH - 70)
            rand_speed = randint(2, 4)
            ufos.add(Enemy(ufo_image, width = 80, height = 50, x = rand_x, y = rand_y, speed = rand_speed))

        spritelist = sprite.groupcollide(aliens, bullets, False, True, sprite.collide_mask)
        for collide in spritelist:
            print(collide)
            collide.hp -=1
            if collide.hp ==0:
                collide.kill()
                score += 1
                score_text.set_text("Score:" + str(score))
                rand_y = randint(-500, -100)
                rand_x = randint(0, WIDTH - 70)
                rand_speed = randint(2, 4)
                aliens.add(Alien(ufo2_image, width = 130, height = 110, x = rand_x, y = rand_y, speed = rand_speed))

        #зіткнення гравця і ворогів
        spritelist = sprite.spritecollide(player, ufos, False, sprite.collide_mask)
        for collide in spritelist:
            finish = True
            result_text.set_text("YOU LOSE!")
        spritelist = sprite.spritecollide(player, asteroids, False, sprite.collide_mask)
        for collide in spritelist:
            finish = True
            result_text.set_text("YOU LOSE!")
        spritelist = sprite.spritecollide(player, aliens, False, sprite.collide_mask)
        for collide in spritelist:
            finish = True
            result_text.set_text("YOU LOSE!")
        
        if lost >= 40:
            finish = True
            result_text.set_text("YOU LOSE!")
        if score >= 40:
            finish = True
        
        window.blit(bg, (0, bg1_y)) #додаємо фон
        window.blit(bg2, (0, bg2_y)) #додаємо фон
        bg1_y +=1
        bg2_y +=1
        if bg1_y > HEIGHT:
            bg1_y = -HEIGHT
        if bg2_y > HEIGHT:
            bg2_y = -HEIGHT
        player.draw() #відрисовуємо спрайти
        ufos.draw(window)
        bullets.draw(window) #відрисовка куль
        aliens.draw(window)
        asteroids.draw(window)
        lost_text.draw()
        score_text.draw()
    else:
        result_text.draw()
    lost_text.draw()
    score_text.draw()
    display.update()
    clock.tick(FPS)