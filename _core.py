import ui,crate,item,status,level,sound,npc,settings
from math import atan2,sqrt
from ursina import *

map_coordinate=None
LOD_refresh=1
map_zone=None
map_size=None

playerInstance=[]
level_ready=False
C=crate

## player
def set_val(d):
	for _a in ['run_anim','jump_anim','idle_anim','spin_anim','land_anim','fall_anim','flip_anim','attack_time','walk_snd','count_time','fall_time','blink_time','death_anim']:
		setattr(d,_a,0)
	for _v in ['block_input','walking','jumping','landed','is_touch_crate','first_land','is_landing','is_attack','is_flip','warped','freezed','injured']:
		setattr(d,_v,False)
	d.lpos=None
	d.move_speed=2
	playerInstance.append(d)
def set_jump_type(d,t):
	d.jumping=True
	tp={0:1,1:1.2,2:1.5}
	d.lpos=d.y+tp[t]
def p_attack(d):
	for atk in scene.entities[:]:
		cid=str(atk)
		if is_nearby_pc(n=atk,DX=.5,DY=.5):
			if is_crate(atk) and not atk.vnum == 13 and status.d_delay <= 0:
				if atk.vnum in [3,11]:
					atk.empty_destroy()
				else:
					atk.destroy()
			if cid in npc.npc_list and not atk.is_hitten:
				atk.is_hitten=True
				Audio(sound.snd_nbeat)
def get_damage(c):
	if not c.injured and not status.is_dying:
		if status.aku_hit > 0:
			status.aku_hit-=1
			c.injured=True
			status.player_protect=2
			Audio(sound.snd_damg,pitch=.8)
		else:
			c.collider=None
			Audio(sound.snd_woah,pitch=.8)
			status.is_dying=True
def p_death_event(d):
	ui.BlackScreen()
	status.crate_count-=status.crate_to_sv
	status.fails+=1
	if status.is_death_route:
		status.is_death_route=False
	if status.bonus_round:
		status.wumpa_bonus=0
		status.crate_bonus=0
		status.lives_bonus=0
		status.bonus_round=False
	else:
		status.extra_lives-=1
	if status.fails < 3:
		status.aku_hit=0
	else:
		status.aku_hit=1
		if not status.aku_exist:
			npc.AkuAkuMask(pos=(d.x,d.y,d.z))
	reset_crates()
	reset_wumpas()
	reset_npc()
	d.position=status.checkpoint
	d.collider=d.DEFAUL_COLLIDER
	d.is_reset_phase=False
def various_val(c):
	if status.bonus_solved:
		if status.wumpa_bonus > 0 or status.crate_bonus > 0 or status.lives_bonus > 0:
			bonus_reward(c)
	if c.walk_snd > 0:
		c.walk_snd-=time.dt
	if c.blink_time > 0:
		c.blink_time-=time.dt
	if c.injured:
		c.hurt_blink()
	if status.c_delay > 0:
		status.c_delay-=time.dt
	if status.d_delay > 0:
		status.d_delay-=time.dt
	if status.player_protect > 0:
		status.player_protect-=time.dt
		if status.player_protect <= 0:
			c.alpha=1
			c.injured=False

## world, misc
def collect_reset():
	status.C_RESET.clear()
	status.W_RESET.clear()
	status.crate_to_sv=0
	status.fails=0
	check_cstack()
def c_subtract(cY):
	if cY < -20:
		status.crates_in_bonus-=1
	status.crates_in_level-=1
def reset_crates():
	for ca in scene.entities[:]:
		if is_crate(ca):
			if ca.poly == 1:
				scene.entities.remove(ca)
				ca.disable()
			if ca.vnum == 3:
				ca.ltime=0
				ca._empty=5
	for cv in status.C_RESET[:]:
		if cv.vnum in [9,10]:
			cv.c_reset()
		elif cv.vnum == 13:
			if not cv.c_ID == 0:
				c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum,m=cv.mark,l=cv.c_ID,pse=cv.poly)
		else:
			c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum)
	status.C_RESET.clear()
	status.crate_to_sv=0
def reset_wumpas():
	for wu in status.W_RESET[:]:
		wu.destroy()
	status.W_RESET.clear()
def reset_npc():
	for NP in status.NPC_RESET[:]:
		npc.spawn(mID=NP.vnum,pos=NP.spawn_pos,mDirec=NP.m_direction,mTurn=0)
	status.NPC_RESET.clear()
