
from sprites.bullet import * # 包内必须绝对路径
from constant import *
from sprites.base import *

hero_img=[]
hero_invin_img=[]
for i in range(4):
    hero_img.append([pygame.image.load(BASE_DIR+'image/hero1_'+str(i)+'.png'),pygame.image.load(BASE_DIR+'image/hero2_'+str(i)+'.png')])
    hero_invin_img.append([pygame.image.load(BASE_DIR+'image/hero1_'+str(i)+'.png'),pygame.image.load(BASE_DIR+'image/hero3.png')])
hero_down_img=[]
for j in range(4):
    hero_cur=[]
    for i in range(1,5):
        hero_cur.append(pygame.image.load(BASE_DIR+'image/hero_'+str(j)+'_blowup_n'+str(i)+'.png'))
    hero_down_img.append(hero_cur)

offset=40
class Hero(GameSprite):
    def __init__(self):
        super().__init__(hero_img[0][0], HERO_SPEED)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 60
        self.atk=NORMAL_ATK
        self.rank=1
        self.dir = [0, 0]
        self.index = 0
        self.fireCooldown = 0
        self.bullet_Group = pygame.sprite.Group()
        self.active=True
        self.death=0
        self.fire_num=1
        self.invincibility=INVINCIBILITY_TIME

    def update(self):

        if self.active:
            self.__move()
            if self.invincibility == 0:
                self.index += 1
                if self.index >= 20:
                    self.index = 0
                self.image = hero_img[self.rank-1][self.index // 10 % 2]
            else:
                self.image = hero_invin_img[self.rank-1][self.invincibility // 8 % 2]
                self.invincibility -= 1
        else:
            self.image=hero_down_img[self.rank][self.death//10%4]
            self.death+=1
            if self.death >= 40:
                self.kill()
    def __move(self):
        self.rect.move_ip(self.dir[0] * self.speed, self.dir[1] * self.speed)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_RECT.height-60:
            self.rect.bottom = SCREEN_RECT.height-60
        if self.fireCooldown > 0:
            self.fireCooldown -= 1
    def fire(self):
        self.fire_pos_list = [
            (self.rect.centerx, self.rect.y)
            ,(self.rect.x+self.rect.width/6,self.rect.y+self.rect.height/2)
            ,(self.rect.right-self.rect.width/6,self.rect.y+self.rect.height/2)
            ,(self.rect.centerx, self.rect.y-offset)
            , (self.rect.x + self.rect.width / 6, self.rect.y + self.rect.height / 2-offset)
            , (self.rect.right - self.rect.width / 6, self.rect.y + self.rect.height / 2-offset)
        ]
        if self.fireCooldown == 0:
            for i in range(self.fire_num):
                pos=self.fire_pos_list[i]
                # bullet = BulletPool.get(self.atk)
                bullet=bulletpool.get(self.atk)
                bullet.rect.centerx = pos[0]
                bullet.rect.bottom = pos[1]
                self.bullet_Group.add(bullet)
            self.fireCooldown = 12
    def uprank(self):
        if self.rank<4:
            if self.rank==1:
                self.atk=ADVANCED_ATK
            elif self.rank==2:
                self.fire_num =3
            else:
                self.atk=FINAL_ATK
            self.rank += 1

    def injure(self):
        if self.rank==4:
            self.atk=ADVANCED_ATK
        elif self.rank==3:
            self.fire_num=1
        elif self.rank==2:
            self.atk=NORMAL_ATK
        elif self.rank==1:
            self.active=False
        self.rank-=1
        self.invincibility=INVINCIBILITY_TIME