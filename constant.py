import os
import sys

import pygame
# 根路径
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))+'/'

# screen
SCREEN_RECT=pygame.Rect(0,0,400,700)
FRAME_PER_SEC=60
# speed
HERO_SPEED=8
SMALL_SPEED=[2,3,5]
MID_SPEED=[1,2,4]
BIG_SPEED=[1,2,2]
BULLET_SPEED=-12
SUPPLY_SPEED=4

# enemy
SMALL_BLOOD=[4,10,20]
MID_BLOOD=[16,32,60]
BIG_BLOOD=[50,100,200]
HIT_TIME=12

# 子弹的伤害
NORMAL_ATK=1
ADVANCED_ATK=2
FINAL_ATK=3

# 血条宽度
BLOOD_BAR_WIDTH=4

# 创建供给时间
SUPPLY_TIME=1*1000

# 标志
SUPPLY_MASK=pygame.USEREVENT

# 无敌时间
INVINCIBILITY_TIME=120

# score
BULLET_SCORE=200
BOMB_SCORE=300
SMALL_SCORE=100
MID_SCORE=500
BIG_SCORE=2000
SMALL_EXTRA=20
MID_EXTRA=100
BIG_EXTRA=300

# 回收池容量
BULLET_NUM=500
SMALL_NUM=100
MID_NUM=100
BIG_NUM=100