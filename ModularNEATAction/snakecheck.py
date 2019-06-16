#!/usr/bin/env python
#coding: utf-8

from __future__ import print_function

import os
import pickle
import pygame
from pygame.locals import*
import sys
import re
import math
from time import sleep
import numpy as np
#from time import sleep
#ゲーム動作確認用
maxy=0
runs_per_net = 5
Speedtimes=1
simulation_seconds = 50000.0//Speedtimes
SCR_RECT=Rect(0,0,480,384)
mapleftx=0.0
maprightx=0.0
maptopy=0.0
mapbottomy=0.0
START,PLAY,GAMEOVER,GAMECLEAR=(0,1,2,3)
RIG,LEF=(0,1)
GS=32
Crushpoint=0
bpoint=np.zeros(100*100,dtype=np.int)
ipoint=np.zeros(100*100,dtype=np.int)
epoint=np.zeros(100*100,dtype=np.int)
spoint=np.zeros(100*100,dtype=np.int)
pythonx=0.0
pythony=0.0
firstdif=0.0
class PyAction():
    GS=32
    def __init__(self,t,mapname):
        pygame.init()
        self.screen=pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("アクションゲーム")

        Python.left_images[0]=load_image("python2.bmp",-1)
        Python.right_images[0]=pygame.transform.flip(Python.left_images[0],1,0)
        Python.left_images[1]=load_image("python.bmp",-1)
        Python.right_images[1]=pygame.transform.flip(Python.left_images[1],1,0)
        Block.image=load_image("block.bmp",-1)
        Spike.image=load_image("spike.bmp",-1)
        Enemy.images[0]=load_image("Enea.bmp",-1)
        Enemy.images[1]=load_image("Eneb.bmp",-1)
        Enemy.images[2]=load_image("Enec.bmp",-1)
        Enemy.images[3]=load_image("Ened.bmp",-1)
        Enemy.images[4]=load_image("Enee.bmp",-1)
        Item.images[0]=load_image("Itea.bmp",-1)
        Item.images[1]=load_image("Iteb.bmp",-1)
        Item.images[2]=load_image("Itec.bmp",-1)
        Item.images[3]=load_image("Ited.bmp",-1)
        Dattack.images[0]=load_image("Dirattacka.bmp",-1)
        Dattack.images[1]=load_image("Dirattackb.bmp",-1)
        #Sattack.images[0]=load_image("speattaca.bmp",-1)
        #Sattack.images[1]=load_image("speattacb.bmp",-1)
        self.map=Map(mapname)
        self.game_state=PLAY
        self.t=t
        self.mapname=mapname
        clock=pygame.time.Clock()
        self.lx=0.0
        self.ty=0.0
        self.gametime=1840
        self.input=np.zeros(57,dtype=np.float)
        
        while True:
            clock.tick(60)
            self.update()
            self.draw(self.screen)
            self.mapbound_calluculate()
            pygame.display.update()
            self.key_handler()
            #sleep(0.2)
            """
            self.get_displayinfo()
            print(self.input[0:7])
            print(self.input[7:14])
            print(self.input[14:21])
            print(self.input[21:28])
            print(self.input[28:35])
            print(self.input[35:42])
            print(self.input[42:49])
            print()
            sleep(0.5)
            """
            
    def running(self,controll):
        Python.controll=controll
        self.t+=50
        self.update()
        #self.draw(self.screen)
        self.mapbound_calluculate()
        #pygame.display.update()
        #self.key_handler()

    def mapbound_calluculate(self):
        global mapleftx,maprightx,maptopy,mapbottomy
        offsetx,offsety=self.map.calc_offset()
        if offsetx < 0:
            offsetx=0
            self.lx=0
        elif offsetx>self.map.width-SCR_RECT.width:
            offsetx=self.map.width-SCR_RECT.width
            self.lx=self.map.width-SCR_RECT.width
        if offsety < 0:
            offsety=0
            self.ty=0
        elif offsety>self.map.height-SCR_RECT.height:
            offsety=self.map.height-SCR_RECT.height
            self.ty=self.map.height-SCR_RECT.height
            #print(offsetx,offsety)
        mapleftx=offsetx
        maprightx=offsetx+480.0
        maptopy=offsety
        mapbottomy=offsety+384.0

    def exitrun(self):
        pygame.init()
        self.screen=[]
        for enemy in self.map.enemies:
            pygame.sprite.Sprite.kill(enemy)
        for block in self.map.blocks:
            pygame.sprite.Sprite.kill(block)
        for item in self.map.items:
            pygame.sprite.Sprite.kill(item)
        self.map=[]
        self.input=[]
        pygame.quit()
        #if self.game_state==GAMEOVER or self.game_state==GAMECLEAR or self.t>simulation_seconds:
        #    pygame.quit()
        """while True:
            clock.tick(60)
            self.t=pygame.time.get_ticks
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()"""

    def update(self):
        if self.game_state==PLAY:
            self.gametime-=1
            if(self.gametime<-20):
                self.game_state=GAMEOVER
            self.map.update()
        if self.map.python.HP<=0:
            self.game_state=GAMEOVER
        if self.map.python.clear==1:
            self.game_state=GAMECLEAR
        if self.map.python.corrup==1:
            self.game_state=GAMEOVER
            

    def draw(self,screen):
        global mapleftx,maprightx,maptopy,mapbottomy
        screen.fill((0,0,0))
        if self.game_state==START:
            title_font=pygame.font.SysFont(None,80)
            title=title_font.render("ACTION GAME",False,(255,0,0))
            screen.blit(title,((SCR_RECT.width-title.get_width())/2,100))

            push_font=pygame.font.SysFont(None,40)
            push_space=push_font.render("PUSH Z KEY",False,(255,255,255))
            screen.blit(push_space,((SCR_RECT.width-push_space.get_width())/2,300))
        if self.game_state==PLAY:
            self.map.draw()
            offsetx,offsety=self.map.calc_offset()
            if offsetx < 0:
                offsetx=0
                self.lx=0
            elif offsetx>self.map.width-SCR_RECT.width:
                offsetx=self.map.width-SCR_RECT.width
                self.lx=self.map.width-SCR_RECT.width
            if offsety < 0:
                offsety=0
                self.ty=0
            elif offsety>self.map.height-SCR_RECT.height:
                offsety=self.map.height-SCR_RECT.height
                self.ty=self.map.height-SCR_RECT.height
            mapleftx=offsetx
            maprightx=offsetx+640.0
            maptopy=offsety
            mapbottomy=offsety+480.0
            screen.blit(self.map.surface,(0,0),(offsetx,offsety,SCR_RECT.width,SCR_RECT.height))
            HP_font=pygame.font.SysFont(None,60)
            Score_font=pygame.font.SysFont(None,60)
            nowHP="LIFE:{}".format(self.map.python.HP)
            nowScore="Score:{}".format(self.map.python.score)
            nowTime="TIME:{}".format(self.gametime//60)
            HP=HP_font.render(nowHP,False,(0,255,0))
            Score=Score_font.render(nowScore,False,(0,128,128))
            Time=Score_font.render(nowTime,False,(0,128,255))
            screen.blit(HP,((SCR_RECT.width-HP.get_width()-200)/2,0))
            screen.blit(Score,((SCR_RECT.width-Score.get_width()+200)/2,0))
            screen.blit(Time,((SCR_RECT.width-Time.get_width()-240)/2,40))
        elif self.game_state==GAMEOVER:
            #print(-10+self.map.python.score//50+firstdif-math.sqrt(abs(self.map.goalx-self.map.python.fpx)/2.0))
            #print(str((self.map.python.fpx/self.map.goalx)*100)+'%')
            gameover_font=pygame.font.SysFont(None,80)
            gameover=gameover_font.render("GAME OVER",False,(255,0,0))
            screen.blit(gameover,((SCR_RECT.width-gameover.get_width())/2,100))
            push_font=pygame.font.SysFont(None,40)
            push_space=push_font.render("PUSH Z KEY",False,(255,255,255))
            screen.blit(push_space,((SCR_RECT.width-push_space.get_width())/2,300))
        elif self.game_state==GAMECLEAR:
            #print(150+self.map.python.HP+self.map.python.score//100+self.gametime//120)
            gameover_font=pygame.font.SysFont(None,80)
            gameover=gameover_font.render("STAGE CLEAR",False,(255,0,0))
            screen.blit(gameover,((SCR_RECT.width-gameover.get_width())/2,100))
            push_font=pygame.font.SysFont(None,40)
            push_space=push_font.render("TRY OTHER STAGE",False,(255,255,255))
            screen.blit(push_space,((SCR_RECT.width-push_space.get_width())/2,300))

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
                #PyAction()
            elif event.type==KEYDOWN and event.key==K_ESCAPE:
                pygame.quit()
                exit()
                #PyAction()
            elif event.type==KEYDOWN and event.key==K_z:
                if self.game_state==START:
                    self.game_state=PLAY
                elif self.game_state==GAMEOVER or self.game_state==GAMECLEAR:
                    pygame.quit()
                    PyAction(self.t,self.mapname)
                    #exit()
                    #PyAction()

    def get_playerstate(self):
        return [self.map.python.fpx,self.map.python.fpy,-math.sqrt((self.map.python.rect.x-self.map.goalx)**2+(self.map.python.rect.y-self.map.goaly)**2)/100.0]
    def get_displayinfo(self):
        #input=np.zeros(300,dtype=np.int)
        for i in range(-3,4):
            nowy=self.map.python.fpy+GS*i
            for j in range(-3,4):
                if(i==0 and j==0):
                    continue
                nowx=self.map.python.fpx+GS*j
                checkx=int(nowx//GS)
                checky=int(nowy//GS)
                #print(checky,checkx)
                #print(self.map.bpoint)
                self.input[i*7+21+j+3]=float(0.0)
                if(checkx<0 or checkx>=self.map.col or checky<0 or checky>=self.map.row):
                    continue
                if bpoint[checky][checkx]==1:
                    self.input[i*7+21+j+3]=float(-1.0)
                if ipoint[checky][checkx]==1:
                    self.input[i*7+21+j+3]=float(-0.5)
                if epoint[checky][checkx]==1:
                    self.input[i*7+21+j+3]=float(0.5)
                if spoint[checky][checkx]==1:
                    self.input[i*7+21+j+3]=float(1.0)
                """
                for enemy in self.map.enemies:
                    if enemy.rect.center[0]>nowx and enemy.rect.center[0]<nowx+self.GS and enemy.rect.center[1]>nowy and enemy.rect.center[1]>nowy+self.GS:
                        self.input[i*6+18+j+3]=float(1.0)"""
        #print(input)
        self.input[49]=self.map.python.fpx/self.map.width
        self.input[50]=self.map.python.fpy/self.map.height
        self.input[51]=self.map.python.fpvx/5.0
        self.input[52]=self.map.python.fpvy/10.0
        self.input[53]=self.map.python.state
        if(self.map.python.on_floor==True):
            self.input[54]=1.0
        else:
            self.input[54]=0.0
        if(self.map.python.dive==True):
            self.input[55]=1.0
        else:
            self.input[55]=0.0
        self.input[56]=self.map.python.HP/100.0
        
        return self.input
        #print(input)
        #return tolist(input)
            

class Python(pygame.sprite.Sprite):
    GS=32
    MOVE_SPEED=5.0*Speedtimes
    MOVE_SPEEDlist=[5.0,7.0]
    DASH_SPEED=10.0
    JUMP_SPEED=7.0*Speedtimes
    GRAVITY=0.3*(Speedtimes**2)
    initHP=100
    redamage_time=240//Speedtimes
    rejump_time=30//Speedtimes
    Maxjumplist=[2,1]
    redattacklist=[32,10]
    dlivelist=[21,4]
    dgravlist=[1.0,0]
    guardlist=[1.0,0.8]
    resistlist=[0.8,1.0]
    gliplist=[1.0,0.5]
    controll=100
    left_images={}
    right_images={}
    global Crushpoint
    def __init__(self,pos,blocks,enemies,items,maxy,spikes):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image=self.right_images[0]
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y=pos[0],pos[1]
        self.state=0
        self.blocks=blocks
        self.enemies=enemies
        self.items=items
        self.spikes=spikes
        self.jump_count=0
        self.score=0
        self.fpx=float(self.rect.x)
        self.fpy=float(self.rect.y)
        self.fpvx=0.0
        self.fpvy=0.0
        self.HP=self.initHP
        self.on_floor=False
        self.dive=False
        self.redamage_timer=0
        self.rejump_timer=0
        self.rechange_timer=0
        self.clear=0
        self.corrup=0
        self.redattack_timer=0
        self.maxy=maxy
        self.MAX_JUMP_COUNT=self.Maxjumplist[0]
        self.guard=self.guardlist[0]
        self.resit=self.resistlist[0]
        self.glip=self.gliplist[0]
        self.redattack_time=self.redattacklist[0]
        self.dir=RIG
        self.trace=[]
    def update(self):
        global pythonx
        global pythony
        global Crushpoint
        if len(self.trace)>=60:
            del self.trace[0]
        #self.trace.append([self.rect.x,self.rect.y])
        if len(self.trace)>=60:
            if self.trace[59]==self.trace[0]:
                self.corrup=1
            
        if Crushpoint>0:
            self.score+=Crushpoint
            Crushpoint=0
        pressed_keys=pygame.key.get_pressed()
        #print(self.controll)
        if pressed_keys[K_RIGHT] or self.controll==3 or self.controll==6 or self.controll==7 or \
           self.controll==12 or self.controll==15 or self.controll==16 or self.controll==20:
            self.image=self.right_images[self.state]
            self.fpvx=self.MOVE_SPEED
            self.dir=RIG
        elif pressed_keys[K_LEFT] or self.controll==1 or self.controll==5 or self.controll==8 or \
             self.controll==10 or self.controll==14 or self.controll==17 or self.controll==19:
            self.image=self.left_images[self.state]
            self.fpvx=-self.MOVE_SPEED
            self.dir=LEF
        else:
            self.fpvx=0.0
        if pressed_keys[K_UP] or self.controll==2 or self.controll==5 or self.controll==6 or \
           self.controll==11 or self.controll==14 or self.controll==15:
            if self.on_floor:
                self.fpvy=-self.JUMP_SPEED
                self.on_floor=False
                self.jump_count=1
                self.rejump_timer=self.rejump_time
            elif self.rejump_timer==0 and self.jump_count < self.MAX_JUMP_COUNT and self.state==0:
                self.fpvy=-self.JUMP_SPEED
                self.on_floor=False
                self.jump_count+=1
            elif self.rejump_timer==0 and self.on_floor==False and self.jump_count < self.MAX_JUMP_COUNT and self.state==0:
                self.fpvy=-self.JUMP_SPEED
                self.on_floor=False
                self.jump_count=2
        if pressed_keys[K_z] or (self.controll>=9 and self.controll<=17):
            if self.redattack_timer==0:
                if self.dir==RIG:
                    Dattack(self.state,self.fpx+self.GS,self.fpy,self.dlivelist[self.state],self.dgravlist[self.state],self.enemies,self.blocks,self.state)
                else:
                    Dattack(self.state,self.fpx-self.GS,self.fpy,self.dlivelist[self.state],self.dgravlist[self.state],self.enemies,self.blocks,self.state)
                self.redattack_timer=self.redattack_time
        if pressed_keys[K_DOWN] or self.controll==4 or self.controll==7 or self.controll==8 or \
           self.controll==13 or self.controll==16 or self.controll==17:
            if not self.on_floor and not self.dive:
                self.fpvy=self.JUMP_SPEED
                self.dive=True

        if pressed_keys[K_c] or (self.controll>=18 and self.controll<=20):
            if self.on_floor:
                if self.rechange_timer==0:
                    self.state=(self.state+1)%2
                    if(self.image==self.right_images[(self.state+1)%2]):
                    	self.image=self.right_images[(self.state)%2]
                    elif(self.image==self.left_images[(self.state+1)%2]):
                    	self.image=self.left_images[(self.state)%2]
                    self.MAX_JUMP_COUNT=self.Maxjumplist[self.state]
                    self.MOVE_SPEED=self.MOVE_SPEEDlist[self.state]
                    self.guard=self.guardlist[self.state]
                    self.resit=self.resistlist[self.state]
                    self.glip=self.gliplist[self.state]
                    self.redattack_time=self.redattacklist[self.state]
                    self.rechange_timer=6
                else:
                    self.rechange_timer-=1

        if not self.on_floor:
            self.fpvy += self.GRAVITY
        self.eneitemcollision()
        self.blockcollision_x()
        self.blockcollision_y()
        self.rect.x=int(self.fpx)
        self.rect.y=int(self.fpy)
        pythonx=self.fpx
        pythony=self.fpy
        if self.rejump_timer>0:
            self.rejump_timer-=1
        if self.redattack_timer>0:
            self.redattack_timer-=1

    def eneitemcollision(self):
        global epoint
        width=self.rect.width
        height=self.rect.height
        newx=self.fpx+self.fpvx
        newy=self.fpy+self.fpvy
        myblx=int(newx)
        mybly=int(newy+GS)
        mytrx=int(newx+GS)
        mytry=int(newy)
        if newy > (self.maxy+64):
            self.HP=0
        for enemy in self.enemies:
            eneblx=int(enemy.fpx+15)
            enebly=int(enemy.fpy+GS-15)
            enetrx=int(enemy.fpx+GS-15)
            enetry=int(enemy.fpy+15)
            if not(enetrx <= myblx or mytrx <= eneblx or enebly <= mytry or enetry >= mybly) :
                if self.redamage_timer>0:
                    self.redamage_timer-=1
                    break
                else:
                    self.HP-=int(enemy.collidedamage*self.guardlist[self.state])
                    self.redamage_timer=self.redamage_time
                    break
            else:
                if self.redamage_timer>0:
                    self.redamage_timer-=1

        if(mybly<maxy and ~(ipoint[mybly//GS][myblx//GS]==False and ipoint[mytry//GS][myblx//GS]==False and \
            ipoint[mytry//GS][mytrx//GS]==False and ipoint[mybly//GS][mytrx//GS]==False)):
            for item in self.items:
                iteblx=int(item.fpx)
                itebly=int(item.fpy+GS)
                itetrx=int(item.fpx+GS)
                itetry=int(item.fpy)
                if not(itetrx <= myblx or mytrx <= iteblx or itebly <= mytry or itetry >= mybly) :
                    self.score+=item.point
                    if self.HP+item.recov>=100:
                        self.HP=100
                    else:
                        self.HP+=item.recov
                    if item.id==1:
                        self.clear=1
                    pygame.sprite.Sprite.kill(item)
                    ipoint[itetry//GS][iteblx//GS]=0
        if(mybly<maxy and ~(spoint[mybly//GS][myblx//GS]==False and spoint[mytry//GS][myblx//GS]==False and \
            spoint[mytry//GS][mytrx//GS]==False and spoint[mybly//GS][mytrx//GS]==False)):
            for spike in self.spikes:
                spiblx=int(spike.fpx+10)
                spibly=int(spike.fpy+GS-10)
                spitrx=int(spike.fpx+GS-10)
                spitry=int(spike.fpy+10)
                if not(spitrx <= myblx or mytrx <= spiblx or spibly <= mytry or spitry >= mybly) :
                    self.HP-=100
    def blockcollision_x(self):
        newx=self.fpx+self.fpvx
        newy=self.fpy
        myblx=int(newx)
        mybly=int(newy+GS)
        mytrx=int(newx+GS)
        mytry=int(newy)
        if(abs(self.fpvx)<1e-9 or mybly>=self.maxy):
            self.fpx=newx
            return
        if(bpoint[mybly//GS][myblx//GS]==False and bpoint[mytry//GS][myblx//GS]==False and \
           bpoint[mytry//GS][mytrx//GS]==False and bpoint[mybly//GS][mytrx//GS]==False):
            self.fpx=newx
            return
        if self.on_floor==True:
            if((self.fpvx>0.0 and bpoint[mytry//GS][mytrx//GS]==False) or \
               (self.fpvx<0.0 and bpoint[mytry//GS][myblx//GS]==False)):
                self.fpx=newx
                return
        """
        for block in self.blocks:
            bloblx=int(block.fpx)
            blobly=int(block.fpy+GS)
            blotrx=int(block.fpx+GS)
            blotry=int(block.fpy)
            if not(blotrx <= myblx or mytrx <= bloblx or blobly <= mytry or blotry >= mybly) :
                if self.fpvx > 0:
                    self.fpx=block.fpx-GS
                    self.fpvx=0
                elif self.fpvx < 0:
                    self.fpx=block.fpx+GS
                    self.fpvx=0
                break
            else:
                self.fpx=newx
        """
        if(self.fpvx>0.0 and bpoint[((mytry+mybly)//2)//GS][mytrx//GS]==True):
            self.fpx=(mytrx//GS)*GS-GS
            self.fpvx=0
            return
        elif(self.fpvx<0.0 and bpoint[((mytry+mybly)//2)//GS][myblx//GS]==True):
            self.fpx=(myblx//GS)*GS+GS
            self.fpvx=0
            return
        else:
            self.fpx=newx
    def blockcollision_y(self):
        newx=self.fpx
        newy=self.fpy+self.fpvy
        myblx=int(newx)
        mybly=int(newy+GS)
        mytrx=int(newx+GS)
        mytry=int(newy)
        if(mybly>=maxy):
            self.fpy=newy
            self.on_floor=False
            return
        if(bpoint[mybly//GS][(myblx+10)//GS]==False and bpoint[mytry//GS][(myblx+10)//GS]==False and \
           bpoint[mytry//GS][(mytrx-10)//GS]==False and bpoint[mybly//GS][(mytrx-10)//GS]==False):
            self.fpy=newy
            self.on_floor=False
            return
        if self.on_floor==True:
            return
        """
        for block in self.blocks:
            bloblx=int(block.fpx)
            blobly=int(block.fpy+GS)
            blotrx=int(block.fpx+GS)
            blotry=int(block.fpy)
            if not(blotrx <= myblx or mytrx <= bloblx or blobly <= mytry or blotry >= mybly) :
                if self.fpvy > 0:
                    self.fpy=block.fpy - GS
                    self.fpvy=0
                    self.on_floor=True
                    self.dive=False
                elif self.fpvy < 0:
                    self.fpy=block.fpy+GS
                    self.fpvy=0
                break
            else:
                self.fpy=newy
                self.on_floor=False
        """
        if(self.fpvy>0.0 and (bpoint[mybly//GS][(mytrx-2)//GS]==True or bpoint[mybly//GS][(myblx+2)//GS]==True)):
            self.fpy=(mybly//GS)*GS-GS
            self.fpvy=0.0
            self.on_floor=True
            self.jump_count=0
            self.dive=False
            return
        elif(self.fpvy<0.0 and (bpoint[mytry//GS][(mytrx-2)//GS]==True or bpoint[mytry//GS][(myblx+2)//GS]==True)):
            self.fpy=(mytry//GS)*GS+GS
            self.fpvy=0
            return
        else:
            self.fpy=newy
            self.on_floor=False


class Dattack(pygame.sprite.Sprite):
    images={}
    GS=32
    def __init__(self,id,x,y,live,grav,enemies,blocks,state):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.id=id
        self.image=self.images[id]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.fpx=float(self.rect.x)
        self.fpy=float(self.rect.y)
        self.fpvx=0
        self.fpvy=grav*(Speedtimes**2)
        self.livetimer=0
        self.limit=live//Speedtimes
        self.enemies=enemies
        self.blocks=blocks
        self.on_floor=False
        self.state=state
    def update(self):
        self.livetimer+=1
        if self.livetimer>self.limit:
            self.kill()
            return
        self.collision_x()
        if(self.alive()==True):
            self.collision_y()
        self.rect.x=int(self.fpx)
        self.rect.y=int(self.fpy)
    def collision_x(self):
        global Crushpoint
        global epoint
        newx=self.fpx+self.fpvx
        newy=self.fpy
        myblx=int(newx)
        mybly=int(newy+GS)
        mytrx=int(newx+GS)
        mytry=int(newy)
        if(mybly>=maxy or ~(bpoint[mytry//GS][myblx//GS]==False and bpoint[(mybly-5)//GS][myblx//GS]==False and\
                            bpoint[mytry//GS][mytrx//GS]==False and bpoint[(mybly-5)//GS][mytrx//GS]==False)):
            self.kill()
            return
        for enemy in self.enemies:
            eneblx=int(enemy.fpx)
            enebly=int(enemy.fpy+GS)
            enetrx=int(enemy.fpx+GS)
            enetry=int(enemy.fpy)
            if(self.state==1):
                eneblx=eneblx+12
                enebly=enebly-12
                enetrx=enetrx-12
                enetry=enetry+12
            if not(enetrx <= myblx or mytrx <= eneblx or enebly <= mytry or enetry >= mybly) :
                Crushpoint+=enemy.point
                if enemy.id>10:
                    self.clear=1
                pygame.sprite.Sprite.kill(enemy)
                epoint[enetry//GS][eneblx//GS]=0
                epoint[enebly//GS][enetrx//GS]=0
        
        """for block in self.blocks:
            bloblx=int(block.fpx)
            blobly=int(block.fpy+GS)
            blotrx=int(block.fpx+GS)
            blotry=int(block.fpy)
            if not(blotrx <= myblx or mytrx <= bloblx or blobly <= mytry or blotry >= mybly) :
                self.kill()
            else:
                self.fpx=newx"""

    def collision_y(self):
        global Crushpoint
        global epoint
        newx=self.fpx
        newy=self.fpy+self.fpvy
        myblx=int(newx)
        mybly=int(newy+GS)
        mytrx=int(newx+GS)
        mytry=int(newy)
        if(mybly>=maxy):
            self.kill()
            return
        for enemy in self.enemies:
            eneblx=int(enemy.fpx)
            enebly=int(enemy.fpy+GS)
            enetrx=int(enemy.fpx+GS)
            enetry=int(enemy.fpy)
            if(self.state==1):
                eneblx=eneblx+8
                enebly=enebly-8
                enetrx=enetrx-8
                enetry=enetry+8
            if not(enetrx <= myblx or mytrx <= eneblx or enebly <= mytry or enetry >= mybly) :
                Crushpoint+=enemy.point
                if enemy.id>10:
                    self.clear=1
                pygame.sprite.Sprite.kill(enemy)
                epoint[enetry//GS][eneblx//GS]=0
                epoint[enebly//GS][enetrx//GS]=0
        if(bpoint[mybly//GS][myblx//GS]==False and bpoint[mytry//GS][myblx//GS]==False and \
           bpoint[mytry//GS][mytrx//GS]==False and bpoint[mybly//GS][mytrx//GS]==False):
            self.fpy=newy
            self.on_floor=False
            return
        if (abs(self.fpvy)<1e-9 or self.on_floor==True):
            self.fpy=newy
            return
        for block in self.blocks:
            bloblx=int(block.fpx)
            blobly=int(block.fpy+GS)
            blotrx=int(block.fpx+GS)
            blotry=int(block.fpy)
            if not(blotrx <= myblx or mytrx <= bloblx or blobly <= mytry or blotry >= mybly) :
                if self.fpvy > 0:

                    self.fpy=block.rect.top - GS
                    self.fpvy=0
                    self.on_floor=True
                elif self.fpvy < 0:
                    self.fpy=block.rect.bottom
                    self.fpvy=0
                break
            else:
                self.fpy=newy
                self.on_floor=False

                    
           
class Block(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.rect=self.image.get_rect()
        self.rect.topleft=pos
        self.fpx=pos[0]
        self.fpy=pos[1]

class Spike(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.rect=self.image.get_rect()
        self.rect.topleft=pos
        self.fpx=pos[0]
        self.fpy=pos[1]

class Item(pygame.sprite.Sprite):
    vx=0
    vy=0
    recov=0
    GRAVITY=0
    act=0
    point=0
    images={}
    def __init__(self,id,pos,vx,vy,recov,point,grav,act,blocks):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.id=id
        self.image=self.images[id]
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y=pos[0],pos[1]
        self.fpx=float(self.rect.x)
        self.fpy=float(self.rect.y)
        self.fpvx=vx
        self.fpvy=vy
        self.point=point
        self.GRAVITY=grav
        self.recov=recov
        self.on_floor=False
        self.blocks=blocks   

class Enemy(pygame.sprite.Sprite):
    vx=0
    vy=0
    collidedagamage=0
    GRAVITY=0
    HP=0
    deff=0
    resi=0
    images={}
    global epoint
    def __init__(self,id,pos,vx,vy,cold,hp,point,deff,resi,grav,act,blocks):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.id=id
        self.image=self.images[id]
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y=pos[0],pos[1]
        self.HP=hp
        self.GRAVITY=grav*(Speedtimes**2)
        self.point=point
        self.fpx=float(self.rect.x)
        self.fpy=float(self.rect.y)
        self.initvy=vy
        self.initvx=vx
        self.fpvx=-vx*Speedtimes
        self.fpvy=vy*Speedtimes
        self.act=act
        self.on_floor=False
        self.blocks=blocks
        self.collidedamage=cold
    def update(self):
        if(self.fpy>maxy+24):
            epoint[self.fpy//GS][self.fpx//GS]=0
            self.kill()
            return
        if(self.fpx>(mapleftx-GS) and self.fpx<(maprightx+GS) and self.fpy>(maptopy-GS) and self.fpy<(mapbottomy+GS)):
            if(self.act==1):
                if(abs(self.fpy-pythony)<5.0):
                    if(self.fpx>pythonx):
                        self.fpvx=-10*Speedtimes
                    elif(self.fpx<=pythonx):
                        self.fpvx=10*Speedtimes
                else:
                    self.fpvx=self.fpvx/abs(self.fpvx)*self.initvx
            self.blockcollision_x()
            self.blockcollision_y()
        self.rect.x=int(self.fpx)
        self.rect.y=int(self.fpy)
        if(self.fpx>(mapleftx-GS) and self.fpx<(maprightx+GS) and self.fpy>(maptopy-GS) and self.fpy<(mapbottomy+GS)):
            if not self.on_floor:
                self.fpvy += self.GRAVITY

    def blockcollision_x(self):
        newx=self.fpx+self.fpvx
        newy=self.fpy
        myblx=int(newx)
        mybly=int(newy+GS)
        mytrx=int(newx+GS)
        mytry=int(newy)
        epoint[int(self.fpy)//GS][int(self.fpx)//GS]=0
        if(abs(self.fpvx)<1e-9 or mybly>=maxy):
            self.fpx=newx
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            return
        if(bpoint[mybly//GS][myblx//GS]==False and bpoint[mytry//GS][myblx//GS]==False and \
           bpoint[mytry//GS][mytrx//GS]==False and bpoint[mybly//GS][mytrx//GS]==False):
            self.fpx=newx
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            return
        if self.on_floor==True or abs(self.GRAVITY)<1e-9:
            if((self.fpvx>0.0 and bpoint[mytry//GS][mytrx//GS]==False) or \
               (self.fpvx<0.0 and bpoint[mytry//GS][myblx//GS]==False)):
                self.fpx=newx
                epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
                return
        """
        for block in self.blocks:
            bloblx=int(block.fpx)
            blobly=int(block.fpy+GS)
            blotrx=int(block.fpx+GS)
            blotry=int(block.fpy)
            if not(blotrx <= myblx or mytrx <= bloblx or blobly <= mytry or blotry >= mybly) :
                if self.fpvx > 0:
                    self.fpx=block.fpx-GS
                    self.fpvx*=-1.0
                elif self.fpvx < 0:
                    self.fpx=block.fpx+GS
                    self.fpvx*=-1.0
                break
            else:
                self.fpx=newx
        """

        if(self.fpvx>0.0 and bpoint[mytry//GS][mytrx//GS]==True):
            self.fpx=(mytrx//GS)*GS-GS
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            self.fpvx*=-1.0
            return
        if(self.fpvx<0.0 and bpoint[mytry//GS][myblx//GS]==True):
            self.fpx=(myblx//GS)*GS+GS
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            self.fpvx*=-1.0
            return
    def blockcollision_y(self):
        if(abs(self.GRAVITY)<1e-9 and self.act==0):
            return
        epoint[int(self.fpy)//GS][int(self.fpx)//GS]=0
        newx=self.fpx
        newy=self.fpy+self.fpvy
        myblx=int(newx)
        mybly=int(newy+GS)
        mytrx=int(newx+GS)
        mytry=int(newy)
        if(mybly>=maxy):
            self.fpy=newy
            if(newy<maxy):
                epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            else:
                self.kill()
            self.on_floor=False
            return
        if(bpoint[mybly//GS][myblx//GS]==False and bpoint[mytry//GS][myblx//GS]==False and \
           bpoint[mytry//GS][mytrx//GS]==False and bpoint[mybly//GS][mytrx//GS]==False):
            self.fpy=newy
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            self.on_floor=False
            return
        if self.on_floor==True:
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            return
        """
        for block in self.blocks:
            bloblx=int(block.fpx)
            blobly=int(block.fpy+GS)
            blotrx=int(block.fpx+GS)
            blotry=int(block.fpy)
            if not(blotrx <= myblx or mytrx <= bloblx or blobly <= mytry or blotry >= mybly) :
                if self.fpvy > 0:
                    self.fpy=block.fpy - GS
                    self.fpvy=0
                    self.on_floor=True
                elif self.fpvy < 0:
                    self.fpy=block.fpy+GS
                    self.fpvy=0
                break
            else:
                self.fpy=newy
                self.on_floor=False
        """
        if(self.fpvy>0.0 and (bpoint[mybly//GS][(mytrx-2)//GS]==True or bpoint[mybly//GS][(myblx+2)//GS]==True)):
            self.fpy=(mybly//GS)*GS-GS
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            self.fpvy=self.initvy
            self.on_floor=True
            self.dive=False
            return
        elif(self.fpvy<0.0 and (bpoint[mytry//GS][(mytrx-2)//GS]==True or bpoint[mytry//GS][(myblx+2)//GS]==True)):
            self.fpy=(mytry//GS)*GS+GS
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            self.fpvy=-self.initvy
            return
        else:
            self.fpy=newy
            epoint[int(self.fpy)//GS][int(self.fpx)//GS]=1
            self.on_floor=False

class Map:
    GS=32

    def __init__(self,filename):
        self.all=pygame.sprite.RenderUpdates()
        self.blocks=pygame.sprite.Group()
        self.enemies=pygame.sprite.Group()
        self.items=pygame.sprite.Group()
        self.spikes=pygame.sprite.Group()
        Python.containers=self.all
        Block.containers=self.all,self.blocks
        Enemy.containers=self.all,self.enemies
        Item.containers=self.all,self.items
        Spike.containers=self.all,self.spikes
        Dattack.containers=self.all
        self.px=0.0
        self.py=0.0
        self.goalx=0.0
        self.goaly=0.0
        self.load(filename)
        self.surface=pygame.Surface((self.col*self.GS,self.row*self.GS)).convert()

    def draw(self):
        self.q=0
        self.surface.fill((0,0,0))
        self.all.draw(self.surface)
    def update(self):
        self.all.update()

    def load(self,filename):
        global firstdif
        global bpoint
        global ipoint
        global epoint
        global spoint
        global maxy
        map=[]
        enemy=[]
        item=[]
        fp=open(filename,"r")
        for line in fp:
            line=line.rstrip()
            map.append(list(line))
            self.row=len(map)
            self.col=len(map[0])
        bpoint=np.zeros(self.row*self.col,dtype=np.int).reshape(self.row,self.col)
        ipoint=np.zeros(self.row*self.col,dtype=np.int).reshape(self.row,self.col)
        epoint=np.zeros(self.row*self.col,dtype=np.int).reshape(self.row,self.col)
        spoint=np.zeros(self.row*self.col,dtype=np.int).reshape(self.row,self.col)
        self.width=self.col*self.GS
        self.height=self.row*self.GS
        maxy=self.height
        fp.close()
        fp2=open('data/monster.ene',"r")
        for line in fp2:
            line=line.rstrip()
            if line.startswith("#"): continue
            data=line.split(",")
            enemy.append(list(data))
        fp2.close()
        fp3=open('data/item.item',"r")
        for line in fp3:
            line=line.rstrip()
            if line.startswith("#"): continue
            data=line.split(",")
            item.append(list(data))
        fp3.close()
            

        for i in range(self.row):
            for j in range(self.col):
                isearch=re.search(r"[0-9]",map[i][j])
                if map[i][j]=='#':
                    Block((j*self.GS,i*self.GS))
                    bpoint[i,j]=1
                elif map[i][j]=='A':
                    id=0
                    Enemy(id,(j*self.GS,i*self.GS),int(enemy[id][1]),int(enemy[id][2]),int(enemy[id][3]),int(enemy[id][4]),int(enemy[id][5]),int(enemy[id][6]),int(enemy[id][7]),float(enemy[id][8]),int(enemy[id][9]),self.blocks)
                elif map[i][j]=='C':
                    id=1
                    Enemy(id,(j*self.GS,i*self.GS),int(enemy[id][1]),int(enemy[id][2]),int(enemy[id][3]),int(enemy[id][4]),int(enemy[id][5]),int(enemy[id][6]),int(enemy[id][7]),float(enemy[id][8]),int(enemy[id][9]),self.blocks)
                elif map[i][j]=='B':
                    id=2
                    Enemy(id,(j*self.GS,i*self.GS),int(enemy[id][1]),int(enemy[id][2]),int(enemy[id][3]),int(enemy[id][4]),int(enemy[id][5]),int(enemy[id][6]),int(enemy[id][7]),float(enemy[id][8]),int(enemy[id][9]),self.blocks)
                elif map[i][j]=='D':
                    id=3
                    Enemy(id,(j*self.GS,i*self.GS),int(enemy[id][1]),int(enemy[id][2]),int(enemy[id][3]),int(enemy[id][4]),int(enemy[id][5]),int(enemy[id][6]),int(enemy[id][7]),float(enemy[id][8]),int(enemy[id][9]),self.blocks)
                elif map[i][j]=='E':
                    id=4
                    Enemy(id,(j*self.GS,i*self.GS),int(enemy[id][1]),int(enemy[id][2]),int(enemy[id][3]),int(enemy[id][4]),int(enemy[id][5]),int(enemy[id][6]),int(enemy[id][7]),float(enemy[id][8]),int(enemy[id][9]),self.blocks)
                elif map[i][j]=='P':
                    self.px=j*self.GS
                    self.py=i*self.GS
                elif map[i][j]=='*':
                    Spike((j*self.GS,i*self.GS))
                    spoint[i,j]=1
                elif isearch:
                    id=int(map[i][j])
                    Item(id,(j*self.GS,i*self.GS),int(item[id][1]),int(item[id][2]),int(item[id][3]),int(item[id][4]),float(item[id][5]),int(item[id][6]),self.blocks)
                    ipoint[i,j]=1
                    if id==1:
                        self.goalx=j*self.GS
                        self.goaly=i*self.GS
                        ipoint[i,j]=1
                    if id==0:
                        ipoint[i,j]=1
        self.python=Python((self.px,self.py),self.blocks,self.enemies,self.items,self.height,self.spikes)
        firstdif=(math.sqrt(abs(self.goalx-self.python.fpx)/2.0))

    def calc_offset(self):
        offsetx=self.python.rect.center[0]-SCR_RECT.width/2
        offsety=self.python.rect.center[1]-SCR_RECT.height/2
        return offsetx,offsety


def load_image(filename,colorkey=None):
    filename=os.path.join("data",filename)
    try:
        image=pygame.image.load(filename)
    except pygame.error(message):
        print("Cannot Load image:",filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey= image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image

def discrete_actuator_force(action):
    controller=[]
    if action[0]>0.5:
        controller.append(10.0)
    else:
        controller.append(-10.0)
    if action[1]>0.5:
        controller.append(10.0)
    else:
        controller.append(-10.0)
    if action[2]>0.5:
        controller.append(10.0)
    else:
        controller.append(-10.0)
    if action[3]>0.5:
        controller.append(10.0)
    else:
        controller.append(-10.0)
    if action[4]>0.5:
        controller.append(10.0)
    else:
        controller.append(-10.0)
    if action[5]>0.5:
        controller.append(10.0)
    else:
        controller.append(-10.0)
    return controller

def parser():
    usage='Usage: python{} musictrain.py --stage [STAGENAME.map]'.format(__file__)
    arguments=sys.argv
    stage_position=""
    if len(arguments)!=3:
        print(usage)
        quit()
    arguments.pop(0)
    frame=arguments[0]
    options=[option for option in arguments if option.startswith('-')]
    if '-h' in options or '--help' in options:
        print(usage)
        quit()
    if '-s' in options or '--stage' in options:
        stage_position=arguments.index('-s')\
                        if '-s' in options else arguments.index('--stage')
        stage_file=arguments[stage_position+1]
        stage_file="data/"+stage_file
        PyAction(0,stage_file)

if __name__ == "__main__":
    parser()
    #PyAction(0,"data/test6.map")

