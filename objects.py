import _core,player,status,item,sound,ui,animation
from ursina.shaders import *
from ursina import *

texp='res/terrain/texture/'
terra_path='res/terrain/'
omf='res/objects/'
m='mesh'
b='box'
st=status
cc=_core

## map objects

def spawn_tree_wall(pos,cnt,d):
	tro={0:-45,1:45}
	for tsp in range(0,cnt):
		Tree2D(pos=(pos[0]+random.uniform(-.2,.2),pos[1],pos[2]+tsp*2),rot=tro[d])

def platform_move(d):
	if d.direct == 0:
		if d.turn == 0:
			d.x+=time.dt*d.speed
			if d.x >= d.spawn_pos[0]+1:
				d.turn=1
		if d.turn == 1:
			d.x-=time.dt*d.speed
			if d.x <= d.spawn_pos[0]-1:
				d.turn=0

def bush(pos,s,c):
	Entity(model='quad',texture=omf+'bush/bush1.png',position=pos,scale=s,color=c)

class MossPlatform(Entity):
	def __init__(self,p,MO,TU):
		super().__init__(model=omf+'p_moss/moss.ply',texture=omf+'p_moss/moss.tga',rotation_x=-90,scale=0.00075,position=p,collider=b,unlit=False)
		self.spawn_pos=p
		self.movable=MO
		self.direct=0
		self.speed=.7
		self.turn=TU
		if not self.movable:
			self.collider=None
			self.pgnd=Entity(model='cube',scale=(.6,1,.6),position=(self.x,self.y-.48,self.z),collider=b,visible=False)
	def update(self):
		if self.movable:
			platform_move(self)

class StoneTile(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'tile0/tile.obj',texture=omf+'tile0/platform_top.png',position=pos,scale=.3)
		self.hit_b=Entity(model='cube',scale=(.7,self.scale_y,.7),position=self.position,collider=b,visible=False)

class Water(Animation):
	def __init__(self,pos,s,c,a):
		super().__init__(omf+'water/water.gif',position=pos,scale=(s[0],s[1]),rotation_x=90,texture_scale=(s[0],s[1]),color=c,alpha=a)
		WaterHit(p=(self.x,self.y-.1,self.z),sc=s)

class WaterFlow(Entity):
	def __init__(self,pos):
		super().__init__(model='plane',texture=omf+'water_flow/water_f0.png',scale=(3.5,.1,96),texture_scale=(1,16),position=pos,filtering='linear')
		self.dark_area=Entity(model='plane',color=color.black,scale=self.scale,position=(self.x,self.y-.001,self.z),alpha=.7)
		self.static_y=self.y
		self.s_texture=0
		#self.tileset_size
	def update(self):
		self.s_texture+=time.dt*9
		if self.s_texture > 3.8:
			self.s_texture=0
		self.texture=omf+'water_flow/water_f'+str(int(self.s_texture))+'.png'

class SingleBlock(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'sblock/sblock.obj',texture='sblock/sblock.png',scale=0.5,collider=b,position=pos)

class BackgroundWall(Entity):
	def __init__(self,p):
		super().__init__(model=omf+'wall_0/turtle_wall.obj',texture=omf+'wall_0/wall_wood.tga',scale=.02,position=p,rotation_y=-90,double_sided=True,unlit=False)
		self.curtain=Entity(model='quad',texture=omf+'bush/bush1.png',position=(self.x,self.y,self.z+1.5),scale=(20,6),color=color.rgb(0,50,0))
		self.inv_wall=Entity(model='cube',scale=(20,6),position=self.position,collider=b,visible=False)
		for bu in range(8):
			aC=random.choice([color.green,color.orange,color.yellow])
			Entity(model='quad',texture=omf+'bush/bush1.png',position=(self.x-8+bu*2,self.y+2.75,self.z-1+random.uniform(.1,.5)),scale=random.uniform(3,4),color=aC)

class MapTerrain(Entity):
	def __init__(self,MAP,size,t,co):
		super().__init__(model=Terrain(terra_path+MAP,skip=18),collider=m,scale=size,texture=t,texture_scale=(size[0],size[2]),color=co)
		cc.map_zone=self
		cc.map_coordinate=self.model.height_values
		cc.map_size=self.scale
		FallingZone(pos=(self.x,self.y-1.5,self.z),s=(size[0]*1.5,1,size[2]*1.5))

