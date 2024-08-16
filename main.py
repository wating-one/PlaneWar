import configparser
import sys
import traceback
import random
import json

import pygame

from constant import *
from sprites.hero import *
from sprites.background import *
from sprites.enemy import *
from sprites.unit import *
from sprites.supply import *

BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
icon = pygame.image.load(BASE_DIR+'image/icon.png')
level_path = BASE_DIR+"levels.json"
config_path = BASE_DIR+'config.ini'


# TODO:音效补全
class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        # 游戏窗口初始化
        self.__init_frame()
        # 载入游戏关卡数据
        self.__load()
        # 3.调用私有方法实现精灵组的创建
        self.__create_sprite_group()
        # 创建重复使用精灵
        self.__once_create_sprites()
        # 初始化音乐
        self.__init_music()
        # 初始化字体
        self.__init_font()

    def __init_frame(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('PlaneWar')
        # 设置游戏图标
        pygame.display.set_icon(icon)
        # 1.创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建游戏的时钟
        self.clock = pygame.time.Clock()

    def __init_music(self):
        pygame.mixer.music.load(BASE_DIR+'sound/game_music.wav')
        # 子弹音效
        self.bullet_sound = pygame.mixer.Sound(BASE_DIR+'sound/bullet.wav')
        # 使用炸弹音效
        self.bomb_sound = pygame.mixer.Sound(BASE_DIR+'sound/use_bomb.wav')
        # 获取炸弹音效
        self.get_bomb_sound = pygame.mixer.Sound(BASE_DIR+'sound/get_bomb.wav')
        # 获取子弹音效
        self.get_bullet_sound = pygame.mixer.Sound(BASE_DIR+'sound/get_double_laser.wav')
        # 大飞机出场音效
        self.enemy3_fly_sound = pygame.mixer.Sound(BASE_DIR+'sound/big_plane_flying.wav')
        # 小飞机死亡音效
        self.enemy1_down_sound = pygame.mixer.Sound(BASE_DIR+'sound/enemy0_down.wav')
        # 中飞机死亡音效
        self.enemy2_down_sound = pygame.mixer.Sound(BASE_DIR+'sound/enemy1_down.wav')
        # 大飞机死亡音效
        self.enemy3_down_sound = pygame.mixer.Sound(BASE_DIR+'sound/enemy2_down.wav')
        # 游戏结束音效
        self.game_over_sound = pygame.mixer.Sound(BASE_DIR+'sound/game_over.wav')
        # 按钮音效
        self.button_sound= pygame.mixer.Sound(BASE_DIR+'sound/button.wav')
        # 我们俩MP3
        self.author_bgm_sound= pygame.mixer.Sound(BASE_DIR+'sound/我们俩.wav')
        pygame.mixer.music.play(-1)
    def __init_prams(self):
        """
        游戏参数初始化
        :return:
        """
        # 初始化游戏关卡
        self.level = 0
        # 初始化游戏分数
        self.score = 0
        # 初始化炸弹数量
        self.bomb.num=0
        # 初始化游戏状态
        self.is_pause = False
        # 初始化供给定时器
        pygame.time.set_timer(SUPPLY_MASK, 0)
        # 重置暂停按键
        self.pause.isPaused=False
        self.num=0

    def __init_font(self):
        # 初始化分数字体
        self.score_font = pygame.font.Font('font/Marker Felt.ttf', 30)
        # 初始化炸弹数量字体
        self.bomb_font = pygame.font.Font('font/Marker Felt.ttf', 50)
        # 初始化音量字体
        self.volume_font = pygame.font.Font('font/字魂50号-白鸽天行体.ttf', 40)
        # 初始化游戏结束画面
        self.game_over_font=pygame.font.Font('font/Marker Felt.ttf', 55)

    def start_game(self):
        # 初始化游戏参数
        self.__init_prams()

        # 创建精灵
        self.__recreate_sprites()

        # 设置音乐
        if self.silent.isSilent:
            self.__set_music(0)
        else:
            self.__set_music(1)
            pygame.mixer.music.unpause()
        # 4.设置定时器事件-创建供给
        pygame.time.set_timer(SUPPLY_MASK, SUPPLY_TIME)

        while True:
            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # 播放音乐
            self.__play_music()
            # 更新显示
            self.__update_sprites()
            # 下一关
            self.__up_level()
    def __create_sprite_group(self):
        # 创建背景精灵和精灵组
        self.back_group = pygame.sprite.Group()
        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()
        self.small_group = pygame.sprite.Group()
        self.mid_group = pygame.sprite.Group()
        self.big_group = pygame.sprite.Group()
        # 创建英雄的精灵和精灵组
        self.hero_group = pygame.sprite.Group()
        # 创建游戏组件组
        self.unit_game_group = pygame.sprite.Group()
        # 创建补给精灵组
        self.supply_group = pygame.sprite.Group()
        # 创建生命图精灵组
        self.life_group = pygame.sprite.Group()
        # 创建设置界面各组件组
        self.unit_setting_group = pygame.sprite.Group()
        # 创建暂停界面各组件组
        self.unit_pause_group = pygame.sprite.Group()

    def __recreate_sprites(self):
        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group.add(self.hero)
        # 创建生命图精灵
        for i in range(self.hero.rank):
            self.life_group.add(Life())
        # self.cheat()
        # 创建敌机精灵
        self.__add_enemies()
    def __once_create_sprites(self):
        # 创建背景精灵和精灵组
        bgl1 = Background()
        bgl2 = Background(True)
        # 创建静态背景
        self.bg = Background()
        self.bg.speed = 0
        # 创建作者界面背景
        self.author_bg=Author_BG()
        self.back_group.add(bgl1)
        self.back_group.add(bgl2)
        # 创建作者组件
        self.author=Author()
        self.unit_game_group.add(self.author)
        # 创建游戏组件
        self.pause = Pause()
        self.bomb = Bomb()
        self.silent = Silent()
        self.setting = Setting()
        self.unit_game_group.add(self.pause)
        self.unit_game_group.add(self.bomb)
        self.unit_game_group.add(self.silent)
        self.unit_game_group.add(self.setting)
        # 创建音量条
        self.volume_bar_bgm = Volume()
        self.volume_bar_music = Volume(True)
        # 创建音量杆
        self.volume_pole_bgm = Volume_Pole(self.volume_bar_bgm, self.bgm_remain)
        self.volume_pole_music = Volume_Pole(self.volume_bar_music, self.music_remain, True)
        self.unit_setting_group.add(self.volume_bar_bgm)
        self.unit_setting_group.add(self.volume_bar_music)
        self.unit_setting_group.add(self.volume_pole_bgm)
        self.unit_setting_group.add(self.volume_pole_music)
        # 创建暂停界面各组件
        self.button_quit=Button('退出游戏')
        self.button_restart=Button('重新开始')
        self.unit_pause_group.add(self.pause)
        self.unit_pause_group.add(self.bomb)

    def __event_handler(self):
        keys_pressed = pygame.key.get_pressed()
        # 控制方向
        if self.hero.active:
            dir = [0, 0]
            if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
                dir[1] -= 1
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                dir[1] += 1
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                dir[0] -= 1
            if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                dir[0] += 1
            self.hero.dir = dir
            # 控制开火
            if keys_pressed[pygame.K_SPACE]:
                self.hero.fire()

        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                self.__exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 判断是否按下暂停
                if self.pause.isPressed:
                    self.__into_pause()
                # 判断是否按下静音
                if self.silent.isPressed:
                    self.__pressed_silent()
                # 判断是否按下设置键
                if self.setting.isPressed:
                    self.__into_setting()
                # 判断是否按下作者键
                if self.author.isPressed:
                    self.__into_author()

            elif event.type == pygame.MOUSEMOTION:
                # 判断是否鼠标悬停在暂停键
                self.pause.isPressed = self.pause.rect.collidepoint(event.pos)
                # 判断是否鼠标悬停在静音键
                self.silent.isPressed = self.silent.rect.collidepoint(event.pos)
                # 判断是否鼠标悬停在设置键
                self.setting.isPressed = self.setting.rect.collidepoint(event.pos)
                # 判断是否鼠标悬停在作者键
                self.author.isPressed = self.author.rect.collidepoint(event.pos)
            # 键盘按下事件
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.__use_bomb()
                elif event.key==pygame.K_ESCAPE:
                    self.__into_pause()
                elif event.key==pygame.K_m:
                    self.__pressed_silent()
                elif event.key==pygame.K_q:
                    self.__into_setting()
                elif event.key==pygame.K_i:
                    self.__into_author()

            # 供给时间到
            elif event.type == SUPPLY_MASK:
                self.__suppy()
            # elif event.type==CREATE_ENEMY_EVENT:
            #     # 创建敌机精灵
            #     enemy=Enemy()
            #     # 将敌机精灵加入组
            #     self.enemy_group.add(enemy)

    def __check_collide(self):
        # pygame.sprite.groupcollide(self.hero.bullet_Group,self.enemy_group,True,True)
        for enemy in self.enemy_group:
            for bullet in self.hero.bullet_Group:
                if pygame.sprite.collide_mask(bullet, enemy):
                    bullet.kill()
                    self.score += enemy.injure(self.hero.atk)
            if enemy.active and self.hero.active and pygame.sprite.collide_mask(self.hero, enemy):
                self.__hero_injure()
        for supply in self.supply_group:
            if self.hero.active and pygame.sprite.collide_mask(supply, self.hero):
                if supply.name == 'bomb':
                    self.__get_bomb()
                else:
                    self.__get_bullet()
                supply.failure()
                # PlaneGame.__game_over()
        # enemies=pygame.sprite.spritecollide(self.hero,self.enemy_group,False,pygame.sprite.collide_mask) # 第三个参数：是否销毁组，第四个参数，碰撞类型
        # 类内需要有self.mask=pygame.mask.from_surface(self.image)
        # if enemies:
        #     self.hero.kill()
        #     PlaneGame.__game_over()

    def __pressed_silent(self):
        self.silent.isSilent = not self.silent.isSilent
        if self.silent.isSilent:
            self.__set_music(0)
        else:
            self.__set_music(1)
            pygame.mixer.music.unpause()
            # 不清楚为什么会暂停
    def __update_sprites(self):
        # 更新
        # 背景更新
        self.back_group.update()
        # 供给更新
        self.supply_group.update()
        # 敌机更新
        self.enemy_group.update()
        # 英雄更新
        self.hero_group.update()
        # 子弹更新
        self.hero.bullet_Group.update()
        # 组件更新
        self.unit_game_group.update()

        # 绘制
        # 背景绘制
        self.back_group.draw(self.screen)
        # 供给绘制
        self.supply_group.draw(self.screen)
        # 敌机绘制
        self.big_group.draw(self.screen)
        self.small_group.draw(self.screen)
        self.mid_group.draw(self.screen)
        # 英雄绘制
        self.hero_group.draw(self.screen)
        # 子弹绘制
        self.hero.bullet_Group.draw(self.screen)
        # 绘制血条
        self.__draw_bloodbar()
        # 绘制分数
        self.__draw_score()
        # 绘制组件
        self.unit_game_group.draw(self.screen)
        # 绘制炸弹数量
        self.__draw_bomb_num()
        # 绘制生命图
        self.life_group.draw(self.screen)

        pygame.display.update()
        # 是否游戏结束
        if self.hero.death>=40:
            self.__game_over()

    def __into_setting(self):
        bgm_text = self.volume_font.render(f'背景音乐: ', True, BLACK)
        music_text = self.volume_font.render(f'游戏音效: ', True, BLACK)
        width = bgm_text.get_rect().width
        height = bgm_text.get_rect().height
        flag_bgm, flag_music = False, False
        while True:
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            for event in pygame.event.get():
                # 退出游戏
                if event.type == pygame.QUIT:
                    self.__exit_game()
                # 退出设置
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key==pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    flag_bgm = self.volume_pole_bgm.rect.collidepoint(event.pos)
                    flag_music = self.volume_pole_music.rect.collidepoint(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    flag_bgm = False
                    flag_music = False
                elif event.type==pygame.MOUSEMOTION:
                    if flag_bgm:
                        self.__follow(event,self.volume_pole_bgm,True)
                    if flag_music:
                        self.__follow(event,self.volume_pole_music,False)
            # 更新状态
            # 绘制
            # 绘制背景
            self.screen.blit(self.bg.image, self.bg.rect)
            # 绘制音量条
            self.screen.blit(self.volume_bar_bgm.image, self.volume_bar_bgm.rect)
            self.screen.blit(self.volume_bar_music.image, self.volume_bar_music.rect)
            # 绘制音量杆
            self.screen.blit(self.volume_pole_bgm.image, self.volume_pole_bgm.rect)
            self.screen.blit(self.volume_pole_music.image, self.volume_pole_music.rect)
            # 绘制字体
            self.screen.blit(bgm_text,
                             (self.volume_bar_bgm.rect.x - width, self.volume_bar_bgm.rect.centery - height / 2))
            self.screen.blit(music_text,
                             (self.volume_bar_music.rect.x - width, self.volume_bar_music.rect.centery - height / 2))

            pygame.display.flip()

    def __into_pause(self):
        self.__to_pause()
        while True:
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__exit_game()
                elif event.type == pygame.MOUSEMOTION:
                    # 判断是否鼠标悬停在暂停键
                    self.pause.isPressed = self.pause.rect.collidepoint(event.pos)
                    # 判断是否鼠标悬停在退出游戏键
                    self.button_quit.isPressed = self.button_quit.rect.collidepoint(event.pos)
                    # 判断是否鼠标悬停在重新开始键
                    self.button_restart.isPressed = self.button_restart.rect.collidepoint(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 判断是否按下暂停
                    if self.pause.isPressed:
                        self.__to_resume_pause()
                        return
                    # 判断是否按下退出游戏
                    if self.button_quit.isPressed:
                        self.button_sound.play()
                        self.__exit_game()
                    # 判断是否重新开始
                    if self.button_restart.isPressed:
                        self.button_sound.play()
                        self.__reset()
                        return
                elif event.type==pygame.KEYDOWN:
                    # 返回
                    if event.key == pygame.K_ESCAPE:
                        self.__to_resume_pause()
                        return
                    # 重新开始
                    elif event.key==pygame.K_SPACE:
                        self.__reset()
                        return
                    elif event.key==pygame.K_h:
                        self.__exit_game()

            # 更新
            self.unit_pause_group.update()
            # 绘制
            # 绘制静态背景
            self.screen.blit(self.bg.image, self.bg.rect)
            # 绘制各组件
            self.unit_pause_group.draw(self.screen)
            # 绘制按钮
            self.button_quit.draw(self.screen)
            self.button_restart.draw(self.screen)
            # 绘制生命图
            self.life_group.draw(self.screen)
            # 绘制字体
            self.__draw_score()
            self.__draw_bomb_num()
            pygame.display.update()
    def __up_level(self): #TODO
        if self.score > self.level_list[self.level]['score']:
            if self.level < self.max_level:
                self.level += 1
                self.__add_enemies()
            else:
                self.__game_over()

    def __into_author(self):
        # 暂停音乐
        pygame.mixer.music.pause()
        pygame.mixer.pause()
        self.author_bgm_sound.play(-1)
        while True:
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i or event.key==pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        self.author_bgm_sound.stop()
                        return
            # 绘制
            self.screen.blit(self.author_bg.image, self.author_bg.rect)
            pygame.display.flip()
    def __game_over(self):
        history_socre=self.config.get('history','score')
        # 历史记录
        history_text=self.game_over_font.render('your history is',True,BLACK)
        rect1=history_text.get_rect()
        rect1.centerx=SCREEN_RECT.centerx
        rect1.centery=SCREEN_RECT.height/4
        history_num=self.game_over_font.render(f'{history_socre}',True,BLACK)
        rect2=history_num.get_rect()
        rect2.centerx=SCREEN_RECT.centerx
        rect2.top=rect1.bottom+10
        # 最终得分
        finally_text=self.game_over_font.render('your final score is',True,BLACK)
        rect3=finally_text.get_rect()
        rect3.centerx = SCREEN_RECT.centerx
        rect3.top= rect2.bottom+10
        finally_num=self.game_over_font.render(f'{self.score}',True,BLACK)
        rect4=finally_num.get_rect()
        rect4.centerx = SCREEN_RECT.centerx
        rect4.top=rect3.bottom+10
        if self.score>int(self.config.get('history','score')):
            self.config.set('history','score',str(self.score))
        while True:
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__exit_game()
                elif event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.__reset()
                        return
                    if event.key==pygame.K_h:
                        self.__exit_game()
            # 绘制
            # 绘制静态背景
            self.screen.blit(self.bg.image, self.bg.rect)
            # 绘制历史分数
            self.screen.blit(history_text, rect1)
            self.screen.blit(history_num, rect2)
            # 绘制最终分数
            self.screen.blit(finally_text, rect3)
            self.screen.blit(finally_num, rect4)
            pygame.display.flip()

    def __exit_game(self):
        # 更新历史
        with open(config_path,'w') as f:
            self.config.write(fp=f)
        pygame.quit()
        sys.exit()
    def __reset(self):
        # 清空精灵组
        self.__group_remove()
        # 开始游戏
        self.start_game()

    def __load(self):
        # 载入关卡数据
        with open(level_path, "r", encoding="utf-8") as f:
            self.level_list = json.load(f)
            self.max_level = len(self.level_list) - 1
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')
        # 两种最大音量
        self.volume1 = float(self.config.get('volume', 'volume1'))
        self.volume2 = float(self.config.get('volume', 'volume2'))
        # 背景音乐和游戏音效
        self.music_remain = float(self.config.get('volume', 'remain'))
        self.bgm_remain = float(self.config.get('volume', 'remain'))

    def __play_music(self):# TODO
        # 管理出场音乐
        flag = False
        for enemy in self.big_group:
            if enemy.rect.bottom > -50 and not enemy.play_entry:
                self.enemy3_fly_sound.play(-1)
                enemy.play_entry = True
                flag = True
            if enemy.active:
                flag = True
        if not flag:
            self.enemy3_fly_sound.stop()

        # 播放击毁音效
        self.__play_enemy_sound(self.small_group, self.enemy1_down_sound)
        self.__play_enemy_sound(self.mid_group, self.enemy2_down_sound)
        self.__play_enemy_sound(self.big_group, self.enemy3_down_sound)

    def __suppy(self):
        if random.choice([True, False]):
            self.supply_group.add(Bomb_Supply())
        else:
            self.supply_group.add(Bullet_Supply())

    def __hero_injure(self):
        if self.hero.active and self.hero.invincibility == 0:
            self.hero.injure()
            self.game_over_sound.play()
            Life.remove()

    def __to_pause(self):
        self.pause.isPaused=True
        # 暂停定时器
        pygame.time.set_timer(SUPPLY_MASK, 0)
        # 暂停音乐
        pygame.mixer.music.pause()
        pygame.mixer.pause()

    def __to_resume_pause(self):
        self.pause.isPaused=False
        # 恢复定时器
        pygame.time.set_timer(SUPPLY_MASK, SUPPLY_TIME)
        # 恢复音乐
        pygame.mixer.music.unpause()
        pygame.mixer.unpause()

    def __set_music(self, flag): #TODO
        """
        :param flag: 0:静音 or 1:播放
        :return:
        """
        v1, v2, v3 = flag * self.bgm_remain * self.volume1, flag * self.music_remain * self.volume1, flag * self.music_remain * self.volume2
        pygame.mixer.music.set_volume(v1)
        self.bullet_sound.set_volume(v2)
        self.bomb_sound.set_volume(v2)
        self.get_bomb_sound.set_volume(v2)
        self.get_bullet_sound.set_volume(v2)
        self.enemy3_fly_sound.set_volume(v2)
        self.enemy1_down_sound.set_volume(v2)
        self.enemy2_down_sound.set_volume(v2)
        self.enemy3_down_sound.set_volume(v3)
        self.game_over_sound.set_volume(v2)
        self.bullet_sound.set_volume(v2)
        self.author_bgm_sound.set_volume(v3)
        self.button_sound.set_volume(v2)
    def __get_bullet(self):
        self.get_bullet_sound.play()
        self.score+=BULLET_SCORE
        if self.hero.rank < 4:
            self.hero.uprank()
            self.life_group.add(Life())

    def __get_bomb(self):
        self.get_bomb_sound.play()
        self.score+=BOMB_SCORE
        if self.bomb.num < 3:
            self.bomb.num += 1

    def __use_bomb(self):
        if self.bomb.num > 0:
            self.bomb_sound.play()
            self.bomb.num -= 1
            for enemy in self.enemy_group:
                if SCREEN_RECT.colliderect(enemy.rect):
                    enemy.blood = 0
                    enemy.active = False
                    self.score+=enemy.score

    def __play_enemy_sound(self, group, sound):
        for enemy in group:
            if not enemy.active and enemy.death == 1:  # 播放一次
                sound.play()

    def __draw_bloodbar(self):
        for enemy in self.enemy_group:
            # 血槽-黑色
            pygame.draw.line(self.screen, BLACK, (enemy.rect.x, enemy.rect.y - 5), (enemy.rect.right, enemy.rect.y - 5),
                             BLOOD_BAR_WIDTH)
            blood_remain = enemy.blood / enemy.max_blood
            if blood_remain > 0.5:
                # 高血量-紫色
                pygame.draw.line(self.screen, PURPLE, (enemy.rect.x, enemy.rect.y - 5),
                                 (enemy.rect.x + enemy.rect.width * blood_remain, enemy.rect.y - 5), BLOOD_BAR_WIDTH)
            else:
                # 低血量-红色
                pygame.draw.line(self.screen, RED, (enemy.rect.x, enemy.rect.y - 5),
                                 (enemy.rect.x + enemy.rect.width * blood_remain, enemy.rect.y - 5), BLOOD_BAR_WIDTH)

    def __draw_score(self):
        score_text = self.score_font.render(f'Score: {self.score}', True, WHITE)  # True：打开抗锯齿， WHITE:文本颜色
        self.screen.blit(score_text, (10, 10))
        score_text = self.score_font.render(f'Level: {self.level+1}', True, WHITE)  # True：打开抗锯齿， WHITE:文本颜色
        self.screen.blit(score_text, (10, 50))

    # 绘制炸弹数量
    def __draw_bomb_num(self):
        bomb_num_text = self.bomb_font.render(f'X {self.bomb.num}', True, WHITE)
        self.screen.blit(bomb_num_text,
                         (20 + self.bomb.rect.width, SCREEN_RECT.height - 5 - bomb_num_text.get_rect().height))

    def __add_enemies(self):
        num1, num2, num3 = self.level_list[self.level]['num1'], self.level_list[self.level]['num2'], \
        self.level_list[self.level]['num3']
        rank1,rank2,rank3= self.level_list[self.level]['rank1'], self.level_list[self.level]['rank2'], \
        self.level_list[self.level]['rank3']
        self.__add_small_enemies(self.enemy_group, self.small_group, num1,rank1)
        self.__add_mid_enemies(self.enemy_group, self.mid_group, num2,rank2)
        self.__add_big_enemies(self.enemy_group, self.big_group, num3,rank3)


    def __add_small_enemies(self, group1, group2, num,rank):
        for i in range(num):
            enemy = SmallEnemyPool.get(rank)
            group1.add(enemy)
            group2.add(enemy)

    def __add_mid_enemies(self, group1, group2, num,rank):
        for i in range(num):
            enemy = MidEnemyPool.get(rank)
            group1.add(enemy)
            group2.add(enemy)

    def __add_big_enemies(self, group1, group2, num,rank):
        for i in range(num):
            enemy = BigEnemyPool.get(rank)
            group1.add(enemy)
            group2.add(enemy)

    # 音量杆跟随鼠标
    def __follow(self,event ,pole,flag):
        pos = event.pos
        # if pos[0] in range(self.volume_bar_bgm.rect.left,self.volume_bar_bgm.rect.right):
        #     pole.rect.x=pos[0]
        # 调整音量杆位置
        pole.rect.x = pos[0]
        if pole.rect.x<self.volume_bar_bgm.rect.left:
            pole.rect.x=self.volume_bar_bgm.rect.left
        if pole.rect.x>self.volume_bar_bgm.rect.right:
            pole.rect.x=self.volume_bar_bgm.rect.right
        # 同步音量
        if flag:
            self.bgm_remain = (pole.rect.x - self.volume_bar_bgm.rect.left) / self.volume_bar_bgm.rect.width
        else:
            self.music_remain=(pole.rect.x-self.volume_bar_music.rect.left)/self.volume_bar_music.rect.width
        self.__set_music(1)

    def __group_remove(self):
        # 敌机的精灵组
        self.enemy_group.empty()
        self.small_group.empty()
        self.mid_group.empty()
        self.big_group.empty()
        # 英雄的精灵和精灵组
        self.hero_group.empty()
        self.hero=None
        # 补给精灵组
        self.supply_group.empty()
        # 生命图精灵组
        while self.life_group.sprites():
            Life.remove()

    def __cheat(self):
        for i in range(3):
            self.hero.uprank()
        self.bomb.num=1000
        # self.hero.invincibility=-1
        self.level=9
        self.score=0
if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()
    #启动游戏
    game.start_game()
