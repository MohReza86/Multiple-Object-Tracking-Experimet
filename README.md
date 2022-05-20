# Multiple Object Tracking (MOT)

MOT is a 2-player game where two participants track objects appearing on the screen on two different PCs.
By starting the game, some 18 round objects will appear on the screen. Five of these objets are turned grey randomly for 
a few seconds and all objects will start moving randomly in space. Throughout this time participants are asked to gaze their 
attention to a center point on the screen. After 10 seconds the objects stop moving and participants are required to select
the objects that were turned grey in the beginning. This repeats a total of 100 trials. The more objects are correctly selected
by the participant in each trial, the higher the score in that trial. Throughut the entire experiment, partitcipants are wearing
an eyetracker that measure their pupul size while playing the game. All the scores and eye tracking data are stored in separate
CSV files.

The game module is connected to an eye tracker device. The eye tracker waits for cue by the game module as when to start and stop
recording. Pupil sizes are being recorded during the 10 seconds when participants gaze their attention to the center of the screen.


# Running the experiment 

Before starting the experiment:

- connect two computer via a LAN cable or have them connected within a local network

- make sure to have installed python and the libraries numpy and pygame

- copy the „server“ code (all files in the folder server) to one computer, copy the „client“ code (all files in the folder client) to the other computer

- the computer with the server code must have a name/alias


How to start the experiment:

- open a terminal on the computer with the server code, go to the folder where the code is located, type „python server.py“ to start the code. A black window will open.

- in the terminal, enter a participant number (e.g., 101) and confirm it with enter. Then the name of the computer should appear in the terminal („hostname: name of computer“)

- open a terminal on the computer with the client code and start the client code („python client.py“). In the terminal, the client code then requests the hostname of the server. Type in the hostname and confirm with enter. The black window on the server computer should turn white and it should say „connected“. Press space on the server and client computer to continue. 
