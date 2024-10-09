from ursina import *
app=Ursina()

## UI
Entity(model='quad',scale=(2,1),color=color.black,parent=camera.ui,z=1)
# class as Text doesnt refresh in update, it must be entity or animation
class MyText(Entity):
	def __init__(self):
		super().__init__()
		self.info=Text('',scale=2,position=(-.5,0),color=color.orange,parent=camera.ui)
	def update(self):
		self.info.color=color.random_color()
		self.info.text=f'DELTA TIME: {time.dt}'
MyText()
####
app.run()