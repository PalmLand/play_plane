# -*- coding: utf-8 -*-
#导入pygame库
import random
import pygame
#向sys模块借一个exit函数用来退出程序
from sys import exit

#定义一个Bullet类，封装子弹相关的数据和方法
class Bullet:
    def __init__(self):
        #初始化成员变量，x，y，image
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.png').convert_alpha()
        #默认不激活
        self.active = False
    def move(self):
        # 激活状态下，向上移动
        if self.active:
            self.y -= 3
        # 当飞出屏幕，就设为不激活
        if self.y < 0:
            self.active = False
    def restart(self):
        # 重置子弹位置
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        # 激活子弹
        self.active = True

#定义一个Enemy类
class Enemy:
    #重置敌机位置和速度
    def restart(self):
        self.x = random.randint(30,450)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 0.1
    def __init__(self):
        #初始化
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()
    def move(self):
        if self.y < 800:
            #向下移动
            self.y += self.speed
        else:
            self.restart()

#定义一个Plane类
class Plane:
    def restart(self):
        self.x = 200
        self.y = 600

    def __init__(self):
        self.restart()
        self.image = pygame.image.load('plane.png').convert_alpha()

    def move(self):
        x, y = pygame.mouse.get_pos()
        x -= self.image.get_width() / 2
        y -= self.image.get_height() / 2
        self.x = x
        self.y = y

# 检测敌机与本地是否相撞
def checkCrash(enemy, plane):
    if (plane.x + 0.7 * plane.image.get_width() > enemy.x) and (
                    plane.x + 0.3 * plane.image.get_width() < enemy.x + enemy.image.get_width()) and (
                    plane.y + 0.7 * plane.image.get_height() > enemy.y) and (
                    plane.y + 0.3 * plane.image.get_width() < enemy.y + enemy.image.get_height()
    ):
        return True
    return False
#碰撞检测
def checkHit(enemy, bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) and (
        bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()
    ):
        enemy.restart()
        bullet.active = False
        #增加返回值
        return True
    return False

#初始化pygame,为使用硬件做准备
pygame.init()
#创建了一个窗口,窗口大小和背景图片大小一样
screen = pygame.display.set_mode((480, 800), 0, 32)
#设置窗口标题
pygame.display.set_caption("Hello, pygame!")
#加载并转换图像
background = pygame.image.load('background.png').convert()
#创建Plane对象
plane = Plane()

#创建子弹的list
bullets = []
#向list中添加5发子弹
for i in range(5):
    bullets.append(Bullet())
#子弹总数
count_b=len(bullets)
#即将激活的子弹序号
index_b = 0
#发射子弹的间隔
interval_b = 0
#创建敌机的list
enemies = []
#向list中添加5架敌机
for i in range(5):
    enemies.append(Enemy())
#增加记录游戏是否结束的变量
gameover = False
#分数
score = 0
#用以显示文字的font变量
font = pygame.font.Font(None, 32)

#游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #接收到退出事件后退出程序
            pygame.quit()
            exit()
        # 判断在gameover状态下点击了鼠标
        if gameover and event.type == pygame.MOUSEBUTTONUP:
            # 重置游戏
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            gameover = False
    screen.blit(background, (0, 0))

    if not gameover:
        # 发射间隔递减
        interval_b -= 1
        # 当间隔小于0时，激活一发子弹
        if interval_b < 0:
            bullets[index_b].restart()
            # 重置间隔时间
            interval_b = 200
            #子弹序号周期性递增
            index_b = (index_b + 1) % count_b
        #判断每个子弹的状态
        for b in bullets:
            #处于激活后状态的子弹，移动位置并绘制
            if b.active:
                for e in enemies:
                    # 击中敌机后，分数加100
                    if checkHit(e, b):
                        score += 100
                b.move()
                screen.blit(b.image,(b.x,b.y))
        for e in enemies:
            # 如果撞上敌机，设gameover为True
            if checkCrash(e, plane):
                gameover = True
            e.move()
            screen.blit(e.image, (e.x, e.y))
        # 检测本体的运动
        plane.move()
        screen.blit(plane.image, (plane.x, plane.y))
        # 在屏幕左上角显示分数
        text = font.render("Socre: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (0, 0))
    else:
        # 在屏幕中央显示分数
        text = font.render("Socre: %d" % score, 1, (0, 0, 0))
        screen.blit(text, (190, 400))
        pass
    # 刷新一下画面
    pygame.display.update()