"""
@authors: Mohammadreza Baghery & bwahn

"""


# functions for server

import pygame
import random
import math
import time
import sys
import numpy
import csv
import os
import pickle
import zmq
import msgpack as serializer
from time import sleep

from parameters_server import *

pygame.init()


# send notification:
def notify(notification, remote_control):
    """Sends ``notification`` to Pupil Remote"""
    topic = 'notify.' + notification['subject']
    payload = serializer.dumps(notification, use_bin_type=True)
    remote_control.send_string(topic, flags=zmq.SNDMORE)
    remote_control.send(payload)
    return remote_control.recv_string()


    # define utility function that sends trigger to Pupil Capture
def send_trigger(action, trial, remote_control):
    remote_control.send_string('t')
    pupil_time = float(remote_control.recv_string())  # get current Pupil Capture time
    # create notification dictionary
    trigger = {'subject': 'annotation',
               'label': 'gretas_trigger {} {}'.format(trial, action),
               'timestamp': pupil_time,
               'duration': 0.0,
               'source': 'local',
               'record': True}
    notify(trigger, remote_control)


def count_unique(keys):
    uniq_keys = numpy.unique(keys)
    bins = uniq_keys.searchsorted(keys)
    return uniq_keys, numpy.bincount(bins)

def displayTextcenter(textlist,shiftup, fontcolor = BLACK):    
    basicfont = pygame.font.SysFont(None, FONTSIZE)
    SCREEN.fill(BGCOLOR)

    for i,text in enumerate(textlist):

        line = basicfont.render(text, True, fontcolor, WHITE)            
        textrect = line.get_rect()
        textrect.centerx = SCREEN.get_rect().centerx 
        textrect.centery = SCREEN.get_rect().centery + (i+1)*FONTSIZE - shiftup         
        SCREEN.blit(line, textrect)

    pygame.mouse.set_visible(0)
    pygame.display.flip()
    pressnext = 0    
    
    while pressnext == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pressnext = 1
                    another = 1
                    return another
                    break
                if event.key == pygame.K_n:
                    another = 0
                    return another
                    break

def fixcross():
    pygame.draw.circle(SCREEN, BLACK, (CX,CY), FIXCROSSSIZE, 0)


def collide_points(p1,p2,selectsize):
	dx = p1[0] - p2[0]
	dy = p1[1] - p2[1]       
	dist = math.hypot(dx, dy)
	if dist < selectsize:
		return True
	else:
		return False

def collide_objpoint(object,(CX,CY),selectsize):
	dx = object.x - CX
	dy = object.y - CY
	dist = math.hypot(dx, dy)
	if dist < selectsize:
		tangent = math.atan2(dy, dx)
		angle = 0.5 * math.pi + tangent
		new_angle = 2*tangent - object.angle 
		object.angle = new_angle #+ random.uniform(0, 2*math.pi)
		object.x += math.sin(angle)
		object.y -= math.cos(angle)


# classes & functions
def collide(p1, p2): 
	dx = p1.x - p2.x
	dy = p1.y - p2.y
	
	# measure distance between the two relative to zero
	dist = math.hypot(dx, dy)	
	if dist < 1.5*(p1.size + p2.size):                      
		
		tangent = math.atan2(dy, dx)
		angle = 0.5 * math.pi + tangent

		angle1 = 2*tangent - p1.angle 
		angle2 = 2*tangent - p2.angle 
		speed1 = p1.speed
		speed2 = p2.speed

		(p1.angle, p1.speed) = (angle1, speed1)
		(p2.angle, p2.speed) = (angle2, speed2)

		p1.x += math.sin(angle)
		p1.y -= math.cos(angle)
		p2.x -= math.sin(angle)
		p2.y += math.cos(angle) 


def convert_degrees(h,d,r,spx):
	deg_per_px = math.degrees(math.atan2(.5*h, d)) / (.5*r)
	sdeg = spx * deg_per_px
	return sdeg


def MOT(objects, trial=999, Subnum=999, SUBDIR=999):
    # object motion
    framecount = 0
    fpsClock = pygame.time.Clock()
    running = True    
    pygame.mouse.set_visible(0) 
    start = time.time()
    time.clock()    
    elapsed = 0
    framedata_collect = []
                   
    while framecount < MOTTf and running:
        framedata = []
        fpsClock.tick(FPS)
        framecount += 1
        SCREEN.fill(BGCOLOR)    
        fixcross()
        
        for i, object in enumerate(objects):
            if running:

                object.move()
                object.bounce()
          
                collide_objpoint(object,(CX,CY),OBJRADIUS+8)
                                
                for object2 in objects[i+1:]:
                    collide(object, object2)
              
                object.display()

        if trial != 999:
            framedata.append(framecount)
            for object in objects:
                framedata.append(object.x)
                framedata.append(object.y)
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        elapsed = time.time() - start
        framedata_collect.append(framedata)

        if trial != 999:
            csvfile = "Pair%d_%d.csv" % (Subnum,trial)
            path_frame = SUBDIR + csvfile
            with open(path_frame, 'wb') as f:    
                wr = csv.writer(f)
                wr.writerows(framedata_collect)            

    return objects



