from ursina import *
app=Ursina()

## UI
Entity(model='quad',scale=(2,1),color=color.black,parent=camera.ui,z=1)
Text('ABCDEF 123456789',position=(0,0),scale=2,parent=camera.ui,color=color.orange)
####
app.run()