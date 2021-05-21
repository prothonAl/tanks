import pygame
from time import time
from random import randint
class Tank():
    def __init__(self, x, y):
        self.sprites=(pygame.image.load('sprites/tankUp.png'), pygame.image.load('sprites/tankDown.png'),
                      pygame.image.load('sprites/tankLeft.png'), pygame.image.load('sprites/tankRight.png'))
        self.sriteTank=self.sprites[0]
        self.bulletImg=pygame.image.load('sprites/bullet.png')
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        self.oX=x
        self.oY=y
        self.speed=7
        self.move='UP'
        self.bulletSpeed=20
        self.bullets=[] 
        self.isFire=False
        self.recharge=False
        self.timer=100
        self.rechTime=1
        self.patrons=50
        self.lifes=1
        self.hasRecharge=True
        self.idt=(randint(0, 100_000)) 
        self.to='f'
        self.enemy=False
        #width and height
        self.width=80
        self.height=80
        self.sl=0
        self.typ='Tank'
    def drawTank(self, surf): 
        if ((time())-self.timer)>=self.rechTime:
            self.recharge=False
        self.fireMove()
        surf.blit(self.sriteTank, (self.oX, self.oY))
        for i in self.bullets:
            surf.blit(self.bulletImg, (i[0], i[1]))


    def sensors(self, world):
        listLeft=[12345]
        listUp=[12345]
        listDown=[12345]
        listRight=[12345]
        for i in world:
            if i[2]!=self.idt:
                for j in range(0, 80):
                    if ((i[1]+j>self.oY) and (i[1]+j<self.oY+80)):
                        if ((self.oX+80)-i[0])<0:
                            listRight.append(abs((self.oX+80)-i[0]))
                        elif (self.oX-(i[0]+80))>0:
                            listLeft.append(self.oX-(i[0]+80))
                        break
                for x in range(0, 80):
                    if (i[0]+x>self.oX) and (i[0]+x<self.oX+80):
                        if ((self.oY)-i[1])<0:
                            listDown.append(abs(self.oY-i[1]))
                        elif (self.oY-i[1])>0:
                            listUp.append((self.oY-i[1])-90)
                        break
        for i in (listUp, listDown, listLeft, listRight):
            if len(i)>1:
                i.remove(12345)
        return min(listUp), min(listDown), min(listLeft), min(listRight)
    def rightMove(self, dist):
        self.sriteTank=self.sprites[3]
        if self.oX<1120:
            self.oX+=dist #self.speed
        self.move='RIGHT'
    def leftMove(self, dist):
        self.sriteTank=self.sprites[2]
        if self.oX>5:
            self.oX-=dist# self.speed
        self.move='LEFT'
    def upMove(self, dist):
        self.sriteTank=self.sprites[0]
        if self.oY>5:
            self.oY-=dist #self.speed
        self.move='UP'
    def downMove(self, dist):
        self.sriteTank=self.sprites[1]
        if self.oY<580:
            self.oY+=dist #self.speed
        self.move='DOWN'
    def tankMove(self, to, world): 
        if (to=='right'): #w3
            self.rightMove(0)
        elif (to=='left'): #w2
            self.leftMove(0)
        elif (to=='up'):
            self.upMove(0)
        elif (to=='down'):
            self.downMove(0)

        w=self.sensors(world)
   
        if (to=='right') and ((w[3])>14): #w3
            self.rightMove(self.speed)
        elif (to=='left') and (w[2]>14): #w2
            self.leftMove(self.speed)
        elif (to=='up') and (w[0]>3):
            self.upMove(self.speed)
        elif (to=='down') and (w[1]>87):
            self.downMove(self.speed)
    def fire(self):
        if (self.recharge==False) and self.patrons>0:
            self.timer=round(time())
            self.recharge=True if self.hasRecharge else False
            if self.move=='UP':
                self.bullets.append([self.oX+37, self.oY, self.move])
            elif self.move=='DOWN':
                self.bullets.append([self.oX+35, self.oY+80, self.move])
            elif self.move=='LEFT':
                self.bullets.append([self.oX, self.oY+35, self.move])
            elif self.move=='RIGHT':
                self.bullets.append([self.oX+80, self.oY+37, self.move])
            self.patrons-=1
    def fireMove(self):
        for i in enumerate(self.bullets):
            if i[1][2]=='UP':
                i[1][1]-=self.bulletSpeed
                if i[1][1]<=0:
                    del self.bullets[i[0]]
            elif i[1][2]=='DOWN':
                i[1][1]+=self.bulletSpeed
                if i[1][1]>=700:
                    del self.bullets[i[0]]
            elif i[1][2]=='LEFT':
                i[1][0]-=self.bulletSpeed
                if i[1][0]<=0:
                    del self.bullets[i[0]]
            elif i[1][2]=='RIGHT':
                i[1][0]+=self.bulletSpeed
                if i[1][0]>=1200:
                    del self.bullets[i[0]]
    def __repr__(self):
        return f'Tank < |enemy: {self.enemy}|  |id: {str(self.idt)}| >'
    def __str__(self):
        return f'{self.typ}({self.oX}, {self.oY})'
class playerTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y)
class compTank(Tank):
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.speed=speed
        self.enemy=True
        self.typ='comTank'
        self.sprites=self.sprites=(pygame.image.load('sprites/tankUpC.png'), pygame.image.load('sprites/tankDownC.png'),
                                   pygame.image.load('sprites/tankLeftC.png'), pygame.image.load('sprites/tankRightC.png'))
    def foolowPlayer(self, cor, world, bullets):
        if len(bullets)==0:
            self.to='f'
        for i in bullets:
            if ((i[0]>self.oX-200) and (i[1]>self.oY-10 and i[1]<self.oY+90)) and i[2]=='LEFT':
                self.to='up'
            elif ((i[0]<self.oX+200) and (i[1]>self.oY-10 and i[1]<self.oY+80+10)) and i[2]=='RIGHT':
                self.to='down'
            elif ((i[0]>self.oX and i[0]<self.oX+80)) and (i[1]>self.oY-300) and i[2]=='DOWN':
                self.to='left'
            elif ((i[0]>self.oX and i[0]<self.oX+80)) and (i[1]<self.oY+300) and i[2]=='UP':
                self.to='right'
            else:
                self.to=='f'
        if self.to=='left':
            self.tankMove('left', world)
        elif self.to=='right':
            self.tankMove('right', world)
        elif self.to=='up':
            self.tankMove('up', world)
        elif self.to=='down':
            self.tankMove('down', world)
        elif self.to=='f':
            if ((cor[0]<self.oX+10) and (cor[0])>self.oX)==False:
                if self.oX>=cor[0]:
                    self.tankMove('left', world)
                elif self.oX<=cor[0]:
                    self.tankMove('right', world)


                if (cor[1]>self.oY and cor[1]<self.oY+80) or (cor[1]+80>self.oY and cor[1]+80<self.oY+80):
                    self.fire()
            else:

                if self.oY+40<cor[1]:
                    self.move='DOWN'
                    self.sriteTank=self.sprites[1]
                    self.fire()
                elif self.oY>cor[1]:
                    self.move='UP'
                    self.sriteTank=self.sprites[0]
                    self.fire()
