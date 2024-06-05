from pygame.math import Vector2
from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__()
        self.image = transform.scale(image.load(pl_im), (65,65))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def reset(self): 
        win.blit(self.image, (self.rect.x, self.rect.y))  


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 425:
            self.rect.y += self.speed  
        if keys_pressed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed


class Enemy(GameSprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed, x1, x2):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)
        self.x1 = x1
        self.x2 = x2
        self.direction = 'left'

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        if self.rect.x <= self.x1:
            self.direction = 'right'
        if self.rect.right >= self.x2:
            self.direction = 'left'


class Meteorite(GameSprite):
    def __init__(self,  pl_x, pl_y, pl_im, pl_speed):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)
        self.copy = self.image
        self.position = Vector2(self.rect.center)
        self.direction = Vector2(0, -1)
        self.angle = 0

    def update(self):
        self.rotate(self.speed)
        
    def rotate(self, rotate_speed):
        self.direction.rotate_ip(-rotate_speed)
        self.angle += rotate_speed                   
        self.image = transform.rotate(self.copy, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Comet(GameSprite):
    def __init__(self, pl_x, pl_y, pl_im, pl_speed):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -100:
            self.kill()


class Portal(GameSprite):
    def __init__(self,  pl_x, pl_y, pl_im, pl_speed):
        super().__init__(pl_x, pl_y, pl_im, pl_speed)
        self.copy = self.image
        self.position = Vector2(self.rect.center)
        self.direction = Vector2(0, -1)
        self.angle = 0

    def update(self):
        self.rotate(self.speed)
        
    def rotate(self, rotate_speed):
        self.direction.rotate_ip(-rotate_speed)
        self.angle += rotate_speed                   
        self.image = transform.rotate(self.copy, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


mode = 'menu'
win_size_w = 700
win_size_h = 500
FPS = 60


win = display.set_mode((win_size_w, win_size_h))
win_icon = image.load('icon_win.png')
display.set_icon(win_icon)
display.set_caption('Space game')


_iter_ = 0
health = 3


background = transform.scale(image.load('background.png'), (win_size_w, win_size_h))
win_back = transform.scale(image.load('win.jpg'), (win_size_w, win_size_h))
lose_back = transform.scale(image.load('lose.jpg'), (win_size_w, win_size_h))


mixer.init()
mixer.music.load('main_music.mp3')


#win_music = mixer.Sound('win_music.mp3')
#lose_music = mixer.Sound('lose_music.mp3')
kick = mixer.Sound('kick.ogg')


player = Player(20, 300, 'hero.png', 10)
portal = Portal(620, 380, 'portal.png', 22)


font.init()
font_0 = font.Font(None, 70)
font_1 = font.Font(None, 60)

butt = Rect(220, 230, 280, 50)
label = font_1.render('PLAY', True, (0,0,0))

win_win = font_0.render('YOU WIN!', True, (24, 237, 94))
win_lose = font_0.render('YOU LOSE!', True, (225, 17, 17))
end = font_0.render('Для повтора игры', True, (255,255,255))
end_1 = font_0.render('нажмите пробел', True, (255,255,255))

 
spisok_metiorits = []
spisok_comets = []
spisok_health = []
spisok_enemy = []


def start():
    x = 40
    for i in range(3):
        health = GameSprite(x, 35, 'health.png', 0)
        x += 70
        spisok_health.append(health)

    for i in range(3):
        metiorit = Meteorite(randint(90,500), randint(0,win_size_h-50), 'meteorite.png', 10)
        spisok_metiorits.append(metiorit)

    for i in range(4):
        _x_ = randint(120, win_size_w)
        _y_ = randint(0, 240)
        enemy = Enemy(_x_, _y_, 'cyborg.png', 4, _x_-120, _x_+120)
        spisok_enemy.append(enemy)


start()
clock = time.Clock()
mixer.music.play()

while mode != 'end':
    
    if mode == 'menu':
        win.blit(background, (0,0))
        draw.rect(win, (85, 12, 167), butt)   
        win.blit(label, (315,240))
    
    elif mode == 'game':
        win.blit(background, (0,0))

        player.reset()
        player.update()
            
        portal.reset()
        portal.update()

        for enemy in spisok_enemy:
            enemy.reset()
            enemy.update()
            if len(spisok_health) >= 1:
                if sprite.collide_rect(player, enemy):
                    kick.play()
                    spisok_health.pop()
                    spisok_enemy.remove(enemy)
                    player.rect.x = 20
                    player.rect.y = 300
                    enemy.kill()

        for metiorit in spisok_metiorits:
            metiorit.reset()
            metiorit.update()
            if len(spisok_health) >= 1:
                if sprite.collide_rect(player, metiorit):
                    kick.play()
                    spisok_health.pop()
                    spisok_metiorits.remove(metiorit)   
                    player.rect.x = 20
                    player.rect.y = 300
                    metiorit.kill()
            
        for comet in spisok_comets:
            comet.reset()
            comet.update()
            if len(spisok_health) >= 1:
                if sprite.collide_rect(player, comet):
                    kick.play()
                    spisok_health.pop()
                    spisok_comets.remove(comet)   
                    player.rect.x = 20
                    player.rect.y = 300
                    comet.kill()

        for health in spisok_health:    
                health.reset()
                health.update()

        if _iter_ == 75:
            cometa = Comet(randint(win_size_w, win_size_w+200), randint(0, win_size_h), 'comet.png', randint(1, 5))
            spisok_comets.append(cometa)
            _iter_ = 0


        if len(spisok_health) == 0:
            #lose_music.play()
            mode = 'lose'

        if sprite.collide_rect(player, portal):
            #win_music.play()
            mode = 'win'        


    elif mode == 'win':
        win.blit(win_back, (0,0))
        win.blit(win_win, (250,200))
        win.blit(end, (130, 270))
        win.blit(end_1, (150, 320))
        
    elif mode == 'lose':
        win.blit(lose_back, (0,0))
        win.blit(win_lose, (250,200))
        win.blit(end, (130, 270))
        win.blit(end_1, (150, 320))
        
            
    for e in event.get():
        if e.type == QUIT:
            mode = 'end'
            
        elif e.type == KEYDOWN:    
            if e.key == K_SPACE and (mode == 'win' or mode == 'lose'):
                mode = 'game' 
                _iter_ = 0
                health = 3   
                player.rect.x = 20
                player.rect.y = 300
                spisok_metiorits = []
                spisok_comets = []
                spisok_health = []
                spisok_enemy = []
                start()
                
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1 and mode == 'menu':
                if butt.collidepoint(e.pos):        
                    mode = 'game'
                
                 
    clock.tick(FPS)
    _iter_ += 1
    display.update()
