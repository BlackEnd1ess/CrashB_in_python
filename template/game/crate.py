from ursina import *
app=Ursina()

###################
Sky(color=color.black)
EditorCamera()
Entity(model='plane',texture='grass',color=color.green,scale=16)

crates_collected=0
crates_in_level=0

## counter
class CrateCounter(Entity):
	def __init__(self):
		super().__init__()
		self.count=Text('',color=color.orange,position=(0,.4,0),parent=camera.ui,scale=2)
	def update(self):
		self.count.text=f'{crates_collected}/{crates_in_level}'
CrateCounter()

## crate
class MyCrate(Entity):
	def __init__(self,pos,ID):
		super().__init__(model='cube',texture='brick',position=pos,scale=.5,color=color.gray)
		self.vnum=ID
		if ID == 3:
			self.color=color.green
	def input(self,key):
		if self.vnum == 3:
			if key == 'space':
				self.destroy()
	def destroy(self):
		global crates_collected
		crates_collected+=1
		self.parent=None
		self.disable()
		scene.entities.remove(self)

## spawn multible crates
for crates in range(8):
	crates_in_level+=1
	MyCrate(pos=(0+crates,.5,0),ID=crates)

#####################
app.run()