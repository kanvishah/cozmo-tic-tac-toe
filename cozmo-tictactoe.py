import math
import cozmo
import asyncio
import random
import time

from cozmo.util import degrees, Pose
from cozmo.util import *
from tkinter import *
from algorithms import *

class TicTacToe:

    DEBUG = True

    def __init__(self):
        distance_mm(60)
        self.width = 600
        self.height = 600
        self.timerDelay = 100 # milliseconds

        self.state = "start"
        self.margin = self.width/10
        self.boardW = self.width - 2*self.margin
        self.boardH = self.height - 2*self.margin
        self.squareW = self.boardW/3
        self.squareH = self.boardH/3

        if random.randint(1, 2) == 1:
            self.turn = False # true is cozmo, false is human
            self.cozmo = "O"
            self.human = "X"
        else:
            self.turn = True
            self.cozmo = "X"
            self.human = "O"

        self.board = [ [" ", " ", " "], [" ", " ", " "], [" ", " ", " "] ]
        self.boardDestinations = [ [None, None, None], [None, None, None], [None, None, None] ]

        self.won = None


    def runEverything(self, sdk_conn):
        cozmo.setup_basic_logging()

        self.robot = sdk_conn.wait_for_robot()

        self.robot.camera.image_stream_enabled = True
        self.robot.camera.color_image_enabled = True

        self.robot.set_lift_height(1).wait_for_completed()

        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.canvas.create_rectangle(0, 0, self.width, self.height, fill='white', width=0)
            self.redrawAll()
            self.canvas.update()    

        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()

        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()

        def timerFiredWrapper(str):
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerDelay, timerFiredWrapper, self.canvas)

        # create the root and the canvas
        root = Tk()
        root.resizable(width=False, height=False) # prevents resizing window
        self.canvas = Canvas(root, width=self.width, height=self.height)
        self.canvas.configure(bd=0, highlightthickness=0)
        self.canvas.pack()
        # set up events
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event))
        timerFiredWrapper("moo")
        # and launch the app
        root.mainloop()  # blocks until window is closed
        print("bye!")

    def startGame(self, mode):        
        self.mode = mode
        self.findBoard()
    
    def drawBoard(self):
        self.robot.set_lift_height(0.7).wait_for_completed()
        # self.robot.go_to_pose(Pose(updatePos.x, updatePos.y+offset, updatePos.z, angle_z=degrees(0)), relative_to_robot=False).wait_for_completed()
        
        self.robot.set_lift_height(0.1).wait_for_completed()
        self.robot.drive_wheels(200, 200, duration=1)

        self.robot.set_lift_height(0.7).wait_for_completed()
        self.robot.drive_wheels(-200, -200, duration=1)

        self.robot.turn_in_place(degrees(90)).wait_for_completed()
        self.robot.drive_wheels(100, 100, duration=1)
        self.robot.turn_in_place(degrees(-90)).wait_for_completed()

        self.robot.set_lift_height(0.1).wait_for_completed()
        self.robot.drive_wheels(200, 200, duration=1)

        self.robot.set_lift_height(0.7).wait_for_completed()
        #self.robot.drive_wheels(-100, -100, duration=1)

        #self.robot.drive_wheels(100, 100, duration=1)
        self.robot.turn_in_place(degrees(90)).wait_for_completed()
        #self.robot.drive_wheels(100, 100, duration=1)

        self.robot.set_lift_height(0.1).wait_for_completed()
        self.robot.drive_wheels(-200, -200, duration=1)

        self.robot.set_lift_height(0.7).wait_for_completed()
        self.robot.turn_in_place(degrees(-90)).wait_for_completed()
        self.robot.drive_wheels(100, 100, duration=1)
        self.robot.turn_in_place(degrees(90)).wait_for_completed()

        self.robot.set_lift_height(0.1).wait_for_completed()
        self.robot.drive_wheels(200, 200, duration=1)

        self.robot.set_lift_height(0.7).wait_for_completed()
        self.robot.drive_wheels(-200, -200, duration=1)

    def goToSpotAndLetter(self, row, col, letter):
        
        self.robot.set_lift_height(0.7)
        
        if row == 0:
            if col == 0:
                self.robot.go_to_object(self.homeCube, distance_mm(60), in_parallel=True).wait_for_completed()
            if col == 1:
                self.robot.go_to_object(self.homeCube, distance_mm(60), in_parallel=True).wait_for_completed()
                self.robot.go_to_object(self.topCube, distance_mm(160)).wait_for_completed()
            if col == 2:
                self.robot.go_to_object(self.topCube, distance_mm(60), in_parallel=True).wait_for_completed()

        if row == 1:
            if col == 0:
                self.robot.go_to_object(self.homeCube, distance_mm(70), in_parallel=True).wait_for_completed()
                self.robot.go_to_object(self.bottomCube, distance_mm(160)).wait_for_completed()
            if col == 1:        
                self.robot.go_to_object(self.homeCube, distance_mm(70), in_parallel=True).wait_for_completed()
                self.robot.go_to_object(self.bottomCube, distance_mm(160)).wait_for_completed()
                self.robot.turn_in_place(degrees(90)).wait_for_completed()
            if col == 2:
                self.robot.go_to_object(self.homeCube, distance_mm(70), in_parallel=True).wait_for_completed()
                self.robot.go_to_object(self.topCube, distance_mm(70)).wait_for_completed()
                self.robot.turn_in_place(degrees(-90)).wait_for_completed()
                self.robot.drive_straight(distance_mm(120), speed_mmps(60)).wait_for_completed()
        
        if row == 2:
            if col == 0:
                self.robot.go_to_object(self.bottomCube, distance_mm(70), in_parallel=True).wait_for_completed()
            if col == 1:
                self.robot.go_to_object(self.homeCube, distance_mm(70), in_parallel=True).wait_for_completed()
                self.robot.go_to_object(self.bottomCube, distance_mm(70)).wait_for_completed()
                self.robot.turn_in_place(degrees(90)).wait_for_completed()
                self.robot.drive_straight(distance_mm(120), speed_mmps(60)).wait_for_completed()
            if col == 2:
                self.robot.go_to_object(self.homeCube, distance_mm(70), in_parallel=True).wait_for_completed()
                self.robot.go_to_object(self.bottomCube, distance_mm(70)).wait_for_completed()
                self.robot.turn_in_place(degrees(90)).wait_for_completed()
                self.robot.drive_straight(distance_mm(300), speed_mmps(60)).wait_for_completed()
        
        self.drawLetter(letter)

    def drawLetter(self, letter):
        if letter == 'X':

            self.robot.set_lift_height(0.7).wait_for_completed()
            self.robot.set_lift_height(0).wait_for_completed()
            self.robot.drive_wheels(-200, -200, duration=1)
            self.robot.set_lift_height(0.7).wait_for_completed()
            self.robot.drive_wheels(100, 100, duration=1)
            self.robot.turn_in_place(degrees(-70)).wait_for_completed()
            self.robot.set_lift_height(0).wait_for_completed()
            self.robot.drive_wheels(200, 200, duration=0.5)
            self.robot.set_lift_height(0).wait_for_completed()
            self.robot.drive_wheels(-200, -200, duration=1)
            self.robot.set_lift_height(0.7).wait_for_completed()

        else:
            self.robot.set_lift_height(0.7).wait_for_completed()
            # self.robot.go_to_pose(Pose(updatePos.x, updatePos.y+offset, updatePos.z, angle_z=degrees(0)), relative_to_robot=False).wait_for_completed()
            self.robot.drive_wheels(50, 50, duration=0.9)
            self.robot.set_lift_height(0).wait_for_completed()
            self.robot.turn_in_place(degrees(170)).wait_for_completed()
            self.robot.set_lift_height(0).wait_for_completed()
            self.robot.turn_in_place(degrees(170)).wait_for_completed()
            self.robot.set_lift_height(0).wait_for_completed()
            self.robot.turn_in_place(degrees(25)).wait_for_completed()
            self.robot.set_lift_height(0.7).wait_for_completed()

    def findBoard(self):
        lookaround = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = self.robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
        lookaround.stop()

        for cube in cubes:
            if cube.cube_id == 1:
                self.homeCube = cube
            if cube.cube_id == 2:
                self.bottomCube = cube
            if cube.cube_id == 3:
                print("HIIII")
                self.topCube = cube

        self.robot.go_to_object(self.homeCube, distance_mm(60)).wait_for_completed()
        self.robot.turn_in_place(degrees(180)).wait_for_completed()

    def cozmoModeMove(self):
        row, col = None, None
        if self.mode == "easy":
            row, col = cozmoRandomMove(self.board)
        if self.mode == "medium":
            row, col = cozmoDecentMove(self.board, self.cozmo, self.human)
        if self.mode == "hard":
            row, col = cozmoBestMove(self.board, self.cozmo, self.human)
        self.cozmoMove(row, col)

    def cozmoMove(self, row, col):
        print(self.board)
        if self.board[row][col] == " ":
            self.board[row][col] = self.cozmo
            self.robot.say_text(self.cozmo + " at " + str(row) + " " + str(col)).wait_for_completed()
            self.goToSpotAndLetter(row, col, self.cozmo)
            self.turn = not self.turn
            self.robot.say_text("Your turn!").wait_for_completed()

            if evaluateVictory(self.board, self.cozmo, self.human) > 0:
                self.won = "cozmo"
                self.robot.say_text("Ha! I won!").wait_for_completed()
                print("cozmo wins")
            elif not movesLeft(self.board):
                self.won = "draw"
                self.robot.say_text("Guess we'll find out who is better next time...").wait_for_completed()
                print("tie!")

        else:
            return False

    def humanMove(self, row, col):
        print(self.board)
        if self.board[row][col] == " ":
            self.board[row][col] = self.human
            self.goToSpotAndLetter(row, col, self.human)
            self.turn = not self.turn

            if evaluateVictory(self.board, self.cozmo, self.human) < 0:
                self.won = "human"
                self.robot.say_text("Oh, you won!").wait_for_completed()
                print("human wins")
            elif not movesLeft(self.board):
                self.won = "draw"
                self.robot.say_text("Guess we'll find out who is better next time...").wait_for_completed()
                print("tie!")

        else:
            return False
  
