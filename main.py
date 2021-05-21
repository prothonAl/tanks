
import pygame
from Tank import playerTank, compTank
from kProcessing import *
from random import randint, randrange
from time import time

keyProcessor=keyInit()
window=pygame.display.set_mode((1200, 700))
gameWindow=pygame.Surface((1200, 660))
infoWindow=pygame.Surface((1200, 40))
pygame.display.set_caption('First attack')


run=True
done=True
score=0

pygame.font.init()
gameFont=pygame.font.Font(None, 50)
gameFont2=pygame.font.Font(None, 100)
myTank=playerTank(550, 276)
myTank.speed=8

clock=pygame.time.Clock()

compTanks=[compTank(randint(0, 1100), randint(0, 580), 5)]
bumIMG=pygame.image.load('sprites/bum.png')
bumIMG2=pygame.image.load('sprites/bum2.png')
kirpich=pygame.image.load('sprites/kirpich.png')
stena=pygame.image.load('sprites/ironStena.png')

objCoordinats=[]
isBum=False
errors=0
oError=0
world=[]



def collisinobjs(obj, group):
    def checkolission(obj0, obj1):
        l=set()
        l1=set()
        for x in range(obj0.oX, obj0.oX+obj0.width, 5):
            for y in range(obj0.oY, obj0.oY+obj0.height, 5):
                l.add((x, y))

        for x1 in range(obj1.oX, obj1.oX+obj1.width, 5):
            for y1 in range(obj1.oY, obj1.oY+obj1.height, 5):
                l1.add((x1, y1))
        if len(l&l1)>0:
            return True
        return False
    for i in group:
        if obj.idt!=i.idt:
            if checkolission(obj, i):
                return 1
    return 0



def drawText():
    infoWindow.blit(gameFont.render(f'patrons: {myTank.patrons}', 1, (0, 0, 255)), (10, 5))
    infoWindow.blit(gameFont.render(f'lifes: {myTank.lifes}', 1, (0, 0, 255)), (300, 5))
    infoWindow.blit(gameFont.render(f'Errors: {errors}', 1, (0, 0, 255)), (500, 5))
    infoWindow.blit(gameFont.render(f'score: {score}', 1, (0, 0, 255)), (700, 5))
    if myTank.recharge:
        infoWindow.blit(gameFont.render(f'ПЕРЕЗАРЯДКА', 1, (0, 0, 255)), (900, 5))


def initBulletAndTank(bullets): 
    global t, isBum, errors, t, x, y, tboom, world, score
 
    for i in compTanks:
        i.foolowPlayer(objCoordinats[0], world, bullets)
        for j in i.bullets:
            if (((j[0]>myTank.oX) and (j[0]<myTank.oX+80)) and ((j[1]>myTank.oY) and (j[1]<myTank.oY+80))):
                myTank.lifes-=1
                i.bullets.remove(j)

    for i in compTanks:
        for j in myTank.bullets:
            if (j[0]>i.oX and j[0]<i.oX+80) and (j[1]>i.oY and j[1]<i.oY+80):
                try:
                    if compTanks[compTanks.index(i)].lifes==0:
                        del compTanks[compTanks.index(i)]
                        del myTank.bullets[myTank.bullets.index(j)]
                        isBum=True
                        x=j[0]
                        y=j[1]
                        t=time()
                        tboom=t
                        score+=1
                    compTanks[compTanks.index(i)].lifes-=1
                    del myTank.bullets[myTank.bullets.index(j)]
                except:
                    errors+=1
        i.drawTank(gameWindow)

def isGameOver():
    global run
    if myTank.lifes<=0:
        gameWindow.blit(gameFont2.render(f'Game Over!', 1, (255, 0, 0)), (400, 200))
        run=False
def drawBoom():
    global isBum, tboom
    if isBum:
        if (time()-tboom)>0.3:
            isBum=False
        gameWindow.blit(bumIMG, (x-40, y-40))
        if (time()-tboom)>=0.1:
            gameWindow.blit(bumIMG2, (x-120, y-120))
def addTank(colvo, world):
    countAddTank=0
    if len(compTanks)==0:
        if (time()-t)>=2:
            xList=[]
            yList=[]
            for i in world:
                xList.append(i[0])
                yList.append(i[1])
            while countAddTank<colvo:
                x, y = randrange(0, 1100, 76), randrange(0, 580, 80)
                if ((x not in xList) and (y not in yList)) and ((x>myTank.oX and x<myTank.oX+80)==False) and ((y>myTank.oY and y<myTank.oY+80)==False):
                    compTanks.append((compTank(x, y, 5)))
                    countAddTank+=1

myTank.lifes=5
myTank.patrons=100

fps=60
myTank.speed=7
while run:
    world.clear()
   
    if keyProcessor.isQuit():
       run=False
   
    clock.tick(fps)
  
    gameWindow.fill((79, 57, 34)) 

    if keyProcessor.key()[0]=='fire':
        myTank.fire()

    myTank.drawTank(gameWindow)

    objCoordinats.clear()
    objCoordinats.append((myTank.oX, myTank.oY, 'player'))

    for i in compTanks:
        world.append((i.oX, i.oY, i.idt))
    world.append((myTank.oX, myTank.oY, myTank.idt))
    myTank.tankMove(keyProcessor.key()[1], world)
    if score>20:
        addTank(8, world)
    else:
        addTank(4, world)
    initBulletAndTank(myTank.bullets)
    isGameOver()
    drawBoom()
    myTank.sensors(world)

    infoWindow.fill((229, 189, 44))
    drawText()
   
    window.blit(gameWindow, (0, 40))
    window.blit(infoWindow, (0, 0))

    pygame.display.flip()
  
while done:
    clock.tick(1)
    if keyProcessor.isQuit():
       done=False
pygame.quit()