def markall(objects,feedback=0):
	pygame.mouse.set_visible(1)

	corrident = 0
	SCREEN.fill(BGCOLOR)    
	for object in objects:
		object.display()
	fixcross()
	pygame.mouse.set_pos([WIDTH/2,HEIGHT/2])
								  
	pygame.display.flip()
	start = time.time()
	elapsed = time.time() - start
	mark_onset = elapsed
	
	
	selobjidx = []
	selcor_objidx = []
	selwrong_objidx = []
	
	notselected = 1
	selectedobj = 0
	selectorder = numpy.zeros(OBJNUM)
	rank = 1
	checkcounter = numpy.zeros(OBJNUM)        
	 
	while notselected:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pos = pygame.mouse.get_pos()
				checkfinish = collide_points((CX,CY),pos,FIXCROSSSIZE) 
				
				if checkfinish:	
					notselected = 0			
					break
				
				for i,object in enumerate(objects):
					objpos = (object.x,object.y)
					check = collide_points(objpos,pos,OBJRADIUS)
					if check:
						selectedobj = selectedobj + 1
						object.thickness = 0
						checkcounter[i] += 1						
						if checkcounter[i] == 1:
						    object.colour = COLORME
						    selobjidx.append(i)
						elif checkcounter[i] == 2:
						    object.colour = COLORME
						elif checkcounter[i] == 3:
						    object.colour = COLORME
						
						object.display()
						selectorder[i] = rank
						rank += 1                            
						pygame.display.flip()
						notcorsel = 0
						for t, tmp in enumerate(objects[0:NUMTAR]):
							if t == i:
								selcor_objidx.append(i)
							if t != i:
								notcorsel += 1
								if NUMTAR == notcorsel:
									selwrong_objidx.append(i)

	if feedback == 1:						
		for sel in selcor_objidx:
			objects[sel].thickness = 0
			objects[sel].colour = GREEN
			corrident += 1

		for sel in selwrong_objidx:
			objects[sel].thickness = 0
			objects[sel].colour = RED
			corrident -= 1
		


	elapsed = time.time() - start        
	mark_response = elapsed
#        print selectorder 
						
	totalperf = numpy.zeros(2*OBJNUM)
	tarint = 0
	corint = 1
	
# 	for i, object in enumerate(objects[0:NUMTAR]):
# 		totalperf[tarint] = 1            
# 		for sel in selobjidx:
# 			if i==sel:
# 				corrident += 1
# 				totalperf[corint] = 1
# 				object.thickness = 0
# 				object.colour = GREEN
# 			if i!=sel and i < NUMTAR:	
# 				corrident -= 1
# 				totalperf[corint] = -1
# 				object.thickness = 0
# 				object.colour = RED

	#tarint += 2
	#corint += 2
	
	for object in objects:
		object.display()
	pygame.display.flip()
	pygame.time.wait(1000)    
	pygame.mouse.set_visible(0)
	mark_rt = mark_response - mark_onset
#        print totalperf
	return corrident, mark_rt, totalperf, selectorder, selobjidx, selcor_objidx, selwrong_objidx, objects
	

	

class Object:
	def __init__(self, (x, y), size, objspeed):
		self.x = x
		self.y = y
		self.size = size
		self.colour = BLACK
		self.thickness = OBJTHICKNESS        
		self.speed = objspeed
		# angle in radians, 1 radians = 180 degrees/pi = 57.295               
		self.angle = math.pi/2 # move left to right

	def display(self):
		# draw a circle
		# arguments: surface on which it is drawn, color, (x,y) coordinates, 
		# the radius, a thickness (optional)
		pygame.draw.circle(SCREEN, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
		pygame.draw.circle(SCREEN, BLACK, (int(self.x), int(self.y)), self.size, 1)


	def move(self):
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed
		
	def bounce(self):
		if self.x > WIDTH - self.size:
			self.x = 2*(WIDTH - self.size) - self.x
			self.angle = - self.angle
		elif self.x < self.size:
			self.x = 2*self.size - self.x
			self.angle = - self.angle
	
		if self.y > HEIGHT - self.size:
			self.y = 2*(HEIGHT - self.size) - self.y
			self.angle = math.pi - self.angle
	
		elif self.y < self.size:
			self.y = 2*self.size - self.y
			self.angle = math.pi - self.angle
	
	def coord(self):
		return (self.x,self.y)        

	def coordx(self):
		return self.x

	def coordy(self):
		return self.y		
		
