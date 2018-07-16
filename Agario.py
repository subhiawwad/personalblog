import pygame



import sys



import time



import random



# import breakout



from pygame.locals import *



SCREEN_WIDTH = 1000

SCREEN_HEIGHT = 700



pygame.init()

pygame.display.set_caption("Basics")

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))



# Define variables



BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

GREEN = (0, 255, 0)

RED = (255, 0, 0)



class Circles(object):



    def __init__(self):

        self.x = 0

        self.y = 0

        self.radius = 50

        

        self.x_velocity = random.randint(-3,3)

        self.y_velocity=random.randint(-3,3)

        self.new_x_velocity=0

        self.new_y_velocity=0

        self.color = RED



class Player_circle(object):

	def __init__(self):

		self.x=SCREEN_WIDTH/2

		self.y=SCREEN_HEIGHT/2

		self.radius=20

		self.color=RED

		self.x_velocity = 0

		self.y_velocity=0

	def set_pos(self, (x, y)):

		self.x = x

		self.y = y

	def get_parameters(self):

		return (self.x,self.y,self.radius,self.color)



def draw_text(x, y, text, color, size):

    myfont = pygame.font.SysFont("monospace", size)

    # render text

    label = myfont.render(text, 1, color)

    screen.blit(label, (x, y))



def choose_random_color():

	r = random.randint(20,255)

	g = random.randint(20,255)

	b = random.randint(20,255)

	return (r,g,b)



def build_circles():

	random_circles=[]

	for n in range(600):

		cc = Circles()

		cc.x=random.randint(-2*SCREEN_WIDTH,SCREEN_WIDTH*3)

		cc.y=random.randint(-2*SCREEN_HEIGHT,SCREEN_HEIGHT*3)

		cc.radius=random.randint(5,100)

		cc.color= choose_random_color() 

		random_circles.append(cc)

	return random_circles





def	move_random_circles():

	for cc in circles:

		x=cc.x

		y=cc.y 

		

			

		# if random.randint(0, 20) == 7:

		# 	cc.y_velocity = cc.y_velocity*-1

		cc.x=x+cc.x_velocity

		cc.y=y+cc.y_velocity

		if (x>3*SCREEN_WIDTH and cc.x_velocity > 0):

			cc.new_x_velocity=(-1) * (cc.x_velocity)

			cc.x_velocity=cc.new_x_velocity

		elif (x<-2*SCREEN_WIDTH and cc.x_velocity < 0):

			cc.new_x_velocity=(-1) * (cc.x_velocity)

			cc.x_velocity=cc.new_x_velocity

		if(y>3*SCREEN_HEIGHT and cc.y_velocity > 0):

			cc.new_y_velocity= (-1)*cc.y_velocity

			cc.y_velocity=cc.new_y_velocity

		elif (y<-2*SCREEN_HEIGHT and cc.y_velocity > 0):

			cc.new_y_velocity= (-1)*cc.y_velocity

			cc.y_velocity=cc.new_y_velocity



def draw_circles():

	for cc in circles:

		x=cc.x

		y=cc.y

		radius=cc.radius

		# x_velocity=cc.x_velocity

		color=cc.color

		pygame.draw.circle(screen, color, [x,y], radius, 0)

	#(x,y,radius,color)

	player = pc.get_parameters()

	pygame.draw.circle(screen, player[3], [player[0],player[1]], player[2], 0)	



def get_colliding_circles():

	for i in range(len(circles)-1, -1, -1):

		cc = circles[i] 

		#check to see if pc collided with circle

			#check if eating smaller or being eaten by bigger

		if (pc.x +pc.radius >= cc.x  and pc.x - pc.radius <= cc.x ):

			if (pc.y +pc.radius  >= cc.y and pc.y - pc.radius <= cc.y):

				

				if (pc.radius>cc.radius):


					pc.radius=pc.radius+cc.radius/7

					del circles[i]

				else:



					

					pygame.quit()

					sys.exit()



		







pc=Player_circle()



start=False

circles = build_circles()	







while True:

	screen.fill(BLACK)

		

	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:

				pygame.quit()

				sys.exit()



		if event.type == QUIT:



			pygame.quit()

			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:

			start = True

			#### Respond to events

	

	if start == True:

		pc.set_pos(pygame.mouse.get_pos())

		draw_text(0, 0, ("score:")+str(pc.radius), WHITE, 40)

		move_random_circles()

		# draw_circles()

		get_colliding_circles()

		draw_circles()





	#### Make animations



	



	#### Update display



	pygame.display.update()



	time.sleep(0.01)

