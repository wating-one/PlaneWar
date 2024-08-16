from sprites.base import *
from constant import *

background_img=pygame.image.load(BASE_DIR+'image/background.png')
class Background(GameSprite):
    """游戏背景"""
    def __init__(self,is_alt=False):
        super().__init__(background_img)
        if is_alt:
            self.rect.y=-self.rect.height
    def update(self):
        super().update()
        if self.rect.y>=SCREEN_RECT.height:
            self.rect.y=-self.rect.height