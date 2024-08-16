import queue
from sprites.base import *
import random
from constant import *


# 飞机图片
small_enemy_img=[]
mid_enemy_img=[]
big_enemy_img=[]
# 中弹图片
mid_hit_img=[]
big_hit_img=[]
for i in range(3):
    small_enemy_img.append(pygame.image.load(BASE_DIR+'image/enemy0_' + str(i) + '.png'))
    mid_enemy_img.append(pygame.image.load(BASE_DIR+'image/enemy1_' + str(i) + '.png'))
    big_enemy_img.append([pygame.image.load(BASE_DIR+'image/enemy2_' + str(i) + '.png'),pygame.image.load(BASE_DIR+'image/enemy2_' + str(i) + '_n2.png')])
    mid_hit_img.append(pygame.image.load(BASE_DIR+'image/enemy1_' + str(i) + '_hit.png'))
    big_hit_img.append(pygame.image.load(BASE_DIR+'image/enemy2_' + str(i) + '_hit.png'))

small_down_img=[]
mid_down_img=[]
big_down_img=[]
for j in range(3):
    small_cur=[]
    mid_cur=[]
    big_cur=[]
    for i in range(1,7):
        big_cur.append(pygame.image.load(BASE_DIR+'image/enemy2_' + str(j) + '_down' + str(i) + '.png'))
        if i<=4:
            small_cur.append(pygame.image.load(BASE_DIR+'image/enemy0_' + str(j) + '_down'+str(i)+'.png'))
            mid_cur.append(pygame.image.load(BASE_DIR+'image/enemy1_' + str(j) + '_down'+str(i)+'.png'))
    small_down_img.append(small_cur)
    mid_down_img.append(mid_cur)
    big_down_img.append(big_cur)
class Enemy(GameSprite):
    def __init__(self,enemy_img,speed,blood,score,extra):
        # 1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__(enemy_img, speed)
        self.blood=blood
        self.max_blood = blood
        self.score=score
        self.active=True
        self.hit=False
        self.death=0
        self.hit_time=-1
        self.first=True
        self.extra=extra

    def update(self):
        # 1.调用父类方法，保持垂直方向的飞行
        super().update()
        # 2.判断是否飞出屏幕，若是则删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # 飞出屏幕外则重新进入屏幕
            self.back()
    def injure(self,atk):
        if self.blood>0:
            self.blood-=atk
            if self.blood<=0:
                self.blood=0
                self.active=False
                if self.first:
                    return self.score+self.extra
                else:
                    return self.score
            else:
                self.hit=True
        return 1

    def back(self):
        self.first=False

    def reset(self):
        self.first=True
        self.active = True
        self.hit = False
        self.death = 0
        self.hit_time = -1


