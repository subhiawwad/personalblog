from turtle import *

class Ball(Turtle):
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
        # self.hideturtle()
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

