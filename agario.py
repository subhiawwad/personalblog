import turtle 
from turtle import *
import time
import math
import random
from ball import Ball
RED = (255, 0 , 0)
tracer(0)
hideturtle()
RUNNING = True
	
SLEEP = 0.0077
SCREEN_WIDTH = getcanvas().winfo_width()/2
SCREEN_HEIGHT = getcanvas().winfo_height()/2




myball = Ball(5,6,7,14,50,"RED")
NUMBER_OF_BALLS = 5
MINIMUM_BALL_RADIUS = 10
MAXIMUM_BALL_RADIUS = 40
MINIMUM_BALL_DX = -5
MAXIMUM_BALL_DX = 5
MINIMUM_BALL_DY = -5
MAXIMUM_BALL_DY = 5

BAAAALL = []
for x in range ( NUMBER_OF_BALLS):
	x = random.randint(-SCREEN_WIDTH + MAXIMUM_BALL_RADIUS , SCREEN_WIDTH - MAXIMUM_BALL_RADIUS)
	y = random.randint(-SCREEN_HEIGHT + MAXIMUM_BALL_RADIUS, SCREEN_HEIGHT - MAXIMUM_BALL_RADIUS)
	dx=random.randint(MINIMUM_BALL_DX, MAXIMUM_BALL_DX)
	dy=random.randint(MINIMUM_BALL_DY, MAXIMUM_BALL_DY)
	r = random.randint(MINIMUM_BALL_RADIUS, MAXIMUM_BALL_RADIUS)
	# while dx ==0:
	# 	dx = random.randint(MINIMUM_BALL_DX, MAXIMUM_BALL_DX)
	# while dy ==0:
	# 	dy = random.randint(MINIMUM_BALL_DY, MAXIMUM_BALL_DY)
	color = (random.random(), random.random(), random.random())
	new_ball = Ball(x,y,dx,dy,r,color)
	BAAAALL.append(new_ball)
def move_all_balls():
	for new_ball in BAAAALL:
		new_ball.move(SCREEN_WIDTH, SCREEN_HEIGHT)
		
def collide (ball_a , ball_b):
	ball_a_x = ball_a.xcor()
	ball_b_x = ball_b.xcor()
	ball_a_y = ball_a.ycor()
	ball_b_y = ball_b.ycor()
	if ball_a == ball_b:
		return False
	D = (((ball_b_x- ball_a_x)**2)+ ((ball_b_y - ball_a_y)**2)**0.5)
	if D + 10 <= ball_a.r + ball_b.r :
		return True
	else:
		return False
def allcollision():
	for ball_a in BAAAALL:
		for ball_b in BAAAALL:
			if (collide(ball_a,ball_b)):
				ball_a_r=ball_a.r
				ball_b_r=ball_b.r
				
				if(ball_a_r>ball_b_r):
					ball_b.hideturtle()					


				if(ball_b_r>ball_a_r):
					ball_a.hideturtle()
def check_my_ball():
	for ball in BAAAALL:
		if (collide(ball,myball)) == True:
			ball_r =ball.r
			myball_r = myball.r

			if (ball_r > myball_r):
				myball.hideturtle()
				myball.r = myball_r + ball_a_r
				myball.shapesize(myball.r/10)
def movearound():
	myball.ondrag(myball.setpos)
def ff():
	for ball_a in BAAAALL:
		if (collide(ball_a,myball)):
			ball_a_r=ball_a.r
			myball_r=myball.r
				
			if(ball_a_r>myball_r):
				myball.hideturtle()					


			if(myball_r>ball_a_r):
				ball_a.hideturtle()	

while RUNNING:
	move_all_balls()
	getscreen().update()
	time.sleep(SLEEP)
	movearound()
	allcollision()
	collide(new_ball , myball)
	check_my_ball()
	ff()
mainloop()

