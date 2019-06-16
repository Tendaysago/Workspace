#!/usr/bin/env python
#coding: utf-8

from __future__ import print_function

import os
import pickle
#import pygame
#from pygame.locals import*
import sys
import re
import math
import neat
import visualize
import snaketrain2
import numpy as np
import random
from time import sleep
#from time import sleep
runs_per_net = 5
Speedtimes=1
simulation_seconds = 50000.0//Speedtimes
sim=[]
action=[]
numtimes=0
frameskip=2
lastcleared=set()
clearnum=0
nowstageindex=0
nowtry=1
firstclear=False
firstclearnum=-1
stableclear=1
clearinfo=[]
stage_list=[]
trainend=False
actorconfig_path=[]
actorconfig=[]
EnemyNets=[]
JumpNets=[]
NoNets=[]
nowBest=0.0
# Use the NN network phenotype and the discrete actuator force function.
def eval_network(net,net_input):
    assert(len(net_input)==16)
    return np.argmax(net.activate(net_input))


def eval_genome(genome, config,stage):
    global sim,action
    global numtimes
    global lastcleared
    global clearnum
    global firstclear
    global firstclearnum
    global nowstageindex
    global nowBest
    cleared=set()
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    #net = neat.nn.RecurrentNetwork.create(genome,config)
    trystage="data/multi"+str(stage)+".map"
    fitness=0.0
    for i in range(1):
        sim=snaketrain2.PyAction(0,trystage)
        firstxdif=(math.sqrt(abs(sim.map.goalx-sim.map.python.fpx)/2.0))
        checkact=0
        # Run the given simulation for up to num_steps time steps.
        bonus = 0.0
        hp=0.0
        score=0.0
        clear=False
        checkact=0
        prev_action=0
        prev_inputs=[]
        while sim.game_state!=2 and sim.game_state!=3 and sim.t < simulation_seconds:
            if(checkact%20==0):
                metainputs=sim.get_metainfo()
                choice=eval_network(net,metainputs)
                if(choice==0):
                    actor=neat.nn.FeedForwardNetwork.create(NoNets[choice],actorconfig)
                elif(choice>=1 and choice<=15):
                    actor=neat.nn.FeedForwardNetwork.create(EnemyNets[choice-1],actorconfig)
                else:
                    choice-=15
                    actor=neat.nn.FeedForwardNetwork.create(JumpNets[choice-1],actorconfig)
            if(checkact%frameskip==0):
                inputs = sim.get_displayinfo()
                #print(inputs)
                prev_inputs=inputs
                action = np.argmax(actor.activate(inputs))
                prev_action=action
            else:
                inputs=prev_inputs
                action = prev_action
            checkact+=1
            sim.running(action)
            hp=sim.map.python.HP
            score=sim.map.python.score
            x=sim.map.python.fpx
            y=sim.map.python.fpy
            if sim.game_state==2 or sim.t>=simulation_seconds:
                bonus=-10.0
            elif sim.game_state==3:
                clear=True
        if(clear==True):
            global trainend
            fitness+=150+hp+score//50+sim.gametime//60
            if(trainend==False):
                trainend=True
                clearinfo.append((nowtry,100.0))
                #with open('Results/multifull'+str(stage)+'.txt','a') as f:
                #    f.write("("+str(nowtry)+","+str(100.0)+")")
                #    f.write('\n')
        #fitness = sim.map.python.HP/4.0+sim.map.python.score/100.0+bonus-math.sqrt((sim.map.python.rect.x-sim.map.goalx)**2+(sim.map.python.rect.y-sim.map.goaly)**2)/20.0
        else:
            fitness =fitness + bonus+hp//20+score//50+firstxdif-(math.sqrt(abs(sim.map.goalx-x)/2.0))
            #print(hp,score,x,y)
        #math.sqrt((sim.map.python.rect.x-sim.map.goalx)**2+(sim.map.python.rect.y-sim.map.goaly)**2)/20.0
        if(nowBest<(x/sim.map.goalx)*100):
            nowBest=(x/sim.map.goalx)*100
        del sim
    #pygame.quit()
    #del sim
    #print(numtimes,fitness)
    #fitnesses.append(fitness)
    # The genome's fitness is its worst performance across all runs.
    if(len(cleared)>len(lastcleared)):
        lastcleared=cleared
    return fitness