class BigPlatform(Entity):
	def __init__(self,p,s):
		super().__init__(model=omf+'ground/ground01.obj',texture=terra_path+'texture/grass.png',scale=(s[0],1.5,s[2]),collider=b,position=p)
		self.front_wall=Entity(model=omf+'ground/ground_wall.obj',texture=texp+'bricks.png',scale=(self.scale_x-.01,3,self.scale_z-.01),color=color.rgb(170,200,170),collider=b)
		self.front_wall.position=(self.x,self.y-self.scale_y+.3,self.z)
		self.front_wall.texture_scale=(8,8)
		self.texture_scale=(self.scale_x*4,self.scale_z*4)
		self.color=color.rgb(0,140,0)

class Corridor(Entity):
	def __init__(self,pos):
		super().__init__(model=omf+'w_corr/corridor.obj',texture=omf+'w_corr/f_room.tga',scale=.1,position=pos,rotation_y=-90,double_sided=True)
		self.wall0=Entity(model='cube',visible=False,scale=3,position=(self.x+2.5,self.y,self.z),collider=b)
		self.wall1=Entity(model='cube',visible=False,scale=3,position=(self.x-2.5,self.y,self.z),collider=b)
		self.wall1=Entity(model='cube',visible=False,scale=3,position=(self.x,self.y+5.5,self.z),collider=b)

class Tree2D(Entity):
	def __init__(self,pos,rot):
		tCOL=random.choice([color.green,color.orange,color.yellow])
		super().__init__(model='quad',texture=omf+'tree/tree'+str(random.randint(1,3))+'.png',scale=3,position=pos,rotation_y=rot,color=tCOL)

class TreeScene(Entity):
	def __init__(self,pos,c,s):
		super().__init__(model=omf+'tree/scene_w.obj',texture=omf+'tree/wood_scene.tga',scale=s,position=pos,color=c,double_sided=True)
		bush(pos=(self.x,self.y+1.3,self.z-.25),c=color.green,s=2)
		bush(pos=(self.x-.6,self.y+.8,self.z-.249),c=color.yellow,s=1)
		bush(pos=(self.x+.6,self.y+.8,self.z-.249),c=color.orange,s=1)

class InvWall(Entity):
	def __init__(self,pos,sca):
		super().__init__(model='cube',position=pos,scale=sca,visible=False,collider=b)

## important objects
class IndoorZone(Entity): ## disable rain
	def __init__(self,pos,ty):
		super().__init__(model='sphere',scale=1,position=pos,visible=False)
		self.active=False
	def check_indoor(self):
		if cc.is_nearby_pc(self,DX=3,DY=3):
			status.c_indoor=True
		else:
			status.c_indoor=False
	def update(self):
		if self.active:
			self.check_indoor()
		if cc.is_nearby_pc(self,DX=3,DY=3):
			self.active=True
			return
		self.active=False

class FallingZone(Entity):## falling
	def __init__(self,pos,s):
		super().__init__(model='cube',collider=b,scale=s,position=pos,visible=False)

class WaterHit(Entity): ## collider for water
	def __init__(self,p,sc):
		super().__init__(model='cube',collider=b,position=p,scale=(sc[0],.2,sc[1]),visible=False)

class WarpRingEffect(Entity): ## spawn animation
	def __init__(self,pos):
		super().__init__(model=omf+'warp_rings/0.ply',texture=omf+'warp_rings/ring.tga',scale=.0016/2,rotation_x=-90,position=pos,color=color.white,alpha=.8,unlit=False)
		Audio(sound.snd_spawn)
		self.rings=0
		self.times=0
	def update(self):
		self.rings+=time.dt*30
		if self.rings > 8.75:
			self.rings=0
			self.times+=1
		if self.times > 5:
			cc.playerInstance[0].warped=True
			self.disable()
			return
		self.model=omf+'warp_rings/'+str(int(self.rings))+'.ply'

class CrateScore(Entity):## game finish
	def __init__(self,pos):
		super().__init__(model='res/crate/crate_sup.obj',texture='res/crate/crate_sup.png',alpha=.5,scale=.18,position=pos)
		self.cc_text=Text(parent=scene,position=(self.x-.2,self.y+.25,self.z),text=None,font='res/ui/font.ttf',color=color.rgb(255,255,128),scale=10)
	def update(self):
		self.cc_text.text=str(st.crate_count)+'/'+str(st.crates_in_level)
		if not st.gproc():
			self.rotation_y-=120*time.dt
		if st.crates_in_level > 0 and st.crate_count >= st.crates_in_level:
			Audio(sound.snd_rward)
			item.GemStone(pos=(self.x,self.y,self.z),c=0)
			self.cc_text.disable()
			self.disable()
			return
		if st.level_index == 1 and st.crate_count <= 0 or st.crates_in_level <= 0:
			self.hide()
			self.cc_text.hide()
			return
		self.show()
		self.cc_text.show()

