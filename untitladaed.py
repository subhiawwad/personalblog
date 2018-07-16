from turtle import Turtle
class ball(Turtle):
	def __init__(self,size,color):
			Turtle.__init__(self)
			self.color(color)
			self.shapesize(size)
			self.shape("circle")
circle=ball(10,"blue")

