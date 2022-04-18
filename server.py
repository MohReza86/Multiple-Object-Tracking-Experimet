
"""
Server
@authors: Mohammadreza Baghery & bwahn

"""

import socket 
import pygame

from parameters_server import *
from functions_server import *

pygame.init()

def Main():
    # MOT prep
	SUB = raw_input("Please enter pair number: ")
	EXPPATH = os.path.dirname(os.path.abspath(__file__))
	SUBDIR = "%s/Data/Pair%s/" %(EXPPATH,SUB)
	csvfile = "Pair%s.csv" % SUB
	path = SUBDIR + csvfile
	
	Subnum = int(SUB)

	header = ['Subnum','Trial','player1correct','player1incorrect',
	'player2correct','player2incorrect','paircorrect','pairincorrect',
	'player1total', 'player2total','pairtotal','doublesel',
	'selobj1','selobj2','selobj3','selobj4','selobj5','selobj6',
	'selobj7','selobj8','selobj9','selobj10','selobj11','selobj12',
	'selobj13','selobj14','selobj15','selobj16','selobj17','selobj18',
	'selobjother1','selobjother2','selobjother3','selobjother4','selobjother5','selobjother6',
	'selobjother7','selobjother8','selobjother9','selobjother10','selobjother11','selobjother12',
	'selobjother13','selobjother14','selobjother15','selobjother16','selobjother17','selobjother18']

	#check if subject folder exists, if not make it:
	if not os.path.exists(SUBDIR):
		os.makedirs(SUBDIR)
		with open(path, 'wb') as f:    
			wr = csv.writer(f)
			wr.writerow(header)        

	if LOCALHOST:
		host = '127.0.0.1'
		port = 5000
		s = socket.socket()
		s.bind((host,port))    
		s.listen(1)
		c,addr = s.accept()
		text = ["Connection from " + str(addr), " ","Please press space to continue"]		
	else:
		ip = '0.0.0.0'
		port = 5005

		# open main socket (will receive the connections from players)
		s0 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s0.bind((ip,port))
		print "server started ..."
		print "hostname: " + socket.gethostname()

		s0.listen(1)

		# accept connection    
		c, addr = s0.accept()
		print "received connection from: " +str(addr)
		c.sendall("accepted.")

	textconnect = ['Connected.'," "]
	#host = '169.254.192.12'    
	displayTextcenter(textconnect,HEIGHT/4)
	running = True

	for trial in range(0,TRIALS):
                print trial
		if trial > 0:
                        if trial % 2 == 0:
			    port += 1
                        if trial % 2 != 0:
                            port -= 1
			#pygame.time.wait(10000)
			if LOCALHOST:
				s = socket.socket()
				s.bind((host,port))    
				s.listen(1)
				c,addr = s.accept()
			else:
				s0 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s0.bind((ip,port))
                                print port
				print "server started ..."
				#print "hostname: " + socket.gethostname()
				s0.listen(1)
				# accept connection    
				c, addr = s0.accept()
				#print "received connection from: " +str(addr)
				c.sendall("accepted.")
				
		data = []
		objects = []
		initialobjpos = [(CX,CY)]

		for n in range(0,OBJNUM):
			conflict = 1   
			(posx,posy) = (random.randint(OBJRADIUS, WIDTH - OBJRADIUS),random.randint(OBJRADIUS, HEIGHT - OBJRADIUS))
			postmp = (posx,posy)
			while conflict:
				conflict = 0                
				for checkpos in initialobjpos:
					if collide_points(postmp,checkpos,6*OBJRADIUS):
						conflict = 1
						(posx,posy) = (random.randint(OBJRADIUS, WIDTH - OBJRADIUS),random.randint(OBJRADIUS, HEIGHT - OBJRADIUS))
						postmp = (posx,posy)
					
			initialobjpos.append(postmp)    

			object = Object((int(posx),int(posy)),OBJRADIUS,OBJSPEED)    
			# random speed option:
			object.speed = int(random.uniform(OBJSPEEDRANGE[0],OBJSPEEDRANGE[1]))
		
			object.angle = random.uniform(0, math.pi*2)
			object.angledeg = int(float(math.degrees(object.angle)))
			object.angle = math.radians(object.angledeg)
			objects.append(object)
		
				
		# connection setup, 192.168.4.1 / 192.168.4.2 
	
