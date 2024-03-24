import ui,crate,item,status,animation,level,sound,npc
from math import atan2,sqrt
from ursina import *

map_coordinate=None
map_zone=None
map_size=None

playerInstance=[]
level_ready=False##shadow map --> player pos
C=crate

## player
def set_val(d):
	for _a in ['run_anim','jump_anim','idle_anim','spin_anim','land_anim','fall_anim','flip_anim','attack_time','walk_snd','count_time','fall_time','blink_time','death_anim']:
		setattr(d,_a,0)
	for _v in ['block_input','walking','jumping','landed','is_touch_crate','first_land','is_landing','is_attack','is_flip','warped','freezed','injured']:
		setattr(d,_v,False)
	d.lpos=None
	d.move_speed=1.8
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
				#return
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
	if status.bonus_round:
		status.wumpa_bonus=0
		status.crate_bonus=0
		status.lives_bonus=0
		status.bonus_round=False
	else:
		status.extra_lives-=1
	status.aku_hit=0
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
	status.crate_to_sv=0
def c_subtract(cY):
	if cY < -10:
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
	collect_reset()
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
def wumpa_LOD():
	if not status.LV_CLEAR_PROCESS:
		for WUM in item.item_list[:]:
			if isinstance(WUM,item.WumpaFruit):
				if is_nearby_pc(n=WUM,DX=8,DY=8):
					WUM.world_visible=True
				else:
					WUM.world_visible=False

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
			c.landing()
			c.y=terraincast(c.world_position,map_zone,map_coordinate)
			return
	hit_info=boxcast(c.world_position,Vec3(0,1,0),distance=.01,thickness=(.15,.15),ignore=[c],debug=False)
	if hit_info.normal:
		hte=hit_info.entity
		hw=str(hte)
		if not hte in item.item_list:
			if is_crate(hte):
				if hw == 'iron' or hw in ['switch_empty','switch_nitro','tnt'] and hte.activ:
					c.landing()
					c.y=hit_info.world_point.y
				else:
					crate_action(c=c,e=hte)
				return
			if hw in ['water_hit','falling_zone']:
				death_zone(c=c,e=hte)
				return
			if hw in npc.npc_list:
				jump_enemy(c=c,e=hte)
				return
			if hw == 'level_finish':
				jump_levelfin(c=c,e=hte)
				return
			if hw == 'bonus_platform' and not status.bonus_solved or hw == 'gem_platform':
				freeze_by_platform(c=c,e=hte)
			else:
				if hw == 'moss_platform' and hte.movable:
					platform_sync(c=c,e=hte)
				c.landing()
				c.y=hit_info.world_point.y
	else:
		c.landed=False
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
		if c.is_attack:
			J=time.dt*3
		else:
			J=time.dt*2
		vecL={Vec3(1,0,0):lambda:setattr(c,'x',c.x+J),
			Vec3(-1,0,0):lambda:setattr(c,'x',c.x-J),
			Vec3(0,0,1):lambda:setattr(c,'z',c.z+J),
			Vec3(0,0,-1):lambda:setattr(c,'z',c.z-J),
			Vec3(0,-1,0):lambda:ceiling(c=c,e=wE)}
		if wH in vecL and not wH == Vec3(0,1,0):
			if not wE in item.item_list:
				vecL[wH]()
def platform_sync(c,e):
	if e.movable:
		c.x=e.x
		c.z=e.z
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
			print('platform works')
			return
		if str(m) == 'bonus_platform':
			enter_bonus(c=m.target)
		else:
			print('go to death route')
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
def freeze_by_platform(c,e):
	if not c.freezed:
		c.freezed=True
		e.catch_player=True

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
def is_crate(e):
	cck=[C.Iron,C.Normal,C.QuestionMark,C.Bounce,C.ExtraLife,
		C.AkuAku,C.Checkpoint,C.SpringWood,C.SpringIron,
		C.SwitchEmpty,C.SwitchNitro,C.TNT,C.Nitro,C.Air]
	if any(isinstance(e,crate_class) for crate_class in cck):
		return True
def crate_action(c,e):
	if e.vnum in [7,8]:
		set_jump_type(d=c,t=2)
		animation.spring_animation(e)
		Audio(sound.snd_sprin)
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
					co.fall_exec=True
					co.animate_y(co.y-co.scale_y*2,duration=.15)
					co.fall_exec=False

## bonus level
def enter_bonus(c):
	status.loading=True
	status.checkpoint=status.bonus_checkpoint[status.level_index]
	collect_reset()
	if status.bonus_round:
		invoke(lambda:back_to_level(c),delay=.5)
	else:
		invoke(lambda:load_bonus(c),delay=.5)
def back_to_level(c):
	status.bonus_round=False
	dMN={0:'bonus',1:'woods',2:'evening'}
	status.day_mode=dMN[status.level_index]
	c.position=status.checkpoint
	status.bonus_solved=True
	status.loading=False
	c.freezed=False
def load_bonus(c):
	status.bonus_round=True
	status.day_mode='bonus'
	sound.BonusMusic(T=status.level_index)
	ui.BonusText()
	c.position=status.bonus_zone_position[status.level_index]
	status.loading=False
	c.freezed=False
def bonus_reward(p):
	if status.wumpa_bonus > 0:
		p.count_time+=time.dt
		if p.count_time >= 0.075:
			p.count_time=0
			if status.wumpa_bonus > 0:
				bonus_give_wumpa()
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

## npc
def set_val_npc(m):
	if str(m) in ['rat','eating_plant','vulture']:
		m.can_move=False
	else:
		m.can_move=True
	m.spawn_point=m.position
	m.is_hitten=False
	m.is_purge=False
	m.unlit=False
	m.anim_frame=0
def npc_action(m):
	if m.is_purge:
		npc_purge(m)
	if not m.is_hitten:
		if str(m) == 'hedgehog' and m.defend_mode:
			animation.hedge_defend(m)
		else:
			animation.npc_walking(m)
		npc_walk(m)
	else:
		#m.collider=None
		fly_away(m)
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

## avoid laggs by first loading
def preload_objects():
	item.WumpaFruit(pos=(255,-255,255))
	for CCA in range(14):
		crate.place_crate(ID=CCA,p=(255,-255,255),m=1,l=1)
	for DCA in scene.entities[:]:
		if is_crate(DCA) and DCA.y == -255:
			DCA.parent=None
			DCA.disable()