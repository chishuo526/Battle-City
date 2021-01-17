import pygame,time,random
_display=pygame.display
COLOR_BLACK=pygame.Color(0,0,0)
COLOR_RED=pygame.Color(255,0,0)
# 主逻辑类
class MinGame():
    # 游戏主窗口
    window=None
    # 屏幕宽度
    SCREEN_WIDTH=800
    SCREEN_HEIGHT=500
    # 创建我方坦克
    Tank_p1=None
    # 创建我方子弹列表
    bullet_list=[]
    # 创建敌方坦克
    EnemyTank_list=[]
    # 创建墙壁列表
    Wall_list=[]
    #存储敌方子弹列表
    Enemy_bullet_list=[]
    # 创建敌方坦克的数量
    EnemyTank_count=5
    # 创建爆炸效果列表
    Explode_list=[]
    def __init__(self):
        pass
    # 开始游戏
    def startGame(self):
       # 初始化显示模块
       _display.init()
       #初始化要显示的窗口和屏幕
       MinGame.window=_display.set_mode([MinGame.SCREEN_WIDTH,MinGame.SCREEN_HEIGHT])
       # 创建我方坦克
       self.createMytank()
       # 创建敌方坦克
       self.CreateEnemyTank()
       #设置当前的窗口标题
       _display.set_caption('坦克大战1.03')
       # self.getTextSuffer('aaaa')
       # 让窗口持续刷新
       while True:
           # 给窗口填充颜色
           MinGame.window.fill(COLOR_BLACK)
           # 在循环中持续完成事件的获取
           self.getEvent()
           # 将绘制文字的小画布，粘贴到窗口中
           MinGame.window.blit(self.getTextSuffer('剩余敌方坦克%d辆'%len(MinGame.EnemyTank_list)),(5,5))
           self.blitWalls()
           # 将我方坦克加载到窗口中
           if MinGame.Tank_p1 and MinGame.Tank_p1.live:
               MinGame.Tank_p1.displayTank()
           else:
               del MinGame.Tank_p1
               MinGame.Tank_p1=None
           # 将敌方坦克添加到窗口中
           self.biltEnemyTank()
           # 根据坦克的开关进行坦克持续移动
           if MinGame.Tank_p1 and not MinGame.Tank_p1.stop:
               MinGame.Tank_p1.move()
               MinGame.Tank_p1.hitWalls()
               MinGame.Tank_p1.hitEnemyTank()
           # 调用渲染我方子弹的列表方法
           self.biltBullet()
           # 调用渲染敌方子弹的列表方法
           self.biltEnemyBullet()
           # 展示爆炸效果
           self.displayexplode()
           # 展示墙壁
           self.createWalls()
           time.sleep(0.02)
           _display.update()
    # 创建我方坦克
    def createMytank(self):
        # 创建我方坦克
        MinGame.Tank_p1 = MyTank(400, 300)
        #创建音效对象
        music = Music('img/start.wav')
        # 播放音乐
        music.play()

    # 创建敌方坦克
    def CreateEnemyTank(self):
        top=100

        for i in range(MinGame.EnemyTank_count):
            speed = random.randint(3, 5)
            # 每次随机生成一个left值
            left = random.randint(1,7)
            eTank= EnemyTank(left*100,top,speed)
            MinGame.EnemyTank_list.append(eTank)

    # 将敌方坦克添加到桌面上
    def biltEnemyTank(self):
        for eEnemy in MinGame.EnemyTank_list:
            #判断敌方坦克是否活着
            if eEnemy.live:
                # 调用坦克的随机方法
                eEnemy.randMove()
                # 敌方坦克是否撞墙
                eEnemy.hitWalls()
                eEnemy.displayTank()
                # 敌方坦克是否与我方坦克碰撞
                eEnemy.hitMyTank()
                # 调用敌方坦克的射击方法
                eBullet = eEnemy.shot()
                # 如果子弹为None，不加入列表
                if eBullet:
                    # 将敌方坦克子弹添加到列表中
                    MinGame.Enemy_bullet_list.append(eBullet)
            else:
                MinGame.EnemyTank_list.remove(eEnemy)

    # 将我方子弹添加到窗口中
    def biltBullet(self):
        for bullet in MinGame.bullet_list:
            if bullet.live:
                # 将子弹添加到窗口中
                bullet.displayBullet()
                # 子弹移动
                bullet.bulletMove()
                #调用我方子弹与敌方坦克的碰撞方法
                bullet.hitEnemyTank()
                #判断我方子弹是否和墙壁发生碰撞
                bullet.hitWalls()
            else:
                MinGame.bullet_list.remove(bullet)

    # 将敌方子弹添加到窗口中
    def biltEnemyBullet(self):
        for eBullet in MinGame.Enemy_bullet_list:
            if eBullet.live:
                # 将子弹添加到窗口中
                eBullet.displayBullet()
                # 子弹移动
                eBullet.bulletMove()
                # 判断敌方子弹是否和墙壁发生碰撞
                eBullet.hitWalls()
                if MinGame.Tank_p1 and MinGame.Tank_p1.live:
                    # 产生一个爆炸效果
                    eBullet.hitMyTank()
            else:
                MinGame.Enemy_bullet_list.remove(eBullet)

    # 创建一个爆炸效果列表
    def displayexplode(self):
        for explode in MinGame.Explode_list:
            if explode.live:
                explode.explodedisplay()
            else:
                MinGame.Explode_list.remove(explode)

    # 创建墙壁方法
    def createWalls(self):
        for i in range(6):
            wall = Wall(130*i,240)
            MinGame.Wall_list.append(wall)
    #上传墙壁
    def blitWalls(self):
        for wall in MinGame.Wall_list:
            if wall.live:
                wall.walldisplay()
            else:
                MinGame.Wall_list.remove(wall)


    # 获取程序运行期间的所有事件
    def getEvent(self):
        # 获取所有事件
        Eventlist=pygame.event.get()
        #对事件进行判断处理
        for event in Eventlist:
            if event.type==pygame.QUIT:
                # 在当前类中调用其他方法可以使用self
                self.endGame()
            #判断事件是否是按键按下，如果是，继续判断是哪-个按键，来继续对应的按键
            if event.type==pygame.KEYDOWN:
                # 点击Esc按键进行坦克重生
               if event.key == pygame.K_ESCAPE and not MinGame.Tank_p1:
                    self.createMytank()
                # 在具体判断这个键是哪一个键
               if MinGame.Tank_p1 and MinGame.Tank_p1.live:
                   if event.key == pygame.K_LEFT:
                       print('坦克向左调头，移动')
                       # 修改坦克的方向
                       MinGame.Tank_p1.direction = 'L'
                       MinGame.Tank_p1.stop = False
                   elif event.key == pygame.K_RIGHT:
                       print('坦克向右调头，移动')
                       MinGame.Tank_p1.direction = 'R'
                       MinGame.Tank_p1.stop = False
                   elif event.key == pygame.K_UP:
                       print('坦克向上调头，移动')
                       MinGame.Tank_p1.direction = 'U'
                       MinGame.Tank_p1.stop = False
                   elif event.key == pygame.K_DOWN:
                       print('坦克向下调头，移动')
                       MinGame.Tank_p1.direction = 'D'
                       MinGame.Tank_p1.stop = False
                   elif event.key == pygame.K_SPACE:
                       print('发射子弹')
                       if len(MinGame.bullet_list) < 3:
                           # 创建一刻子弹
                           m = Bullet(MinGame.Tank_p1)
                           # 将子弹添加到子弹列表中bullet_list
                           MinGame.bullet_list.append(m)
                           #加载音乐对象
                           music = Music('img/fire.wav')
                           #播放音乐
                           music.play()
                       else:
                           print('子弹数量不足')
                       print('当前子弹数量为:%d' % len(MinGame.bullet_list))
            # 按键弹起的操作
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    # 判断坦克是否活着或者存在
                    if MinGame.Tank_p1 and MinGame.Tank_p1.live:
                        MinGame.Tank_p1.stop=True
    # 绘制左上角的文字
    def getTextSuffer(self,text):
        #初始化字体模块
        pygame.font.init()
        # 测试 获取所有可用的字体
        # fontlist=pygame.font.get_fonts()
        # print(fontlist)
        #从系统对象创建一个合适的字体
        font=pygame.font.SysFont('Kaiti',18)
        # 通过对应的字符完成内容相关的绘制
        TextSurface=font.render(text,True,COLOR_RED)
        return TextSurface

    # 结束游戏
    def endGame(self):
        print('谢谢使用')
        exit()