# animation starter code from 15-112 course notes: https://www.cs.cmu.edu/~112/notes/notes-oopy-animation.html

    def mousePressed(self, event):
        if self.state == "start":
            if event.x > 2*self.margin and event.y > self.height/3 and event.x < self.width-2*self.margin and event.y < self.height/3 + self.margin:
                self.startGame("easy")
                self.state = "play"
            elif event.x > 2*self.margin and event.y > self.height/3 + 1.5*self.margin and event.x < self.width-2*self.margin and event.y < self.height/3 + 2.5*self.margin:
                self.startGame("medium")
                self.state = "play"
            elif event.x > 2*self.margin and event.y > self.height/3 + 3*self.margin and event.x < self.width-2*self.margin and event.y < self.height/3 + 4*self.margin:
                self.startGame("hard")
                self.state = "play"
            
        elif self.state == "play":
            row, col = None, None

            if not self.turn:
                if event.x > self.margin and event.x < self.margin + self.squareW:
                    col = 0
                elif event.x > self.margin + self.squareW and event.x < self.margin + 2*self.squareW:
                    col = 1
                elif event.x > self.margin + 2*self.squareW and event.x < self.width - self.margin:
                    col = 2
                
                if event.y > self.margin and event.y < self.margin + self.squareH:
                    row = 0
                elif event.y > self.margin + self.squareH and event.y < self.margin + 2*self.squareH:
                    row = 1
                elif event.y > self.margin + 2*self.squareH and event.y < self.height - self.margin:
                    row = 2
                
                if row is not None and col is not None:
                    self.humanMove(row, col)
                if self.won == "cozmo" or self.won == "human" or self.won == "draw":
                    self.state = "end"
            
    def redrawAll(self):
        if self.state == "start":
            self.drawStart()
        if self.state == "play":
            self.drawBoard()
        if self.state == "end":
            self.drawEnd()

    def drawStart(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black", width=0)
        self.canvas.create_text(self.width/2, self.height/6, text="Play Tic-Tac-Toe with Cozmo!", font="Verdana 40", fill="white")

        self.canvas.create_rectangle(2*self.margin, self.height/3, self.width-2*self.margin, self.height/3 + self.margin, fill="green", width=0)
        self.canvas.create_rectangle(2*self.margin, self.height/3 + 1.5*self.margin, self.width-2*self.margin, self.height/3 + 2.5*self.margin, fill="yellow", width=0)
        self.canvas.create_rectangle(2*self.margin, self.height/3 + 3*self.margin , self.width-2*self.margin, self.height/3 + 4*self.margin, fill="red", width=0)

        self.canvas.create_text(self.width/2, self.height/3 + 0.5*self.margin, font="Verdana 30", text="EASY", fill="black")
        self.canvas.create_text(self.width/2, self.height/3 + 2*self.margin, font="Verdana 30", text="MEDIUM", fill="black")
        self.canvas.create_text(self.width/2, self.height/3 + 3.5*self.margin, font="Verdana 30",text="HARD", fill="black")

    def drawEnd(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black", width=0)
        if self.won == "human":
            self.canvas.create_text(self.width/2, self.height/2, text= "YOU WIN!", font="Verdana 70", fill="white")
        elif self.won == "cozmo":
            self.canvas.create_text(self.width/2, self.height/2, text= "COZMO WINS!", font="Verdana 70", fill="white")
        elif self.won == "draw":
            self.canvas.create_text(self.width/2, self.height/2, text= "DRAW!", font="Verdana 70", fill="white")

    def drawBoard(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black", width=0)

        self.canvas.create_line(self.squareW + self.margin, self.margin, self.squareW + self.margin, self.height - self.margin, fill="white")
        self.canvas.create_line(2*self.squareW + self.margin, self.margin, 2*self.squareW + self.margin, self.height - self.margin, fill="white")
        self.canvas.create_line(self.margin, self.squareH + self.margin, self.width - self.margin, self.squareH + self.margin, fill="white")
        self.canvas.create_line(self.margin, 2*self.squareH + self.margin, self.width - self.margin, 2*self.squareH + self.margin, fill="white")

        if self.turn:
            txt = "COZMO'S TURN"
        else:
            txt = "YOUR TURN"
        self.canvas.create_text(self.width/2, self.margin/2, font="Verdana 45", text=txt, fill="white")

        self.drawPieces()

    def drawPieces(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] is not " ":
                    self.canvas.create_text(self.margin + (col+.5)*self.squareW, self.margin + (row+.5)*self.squareH, text=self.board[row][col], font="Verdana 70", fill="white")

    def keyPressed(self, event):
        pass

    def timerFired(self):
        if self.won == "cozmo" or self.won == "human" or self.won == "draw":
            self.state = "end"
        if self.state == "play" and self.robot != None and self.turn:
            self.cozmoModeMove()

game = TicTacToe()
cozmo.connect(game.runEverything)