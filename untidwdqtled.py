from turtle import *
from turtle import Turtle
import turtle
import time
import random
turtle.tracer(0)
currentX= 0
currentY = 0
newX = 0
newY = 0
right= 0
left =0
top=0
bottom=0
RUNNING =True
SLEEP= 0.0077
SCREEN_WIDTH =turtle.getcanvas().winfo_width()/2
SCREEN_HEIGHT =turtle.getcanvas().winfo_height()/2
class Ball(Turtle):
    def __init__(self,x,y,dx,dy,r,Color):
        Turtle.__init__(self)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.r = r
        self.color = color
        self.penup()
        self.goto(x,y)
        self.shape('circle')
        self.shapesize(r/10)
        self.color(Color)
        self.hideturtle()
    def move(self,screenWidth,screenHeight):
        currentX= self.x
        currentY = self.y
        newX = currentX +self.dx
        newY = currentY +self.dy
        right= newX+self.r
        left =newX+self.r
        top=newY+self.r
        bottom=newY+self.r
        self.goto(newX,newY)
        self.x = newX
        self.y = newY
        if right>screenWidth:
            self.dx = -self.dx
        elif left<-screenWidth:
            self.dx = -self.dx
        if top > screenHight:
            self.dy = -self.dy
        elif bottom<-screenHeight:
            self.dy = -self.dy

turtle.exitonclick()