def eval_genomes(genomes, config):
    global clearnum
    global nowstageindex
    global nowtry
    global firstclear
    global firstclearnum
    global stableclearnum
    global trainend
    global clearinfo
    print("Now try multi stage No."+str(stage_list[nowstageindex]))
    clearnum=0
    for genome_id,genome in genomes:
        genome.fitness=eval_genome(genome,config,stage_list[nowstageindex])
    print(nowstageindex)
    print(nowtry,clearnum)
    print('Now Max progress is '+str(nowBest)+'%')
    nowtry+=1

def run(file_number):
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    global clearinfo
    global stage_list
    global actorconfig_path
    global actorconfig
    stage_list=[]
    stage_list.append(int(file_number))
    print(stage_list)
    local_dir = os.path.dirname(__file__)
    actorconfig_path = os.path.join(local_dir, 'config-feed-action')
    actorconfig = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         actorconfig_path)
    config_path=os.path.join(local_dir, 'config-action-multi')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    with open('Network/noconnect','rb') as f:
        c=pickle.load(f)
    NoNets.append(c)
    for i in range(15):
        index=i+15
        with open('Network/winner-action-enemy-'+str(index),'rb') as f:
            c=pickle.load(f)
        EnemyNets.append(c)
    print('Enemy Nets stanby complete.')
    sleep(5)
    for i in range(15):
        index=i+10
        if(index>=15):
            index+=1
        with open('Network/winner-action-jump-'+str(index),'rb') as f:
            c=pickle.load(f)
        JumpNets.append(c)
    print('Jump Nets stanby complete.')
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    winner = pop.run(eval_genomes,200)
    """if(trainend==False):
        clearinfo.append((-1,round(nowBest,3)))
        with open('Results/multifull'+str(file_number)+'.txt','a') as f:
            f.write("(-1,"+str(round(nowBest,3))+")")
            f.write('\n')"""

    # Save the winner.
    with open('Network/winner-multi-No'+file_number, 'wb') as f:
        pickle.dump(winner, f)

    #print(winner)
    print("Now Multi Stage with Full Network version Clear info is ")
    print(clearinfo)

    #visualize.plot_stats(stats, ylog=False, view=False, filename="feed-fitness-fs-sigmoid-50hidden-50.svg")
    #visualize.plot_species(stats, view=False, filename="feed-speciation-fs-sigmoid-50hidden-150.svg")

    node_names = {-1: 'Blocknum', -2: 'Enemynum', -3: 'Spikenum', -4: 'Itemnum',-5:'now_HP',-6:'vx',-7:'vy',\
                  -8: 'now_mode', -9: 'on_floor?',-10:'now_dive?',-11:'can_rejump?',-12:'can_attack?',-13:'nowx',\
                  -14:'nowy',-15:'now_score',-16:'rest_time',\
                  0: 'None',1:'Enemy1',2:'Enemy2',3:'Enemy3',4:'Enemy4',5:'Enemy5',6:'Enemy6',7:'Enemy7',8:'Enemy8',\
                  9:'Enemy9',10:'Enemy10',11:'Enemy11',12:'Enemy12',13:'Enemy13',14:'Enemy14',15:'Enemy15',\
                  16:'Jump1',17:'Jump2',18:'Jump3',19:'Jump4',20:'Jump5',21:'Jump6',22:'Jump7',23:'Jump8',\
                  24:'Jump9',25:'Jump10',26:'Jump11',27:'Jump12',28:'Jump13',29:'Jump14',30:'Jump15'
    }
    #visualize.draw_net(config, winner, True, node_names=node_names)

    #visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                   filename="winner-multi"+file_number+"full.gv")
    #visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                   filename="winner-multi-enabled-"+file_number+"frll.gv", show_disabled=False)
    #visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                   filename="winner-multi-enabled-pruned-"+file_number+"frll.gv", show_disabled=False, prune_unused=True)



def parser():
    global trainend
    global nowtry
    global nowBest
    usage='Usage: python {} --stage [Number]'.format(__file__)
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
        num_position=arguments.index('-s')\
                        if '-s' in options else arguments.index('--stage')
        num_file=arguments[num_position+1]
        for i in range(20):
            nowtry=0
            trainend=False
            nowBest=0.0
            run(num_file)
        for data in clearinfo:
            print(data)
        print(clearinfo)

if __name__ == '__main__':
    parser()
