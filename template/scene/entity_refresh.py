from ursina import *
app=Ursina()

#### scene ####
Sky(color=color.black)
Entity(model='plane',texture='grass',scale=(16,1,16),position=(0,-2,0),color=color.green)
EditorCamera()
class MyClass(Entity):
	def __init__(self):
		super().__init__(model='cube',texture='brick',scale=2,color=color.violet,position=(0,0,0),alpha=.7)
	def update(self):
		self.rotation_y+=time.dt*50
MyClass()
##############

app.run()