def clear_level(passed):
	status.LV_CLEAR_PROCESS=True
	scene.clear()
	if passed:
		collect_rewards()
	ui.WhiteScreen()
def collect_rewards():
	if status.level_crystal:
		status.CRYSTAL.append(status.level_index)
		status.collected_crystals+=1
	if status.level_col_gem:
		status.COLOR_GEM.append(status.level_index)
		status.color_gems+=1
	if status.level_col_gem:
		status.CLEAR_GEM.append(status.level_index)
		status.clear_gems+=1
def objectLOD():
	if not status.LV_CLEAR_PROCESS:
		for WUM in item.item_list[:]:
			if isinstance(WUM,item.WumpaFruit):
				if is_nearby_pc(n=WUM,DX=8,DY=8):
					WUM.world_visible=True
				else:
					WUM.world_visible=False
		for vO in scene.entities[:]:
			nL=str(vO)
			jDA=status.LOD_distance(m=vO,c=playerInstance[0])
			if nL in status.OBJ_LIST and not nL in ['water_hit','falling_zone']:
				if jDA:
					vO.hide()
					vO.parent=None
				else:
					vO.show()
					vO.parent=scene
			if nL in npc.npc_list:
				if jDA:
					vO.world_visible=False
				else:
					vO.world_visible=True
			if is_crate(vO) and not vO.vnum in [9,10]:
				if jDA:
					vO.texture=None
					vO.hide()
				else:
					vO.texture=vO.org_tex
					vO.show()

## collisions
def ceiling(c,e):
	if is_crate(e) and not c.is_touch_crate:
		c.is_touch_crate=True
		e.destroy()
		invoke(lambda:setattr(c,'is_touch_crate',False),delay=.1)
	c.jumping=False
	c.y=c.y
def check_ground(c):
	if len(map_coordinate) > 0:
		if c.intersects(map_zone):
			landing(c=c,e=terraincast(c.world_position,map_zone,map_coordinate))
			return
	hit_info=boxcast(c.world_position,Vec3(0,1,0),distance=.01,thickness=(.15,.15),ignore=[c],debug=False)
	if hit_info.normal:
		hte=hit_info.entity
		hw=str(hte)
		if not hte in item.item_list:
			if is_crate(hte):
				if hw == 'iron' or hw in ['switch_empty','switch_nitro','tnt'] and hte.activ:
					landing(c=c,e=hit_info.world_point.y)
				else:
					crate_action(c=c,e=hte)
				return
			if hw in npc.npc_list:
				jump_enemy(c=c,e=hte)
				return
			if hw in status.OBJ_LIST:
				object_interact(c=c,e=hte)
				return
			if hw == 'plank':
				if hte.typ == 1:
					hte.pl_touch()
			landing(c=c,e=hit_info.world_point.y)
	else:
		c.landed=False
def landing(c,e):
	c.landed=True
	if not c.y == e and not c.jumping:
		c.y=e
		if c.first_land:
			c.first_land=False
			c.is_landing=True
			Audio(sound.snd_land)
			invoke(lambda:setattr(c,'is_landing',False),delay=.6)
			invoke(lambda:setattr(c,'land_anim',0),delay=.6)
		c.block_input=False
		c.is_flip=False
		c.flip_anim=0
def check_wall(c):
	wH=c.intersects().normal
	if wH:
		wE=c.intersects().entity
		if wE == map_zone:
			return
		if str(wE) in npc.npc_list and not c.is_attack:
			if not c.jumping:
				get_damage(c)
			return
		if wE in item.item_list:
			if status.c_delay <= 0:
				status.c_delay=.1/6
				wE.collect()
			return
		J=time.dt*c.move_speed*1.1
		vecL={Vec3(1,0,0):lambda:setattr(c,'x',c.x+J),
			Vec3(-1,0,0):lambda:setattr(c,'x',c.x-J),
			Vec3(0,0,1):lambda:setattr(c,'z',c.z+J),
			Vec3(0,0,-1):lambda:setattr(c,'z',c.z-J),
			Vec3(0,-1,0):lambda:ceiling(c=c,e=wE)}
		if wH in vecL and not wH == Vec3(0,1,0):
			if not wE in item.item_list:
				vecL[wH]()
def platform_floating(m,c):
	m.air_time+=time.dt
	m.y+=time.dt
	m.target.x=m.x
	m.target.z=m.z
	m.target.y=m.y+m.scale_y
	if m.air_time >= 3:
		m.air_time=0
		m.catch_player=False
		m.position=m.orginal_pos
		if status.level_index == 6:
			c.freezed=False
			return
		if str(m) == 'bonus_platform':
			load_bonus(c=m.target)
		else:
			load_gem_route(c=m.target)
