# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 14:00:30 2016
Ball Breaker! (Clone of Breakout)
@author: Jake Fortner
"""

import sys, pygame
from pygame.locals import *

"""
#=============================================================================#
This file creates the game objects our game will be using to play the game. 
These objects include:

    * Paddle: The paddle is what the player controls. It moves left and right
        to bounce the ball toward the wall objects. This is found within the 
        player class.
    * Wall: The walls need to be eliminated by the ball for the player to win
        the game.
    * Ball: The ball is hit by the paddle and knocks walls out. It is interacted
        with to play the game.
    * Lives: The lives are by default set to 3. When this number reaches 0 (when
        the ball falls below the screen), it is game over.  
        
The object of the game is to use the paddle to bounce the ball into the walls 
until all of the walls are knocked out or the player loses three lives. 
#=============================================================================#
"""


class Wall():
    
    def __init__(self, size, coords, color):
        self.size = size        
        self.coords = coords
        self.color = color
        self.center = (size[0]/2, size[1]/2)
        self.obj = None


class Ball():
    
    def __init__(self, coords, velocity):
        self.coords = coords
        self.velocity = (0, velocity)
        self.ball_live = True
        self.obj = None
        

class Player():
    
    def __init__(self, size, coords, life=3):
        self.coords = coords
        self.size = size
        self.lives = life
        self.center = (coords[0] + size[0]/2, coords[1] + size[1]/2)
        self.obj = None
        
        

        
        





