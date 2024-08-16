from sprites.base import *
from constant import *
import random

bomb_supply_img=pygame.image.load(BASE_DIR+'image/bomb_supply.png')
bullet_supply_path=pygame.image.load(BASE_DIR+'image/bullet_supply.png')
class Supply(GameSprite):
    def __init__(self,img,name):
        super().__init__(img,SUPPLY_SPEED)
        self.name=name
        self.active=True
        self.rect.x=random.randint(0,SCREEN_RECT.width-self.rect.width)
        self.rect.bottom=random.randint(-SCREEN_RECT.height,0)

    def update(self):
        if self.active:
            super().update()
            if self.rect.y > SCREEN_RECT.height:
                self.kill()
        else:
            self.kill()

    def failure(self):
        self.active=False

class Bomb_Supply(Supply):
    def __init__(self):
        super().__init__(bomb_supply_img,'bomb')

class Bullet_Supply(Supply):
    def __init__(self):
        super().__init__(bullet_supply_path,'bullet')