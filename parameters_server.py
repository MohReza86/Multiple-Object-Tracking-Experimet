"""
@authors: Mohammadreza Baghery & bwahn

"""

import os
import numpy
import pygame

from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

LOCALHOST = False
OS = True
FULLSCREEN = 0


# parameter Joint MOT

# Condition parameters
SHOWSCORE = True
SHOWTEAMSCORE = True
SHOWINDIVIDUALSCORES = False
SHOWSELECTIONS = True
EVALJOINTSELECTION = False

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GRAY = (190,190,190)
LIGHTGRAY = (211,211,211)	
GREEN = (34,139,34)

YELLOW = (255,255,0)
MEDYELLOW = (200,200,0)
DARKYELLOW = (128,128,0)

BLUE = (255,0,255)
MEDBLUE = (200,0,200)
DARKBLUE = (128,0,128)

COLORME = BLUE
COLOROTHER = YELLOW


BGCOLOR = WHITE
FONTSIZE = 34

OVERLAP_FEEDBACKCTRL = True

# Folders
EXPPATH = os.path.dirname(os.path.abspath(__file__))
DATAPATH = EXPPATH + '/Data'

TRIALS = 100

(WIDTH,HEIGHT) = (1920,1000)


FPS = 30
MOTT = 11
MOTTf = 11*FPS

NUMTAR = 6

if FULLSCREEN:
    SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    WIDTH,HEIGHT = SCREEN.get_size()    
else:
    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))  
    

(CX,CY) = (WIDTH/2, HEIGHT/2)

DOUBLESELRAD = (WIDTH*HEIGHT)/15000 
OBJTHICKNESS = 1
OBJNUM = 19


if OS == False:
	FIXCROSSSIZE = WIDTH/150
	OBJRADIUS = (WIDTH*HEIGHT)/15000 
	OBJSPEEDRANGE = [(WIDTH*HEIGHT)/ 40000, (WIDTH*HEIGHT)/ 65000] # for mark all        
    
if OS == True:
	FIXCROSSSIZE = 8
	OBJRADIUS = (WIDTH*HEIGHT)/65000 
	OBJSPEEDRANGE = [(WIDTH*HEIGHT)/ 400000, (WIDTH*HEIGHT)/ 300000] # for mark all              

OBJSPEED = numpy.mean(OBJSPEEDRANGE)    
      
SCREEN.fill(BGCOLOR)