def jump_enemy(c,e):
	e0=str(e)
	if e0 in ['saw_turtle','lizard'] or e0 == 'hedgehog' and e.defend_mode:
		get_damage(c)
		return
	kill_by_jump(m=e,c=c)
def jump_levelfin(c,e):
	if not status.LEVEL_CLEAN:
		status.LEVEL_CLEAN=True
		clear_level(passed=True)
def death_zone(c,e):
	if not status.is_dying:
		status.is_dying=True
		Audio(sound.snd_woah,pitch=.8)
		c.collider=None
def object_interact(c,e):
	iO=str(e)
	if iO in ['water_hit','falling_zone']:
		death_zone(c=c,e=e)
		return
	if iO == 'bonus_platform' and not status.bonus_solved or iO == 'gem_platform':
		if not c.freezed:
			c.freezed=True
			e.catch_player=True
		return
	if iO == 'level_finish':
		jump_levelfin(c=c,e=e)

## interface,collectables
def wumpa_count(n):
	if status.bonus_round:
		status.wumpa_bonus+=n
	else:
		status.wumpa_fruits+=n
		status.show_wumpas=5
	sound.snd_collect()
def give_extra_live():
	Audio(sound.snd_lifes,volume=.5)
	if status.bonus_round:
		status.lives_bonus+=1
	else:
		status.extra_lives+=1
		status.show_lives=5

## crate actions
def crate_set_val(cR,Cpos,Cpse):
	cR.destroy_exp=False
	cR.is_stack=False
	cR.spawn_pos=Cpos
	cR.position=Cpos
	cR.collider='box'
	cR.poly=Cpse
	cR.scale=.16
	cR.org_tex=cR.texture
def is_crate(e):
	cck=[C.Iron,C.Normal,C.QuestionMark,C.Bounce,C.ExtraLife,
		C.AkuAku,C.Checkpoint,C.SpringWood,C.SpringIron,
		C.SwitchEmpty,C.SwitchNitro,C.TNT,C.Nitro,C.Air]
	if any(isinstance(e,crate_class) for crate_class in cck):
		return True
def crate_action(c,e):
	if e.vnum in [7,8]:
		set_jump_type(d=c,t=2)
		e.anim_act()
	else:
		set_jump_type(d=c,t=0)
		e.destroy()
def check_cstack():
	for cSD in scene.entities[:]:
		if is_crate(cSD) and not cSD.vnum ==3:
			for cST in scene.entities[:]:
				if is_crate(cST) and not cST.vnum == 3:
					if cST.x == cSD.x and cST.z == cSD.z:
						dsta=round(abs(cST.y-(cSD.y-cSD.scale_y*2)),2)
						if dsta == 0:
							cST.is_stack=True
							cSD.is_stack=True
def check_crates_over(c):
	for co in scene.entities:
		if is_crate(co) and not c.vnum == 3:
			if c.x == co.x and c.z == co.z and co.y > c.y:
				if co.is_stack:
					co.animate_y(co.y-co.scale_y*2,duration=.15)

## bonus level
def load_bonus(c):
	status.loading=True
	status.checkpoint=status.bonus_checkpoint[status.level_index]
	collect_reset()
	if status.bonus_round:
		invoke(lambda:back_to_level(c),delay=.5)
	else:
		invoke(lambda:enter_bonus(c),delay=.5)
def back_to_level(c):
	if status.is_death_route:
		status.is_death_route=False
	if status.bonus_round:
		status.bonus_round=False
		status.bonus_solved=True
	dMN={0:'bonus',1:'woods',2:'evening'}
	status.day_mode=dMN[status.level_index]
	c.position=status.checkpoint
	status.loading=False
	c.freezed=False
def enter_bonus(c):
	status.bonus_round=True
	status.day_mode='bonus'
	sound.BonusMusic(T=status.level_index)
	ui.BonusText()
	c.position=(0,-35,-3)
	status.loading=False
	c.freezed=False
def bonus_reward(p):
	if status.wumpa_bonus > 0:
		p.count_time+=time.dt
		if p.count_time >= 0.075:
			p.count_time=0
			if status.wumpa_bonus > 0:
				bonus_give_wumpa()
				ui.wumpa_count_anim()
			if status.crate_bonus > 0:
				bonus_give_crate()
			if status.lives_bonus > 0:
				bonus_give_live()
