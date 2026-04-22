import bpy,os,math

# === SETTINGS ===
model_path = "C:/Users/-_-/Desktop/3D_to_2D/gem.obj"
output_dir = "C:/Users/-_-/Desktop/3D_to_2D/frames"
num_frames = 33

os.makedirs(output_dir, exist_ok=True)

# === RESET SCENE ===
bpy.ops.wm.read_factory_settings(use_empty=True)

# === IMPORT ===
bpy.ops.wm.obj_import(filepath=model_path)
obj = bpy.context.selected_objects[0]
obj.scale=(.1,.1,.1)

# === CAMERA ===
cam_data=bpy.data.cameras.new("Cam")
cam=bpy.data.objects.new("Cam",cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

cam.location=(0,-80,25)
cam.rotation_euler = (math.radians(75),0,0)

# === LIGHT ===
light_data = bpy.data.lights.new(name="light",type='AREA')
light = bpy.data.objects.new(name="light", object_data=light_data)
bpy.context.collection.objects.link(light)
light.location = (0,-45,25)
light_data.energy=50000

# === RENDER SETTINGS ===
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.resolution_x = 128
scene.render.resolution_y = 128

# === ROTATION + RENDER ===
for i in range(num_frames):
	angle = (i / num_frames)*2*math.pi
	obj.rotation_euler[2]=angle
	filepath=os.path.join(output_dir, f"{i:01d}.png")
	scene.render.filepath=filepath
	bpy.ops.render.render(write_still=True)

print("Frames fertig!")
input(' ')