# 		if LOCALHOST:
# 			host = '127.0.0.1'
# 		else:
# 			host = raw_input("Please enter host ip number: ")
		text = ["Please press space to continue"]
		displayTextcenter(text,HEIGHT/4)
		running = True 

		print objects
		for objind,object in enumerate(objects):
			if len(str(object.x)) == 3:
				strobjx = '0' + str(object.x)
			elif len(str(object.x)) == 2:     
				strobjx = '00' + str(object.x)
			elif len(str(object.x)) == 1:     
				strobjx = '000' + str(object.x)
			else:
				strobjx = str(object.x)
			
			if objind < 10:
				tmpobjind = '0' + str(objind)
			else:
				tmpobjind = str(objind)
			
			
			coordx = '%sx' %tmpobjind + strobjx       
			print coordx                
			c.send(coordx)        
		
			if len(str(object.y)) == 3:
				strobjy = '0' + str(object.y)
			elif len(str(object.y)) == 2:     
				strobjy = '00' + str(object.y)
			elif len(str(object.y)) == 1:     
				strobjy = '000' + str(object.y)
			else:
				strobjy = str(object.y)

			coordy = '%sy' %tmpobjind + strobjy 
			print coordy                
			c.send(coordy)

			if len(str(object.speed)) == 3:
				strobjs = '0' + str(object.speed)
			elif len(str(object.speed)) == 2:     
				strobjs = '00' + str(object.speed)
			elif len(str(object.speed)) == 1:     
				strobjs = '000' + str(object.speed)
			else:
				strobjs = str(object.speed)

			speed = '%ss' %tmpobjind + strobjs 
			print speed                
			c.send(speed)

			if len(str(object.angledeg)) == 3:
				strobja = '0' + str(object.angledeg)
			elif len(str(object.angledeg)) == 2:     
				strobja = '00' + str(object.angledeg)
			elif len(str(object.angledeg)) == 1:     
				strobja = '000' + str(object.angledeg)
			else:
				strobja = str(object.angledeg)

			angle = '%sa' %tmpobjind + strobja 
			print angle                
			c.send(angle)

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
	
		objects = MOT(objects, trial, Subnum, SUBDIR)
		corrident, mark_rt, totalperf, selectorder, selobjidx, selcor_objidx, selwrong_objidx, objects = markall(objects)

		for o in selobjidx:
			if o > 9:
				print "sending " + str(o) 
				c.send(str(o))        
			else:
				print "sending " + "0" + str(o) 
				c.send('0' + str(o))        
				
		c.send("::")        

		obsposrecv = True
		obspos_other = []
		while obsposrecv:
			received = c.recv(2)
			print "received " + received 
			if received == "::":
				break
				obsposrecv = False
			if received != "::":    
				obspos_other.append(int(float(received)))

		print obspos_other
		
	
		#obspos_other = count_unique(obspos_otherrecv)    
	
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
				c.send("1")
			SCREEN.fill(BGCOLOR)
			pygame.display.flip()
	
			waitother = True
			while waitother:
				received = c.recv(1)
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
	
		print pairtotal
		print player1total
		print player2total
		print doublesel
		
		data.append(Subnum)
		data.append(trial)
		data.append(player1correct)
		data.append(player1incorrect)
		data.append(player2correct)
		data.append(player2incorrect)
		data.append(paircorrect)

		data.append(pairincorrect)
		data.append(player1total)
		data.append(player2total)
		data.append(pairtotal)
		data.append(doublesel)

		# save own selections; selobjidx; other selections  obspos_other		
		for i in range(0,len(selobjidx)):
			data.append(selobjidx[i])
		for i in range(len(selobjidx)+1,OBJNUM):
			data.append(float('nan'))

		for i in range(0,len(obspos_other)):
			data.append(obspos_other[i])
		for i in range(len(obspos_other)+1,OBJNUM):
			data.append(float('nan'))
	


		
		with open(path, 'a') as f:
			wr = csv.writer(f)
			wr.writerow(data)

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
				c.send(str(readyscore)+":")
				waitother = True
				while waitother:
					received = c.recv(2)
					if received == "1:":
						print "ready other " + received 
						waitother = False
						break
                                        

		#c.shutdown(socket.SHUT_RDWR)
		#c.close()

	
	c.close()
                
    
    
if __name__ == '__main__':
    Main()