class StartRoom(Entity): ## game spawn point
	def __init__(self,pos):
		super().__init__(model=omf+'s_room/room1.ply',texture=omf+'s_room/room.tga',position=pos,scale=(.07,.07,.08),rotation=(270,90),collider=None,unlit=False)
		self.floor0=Entity(model='cube',collider=b,position=(self.x,self.y+.6,self.z-.2),scale=(1.7,.5,1.7),visible=False)
		self.floor1=Entity(model='cube',collider=b,position=(self.x,self.y+.2,self.z+1.7),scale=(2,.5,2),visible=False)
		self.wall0=Entity(model='cube',collider=b,position=(self.x-1,self.y+1.5,self.z),scale=(.4,3,6),visible=False,rotation_z=10)
		self.wall1=Entity(model='cube',collider=b,position=(self.x+1,self.y+1.5,self.z),scale=(.4,3,6),visible=False,rotation_z=-10)
		self.back0=Entity(model='cube',collider=b,position=(self.x,self.y+1.5,self.z-1),scale=(5,3,.6),visible=False,rotation_x=10)
		self.ceil=Entity(model='plane',collider=b,position=(self.x,self.y+2.5,self.z-.2),scale=3,visible=False)
		self.curt=Entity(model='plane',position=(self.x,self.y+0.01,self.z),color=color.black,scale=3)
		self.door=Entity(model=omf+'door1/0.ply',texture=omf+'door1/door.tga',position=(self.x,self.y+2,self.z+2.2),scale=.001,rotation=(90,0,0),collider=b,unlit=False)
		self.door1=Entity(model=omf+'door/0.ply',texture=omf+'door/door.tga',position=(self.x,self.y+2.1,self.z+2.2),scale=.001,rotation_x=90,collider=b,unlit=False)
		self.door_open=False
		self.door_move=False
		self.door_time=.7
		ui.PauseMenu()
		cc.preload_items()
		player.CrashB(pos=(self.x,self.y+.6,self.z-.1))
		status.checkpoint=(self.x,self.y+2,self.z)
		camera.position=(self.x,self.y+2,self.z-3)
		IndoorZone(pos=self.position,ty=0)
	def update(self):
		if not self.door_open:
			if cc.is_nearby_pc(self,DX=.09,DY=3):
				self.door_open=True
				self.door_move=True
				Audio(sound.snd_d_opn)
				return
		if self.door_move:
			animation.door_open(self)

class RewardRoom(Entity):## here spawns the gem
	def __init__(self,pos,c):
		eR=omf+'e_room/end_room'
		super().__init__(model=eR+'.obj',texture=eR+'.tga',scale=.025,rotation_y=-90,position=pos,double_sided=True,color=c,unlit=False)
		self.ground_m=Entity(model='cube',position=(self.x,self.y-.95,self.z+1.7),scale=(4,.3,8),collider=b,visible=False)
		self.pod1=Entity(model='cube',position=(self.x+.13,self.y-.75,self.z+3.4),scale=(1.5,.2,1.5),collider=b,visible=False)
		self.pod2=Entity(model='cube',position=(self.x+.15,self.y-.6,self.z+3.4),scale=(.7,.2,.7),collider=b,visible=False)
		self.wall_l=Entity(model='cube',position=(self.x-1.7,self.y,self.z+2),scale=(2,3,7),collider=b,visible=False)
		self.wall_r=Entity(model='cube',position=(self.x+2,self.y,self.z+2),scale=(2,3,7),collider=b,visible=False)
		self.ceil=Entity(model='cube',position=(self.x,self.y+.8,self.z+2),scale=(4,.3,7),collider=b,visible=False)
		self.door=Entity(model=omf+'door1/0.ply',texture=omf+'door1/door.tga',position=(self.x+.2,self.y+.8,self.z-1.3),scale=.001,rotation=(90,0,0),collider=b,unlit=False)
		self.door1=Entity(model=omf+'door/0.ply',texture=omf+'door/door.tga',position=(self.x+.2,self.y+.9,self.z-1.3),scale=.001,rotation_x=90,collider=b,unlit=False)
		IndoorZone(pos=(self.x+.1,self.y,self.z+1.8),ty=1)
		self.gived_gem=False
		self.door_open=False
		self.door_move=False
		self.door_time=.7
		CrateScore(pos=(self.x+.15,self.y-.35,self.z+3.4))
		if status.level_index == 1 and not 4 in status.COLOR_GEM:
			item.GemStone(pos=(self.x+.15,self.y-.35,self.z+3.4),c=4)
	def update(self):
		if not self.door_open and cc.is_nearby_pc(self,DX=3,DY=3):
			self.door_open=True
			self.door_move=True
			Audio(sound.snd_d_opn)
		if self.door_move:
			animation.door_open(self)

