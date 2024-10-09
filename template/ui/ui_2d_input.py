from ursina import *
app=Ursina()

ADD_KEY='+'
SUB_KEY='-'

## UI
Entity(model='quad',scale=(2,1),color=color.black,parent=camera.ui,z=1)
# class as Text doesnt refresh in update, it must be entity or animation
class MyText(Entity):
	def __init__(self):
		super().__init__()
		self.info=Text('',scale=2,position=(-.3,0),color=color.orange,parent=camera.ui)
		self.my_number=0
	def input(self,key):
		if key == ADD_KEY:
			self.my_number+=1
		if key == SUB_KEY:
			if self.my_number > 0:
				self.my_number-=1
	def update(self):
		self.info.text=f'Score: {self.my_number}'
MyText()
####
app.run()