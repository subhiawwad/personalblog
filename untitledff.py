class animal(object):
	def __init__(self,sound,name,age,favorite_color):
		self.sound = sound
		self.name = name
		self.age = age
		self.favorite_color = favorite_color
	def eat(self, food):
		print("Yummy!!" + self.name + " is eating " + food)
	def description(self):
		print(self.name + " is" + self.age + " months old and loves to eat " + self.favorite_color)
	def make_sound(self,num):
		print(self.sound*num)
class person(object):
	def __init__(self, name, age, gender):
		self.age = age
		self.name = name
		self.gender = gender
	def eat(self, food):
		print("Yummy!!" + self.name + " is eating " + food)
	def sleep(self):
		print(self.name + "is sleeping")
cat = animal(" meow", "minmin", " 9", "mansaf")
ta7sheesh = person("ta7sheesh", 3, "male")
cat.eat("mansaf")
cat.description()
cat.make_sound(3)
ta7sheesh.eat("ksldj")
ta7sheesh.sleep()