# 精灵类
class Baseitem(pygame.sprite.Sprite):
    def __init__(self):
        # 进行初始化
        pygame.sprite.Sprite.__init__(self)
# 坦克类
class Tank(Baseitem):
    def __init__(self,left,top):
        self.images={
            'U':pygame.image.load('img/enemy1U.gif'),
            'D':pygame.image.load('img/enemy1D.gif'),
            'L':pygame.image.load('img/enemy1L.gif'),
            'R':pygame.image.load('img/enemy1R.gif')
        }
        # 默认坦克方向
        self.direction='U'
        self.image = self.images[self.direction]
        # 获取坦克所在的区域
        self.rect=self.image.get_rect()
        #指定坦克初始化的位置，分别在x，y轴什么位置
        self.rect.left=left
        self.rect.top=top
        #坦克移动的速度
        self.speed=5
        #添加坦克的开关
        self.stop=True
        #坦克是否发生碰撞活着
        self.live = True
        #新增属性用来记录坦克移动之前的坐标(用于坐标还原来使用)
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top



    # 坦克的移动
    def move(self):
        # 用来记录移动之前的坐标
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        if self.direction=='L':
            if self.rect.left>0:
                self.rect.left-=self.speed
        elif self.direction=='R':
            if self.rect.left + self.rect.height<MinGame.SCREEN_WIDTH:
                self.rect.left+=self.speed
        elif self.direction=='D':
            if self.rect.top +self.rect.height<MinGame.SCREEN_HEIGHT:
                self.rect.top+=self.speed
        elif self.direction=='U':
            if self.rect.top>0:
                self.rect.top-=self.speed
    # 坐标还原方法
    def stay(self):
        self.rect.left=self.oldleft
        self.rect.top=self.oldtop
    # 新增坦克与墙壁的碰撞
    def hitWalls(self):
        for wall in MinGame.Wall_list:
            if pygame.sprite.collide_rect(wall,self):
                self.stay()
    # 坦克的射击方法
    def shot(self):
        return Bullet(self)
    # 界面的展示
    def displayTank(self):
        # 重新设置坦克的图片
        self.image=self.images[self.direction]
        # 将坦克加载到窗口中(blit上传)
        MinGame.window.blit(self.image,self.rect)

