#!/usr/bin/env puthon

from Tkinter import *
import RPi.GPIO as GPIO
import time
import sqlite3
 
GPIO.setmode(GPIO.BCM)
 
enable_pin = 18
motor_1_pin = 4
motor_2_pin = 17
motor_3_pin = 23
motor_4_pin = 24
 
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(motor_1_pin, GPIO.OUT)
GPIO.setup(motor_2_pin, GPIO.OUT)
GPIO.setup(motor_3_pin, GPIO.OUT)
GPIO.setup(motor_4_pin, GPIO.OUT)
 
GPIO.output(enable_pin, 1)
 
 
 
 
def forward(delay, steps):
    power = 0
    GPIO.output(enable_pin, 1)
    for i in range(0, steps):
        power = power ^1
        setStep(power,power,power,power)
        time.sleep(delay)
    GPIO.output(enable_pin, 0)

def backwards(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
 
def setStep(w1, w2, w3, w4):
        GPIO.output(motor_1_pin, w1)
        GPIO.output(motor_2_pin, w2)
        GPIO.output(motor_3_pin, w3)
        GPIO.output(motor_4_pin, w4)


class Application(Frame):
    
    def setstate(self,caption,color,pstate,rcolor,rcaption):
        self.status["text"] = caption
        self.status["bg"] = color
        self.rstate = pstate
        self.run["text"] = rcaption
        self.run["bg"] = rcolor
		
    def select_recipe(self):
        for row in self.curs.execute( "SELECT * FROM recipe WHERE recipename='Default'" ):
            self.RunRecipe["text"] = row[0]
            print row[0]
            for row1 in self.curs.execute( "SELECT * FROM speed WHERE speedname=(?)" , (row[1],)):
                self.delay = row1[1]
                print self.delay
        self.selrecipe["bg"]   = "green"
        self.enable = TRUE
        self.step= 10000
     
        
    def state(self):
        if self.rstate == FALSE :
            print "RUN"
            self.setstate("RUNNING","green",TRUE,"red","STOP")
            time.sleep(.5)
            forward(self.delay, self.step)
		        
	else :
            print "STOP"
            self.setstate("STOPPED","red",FALSE,"green","START")
		
	
    def createWidgets(self):

        self.RecipeFrame = Label(self, text=" Recipe Details ",bg = "white",borderwidth =5)
        self.StatusFrame = Label(self, text=" Pump Status ",bg = "white",borderwidth =5)
        self.ControlFrame = Label(self, text=" Pump Controls ",bg = "white",borderwidth =5)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["bg"]   = "yellow"
        self.QUIT["command"] =  self.quit

        self.selrecipe = Button(self)
        self.selrecipe["text"] = "Select",
        self.selrecipe["bg"]   = "yellow"
        self.selrecipe["command"] = self.select_recipe


        self.RunRecipe = Label(self)
        self.RunRecipe["text"] = "No Recipe"


        self.run = Button(self)
        self.run["text"] = "Start"
        self.run["bg"] = "green"
        self.run["command"] = self.state


        self.status = Label(self)
        self.status["text"] = "STOPPED"
        self.status["bg"] = "red"

        self.RecipeFrame.grid(row=0, columnspan=2, sticky='W', \
            padx=5, pady=5, ipadx=5, ipady=5)	
        self.selrecipe.grid(row = 1, column = 0)
        self.RunRecipe.grid(row = 1 , column = 1)
        self.StatusFrame.grid(row=0, column = 2,columnspan=2, sticky='W', \
            padx=5, pady=5, ipadx=5, ipady=5)	
        self.status.grid(row = 1 , column = 2,columnspan = 2)
        self.ControlFrame.grid(row=4, column = 1,columnspan=2, sticky='W', \
            padx=5, pady=5, ipadx=5, ipady=5)	

        self.run.grid(row = 5 , column = 0)
        self.QUIT.grid(row = 5 , column = 3)
		


    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.wm_title("Pump Control")
        self.pack()
        self.createWidgets()
        self.rstate = FALSE
        self.enable = FALSE
        self.step= 0
        self.delay = 0
        self.conn=sqlite3.connect('pump.db')
        self.curs = self.conn.cursor()
        

 
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