class SmallEnemy(Enemy):
    def __init__(self,rank):
        self.rank=rank
        # 1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__(small_enemy_img[rank], SMALL_SPEED[self.rank],SMALL_BLOOD[self.rank],SMALL_SCORE,SMALL_EXTRA)
        # 3.指定敌机的初始随机位置
        self.rect.bottom = random.randint(-10 * SCREEN_RECT.height, 0)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
    def update(self):
        if self.active:
            super().update()
        else:
            self.image=small_down_img[self.rank][self.death//5%4]
            self.death+=1
            if self.death>=20:
                self.kill()
    def reset(self,rank):
        self.back()
        super().reset()
        self.rank = rank
        self.speed=SMALL_SPEED[self.rank]
        self.blood=SMALL_BLOOD[self.rank]
        self.max_blood = SMALL_BLOOD[self.rank]
        self.image=small_enemy_img[self.rank]


    def back(self):
        super().back()
        self.blood = self.max_blood
        self.rect.bottom = random.randint(-5 * SCREEN_RECT.height, 0)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def kill(self):
        super().kill()
        SmallEnemyPool.put(self)


class MidEnemy(Enemy):
    def __init__(self,rank):
        self.rank=rank
        # 1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__(mid_enemy_img[rank], MID_SPEED[self.rank],MID_BLOOD[self.rank],MID_SCORE,MID_EXTRA)
        # 3.指定敌机的初始随机位置
        self.rect.bottom = random.randint(-10 * SCREEN_RECT.height, -SCREEN_RECT.height)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def update(self):
        if self.active:
            super().update()
            # 更新hit状态
            if self.hit:
                self.hit_time = HIT_TIME
                self.image = mid_hit_img[self.rank]
                self.hit = False
            if self.hit_time > -1:
                if self.hit_time == 0:
                    self.image =mid_enemy_img[self.rank]
                self.hit_time -= 1
        else:
            self.image = mid_down_img[self.rank][self.death // 10 % 4]
            self.death += 1
            if self.death >= 40:
                self.kill()
    def reset(self,rank):
        self.back()
        super().reset()
        self.rank = rank
        self.speed=MID_SPEED[self.rank]
        self.blood = MID_BLOOD[self.rank]
        self.max_blood=MID_BLOOD[self.rank]
        self.image = mid_enemy_img[self.rank]


    def back(self):
        super().back()
        self.blood = self.max_blood
        self.rect.bottom = random.randint(-10 * SCREEN_RECT.height, -SCREEN_RECT.height)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def kill(self):
        super().kill()
        MidEnemyPool.put(self)

class BigEnemy(Enemy):
    def __init__(self,rank):
        self.rank=rank
        # 1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__(big_enemy_img[self.rank][0], BIG_SPEED[self.rank],BIG_BLOOD[self.rank],BIG_SCORE,BIG_EXTRA)
        # 3.指定敌机的初始随机位置
        self.rect.bottom = random.randint(-15 * SCREEN_RECT.height, -5*SCREEN_RECT.height)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.index=0
        self.play_entry=False
    def update(self):
        if self.active:
            super().update()
            # 切换动态效果
            if self.hit_time==-1:
                self.index+=1
                if self.index>=20:
                    self.index=0
                self.image=big_enemy_img[self.rank][self.index//10%2]
            # 更新hit状态
            if self.hit:
                self.hit_time = HIT_TIME
                self.image = big_hit_img[self.rank]
                self.hit = False
            if self.hit_time > -1:
                if self.hit_time == 0:
                    self.image = big_enemy_img[self.rank][self.index//10%2]
                self.hit_time -= 1
        else:
            self.image = big_down_img[self.rank][self.death // 10 % 6]
            self.death += 1
            if self.death >= 60:
                self.kill()

    def reset(self,rank):
        self.back()
        super().reset()
        self.rank = rank
        self.speed=BIG_SPEED[self.rank]
        self.blood = BIG_BLOOD[self.rank]
        self.max_blood=BIG_BLOOD[self.rank]
        self.image = big_enemy_img[self.rank][0]
        self.blood=self.max_blood

    def back(self):
        super().back()
        self.blood += 50
        if self.blood > self.max_blood:
            self.blood = self.max_blood
        self.rect.bottom = random.randint(-15 * SCREEN_RECT.height, -5 * SCREEN_RECT.height)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def kill(self):
        super().kill()
        BigEnemyPool.put(self)
class SmallEnemyPool():
    __pool=queue.Queue(SMALL_NUM)
    @staticmethod
    def get(rank):
        if SmallEnemyPool.__pool.empty():
            return SmallEnemy(rank)
        else:
            enemy=SmallEnemyPool.__pool.get()
            enemy.reset(rank)
            return enemy

    @staticmethod
    def put(enemy):
        if not SmallEnemyPool.__pool.full():
            SmallEnemyPool.__pool.put(enemy)

class MidEnemyPool():
    __pool=queue.Queue(MID_NUM)
    @staticmethod
    def get(rank):
        if MidEnemyPool.__pool.empty():
            return MidEnemy(rank)
        else:
            enemy=MidEnemyPool.__pool.get()
            enemy.reset(rank)
            return enemy

    @staticmethod
    def put(enemy):
        if not MidEnemyPool.__pool.full():
            MidEnemyPool.__pool.put(enemy)
class BigEnemyPool():
    __pool=queue.Queue(BIG_NUM)
    @staticmethod
    def get(rank):
        if BigEnemyPool.__pool.empty():
            return BigEnemy(rank)
        else:
            enemy=BigEnemyPool.__pool.get()
            enemy.reset(rank)
            return enemy

    @staticmethod
    def put(enemy):
        if not BigEnemyPool.__pool.full():
            BigEnemyPool.__pool.put(enemy)
            
if __name__=='__main__':
    pass
    # e=SmallEnemy()
    # while True:
    #     e.update()