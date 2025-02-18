import gc,os,ui,settings,psutil,_loc,status,sys
from collections import defaultdict
from collections import Counter
from ursina import *
CV=camera.ui
LC=_loc
st=status

#pos info
def pos_info(c):
	sx=f"{c.x:.1f}"
	syc=f"{c.y+.16:.2f}"#crate
	syw=f"{c.y+.2:.2f}"#wumpa
	sz=f"{c.z:.1f}"
	#print(f"mt.crate_block(ID=14,POS=({sx},{syc},{sz}),CNT=[2,2,2])")
	#print(f"c.place_crate(ID=0,p=({sx},{syc},{sz}))")
	print(f"mt.wumpa_row(POS=({sx},{syw},{sz}),CNT=4,WAY=1)")

#player attr info
class PlayerDBG(Entity):
	def __init__(self):
		sx=-.87
		fw=1.5
		hg=.225
		s=self
		super().__init__()
		tct=settings.debg_color
		Entity(model='quad',position=(-.76,-.25),color=color.black,alpha=.75,scale=(.4,.8),z=1,parent=CV)
		s.frz_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.075),parent=CV,scale=fw)
		s.sta_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.1),parent=CV,scale=fw)
		s.gnd_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.125),parent=CV,scale=fw)
		s.frl_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.15),parent=CV,scale=fw)
		s.atk_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.175),parent=CV,scale=fw)
		s.bly_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.2),parent=CV,scale=fw)
		s.flp_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.225),parent=CV,scale=fw)
		s.jmp_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.25),parent=CV,scale=fw)
		s.lnd_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.275),parent=CV,scale=fw)
		s.fal_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.3),parent=CV,scale=fw)
		s.run_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.325),parent=CV,scale=fw)
		s.idl_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.35),parent=CV,scale=fw)
		s.bns_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.375),parent=CV,scale=fw)
		s.slp_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.4),parent=CV,scale=fw)
		s.inw_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.425),parent=CV,scale=fw)
		s.ind_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.45),parent=CV,scale=fw)
		s.inj_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.475),parent=CV,scale=fw)
		s.aku_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.5),parent=CV,scale=fw)
		s.mem_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.55),parent=CV,scale=fw)
		s.ent_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.575),parent=CV,scale=fw)
		s.fps_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.6),parent=CV,scale=fw)
		s.dscr_text=Text('player pos:',color=color.azure,font=ui._fnt,position=(sx+.05,hg-.64),parent=CV,scale=1.3)
		s.ppo_state=Text(color=tct,font=ui._fnt,position=(sx,hg-.665),parent=CV,scale=fw)
		s.process=psutil.Process(os.getpid())
		s.cpu_usage=s.process.cpu_percent()
		s.tme=3
	def count_entities(self):
		c=0
		q={g for g in scene.entities if (g.enabled)}
		for k in q:
			c+=1
		return c
	def update(self):
		s=self
		s.tme=max(s.tme-time.dt,0)
		if s.tme <= 0:
			s.tme=.5
			rv=LC.ACTOR
			mem_usage=s.process.memory_info().rss/(1024*1024)
			s.ent_state.text=f'INSTANCES   : {s.count_entities()}/{len(scene.entities)}'
			s.fps_state.text=f'GRAPH FPS   : {int(1//time.dt_unscaled)}'
			s.mem_state.text=f'MEMORY USAGE: {mem_usage:.0f} MB'
			s.ppo_state.text=f'x{rv.x:.1f}  y{rv.y:.1f}  z{rv.z:.1f}'
			s.aku_state.text=f'AKU-AKU HIT : {st.aku_hit}'
			s.ind_state.text=f'INDOOR ZONE : {(rv.indoor > 0)}'
			s.inw_state.text=f'WATER ZONE  : {(rv.inwt > 0)}'
			s.slp_state.text=f'IS SLIPPERY : {rv.is_slippery}'
			s.bns_state.text=f'BONUS ROUND : {st.bonus_round}'
			s.idl_state.text=f'IDLE STATUS : {st.p_idle(LC.ACTOR)}'
			s.run_state.text=f'WALK STATUS : {rv.walking}'
			s.fal_state.text=f'FALL STATUS : {rv.falling}'
			s.lnd_state.text=f'LAND STATUS : {rv.is_landing}'
			s.jmp_state.text=f'JUMP STATUS : {rv.jumping}'
			s.flp_state.text=f'FLIP STATUS : {rv.is_flip}'
			s.bly_state.text=f'BELLY SMASH : {rv.b_smash}'
			s.atk_state.text=f'IS ATTACK   : {rv.is_attack}'
			s.frl_state.text=f'FIRST LAND  : {rv.frst_lnd}'
			s.gnd_state.text=f'IS LANDED   : {rv.landed}'
			s.sta_state.text=f'STAND UP    : {rv.standup}'
			s.inj_state.text=f'INJURED     : {rv.injured}'
			s.frz_state.text=f'FREEZED     : {rv.freezed}'

#check multible objects where in memory
def chck_mem():
	TRG='Entity'
	ATR='name'
	all_objects=gc.get_objects(generation=2)
	class_counts=Counter()
	details=[]
	os.system('cls')
	for obj in all_objects:
		if isinstance(obj,(Entity)):
			class_name=type(obj).__name__
			class_counts[class_name]+=1
			if class_name == TRG and obj.parent == scene:
				fs=getattr(obj,ATR)
				details.append(fs)
	print("MEMORY INFO:")
	print(' ')
	for class_name, count in class_counts.items():
		print(f"{class_name}: {count} Instances")
	print("\n",TRG,'-results in MEMORY:')
	for i, filename in enumerate(details,1):
		print(f"{TRG} {i}: {ATR} = {filename if filename else 'NONE'}")

class MemoryTracker(Entity):
	def __init__(self,interval=5,threshold=100000,**kwargs):
		super().__init__(**kwargs)
		self.interval = interval
		self.threshold = threshold
		self.previous_snapshot = {}
		invoke(self.track_memory_growth,delay=self.interval)
	def get_memory_snapshot(self):
		snapshot = defaultdict(int)
		for obj in gc.get_objects():
			try:
				class_name = type(obj).__name__
				snapshot[class_name] += sys.getsizeof(obj)
			except Exception:
				pass
		return snapshot
	def track_memory_growth(self):
		current_snapshot = self.get_memory_snapshot()
		growth = {}
		for class_name, current_size in current_snapshot.items():
			previous_size = self.previous_snapshot.get(class_name, 0)
			size_increase = current_size - previous_size
			if size_increase > self.threshold:
				growth[class_name] = size_increase
		self.previous_snapshot = current_snapshot
		if growth:
			print("\nKlassen mit signifikantem Speicherwachstum:")
			for class_name, increase in growth.items():
				print(f"{class_name}: +{increase / 1024:.2f} KB")
		invoke(self.track_memory_growth, delay=self.interval)