# 我方坦克
class MyTank(Tank):
    def __init__(self,left,top):
        super(MyTank, self).__init__(left,top)
    #主动碰撞到敌方坦克的方法
    def hitEnemyTank(self):
        for eTank in MinGame.EnemyTank_list:
            if pygame.sprite.collide_rect(self,eTank):
                self.stay()
# 敌方坦克
class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        # 调用父类的初始化方法
        super(EnemyTank, self).__init__(left,top)
        self.images = {
            'U': pygame.image.load('img/p2tankU.gif'),
            'D': pygame.image.load('img/p2tankD.gif'),
            'L': pygame.image.load('img/p2tankL.gif'),
            'R': pygame.image.load('img/p2tankR.gif')
        }
        # 默认随机获取坦克方向
        self.direction = self.randomDirection()
        self.image = self.images[self.direction]
        # 获取坦克所在的区域
        self.rect = self.image.get_rect()
        # 指定坦克初始化的位置，分别在x，y轴什么位置
        self.rect.left = left
        self.rect.top = top
        # 坦克移动的速度
        self.speed = speed
        # 添加坦克的开关
        self.stop = True
        #添加移动步数
        self.step=50


    #随机获取敌方坦克方向
    def randomDirection(self):
        num = random.randint(1,4)
        if num == 1:
           return 'U'
        elif num == 2:
            return 'L'
        elif num == 3:
            return 'R'
        elif num == 4:
           return 'D'
    # 敌方坦克随机移动
    def randMove(self):
        if self.step<=0:
            self.direction=self.randomDirection()
            self.step=50
        else:
            self.move()
            self.step-=1

    # 重写射击方法
    def shot(self):
        num = random.randint(1,1000)
        if num <=20:
            return Bullet(self)
    #敌方坦克和我方坦克的碰撞
    def hitMyTank(self):
        if MinGame.Tank_p1 and MinGame.Tank_p1.live:
            if pygame.sprite.collide_rect(self,MinGame.Tank_p1):
                self.stay()


    # def displayEnemyTank(self):
    #     super().displayTank()


