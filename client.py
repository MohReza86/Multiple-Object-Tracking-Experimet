"""
Client
@authors: Mohammadreza Baghery & bwahn

"""

from parameters_server import *
from functions_server import *

import socket
import pygame

def Main():


	if LOCALHOST:
		host = '127.0.0.1'
		port = 5000
		s = socket.socket()
		s.connect((host,port))
	else:
		host_name = raw_input('enter host name: ')
		host_ip = socket.gethostbyname(host_name)
		port = 5005
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((host_ip,port))
		confirm = s.recv(9)
		print "connect status: %s" %confirm
	
	for trial in range(0,TRIALS):
	
		if trial > 0:
		        pygame.time.wait(500)
                        if trial % 2 == 0:
			    port += 1 
                        if trial % 2 != 0:
                            port -= 1
			if LOCALHOST:
				s = socket.socket()
				s.connect((host,port))
			else:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((host_ip,port))
				confirm = s.recv(9)
				print "connect status: %s" %confirm
			
		running = True
		lastanglereceived = 0
		objects = []
		test = True
		while running:
			received = s.recv(7)        
			for obj in range(0,OBJNUM):
				if obj < 10:
					tmpobj = '0' + str(obj)
				else:
					tmpobj = str(obj)
				if '%sx' %tmpobj in received:
					objx = int(float(received[3:7]))
					print "obj %s x %d received" %(tmpobj,objx)
				if '%sy' %tmpobj in received:
					objy = int(float(received[3:7]))
					print "obj %s y %d received" %(tmpobj,objy)
				if '%ss' %tmpobj in received:
					objspeed = int(float(received[3:7]))
					print "obj %s speed %d received" %(tmpobj,objspeed) 
				if '%sa' %tmpobj in received:
					objangle = math.radians(float(received[3:7]))
					print "obj %s angle %d received" %(tmpobj,objangle)
					object = Object((objx,objy),OBJRADIUS,OBJSPEED)
					object.speed = objspeed
					object.angle = objangle
					objects.append(object)    
					if obj == OBJNUM-1:
						running = False
	
		SCREEN.fill(BGCOLOR)
		fixcross()
		for object in objects:
			object.display()
		
		pygame.display.flip()
		pygame.time.wait(2000)

		SCREEN.fill(BGCOLOR)						
		fixcross()
		for object in objects[0:NUMTAR]:
			object.thickness = 0
			object.colour = GRAY
		for object in objects:
			object.display()
		pygame.display.flip()
		pygame.time.wait(3000)

		for object in objects[0:NUMTAR]:
			object.thickness = 1
			object.colour = BLACK

		objects = MOT(objects)
		corrident, mark_rt, totalperf, selectorder, selobjidx, selcor_objidx, selwrong_objidx, objects = markall(objects)

		for o in selobjidx:
			if o > 9:
				print "sending " + str(o) 
				s.send(str(o))        
			else:
				print "sending " + "0" + str(o) 
				s.send('0' + str(o))        
				
		s.send("::")

		obsposrecv = True
		obspos_other = []
		while obsposrecv:
			received = s.recv(2)
			print "received " + received 
			if received == "::":
				break
				obsposrecv = False
			if received != "::":    
				obspos_other.append(int(float(received)))

		doubleselected = []
		
		for o in obspos_other:
			objects[o].thickness = 0
			objects[o].colour = COLOROTHER
			if o in selobjidx:
				objects[o].thickness = 0
				objects[o].colour = COLORME
				objects[o].size = OBJRADIUS/2
				doublesel_object = Object((objects[o].x,objects[o].y),OBJRADIUS,OBJSPEED)
				doublesel_object.thickness = 0
				doublesel_object.colour = COLOROTHER
				doubleselected.append(doublesel_object)

		fixcross()                
		for doublesel_object in doubleselected:
			doublesel_object.display()                    
		for object in objects:
			object.display()                    
		pygame.display.flip()

			
		if SHOWSELECTIONS == True:
			overlapfeedback = True
			while overlapfeedback:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							pygame.quit()
							sys.exit()
						if event.key == pygame.K_SPACE:
							overlapfeedback = False
			if overlapfeedback == False:
				s.send("1")
			SCREEN.fill(BGCOLOR)
			pygame.display.flip()
	
			waitother = True
			while waitother:
				received = s.recv(1)
				if received == "1":
					print "overlap: ready other " + received 
					waitother = False		

		SCREEN.fill(BGCOLOR)

		fixcross()
		
		player1correct = 0
		player1incorrect = 0
		player2correct = 0
		player2incorrect = 0
	
		paircorrect = 0
		pairincorrect = 0    
		player1total = 0
		player2total = 0
		pairtotal = 0
		doublesel = 0
						
		for object in objects[0:NUMTAR]:
			if object.colour != BLACK:
				print "correct"
				if object.size == OBJRADIUS/2:
					doublesel += 1
					player1correct += 1
					player2correct += 1
				elif object.colour == COLOROTHER:
					player2correct += 1            
				elif object.colour == COLORME:    
					player1correct += 1

				object.colour = GREEN
				object.size = OBJRADIUS
				paircorrect += 1
			
		for object in objects[NUMTAR:]:
			if object.colour != BLACK:
				print "incorrect"                    
				if object.size == OBJRADIUS/2:
					doublesel += 1
					player1incorrect += 1
					player2incorrect += 1
				elif object.colour == COLOROTHER:
					player2incorrect += 1            
				elif object.colour == COLORME:    
					player1incorrect += 1
													
				object.colour = RED            
				object.size = OBJRADIUS
				pairincorrect += 1

		pairtotal = paircorrect - pairincorrect
		player1total = player1correct - player1incorrect
		player2total = player2correct - player2incorrect
		
		
		for object in objects[0:NUMTAR]:
			if object.thickness == 0:
				object.colour = GREEN
				object.size = OBJRADIUS

		for object in objects[NUMTAR:]:
			if object.thickness == 0:
				object.colour = RED
				object.size = OBJRADIUS

		if EVALJOINTSELECTION == True:
			for object in objects:
				object.display()
			pygame.display.flip()
			pygame.time.wait(4000)

		if SHOWSCORE == True:
			readyscore = 0
			if SHOWTEAMSCORE == True and SHOWINDIVIDUALSCORES == True: 
				feedbackscore = ["Me: %d P." %player1total, " ", "Team: %d P." %pairtotal," ","Partner: %d P." %player2total]
			if SHOWTEAMSCORE == True: 
				feedbackscore = [" "," ", "Team: %d P." %pairtotal," "," "]
			if SHOWINDIVIDUALSCORES == True: 
				feedbackscore = ["Me: %d P." %player1total, " ", " "," ","Partner: %d P." %player2total]

			readyscore = displayTextcenter(feedbackscore,shiftup=HEIGHT/4, fontcolor = BLACK)
			SCREEN.fill(BGCOLOR)        
			pygame.display.flip()
			if readyscore == 1:
				s.send(str(readyscore)+":")
				waitother = True
				while waitother:
					received = s.recv(2)
					if received == "1:":
						print "ready other " + received 
						waitother = False
						break
		#s.shutdown(socket.SHUT_RDWR)
		#s.close()

	s.close()
    
if __name__ == '__main__':
    Main()

