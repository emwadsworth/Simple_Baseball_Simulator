# Simple_Baseball_Simulator
This program is intended to solve the baseball puzzle described in an Mar 22, 2019 article entitled,
"Can You Turn America’s Pastime Into A Game Of Yahtzee?" (Oliver Roeder, "FiveThirtyEight," 22-Mar-2019)
https://fivethirtyeight.com/features/can-you-turn-americas-pastime-into-a-game-of-yahtzee/

Given the following pitch outcome table:
     
POT = {    '(1,1)': Double(),
           '(1,2)': Single(),
           '(1,3)': Single(),
           '(1,4)': Single(),
           '(1,5)': BOE(),
           '(1,6)': BOB(),
           '(2,2)': Strike(),
           '(2,3)': Strike(),
           '(2,4)': Strike(),
           '(2,5)': Strike(),
           '(2,6)': Foul_Out(),
           '(3,3)': Out_at_First(),
           '(3,4)': Out_at_First(),
           '(3,5)': Out_at_First(),
           '(3,6)': Out_at_First(),
           '(4,4)': Fly_Out(),
           '(4,5)': Fly_Out(),
           '(4,6)': Fly_Out(),
           '(5,5)': Double_Play(),
           '(5,6)': Triple_Play(),
           '(6,6)': Home_Run()}
    

"... what’s the average number of runs that would be scored in nine innings
of this dice game? What’s the distribution of the number of runs scored? (Histograms welcome.)
You can assume some standard baseball things, like runners scoring from second on singles and
runners scoring from third on fly outs."

Here, we'll describe the approach used in this program.

A game of baseball typically consists of 9 innings, each with a top and a bottom. The game begins
at the top of the 1st inning with one team. The team continues to send batters to the batter's mound
so long as batters are able to get successful base hits, get walked, or hit a home run. When three of them have either struck out, fouled out, fly out, fail to get to 1st base, or advance to other bases, the bottom of the inning begins and the opposing team comes to bat.

In this game, the batter's performance is determined strictly by chance. A routine with a random number generator will select two numbers, each from one to six. That is, a dice roll. The roll will provide a key for the outcome for the batter.

The Game_Status_Board is a dictionary that contains details of the situation. This includes the inning, whether top or bottom, number of outs, what players are on what bases, scores.

