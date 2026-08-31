import status,_core,_loc,sound,time,random
from ursina.ursinastuff import destroy
from panda3d.core import NodePath
from ursina import Entity,color
import gltf

non_loop_index=(3,4,6,9,10,11,15,16,18,19)

cf='res/box/anim/'
nf='res/npc/'

ASC=.0028

st=status
sn=sound
cc=_core
LC=_loc

######################## box animation #########################
vcol={3:color.rgb32(180,110,0),11:color.red,12:color.green,15:color.gold,16:color.rgb32(180,0,180)}
class BoxBreakAnimation(Entity):
	def __init__(self,pos,ID):
		if ID != 6:
			col=color.orange if not (ID in vcol) else vcol[ID]
			scr=.0005
			mdl=LC.box_break_anim
		else:
			col=color.light_gray
			scr=.0008
			mdl=LC.checkp_break_anim
		super().__init__(position=(pos[0],pos[1]-.16,pos[2]))
		set_memory_glb_value(self,fps=25,sca=scr,model=mdl)
		set_glb_color(self,col=col,UNLIT=True,brightness=1.3)
		del pos,ID,col
	def refr_anim(self):
		s=self
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			destroy(s)
			return
		set_glb_frame(s)
	def update(self):
		if st.gproc():
			return
		self.refr_anim()

bna={3:'box_bounce',
	7:'box_spring_wood',
	6:'box_checkpoint',
	8:'box_spring_iron',
	9:'box_switch_empty',
	10:'box_switch_nitro',
	14:'box_protected',
	99:'box_spring_wood'}
class BoxBounceAnimation(Entity):
	def __init__(self,c):
		s=self
		if not c:
			super().__init__()
			destroy(s)
			del s,c
			return
		s.glb_model=f'res/box/{bna[c.vnum] if c.vnum in bna else 99}.glb'
		super().__init__(position=(c.x,c.y-.16,c.z))
		set_glb_value(s,fps=25,sca=.0008)
		set_glb_color(s,col=color.light_gray,UNLIT=True,brightness=1.3)
		s.box_root=c
		del c,s
	def update(self):
		if st.gproc():
			return
		s=self
		if not s.box_root:
			destroy(s)
			return
		if s.box_root.visible:
			s.box_root.visible=False
		s.new_index+=time.dt*s.fps
		if s.new_index >= len(s.frames):
			s.box_root.visible=True
			destroy(s)
			return
		set_glb_frame(s)

###################################################################
###################################################################

######################## player animation #########################
def set_crash_animation(g,sca,fps):
	g.models=LC.crash_animation
	g.frames_all={}
	for n,root in g.models.items():
		root.setScale((ASC,ASC-.001,ASC))
		root.reparentTo(g)
		root.hide()
		frames=list(root.findAllMatches('**/frame_*'))
		frames.sort(key=lambda node:node.getName())
		for frame in frames:
			frame.hide()
		frames[0].show()
		g.frames_all[n]=frames
	g.root=g.models[0]
	set_glb_color(g,col=color.light_gray,UNLIT=True,brightness=1.5)
	g.frames=g.frames_all[0]
	g.frame_index=0
	g.new_index=0
	g.fps=fps
	g.root.show()

def c_animation(idx):
	g=LC.ACTOR
	if idx != g.anim_idx:
		c_switch_model(g,idx)
		g.anim_idx=idx
	g.new_index+=time.dt*g.fps
	if g.new_index >= len(g.frames):
		if not st.death_event:
			cc.c_anim_flag(g.anim_idx)
		if idx in non_loop_index:
			return
		g.new_index=0
	set_glb_frame(g)

def c_switch_model(g,idx):
	if g.anim_idx == idx:
		return
	if g.frames:
		g.frames[g.frame_index].hide()
	g.root.hide()
	g.anim_idx=idx
	g.root=g.models[idx]
	g.frames=g.frames_all[idx]
	set_glb_color(g,col=color.white,UNLIT=False if idx in (14,17) else True,brightness=1.5)
	g.new_index=0
	g.frame_index=0
	g.frames[0].show()
	g.root.show()

