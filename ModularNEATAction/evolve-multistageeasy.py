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
    global clearinfo
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
                with open('Results/multieasy'+str(stage)+'.txt','a') as f:
                    f.write("("+str(nowtry)+","+str(100.0)+")")
                    f.write('\n')
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
        index=i+1
        with open('Network/easyenemy/winner-action-easyenemy-'+str(index),'rb') as f:
            c=pickle.load(f)
        EnemyNets.append(c)
    print('Enemy Nets stanby complete.')
    sleep(5)
    for i in range(15):
        index=i+1
        with open('Network/easyjump/winner-action-easyjump-'+str(index),'rb') as f:
            c=pickle.load(f)
        JumpNets.append(c)
    print('Jump Nets stanby complete.')
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    winner = pop.run(eval_genomes,200)
    if(trainend==False):
        clearinfo.append((-1,round(nowBest,3)))
        with open('Results/multieasy'+str(file_number)+'.txt','a') as f:
            f.write("(-1,"+str(round(nowBest,3))+")")
            f.write('\n')
    
    # Save the winner.
    #with open('Network/winner-multi-No'+file_number, 'wb') as f:
    #    pickle.dump(winner, f)

    #print(winner)
    print("Now Multi Stage with Easy10's Network version Clear info is ")
    print(clearinfo)

    #visualize.plot_stats(stats, ylog=False, view=False, filename="feed-fitness-fs-sigmoid-50hidden-50.svg")
    #visualize.plot_species(stats, view=False, filename="feed-speciation-fs-sigmoid-50hidden-150.svg")

    node_names = {-1: '(-3,-3)', -2: '(-2,-3)', -3: '(-1,-3)', -4: '(0,-3)', -5: '(1,-3)',-6: '(2,-3)', -7: '(3,-3)',\
                  -8: '(-3,-2)', -9: '(-2,-2)', -10: '(-1,-2)', -11: '(0,-2)', -12: '(1,-2)', -13:'(2,-2)', -14:'(3,-2)',\
                  -15: '(-3,-1)', -16: '(-2,-1)', -17:'(-1,-1)',-18:'(0,-1)',-19:'(1,-1)',-20:'(2,-1)',-21:'(3,-1)',\
                  -22: '(-3,0)', -23: '(-2,0)', -24:'(-1,0)',-25:'(0,0)',-26:'(1,0)',-27:'(2,0)',-28:'(3,0)',\
                  -29: '(-3,1)', -30: '(-2,1)', -31:'(-1,1)',-32:'(0,1)',-33:'(1,1)',-34:'(2,1)',-35:'(3,1)',\
                  -36: '(-3,2)', -37: '(-2,2)', -38:'(-1,2)',-39:'(0,2)',-40:'(1,2)',-41:'(2,2)',-42:'(3,2)',\
                  -43: '(-3,3)', -44: '(-2,3)', -45:'(-1,3)',-46:'(0,3)',-47:'(1,3)',-48:'(2,3)',-49:'(3,3)',\
                  -50:'vx',-51: 'vy',-52:'now_mode',-53:'on_floor?',-54:'now_dive?',-55:'now_HP',-56:'can_rejump?',-57:'can_attack?',\
                  0: 'None',1:'←',2:'↑',3:'→',4:'↓',5:'↑+←',6:'↑+→',7:'↓+→',8:'↓+←',9:'Z',10:'←+Z',11:'↑+Z',\
                  12:'→+Z',13:'↓+Z',14:'↑+←+Z',15:'↑+→+Z',16:'↓+→+Z',17:'↓+←+Z',18:'C',19:'←+C',20:'→+C'
    }
    #visualize.draw_net(config, winner, True, node_names=node_names)

    #visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                   filename="winner-feed-jump-"+file_number+".gv")
    #visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                   filename="winner-feed-jump-enabled-"+file_number+".gv", show_disabled=False)
    #visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                   filename="winner-feed-jump-enabled-pruned-"+file_number+".gv", show_disabled=False, prune_unused=True)



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
