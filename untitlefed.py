class Animal(object):
	def __init__(self,name,species,age,favorite_color):
		self.name = name
		self.species = species
		self.age = age
		self.favorite_color = favorite_color
class Cat(Animal):
	 def mashi_wana_mashi(self, sound):
	 	 print(sound + "!","Johhnie mashi wana mashi m3aah" + self.name)

Johhnie = Cat(name= "Johhnie",species="cat",age = "17",favorite_color="blue")
Johhnie.mashi_wana_mashi("Johhnie mashi wana mashi m3aah")



class bird(Animal):
	def fly(self, action):
		print(action+"high"+action+"drunk")
hamada=bird("hamada","bird","2","green")
hamada.fly("shibs")		
class chicken(bird):
	def cant_fly(self, ma3zeh):
		print("sho sawena" +ma3zeh+"bi 3enena"+ma3zeh
tamer=chicken("tamer","bird","28","red")
tamer.cant_fly("i7reg george")			