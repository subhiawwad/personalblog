import turtle
from turtle import *

SCREEN_WIDTH=400
SCREEN_HEIGHT=400
turtle.screensize(SCREEN_WIDTH,SCREEN_HEIGHT)
turtle.setup(SCREEN_WIDTH,SCREEN_HEIGHT)
NUMBER_OF_GHOSTS = 4
ghost_x=10
ghost_y=10          
ghost_r=10
ghost_dx=1
ghost_dy=1
ghost_color="red"
turtle.tracer(0)

class Ghost(Turtle):
    def __init__(self,x,y,dx,dy,r,Color):
        Turtle.__init__(self)
        self.dx = dx
        self.dy = dy
        self.r = r
        self.penup()
        self.goto(x,y)
        self.shape('circle')
        self.shapesize(r/10)
        self.color(Color)
    def move(self,screenWidth,screenHeight):
        currentX= self.xcor()
        currentY = self.ycor()
        newX = currentX +self.dx
        newY = currentY +self.dy
        right= newX+self.r
        left =newX-self.r
        top=newY+self.r
        bottom=newY-self.r
        self.goto(newX,newY)
        print(newX, newY)
        if right>screenWidth:
            self.dx = -self.dx
        elif left<-screenWidth:
            self.dx = -self.dx
        if top > screenHeight:
            self.dy = -self.dy
        elif bottom<-screenHeight:
            self.dy = -self.dy
ghost= Ghost(ghost_x,ghost_y,ghost_r,ghost_dx,ghost_dy,ghost_color)
while  True:
  ghost.move(SCREEN_WIDTH,SCREEN_HEIGHT)
time.sleep(0.0077)

turtle.exitonclick()
