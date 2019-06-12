#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Simple Baseball Simulator
Created on Sat Mar 30 23:59:36 2019
@author: edwardmwadsworth

"""
from random import randint
import pandas as pd

# GLOBAL VARIABLES
# GSB stands for Game Status Board.
# Initialize GSB

Team=['VISITOR','HOME']

def InitializeGSB():
    global GSB
    GSB = dict( Inning          = 1,
                Score           = {Team[0]:0, Team[1]:0},
                Team_at_Bat     = Team[0],
                Bat_Team_Status = dict(Outs      = 0,
                                       Bases     = [0,0,0],    # 1st, 2nd, 3rd 
                                       Batter_Up = dict(Strikes=0, Balls=0))
            )
                
# PROGRAM FUNCTIONS
    
def Game_Over():
    Game_Over = True
    if GSB['Inning']<9:
        Game_Over = False
   # If we're in the bottom of 9th, and the first team is trailing, the game is over
    if GSB['Inning']==9:
        if GSB['Team_at_Bat']==Team[0]:
            Game_Over = False
        if GSB['Bat_Team_Status']['Outs'] < 3 and GSB['Score'][Team[0]] > GSB['Score'][Team[1]]:
            Game_Over = False
# tie game at bottom of ninth:               
#       if GSB['Score'][Team[0]] == GSB['Score'][Team[1]]:
#           Game_Over = False    
# overtime option, continue until one team scores
#   if GSB['Inning'] > 9 and GSB['Score'][Team[0]] == GSB['Score'][Team[1]]:
#       Game_Over = False
    return Game_Over

def Team_Up():
    GSB['Bat_Team_Status'] = dict(Outs      = 0,
                                  Bases     = [0,0,0],    # 1st, 2nd, 3rd 
                                  Batter_Up = dict(Strikes=0, Balls=0))  # Always re-initialize batting team round stats
    if GSB['Team_at_Bat'] == Team[0]:   # If VISITOR was at bat at top
        GSB['Team_at_Bat'] = Team[1]    # HOME goes to bat at bottom of inning
    else:
        GSB['Team_at_Bat'] = Team[0]    # else put HOME at bat 
        GSB['Inning'] += 1              # and increase inning....

def Batter_Up():
    if GSB['Bat_Team_Status']['Outs'] < 3:
        GSB['Bat_Team_Status']['Batter_Up'] = dict(Strikes=0, Balls=0)
    else:
        Team_Up()
        
# NOW, HERE ARE THE 11 "PITCH FUNCTIONS":
def Double():
    GSB['Bat_Team_Status']['Bases'].insert(0,1)
    GSB['Bat_Team_Status']['Bases'].insert(0,0)    
    GSB['Score'][GSB['Team_at_Bat']] += GSB['Bat_Team_Status']['Bases'].pop()
    GSB['Score'][GSB['Team_at_Bat']] += GSB['Bat_Team_Status']['Bases'].pop()    
    Batter_Up()
   
def Single():
    GSB['Bat_Team_Status']['Bases'].insert(0,1)
    GSB['Score'][GSB['Team_at_Bat']] += GSB['Bat_Team_Status']['Bases'].pop()
    Batter_Up()

def BOE():
    if GSB['Bat_Team_Status']['Bases'] in [[1,0,0],[1,1,0],[1,1,1]]:
        GSB['Bat_Team_Status']['Bases'].insert(0,1)
        GSB['Score'][GSB['Team_at_Bat']] += GSB['Bat_Team_Status']['Bases'].pop()
    if GSB['Bat_Team_Status']['Bases'] == [1,0,1]:
        GSB['Bat_Team_Status']['Bases']= [1,1,1]
    if GSB['Bat_Team_Status']['Bases'][0] == 0:
        GSB['Bat_Team_Status']['Bases'][0] = 1    
    Batter_Up()

# In "base on balls" the batter goes to first. The other players advance to 
# the next base, only if they have to (another player is coming for their base).
def BOB():
    if GSB['Bat_Team_Status']['Bases'] in [[1,0,0],[1,1,0],[1,1,1]]:
        GSB['Bat_Team_Status']['Bases'].insert(0,1)
        GSB['Score'][GSB['Team_at_Bat']] += GSB['Bat_Team_Status']['Bases'].pop()
    if GSB['Bat_Team_Status']['Bases'] == [1,0,1]:
        GSB['Bat_Team_Status']['Bases']= [1,1,1]
    if GSB['Bat_Team_Status']['Bases'][0] == 0:
        GSB['Bat_Team_Status']['Bases'][0] = 1    
    Batter_Up()

def Strike():
    GSB['Bat_Team_Status']['Batter_Up']['Strikes'] += 1
    if GSB['Bat_Team_Status']['Batter_Up']['Strikes'] == 3: # 3 strikes, you're out!
        GSB['Bat_Team_Status']['Outs'] += 1
        Batter_Up()

# In foul out, no player on base advances.       
def Foul_Out():
    GSB['Bat_Team_Status']['Outs'] += 1
    Batter_Up()

# Out at first presumes that the other players advance a base. It also presumes that
# the defense would out the man on third before outing the hitter, if only it could!
# If the bases are loaded, then the man at third gets to home. 
# The base states of [0,1,0], [0,0,1],[0,1,1] remain unchanged.       
def Out_at_First():
    GSB['Bat_Team_Status']['Outs'] += 1
    if GSB['Bat_Team_Status']['Outs'] < 3:
        if GSB['Bat_Team_Status']['Bases'] in [[1,0,0],[1,1,0],[1,1,1]]:
            GSB['Bat_Team_Status']['Bases'].insert(0,0)
             # Man on 3rd can score, if bases loaded.
            GSB['Score'][GSB['Team_at_Bat']] += GSB['Bat_Team_Status']['Bases'].pop()
        if GSB['Bat_Team_Status']['Bases'] in [[1,0,1]]:
            GSB['Bat_Team_Status']['Bases'] = [0,1,1] # Man on 3rd dares not try!
    Batter_Up()    

# In Fly_Out, each player on base advances, provided it is not the 3rd out.
def Fly_Out():
    GSB['Bat_Team_Status']['Outs'] += 1
    if GSB['Bat_Team_Status']['Outs'] < 3:
            GSB['Bat_Team_Status']['Bases'].insert(0,0)
            # runner on 3rd base scores!
            GSB['Score'][GSB['Team_at_Bat']] += GSB['Bat_Team_Status']['Bases'].pop()   
    Batter_Up()

def Double_Play():
    GSB['Bat_Team_Status']['Outs'] += 1    # Assume batter is out
    MenOnBase = GSB['Bat_Team_Status']['Bases'].count(1)  # Can out 1 more, if available!
    if GSB['Bat_Team_Status']['Outs'] < 3 and MenOnBase > 0:
        GSB['Bat_Team_Status']['Bases'].remove(1)
        GSB['Bat_Team_Status']['Bases'].insert(0,0)
        GSB['Bat_Team_Status']['Outs'] += 1
        MenOnBase -= 1
    Batter_Up()
    
def Triple_Play():
    GSB['Bat_Team_Status']['Outs'] += 1    # Assume batter is out
    MenOnBase = GSB['Bat_Team_Status']['Bases'].count(1) # Can only out 2 more, if available!
    while GSB['Bat_Team_Status']['Outs'] < 3 and MenOnBase > 0:
        GSB['Bat_Team_Status']['Bases'].remove(1)
        GSB['Bat_Team_Status']['Bases'].insert(0,0)
        GSB['Bat_Team_Status']['Outs'] += 1
        MenOnBase -= 1
    Batter_Up()

def Home_Run():
    GSB['Score'][GSB['Team_at_Bat']] += 1 + sum(GSB['Bat_Team_Status']['Bases'])
    GSB['Bat_Team_Status']['Bases'] = [0,0,0]  # Clear bases
    Batter_Up()


def Pitch():

    def RollEm():
        Roll = randint(1,6), randint(1,6)
        return (min(Roll),max(Roll))

    Roll = RollEm()
    if Roll == (1, 1):
        Double()
    if Roll in [(1, 2),(1, 3),(1, 4)]:
        Single()        
    if Roll == (1, 5):
        BOE()        
    if Roll == (1, 6):
        BOB()       
    if Roll in [(2, 2),(2, 3),(2, 4),(2, 5)]:
        Strike()       
    if Roll == (2, 6):
        Foul_Out()       
    if Roll in [(3, 3),(3, 4),(3, 5),(3, 6)]:
        Out_at_First()       
    if Roll in [(4, 4),(4, 5),(4, 6)]:
        Fly_Out()       
    if Roll == (5, 5):
        Double_Play()        
    if Roll == (5, 6):
        Triple_Play()        
    if Roll == (6, 6):
        Home_Run()
        
def Game():
    InitializeGSB()
    # InitializeCount()
    Num_of_Plays = 0
    while not Game_Over():
        Num_of_Plays += 1
        Pitch()
    return Num_of_Plays, GSB['Score']
    
def Stats( NumGames=100):
    Plays_per_Game = []
    Runs_per_Game  = []
    for n in range(1, NumGames+1):
        game = Game()
        Plays_per_Game.append( game[0])
        Runs_per_Game.append( game[1]['HOME'] + game[1]['VISITOR'])
    return Plays_per_Game, Runs_per_Game

def Run_Program():
    Plays, Runs = Stats(1000)    # games
    SF = pd.DataFrame([Plays, Runs], index=['Plays','Runs'])
    SF = SF.T
    print(SF.describe().round(2))     
    SF.hist(column='Plays', grid=True, color='r', rwidth=0.9)
    SF.hist(column='Runs', grid=True, color='g', rwidth=0.9)

if __name__ == '__main__':
    Run_Program()
    
    


          
