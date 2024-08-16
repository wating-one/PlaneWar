import queue

from sprites.base import *
from constant import *

bullet1_img = pygame.image.load(BASE_DIR + 'image/bullet1.png')
bullet2_img = pygame.image.load(BASE_DIR + 'image/bullet2.png')
bullet3_img = pygame.image.load(BASE_DIR + 'image/bullet3.png')


class Bullet(GameSprite):
    cnt = 0
    """子弹精灵"""

    def __init__(self, atk=1):
        # 调用父类方法
        super().__init__(bullet1_img, BULLET_SPEED)
        self.atk = atk

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()
        if self.atk < ADVANCED_ATK:
            self.image = bullet1_img
        elif self.atk < FINAL_ATK:
            self.image = bullet2_img
        else:
            self.image = bullet3_img

    def kill(self):
        super().kill()
        bulletpool.put(self)


class BulletPool():
    def __init__(self):
        self.__pool = queue.Queue(BULLET_NUM)
        for i in range(BULLET_NUM):
            self.__pool.put(Bullet(1))

    def get(self, atk):
        if self.__pool.empty():
            return Bullet(atk)
        else:
            bullet = self.__pool.get()
            bullet.atk = atk
            return bullet

    def put(self, bullet):
        if not self.__pool.full():
            self.__pool.put(bullet)

bulletpool = BulletPool()
if __name__ == "__main__":
    Bullet()