class EndRoom(Entity): ## finish level
	def __init__(self,pos,c):
		eR=omf+'e_room/e_room2'
		super().__init__(model=eR+'.obj',texture=eR+'.tga',scale=.013,rotation_y=-90,position=pos,double_sided=True,color=c,unlit=False)
		self.door=Entity(model=omf+'door1/0.ply',texture=omf+'door1/door.tga',position=(self.x-.3,self.y+.4,self.z+.6),scale=.001,rotation=(90,0,0),collider=b,unlit=False)
		self.door1=Entity(model=omf+'door/0.ply',texture=omf+'door/door.tga',position=(self.x-.3,self.y+.5,self.z+.6),scale=.001,rotation_x=90,collider=b,unlit=False)
		self.rgnd0=Entity(model='cube',scale=(5,.5,3),position=(self.x,self.y-1.37,self.z+1.6),collider=b,visible=False)
		self.rgnd1=Entity(model='cube',scale=(2,.5,1.5),position=(self.x-.5,self.y-.9,self.z+2.8),collider=b,visible=False)
		self.rcln=Entity(model='cube',scale=(5,.5,3),position=(self.x,self.y+.6,self.z+1.6),collider=b,visible=False)
		self.rwall1=Entity(model='cube',scale=(3,3,4),position=(self.x-2.5,self.y,self.z+1.6),collider=b,visible=False)
		self.rwall2=Entity(model='cube',scale=(3,3,4),position=(self.x+1.9,self.y,self.z+1.6),collider=b,visible=False)
		self.rfront=Entity(model='cube',scale=(5,3,1),position=(self.x,self.y,self.z+4),collider=b,visible=False)
		IndoorZone(pos=(self.x+.1,self.y,self.z+1.8),ty=1)
		LevelFinish(p=(self.x,self.y-.8,self.z+2.7))
		self.door_open=False
		self.door_move=False
		self.door_time=.7
	def update(self):
		if not self.door_open and cc.is_nearby_pc(self,DX=3,DY=3):
			self.door_open=True
			self.door_move=True
			Audio(sound.snd_d_opn)
		if self.door_move:
			animation.door_open(self)

class BonusPlatform(Entity): ## switch -> bonus round
	def __init__(self,pos):
		super().__init__(model=omf+'bonus/bonus.obj',texture='grass',collider=b,color=color.azure,scale=(.15,.2,.15),position=pos)
		self.target=_core.playerInstance[0]
		self.orginal_pos=self.position
		self.catch_player=False
		self.air_time=0
	def update(self):
		if self.catch_player:
			cc.platform_floating(m=self,c=self.target)

class GemPlatform(Entity): ## gem platform
	def __init__(self,pos,t):
		if t in status.COLOR_GEM:
			ne='gem_platform'
			self.is_enabled=True
		else:
			ne='gem_platform_e'
			self.is_enabled=False
		L=180
		GMC={0:color.rgb(130,130,140),1:color.rgb(L,0,0),2:color.rgb(0,L,0),3:color.rgb(L,0,L),4:color.rgb(0,0,L+70),5:color.rgb(L,L,0)}
		super().__init__(model=omf+ne+'/'+ne+'.ply',texture=omf+ne+'/'+ne+'.tga',rotation_x=-90,scale=0.001,position=pos,shader=unlit_shader,collider=b,unlit=False)
		self.bg_darkness=Entity(model=Circle(12,mode='ngon',thickness=.1),position=(self.x,self.y-.011,self.z),rotation_x=90,color=color.black,scale=.7,alpha=.9)
		self.target=_core.playerInstance[0]
		self.orginal_pos=self.position
		self.catch_player=False
		self.air_time=0
		self.color=GMC[t]
		if not self.is_enabled:
			self.collider=None
			self.bg_darkness.hide()
	def update(self):
		if self.is_enabled:
			self.bg_darkness.position=(self.x,self.y-.01,self.z)
			self.rotation_y+=time.dt*20
			if self.catch_player:
				cc.platform_floating(m=self,c=self.target)
				return

class LevelFinish(Entity): ## finish level
	def __init__(self,p):
		super().__init__(model=omf+'podium/gear.obj',collider=b,texture='gear_diffuse.png',scale=(.6,.8,.6),position=p)