def refr_player_animation(c):
	if c.is_flip:
		c_animation(8)#flip
		return
	if c.is_spin:
		c_animation(5)#spin
		return
	if c.stun_time > 0:
		c_animation(12)#stun fly
		return
	if c.pushed:
		c_animation(13)#push back
		return
	if c.standup:
		c_animation(11)#stand up from b smash
		return
	if c.is_landing and c.landed and c.b_smash and not c.standup:
		c_animation(10)#belly smash land
		return
	if c.jumping:
		if c.air_time < .1 and c.walking and not (c.is_flip or c.falling):
			c.is_flip=True
			c.frm=0
			return
		c_animation(4)#jump up
		return
	if c.landed:
		if st.p_idle(c) or c.freezed:
			if c.is_slp:
				c_animation(3)#idle ice slippery
				return
			c_animation(0)#idle stand
			return
		if c.walking and not c.jumping:
			if c.is_slp:
				c_animation(2)#slippery walk
				return
			c_animation(1)#walk normal
			return
		if c.is_landing and not c.jumping:
			c_animation(6)#normal landing
			return
		return
	if c.falling:
		if c.b_smash:
			c_animation(9)#b smash
			return
		c_animation(7)#fall

def refr_npc_animation(n):
	n.new_index+=time.dt*n.fps
	if n.new_index >= len(n.frames):
		n.new_index=0
		if hasattr(n,'rand_wait') and getattr(n,'rand_wait',True):
			n.tme=random.uniform(n.wait_min_max[0],n.wait_min_max[1])
	set_glb_frame(n)

###################################################################
###################################################################

def set_glb_value(g,fps,sca):
	if hasattr(g,'root'):
		g.root.removeNode()
		g.root=None
	g.root=gltf.load_model(g.glb_model,gltf.GltfSettings(legacy_materials=True,no_srgb=True))
	g.root=NodePath(g.root)
	g.root.setScale(sca)
	g.root.reparentTo(g)
	g.frames=list(g.root.findAllMatches('**/frame_*'))
	g.frames.sort(key=lambda node:node.getName())
	g.frame_index=0
	g.new_index=0
	g.fps=fps
	for frame in g.frames:
		frame.hide()
	g.frames[0].show()

def set_switch_glb_value(g,fps,sca,lst):
	g.models={}
	g.frames_all={}
	for n,path in lst.items():
		root=NodePath(gltf.load_model(path,gltf.GltfSettings(legacy_materials=True,no_srgb=True)))
		root.setScale(sca)
		root.reparentTo(g)
		root.hide()
		frames=list(root.findAllMatches('**/frame_*'))
		frames.sort(key=lambda node:node.getName())
		for frame in frames:
			frame.hide()
		frames[0].show()
		g.models[n]=root
		g.frames_all[n]=frames
	g.root=g.models[0]
	g.frames=g.frames_all[0]
	g.root.show()
	g.frame_index=0
	g.new_index=0
	g.fps=fps

def set_memory_glb_value(g,fps,sca,model):
	g.root=model.copyTo(g)
	g.root.setScale(sca)
	g.frames=list(g.root.findAllMatches('**/frame_*'))
	g.frames.sort(key=lambda node:node.getName())
	g.frame_index=0
	g.new_index=0
	g.fps=fps
	for frame in g.frames:
		frame.hide()
	g.frames[0].show()

def set_glb_color(g,col,UNLIT,brightness=1):
	if not UNLIT:
		g.root.setLightOff(0)
		g.setLightOff(0)
	else:
		g.clearLight()
		g.root.clearLight()
	g.root.setColorScale(col.r*brightness,col.g*brightness,col.b*brightness,col.a)
	g.setColorScale(col.r*brightness,col.g*brightness,col.b*brightness,col.a)

def set_glb_frame(g):
	if g.new_index == g.frame_index:
		return
	g.frames[int(g.frame_index)].hide()
	g.frames[int(g.new_index)].show()
	g.frame_index=int(g.new_index)