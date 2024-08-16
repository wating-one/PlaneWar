import pygame
from pygame.examples.moveit import GameObject

from sprites.base import *
from constant import *
# 载入图片
game_pause_nor=pygame.image.load(BASE_DIR+'image/game_pause_nor.png')
game_pause_pressed=pygame.image.load(BASE_DIR+'image/game_pause_pressed.png')
game_resume_nor=pygame.image.load(BASE_DIR+'image/game_resume_nor.png')
game_resume_pressed=pygame.image.load(BASE_DIR+'image/game_resume_pressed.png')
bomb_img=pygame.image.load(BASE_DIR+'image/bomb.png')
life_img=pygame.image.load(BASE_DIR+'image/life.png')
music_img=pygame.image.load(BASE_DIR+'image/music.png')
music_pressed_img=pygame.image.load(BASE_DIR+'image/music_pressed.png')
music_stop_img=pygame.image.load(BASE_DIR+'image/music_stop.png')
music_stop_pressed_img=pygame.image.load(BASE_DIR+'image/music_stop_pressed.png')
setting_img=pygame.image.load(BASE_DIR+'image/setting.png')
setting_pressed_img=pygame.image.load(BASE_DIR+'image/setting_pressed.png')
volume_img=pygame.image.load(BASE_DIR+'image/volume.png')
volume_pole_img=pygame.image.load(BASE_DIR+'image/volume_pole.png')
button_nor_img=pygame.image.load(BASE_DIR+'image/button_nor.png')
button_p_img=pygame.image.load(BASE_DIR+'image/button_p.png')
quit_nor_img=pygame.image.load(BASE_DIR+'image/quit_nor.png')
quit_sel_img=pygame.image.load(BASE_DIR+'image/quit_sel.png')
restart_nor_img=pygame.image.load(BASE_DIR+'image/restart_nor.png')
restart_sel_img=pygame.image.load(BASE_DIR+'image/restart_sel.png')
author_bg_img=pygame.image.load(BASE_DIR+"image/author_liu.png")
author_img=pygame.image.load(BASE_DIR+"image/author.png")
author_pressed_img=pygame.image.load(BASE_DIR+"image/author_pressed.png")
class Unit(pygame.sprite.Sprite):
    def __init__(self,img):
        super().__init__()
        self.image=img
        self.rect=self.image.get_rect()
    def update(self):
        pass
class Pause(Unit):
    def __init__(self):
        super().__init__(game_pause_nor)
        self.isPaused=False
        self.isPressed=False
        self.rect.right=SCREEN_RECT.right-10
        self.rect.top=SCREEN_RECT.top+10
    def update(self):
        if self.isPaused and self.isPressed:
            self.image=game_resume_pressed
        if not self.isPaused and self.isPressed:
            self.image=game_pause_pressed
        if self.isPaused and not self.isPressed:
            self.image=game_resume_nor
        if not self.isPaused and not self.isPressed:
            self.image=game_pause_nor

class Bomb(Unit):
    def __init__(self):
        super().__init__(bomb_img)
        self.rect.left=10
        self.rect.bottom=SCREEN_RECT.bottom-10
        self.num=1

class Life(Unit):
    life_list = []
    def __init__(self):
        super().__init__(life_img)
        self.rect.bottom=SCREEN_RECT.bottom-10
        if Life.life_list:
            right=Life.life_list[-1].rect.left
            self.rect.right=right
        else:
            self.rect.right=SCREEN_RECT.right
        Life.life_list.append(self)

    @staticmethod
    def remove():
        if Life.life_list:
            life=Life.life_list.pop()
            life.kill()

class Silent(Unit):
    def __init__(self):
        super().__init__(music_img)
        self.isSilent=False
        self.isPressed=False
        self.rect.right=SCREEN_RECT.right-10
        self.rect.top=SCREEN_RECT.top+10+60
    def update(self):
        if self.isSilent and self.isPressed:
            self.image=music_stop_pressed_img
        if not self.isSilent and self.isPressed:
            self.image=music_pressed_img
        if self.isSilent and not self.isPressed:
            self.image=music_stop_img
        if not self.isSilent and not self.isPressed:
            self.image=music_img

class Setting(Unit):

    def __init__(self):
        super().__init__(setting_img)
        self.rect.top=SCREEN_RECT.top+10+60+60
        self.rect.right=SCREEN_RECT.right-10
        self.isPressed=False

    def update(self):
        if self.isPressed:
            self.image=setting_pressed_img
        else:
            self.image = setting_img

class Volume(Unit):

    def __init__(self,flag=False):
        super().__init__(volume_img)
        self.rect.x=SCREEN_RECT.centerx
        if flag:
            self.rect.centery=SCREEN_RECT.centery+20
        else:
            self.rect.centery=SCREEN_RECT.centery-20

class Volume_Pole(Unit):

    def __init__(self,volume,remain,flag=False):
        super().__init__(volume_pole_img)
        self.volume=volume
        self.rect.left=volume.rect.x+remain*volume.rect.width
        if flag:
            self.rect.centery = SCREEN_RECT.centery + 20
        else:
            self.rect.centery = SCREEN_RECT.centery - 20

class Button(Unit):

    def __init__(self,name):
        self.name=name
        self.isPressed=False
        # 按钮图片
        super().__init__(button_p_img)
        self.button_p_img=button_p_img
        self.button_nor_img=button_nor_img
        # 字体图片
        if name=='退出游戏':
            self.sel_img=quit_sel_img
            self.nor_img=quit_nor_img
        else:
            self.sel_img=restart_sel_img
            self.nor_img=restart_nor_img
        # 字体矩形
        self.font_rect=self.sel_img.get_rect()
        # 按钮位置
        self.rect.centerx= SCREEN_RECT.centerx
        if name=='退出游戏':
            self.rect.centery=SCREEN_RECT.centery-40
        else:
            self.rect.centery=SCREEN_RECT.centery+40
        # 字体位置
        self.font_rect.centerx=self.rect.centerx
        self.font_rect.centery=self.rect.centery

    def draw(self,screen):
        # 先绘制按钮再绘制字体
        if self.isPressed:
            screen.blit(self.button_p_img,self.rect)
            screen.blit(self.sel_img,self.font_rect)
        else:
            screen.blit(self.button_nor_img, self.rect)
            screen.blit(self.nor_img, self.font_rect)

class Author_BG(Unit):
    def __init__(self):
        super().__init__(author_bg_img)

class Author(Unit):
    def __init__(self):
        super().__init__(author_img)
        self.rect.right=SCREEN_RECT.right-10
        self.rect.top=SCREEN_RECT.top+10+60+60+60
        self.isPressed=False

    def update(self):
        if self.isPressed:
            self.image=author_pressed_img
        else:
            self.image = author_img