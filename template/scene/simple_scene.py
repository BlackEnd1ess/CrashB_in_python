from ursina import *
app=Ursina()

###### the scene
Sky(color=color.cyan)
scene.fog_density=(20,40)
scene.fog_color=color.white
Entity(model='plane',texture='grass',scale=(16,1,16),position=(0,-5,8),color=color.green)
EditorCamera()
################
app.run()