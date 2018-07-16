"""
Breakout game. Implemented using pygame. 

Bouncing and movement functions taken from this particle simulation: http://www.petercollingridge.co.uk/book/export/html/6.
"""

print("hello darkness my old friend")

import pygame
import math
import breakout
import constants

""" 
Paddle: Methods
"""
# Update the position of the paddle. It is confined to the boundaries
# of the screen
paddle = breakout.create_new_paddle()
ball = breakout.create_new_ball()
def paddle_update_position(paddle):

        location = breakout.get_mouse_location()
        x_position = location[0]
        if (constants.SCREEN_WIDTH-constants.PADDLE_WIDTH)>x_position>0: 
            breakout.set_x(paddle, x_position)

   
    
"""
Ball: Methods
"""
# This function must update the coordinates of the ball and changes the 
# direction of the ball bounces of either the left, top, or right walls 
def ball_update_position(ball):

    x=breakout.get_x(ball)
    x_velocity=breakout.get_x_velocity(ball)
    y=breakout.get_y(ball)
    y_velocity=breakout.get_y_velocity(ball)
    x=x+x_velocity
    y=y+y_velocity
    breakout.set_x(ball, x)
    breakout.set_y(ball, y)
    breakout.set_x_velocity(ball, x_velocity)
    breakout.set_y_velocity(ball, y_velocity)
    new_x_velocity=x_velocity
    new_y_velocity=y_velocity
    

    if(constants.BALL_RADIUS>x or x>constants.SCREEN_WIDTH-constants.BALL_RADIUS):
        new_x_velocity= -1*x_velocity
        breakout.set_x_velocity(ball, new_x_velocity)
    if(constants.BALL_RADIUS>y):
        new_y_velocity=-1*y_velocity
        breakout.set_y_velocity(ball, new_y_velocity)
    if(y>constants.SCREEN_HEIGHT-constants.BALL_RADIUS):
        running=False






    #TODO
    

# This function must change the direction of the ball when it hits an 
# object 
def ball_bounce_off(ball):

    new_y_velocity=-1*breakout.get_y_velocity(ball)
    breakout.set_y_velocity(ball, new_y_velocity)



"""
Screen Update: Methods
"""
























































































































































































































































































































































































































































































# This function must render all objects on screen using breakout.py draw 
# methods. No objects should be created in this method. 
def draw_objects():
    breakout.clear_screen()
    for brick in bricks:
        
        brick_x=breakout.get_x(brick)
        brick_y=breakout.get_y(brick)
        brick_width=breakout.get_width(brick)
        brick_height=breakout.get_height(brick)
        brick_color=breakout.get_color(brick)
        breakout.draw_rectangle(brick_x, brick_y, brick_width, brick_height, brick_color)
    paddle_x=breakout.get_x(paddle)
    paddle_y=breakout.get_y(paddle)
    paddle_width=breakout.get_width(paddle)
    paddle_height=breakout.get_height(paddle)
    paddle_color=breakout.get_color(paddle)
    breakout.draw_rectangle(paddle_x, paddle_y, paddle_width, paddle_height, paddle_color) 
    ball_x=breakout.get_x(ball)
    ball_y=breakout.get_y(ball)
    ball_radius=breakout.get_radius(ball)
    ball_color=breakout.get_color(ball)
    breakout.draw_circle(ball_x,ball_y,ball_radius, ball_color)


    # Draw the paddle, ball, and wall of bricks
    # TODO

    # Tell pygame to actually redraw everything (DON'T CHANGE)
    pygame.display.flip()


# This function must create the set of bricks to be drawn at the top of 
# the screen. 
# This function returns a list of bricks created. 
def build_bricks():
    # Create an empty list
    bricks=[]
    # TODO 

        # Create the bricks and add them to list
    # Hint: You need a double or loop to draw the set of bricks on top of the screen. 
    # Set the brick color based on row number by using the colors in the constants.py
    # file. (You can add other colors if you wish). When you create a new brick and 
    # set the x,y, and color using breakout.py methods, add your brick to the list.
    # TODO 
    for n in range(constants.NUM_ROWS):
        y=n*(constants.BRICK_HEIGHT)+n*(constants.GAP)
        for i in range(constants.BRICKS_PER_ROW):
            x=i*(constants.BRICK_WIDTH)+(i+1)*(constants.GAP)
       
            brick=breakout.create_new_brick()
            breakout.set_x(brick, x)
            breakout.set_y(brick, y)
            breakout.set_color(brick, constants.RED)
            bricks.append(brick)
    return bricks
bricks=build_bricks()
    





# Creating the screen 
breakout.build_screen(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

# Create the ball, paddle, and bricks here using breakout.py functions.
# TODO


# These are variables used to detect the state of the game. 
running = True
start = False

while running:
    for brick in bricks:
        if(breakout.ball_did_collide_with(ball, brick, breakout.get_width(brick), breakout.get_height(brick))):
            ball_bounce_off(ball)
            bricks.remove(brick)



    paddle_update_position(paddle)

    if(breakout.ball_did_collide_with(ball, paddle, breakout.get_width(paddle), breakout.get_height(paddle))):
        ball_bounce_off(ball)
    if len(bricks) == 0:
        running=False


    
    # Setup the mouse events 
    # DO NOT change this code
    for event in pygame.event.get():
        # If you click the mouse, the ball will start moving 
        if pygame.mouse.get_pressed() == (1, 0, 0):
            start = True 
        if event.type == pygame.QUIT:
            running = False


    if start == True:
        ball_update_position(ball)
        # Make the ball update its position. 
       

    # Update the position of the paddle based on the mouse
    # TODO 
        
    # Check for collisions using breakout.ball_did_collide_with(ball, obj, width, height) 
    # TODO 

    # If ball hits the bottom wall, we lose.
    # TODO 

    # If bricks are all broken, you won! 
    # TODO 

    # Else, loop through the entire bricks list to see if the ball collided with any brick 
    # TODO 

    # Redraw everything at the end of the while loop
    draw_objects()

pygame.display.update()