def bonus_give_wumpa():
	status.wumpa_bonus-=1
	wumpa_count(1)
def bonus_give_crate():
	status.crate_bonus-=1
	status.crate_count+=1
	status.show_crates=1
def bonus_give_live():
	Audio(sound.snd_lifes)
	status.lives_bonus-=1
	status.extra_lives+=1
	status.show_lives=1

## gem route
def load_gem_route(c):
	status.loading=True
	if status.is_death_route:
		invoke(lambda:back_to_level(c),delay=.5)
	else:
		invoke(lambda:load_droute(c),delay=.5)
def load_droute(c):
	if not status.is_death_route:
		status.is_death_route=True
		c.position=(200,1,-3)
		status.loading=False
		c.freezed=False
		sound.SpecialMusic(T=status.level_index)
	else:
		c.back_to_level(c)

## npc
def set_val_npc(m):
	if str(m) in ['rat','eating_plant','vulture']:
		m.can_move=False
	else:
		m.can_move=True
	m.spawn_point=m.position
	m.world_visible=False
	m.is_hitten=False
	m.is_purge=False
	m.unlit=False
	m.anim_frame=0
def npc_action(m):
	if m.world_visible:
		m.show()
		if m.is_purge:
			npc_purge(m)
			return
		if not m.is_hitten:
			npc.walk_frames(m)
			npc_walk(m)
		else:
			fly_away(m)
		return
	m.hide()
def npc_purge(m):
	u=60
	m.can_move=False
	m.collider=None
	if m.scale_x > 0:
		m.scale_x-=time.dt/u
	if m.scale_y > 0:
		m.scale_y-=time.dt/u
	if m.scale_z > 0:
		m.scale_z-=time.dt/u
	if m.scale_x <= 0 and m.scale_y <= 0 and m.scale_z <= 0:
		status.NPC_RESET.append(m)
		m.disable()
def npc_walk(m):
	if status.pause:
		return
	if m.can_move:
		s=m.move_speed
		m_D=m.m_direction
		if m.m_direction == 0:
			if m.turn == 0:
				m.x+=time.dt*s
				if m.x >= m.spawn_point[0]+1:
					m.rotation_y=90
					m.turn=1
			elif m.turn == 1:
				m.x-=time.dt*s
				if m.x <= m.spawn_point[0]-1:
					m.rotation_y=270
					m.turn=0
		if m.m_direction == 1:
			if m.turn == 0:
				m.z+=time.dt*s
				if m.z >= m.spawn_point[2]+1:
					m.turn=1
					m.rotation_y=0
			elif m.turn == 1:
				m.z-=time.dt*s
				if m.z <= m.spawn_point[2]-1:
					m.rotation_y=180
					m.turn=0
def rotate_to_crash(m):
	target=playerInstance[0]
	relative_position=target.position-m.position
	angle=atan2(relative_position.x,relative_position.z)*(180/pi)+180
	m.rotation_y=angle
	m.rotation_x=-90
def fly_away(n):
	n.z+=time.dt*20
	J=n.intersects()
	if J:
		PNL=J.entity
		if is_crate(PNL):
			if PNL.vnum in [3,12]:
				PNL.empty_destroy()
			else:
				PNL.destroy()
	if n.z >= n.spawn_point[2]+10:
		npc_purge(n)
def kill_by_jump(m,c):
	m.is_purge=True
	set_jump_type(d=c,t=0)
	Audio(sound.snd_jmph)
def is_nearby_pc(n,DX,DY):
	dist_y=abs(playerInstance[0].y-n.y)
	dist_x=distance_xz(playerInstance[0],n)
	if dist_y < DY and dist_x < DX:
		return True
	return False

## reduce lagg by first spawn
def preload_items():
	status.preload_phase=True
	settings.SFX_VOLUME=0
	for PRC in range(13):
		C.place_crate(ID=PRC,p=(0+PRC,-256,0),m=99,l=13)
		item.WumpaFruit(pos=(0+PRC,-256,0))
	for DPR in scene.entities:
		if is_crate(DPR) and DPR.collider != None and DPR.y <= -256:
			if DPR.vnum == 3:
				DPR.empty_destroy()
			else:
				DPR.destroy()
	status.C_RESET.clear()
	invoke(end_preload,delay=.3)
def end_preload():
	settings.SFX_VOLUME=1
	status.preload_phase=False