# 子弹方法
class Bullet(Baseitem):
    def __init__(self,tank):
        #添加子弹图片
        self.image=pygame.image.load('img/tankmissile.gif')
        # 子弹的方向（坦克的方向）
        self.direction = tank.direction
        #获取子弹所在的位置
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top =  tank.rect.top  + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top + tank.rect.width / 2 -self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width/2

        #设置子弹的速度
        self.speed=7
        #判断子弹是否活着
        self.live=True

    # 子弹的移动方法
    def bulletMove(self):
        if self.direction =='U':
            if self.rect.top >0:
                self.rect.top -= self.speed
            else:
                # 修改子弹的状态值
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MinGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                # 修改子弹的状态值
                self.live = False
        elif self.direction == 'L':
            if self.rect.left >0:
                self.rect.left -= self.speed
            else:
                # 修改子弹的状态值
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MinGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                # 修改子弹的状态值
                self.live = False

    # 子弹的展方法
    def displayBullet(self):
        MinGame.window.blit(self.image,self.rect)
    #增加我方子弹碰撞敌方坦克
    def hitEnemyTank(self):
        for eTank in MinGame.EnemyTank_list:
             if pygame.sprite.collide_circle(self,eTank):
                 # 创建一个爆炸效果
                 explode=Explode(eTank)
                 # 将爆炸效果添加到爆炸效果列表中
                 MinGame.Explode_list.append(explode)
                 # 创建一个音乐对象
                 music= Music('img/hit.wav')
                 # 播放音乐
                 music.play()
                 self.live =False
                 eTank.live = False
    #产生一个敌方子弹碰撞我方坦克
    def hitMyTank(self):
        if pygame.sprite.collide_circle(self,MinGame.Tank_p1):
            #创建一个爆炸效果，并将爆炸效果添加到爆炸列表中
            explode=Explode(MinGame.Tank_p1)
            MinGame.Explode_list.append(explode)
            #修改子弹列表
            self.live=False
            #修改我方坦克的状态
            MinGame.Tank_p1.live=False
    #子弹与墙壁的碰撞
    def hitWalls(self):
        for wall in MinGame.Wall_list:
            if pygame.sprite.collide_rect(self,wall):
                # 修改子弹的属性
                self.live = False
                wall.hp -=1
                if wall.hp <=0:
                    wall.live = False



# 爆炸效果
class Explode():
    def __init__(self,tank):
        self.rect=tank.rect
        # 索引值
        self.step=0
        self.images=[pygame.image.load('img/blast0.gif'),
                     pygame.image.load('img/born1.gif'),
                     pygame.image.load('img/born2.gif'),
                     pygame.image.load('img/blast3.gif'),
                     pygame.image.load('img/blast4.gif'),
                     ]
        # 默认获取图片的0
        self.image=self.images[self.step]
        self.live=True
    def explodedisplay(self):
        if self.step < len(self.images):
            MinGame.window.blit(self.image,self.rect)
            self.image = self.images[self.step]
            self.step+=1
        else:
            self.live = False
            self.step=0
# 墙壁
class Wall():
    def __init__(self,left,top):
        self.images =pygame.image.load('img/steels.gif')
        self.rect = self.images.get_rect()
        self.rect.left=left
        self.rect.top=top
        #判断墙壁是否存在
        self.live=True
        #用来记录墙壁的生命值
        self.hp = 3
    # 墙壁页面的展示
    def walldisplay(self):
        MinGame.window.blit(self.images,self.rect)
# 音乐
class Music():
    def __init__(self,filename):
        self.filename=filename
        # 先加载混响器初始化
        pygame.mixer.init()
        # 加载音乐文件进行播放
        pygame.mixer.music.load(self.filename)
    # 音乐的开始方法
    def play(self):
        pygame.mixer.music.play()
MinGame().startGame()



