import ui,crate,item,status,sound,npc,settings,_loc,math,warproom
from math import atan2,sqrt
from ursina import *

level_ready=False
sn=sound
st=status
LC=_loc
C=crate
N=npc

## player
def set_val(c):
	for _a in ['rnfr','jmfr','idfr','spfr','ldfr','fafr','flfr','ssfr','srfr','walk_snd','fall_time','slide_fwd','in_water']:
		setattr(c,_a,0)#animation frames
	for _v in ['aq_bonus','walking','jumping','landed','tcr','frst_lnd','is_landing','is_attack','is_flip','warped','freezed','injured','is_slippery','wall_stop']:
		setattr(c,_v,False)#flags
	c.move_speed=2.4
	c.gravity=2.5
	c.direc=(0,0,0)
	c.vpos=c.y
	c.indoor=.5
	c.CMS=3
	_loc.ACTOR=c
def get_damage(c,rsn):
	if st.aku_hit > 2:
		return
	if not (c.injured or st.death_event):
		if st.aku_hit > 0:
			st.aku_hit-=1
			c.injured=True
			c.hurt_visual()
			sn.pc_audio(ID=6,pit=.8)
			invoke(lambda:setattr(c,'injured',False),delay=2)
			invoke(lambda:setattr(c,'alpha',1),delay=2)
			del rsn
			return
		dth_event(c,rsn=rsn)
def hurt_blink(c):
	c.visible=False
	invoke(lambda:setattr(c,'visible',True),delay=.2)
def dth_event(c,rsn):
	if not st.death_event:
		if rsn == 0:
			sn.pc_audio(ID=14,pit=.8)
		else:
			sn.pc_audio(ID=7,pit=.8)
		st.death_event=True
		c.freezed=True
		c.death_action(rsn=rsn)
def reset_state(c):
	ui.BlackScreen()
	st.crate_count-=st.crate_to_sv
	if st.is_death_route:
		st.is_death_route=False
	if st.bonus_round:
		st.wumpa_bonus=0
		st.crate_bonus=0
		st.lives_bonus=0
		st.bonus_round=False
	else:
		st.extra_lives-=1
		st.fails+=1
		if st.level_index == 2:
			st.gem_death=True
	if st.extra_lives <= 0:
		game_over()
		return
	if st.fails < 3:
		st.aku_hit=0
	else:
		st.aku_hit=1
		if not st.aku_exist:
			sn.crate_audio(ID=14,pit=1.2)
			npc.AkuAkuMask(pos=(c.x,c.y,c.z))
	reset_crates()
	rmv_wumpas()
	reset_wumpas()
	reset_npc()
	check_cstack()
	c.position=status.checkpoint
	camera.position=c.position
	camera.rotation=(15,0,0)
	st.death_event=False
	c.visible=True
	invoke(lambda:setattr(c,'freezed',False),delay=3)
def game_over():
	clear_level(passed=False)
	invoke(lambda:ui.GameOverScreen(),delay=1)
def various_val(c):
	c.indoor=max(c.indoor-time.dt,0)
	c.in_water=max(c.in_water-time.dt,0)
	if not c.is_slippery:
		c.move_speed=2.4
	if st.bonus_solved and not st.wait_screen:
		c.aq_bonus=(st.wumpa_bonus > 0 or st.crate_bonus > 0 or st.lives_bonus > 0)
def c_attack(c):
	for e in scene.entities[:]:
		if distance(c,e) < .5:
			if (is_crate(e) and e.collider != None):
				if e.vnum in [3,11]:
					e.empty_destroy()
				else:
					if not e.falling and not e.vnum == 13:
						e.destroy()
			if is_enemie(e) and not (e.is_hitten or e.is_purge):
				if (e.vnum == 1) or (e.vnum == 5 and e.def_mode):
					get_damage(c,rsn=1)
				bash_enemie(e,h=c)
def c_slide(c):
	if not c.walking:
		if c.slide_fwd > 0 and status.p_last_direc != None:
			if c.move_speed > 0:
				c.move_speed-=time.dt
			c.position+=status.p_last_direc*time.dt*c.slide_fwd
			c.slide_fwd-=time.dt
			if c.slide_fwd <= 0:
				c.slide_fwd=0
				st.p_last_direc=None
		return
	if c.move_speed < 4:
		c.move_speed+=time.dt
		if c.move_speed > 0:
			c.slide_fwd=c.move_speed
def c_invincible(c):
	for inv in scene.entities[:]:
		if distance(c,inv) < 1 and inv.collider != None:
			if is_crate(inv):
				if inv.vnum == 11:
					inv.empty_destroy()
				else:
					inv.destroy()
			if is_enemie(inv):
				bash_enemie(e=inv,h=c)
			if isinstance(inv,item.WumpaFruit):
				inv.collect()

## camera actor
def cam_rotate(c):
	ftt=time.dt*1.5
	if c.jumping:
		camera.rotation_x-=ftt
		return
	if camera.rotation_x < 15:
		camera.rotation_x+=ftt
def cam_follow(c):
	ftr=time.dt*3
	camera.z=lerp(camera.z,c.z-c.CMS,ftr)
	camera.x=lerp(camera.x,c.x,ftr)
	if c.indoor > 0:
		if c.landed:
			camera.y=lerp(camera.y,c.y+1,time.dt)
		camera.rotation_x=12
		return
	if (st.bonus_round or st.is_death_route) and not c.freezed:
		camera.y=lerp(camera.y,c.y+1,time.dt)

## world, misc
def spawn_level_crystal(idx):
	cry_pos={1:(0,1.5,-13),2:(35.5,6.4,28.5),3:(0,2.5,60.5),4:(14,4.25,66),5:(12,.8,-7),6:(0,.3,-19)}
	if not idx in st.CRYSTAL:
		item.EnergyCrystal(pos=cry_pos[idx])
def collect_reset():
	st.C_RESET.clear()
	st.W_RESET.clear()
	st.crate_to_sv=0
	st.fails=0
	if level_ready:
		st.NPC_RESET.clear()
def c_subtract(cY):
	if cY < -20:
		st.crates_in_bonus-=1
	st.crates_in_level-=1
def reset_crates():
	for ca in scene.entities[:]:
		if is_crate(ca):
			if ca.poly == 1:
				purge_instance(ca)
	for cv in st.C_RESET[:]:
		if cv.vnum in [9,10]:
			cv.c_reset()
		elif cv.vnum == 13:
			if not cv.c_ID == 0:
				c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum,m=cv.mark,l=cv.c_ID,pse=cv.poly)
		else:
			if cv.vnum == 11:
				cv.activ=False
				cv.countdown=0
			c_subtract(cY=cv.y)
			C.place_crate(p=cv.spawn_pos,ID=cv.vnum)
	st.C_RESET.clear()
	st.crate_to_sv=0
def reset_wumpas():
	for wres in status.W_RESET[:]:
		item.WumpaFruit(p=wres,c_prg=False)
	st.W_RESET.clear()
def rmv_wumpas():
	for wu in scene.entities[:]:
		if isinstance(wu,item.WumpaFruit) and wu.c_purge:
			wu.destroy()
def reset_npc():
	for NP in st.NPC_RESET[:]:
		if NP.vnum in [10,11]:
			npc.spawn(mID=NP.vnum,pos=NP.spawn_pos,mDirec=NP.m_direction,ro_mode=NP.ro_mode)
		else:
			npc.spawn(mID=NP.vnum,pos=NP.spawn_pos,mDirec=NP.m_direction)
	st.NPC_RESET.clear()
def jmp_lv_fin():
	if not st.LEVEL_CLEAN:
		purge_instance(LC.ACTOR)
		st.LEVEL_CLEAN=True
		clear_level(passed=True)
def clear_level(passed):
	st.LV_CLEAR_PROCESS=True
	scene.clear()
	if passed:
		collect_rewards()
		ui.WhiteScreen()
		return
	st.loading=True
	delete_states()
	invoke(lambda:warproom.level_select(),delay=3)
def delete_states():
	st.level_index=0
	st.crates_in_bonus=0
	st.crates_in_level=0
	st.crate_bonus=0
	st.crate_count=0
	st.crate_to_sv=0
	st.fails=0
	st.NPC_RESET.clear()
	st.W_RESET.clear()
	st.C_RESET.clear()
	st.level_crystal=False
	st.level_col_gem=False
	st.level_cle_gem=False
	st.gem_path_solved=False
	st.is_death_route=False
	st.level_solved=False
	st.bonus_solved=False
	st.bonus_round=False
	st.LEVEL_CLEAN=False
	st.pause=False
	st.day_mode=''
	level_ready=False
def collect_rewards():
	cdx=st.level_index
	if st.level_crystal:
		st.CRYSTAL.append(cdx)
		st.collected_crystals+=1
	if st.level_cle_gem:
		st.CLEAR_GEM.append(cdx)
		st.clear_gems+=1
	if st.level_col_gem:
		wcg={1:4,#lv1#blue
			2:1,#lv2#red
			3:5,#lv3#yellow
			4:2,#lv4#green
			5:3}#lv5#purple
		st.COLOR_GEM.append(wcg[cdx])
		st.color_gems+=1
	delete_states()
	invoke(lambda:warproom.level_select(),delay=2)
def reset_audio():
	st.e_audio=False
	st.n_audio=False
	st.b_audio=False
def purge_instance(v):
	v.parent=None
	scene.entities.remove(v)
	v.disable()
	del v
def game_pause():
	if not st.pause:
		st.pause=True
		return
	st.pause=False

## collisions
def check_ceiling(c):
	vc=c.intersects(ignore=[c,LC.shdw])
	if vc and vc.normal == Vec3(0,-1,0):
		e=vc.entity
		if not (str(e) in LC.item_lst+LC.trigger_lst):
			if is_crate(e) and not c.tcr:
				c.tcr=True
				e.destroy()
				invoke(lambda:setattr(c,'tcr',False),delay=.1)
			c.y=c.y
			c.jumping=False
def check_wall(c):
	if st.aku_hit > 2:
		c_invincible(c)
	hT=c.intersects(ignore=[c,LC.shdw])
	jV=hT.entity
	xa=str(jV)
	if hT and hT.normal != Vec3(0,1,0):
		if xa in LC.trigger_lst:
			jV.do_act()
			return
		if xa in LC.item_lst:
			jV.collect()
			return
		if (is_enemie(jV) and not c.is_attack):
			if jV.vnum == 7:
				get_damage(c,rsn=5)
				return
			get_damage(c,rsn=1)
			return
		c.position-=c.direc*time.dt*c.move_speed
def check_floor(c):
	vj=boxcast(c.world_position,Vec3(0,1,0),distance=.01,thickness=(.13,.13),ignore=[c,LC.shdw],debug=False)
	vp=vj.entity
	if vj.normal and not (str(vp) in LC.item_lst+LC.dangers+LC.trigger_lst):
		if not c.jumping:
			landing(c,e=vj.world_point.y,o=vp)
		return
	c.landed=False
def landing(c,e,o):
	floor_interact(c,o)
	if c.y < e:
		c.y=e
	c.landed=True
	if c.frst_lnd:
		c.frst_lnd=False
		c.is_flip=False
		c.flfr=0
		c.ldfr=0
		c.jmfr=0
		c.is_landing=True
		c.fall_time=0
		c.gravity=2.5
		sn.foot_step(c,o)
def floor_interact(c,e):
	u=str(e)
	if is_crate(e) and not ((e.vnum in [0,14]) or (e.vnum in [9,10,11] and e.activ)) and c.fall_time > .1:
		if e.vnum in [7,8]:
			c.jump_typ(t=4)
			e.c_action()
			return
		if e.vnum == 3:
			c.jump_typ(t=3)
		else:
			c.jump_typ(t=2)
		e.destroy()
		return
	if is_enemie(e) and not e.is_hitten:
		if (e.vnum in [2,9]) or (e.vnum == 5 and e.def_mode):
			get_damage(c,rsn=1)
		else:
			e.is_purge=True
			c.jump_typ(t=2)
			sn.pc_audio(ID=5)
		return
	c.is_slippery=(u == 'iceg')
	if u in ['bonus_platform','gem_platform']:e.catch_p=True
	if u in ['loose_platform','swpt','HPP']:e.active=True
	if (u == 'plank' and e.typ == 1):e.pl_touch()
	if u == 'falling_zone':dth_event(c=LC.ACTOR,rsn=0)
	if u == 'water_hit':dth_event(c,rsn=2)
	if u == 'mptf':e.mv_player()

def ptf_up(p,c):
	if not c.freezed:
		c.freezed=True
		c.position=(p.x,c.y,p.z)
		c.rotation_y=0
	p.y+=time.dt/1.5
	if p.y >= p.start_y+3:
		p.catch_p=False
		p.y=p.start_y
		if str(p) == 'bonus_platform':
			load_bonus(c)
			return
		load_gem_route(c)

## interface,collectables
def wumpa_count(n):
	sn.ui_audio(ID=2)
	invoke(lambda:sn.ui_audio(ID=1),delay=.5)
	if st.bonus_round:
		st.wumpa_bonus+=n
	else:
		st.wumpa_fruits+=n
		st.show_wumpas=5
	sc_ps=LC.ACTOR.screen_position
	if not LC.ACTOR.aq_bonus:
		if n > 1:
			ui.WumpaCollectAnim(pos=(sc_ps[0],sc_ps[1]))
		ui.WumpaCollectAnim(pos=(sc_ps[0],sc_ps[1]+.1))
def give_extra_live():
	sn.ui_audio(ID=3)
	if st.bonus_round:
		st.lives_bonus+=1
		return
	if st.extra_lives < 99:
		st.extra_lives+=1
	ui.live_get_anim()
	st.show_lives=5
def show_status_ui():
	st.show_wumpas=5
	st.show_crates=5
	st.show_lives=5
	st.show_gems=5

## crate actions
def crate_set_val(cR,Cpos,Cpse):
	if cR.vnum == 15:
		cR.texture='res/crate/crate_t'+str(cR.time_stop)+'.png'
	else:
		cR.texture='res/crate/'+str(cR.vnum)+'.png'
	cR.org_tex=cR.texture
	cR.fall_down=False
	cR.is_stack=False
	cR.falling=False
	cR.spawn_pos=Cpos
	cR.position=Cpos
	cR.collider='box'
	cR.poly=Cpse
	cR.scale=.16
def is_crate(e):
	cck=[C.Iron,C.Normal,C.QuestionMark,C.Bounce,C.ExtraLife,
		C.AkuAku,C.Checkpoint,C.SpringWood,C.SpringIron,C.SwitchEmpty,
		C.SwitchNitro,C.TNT,C.Nitro,C.Air,C.Protected,C.cTime,C.LvInfo]
	if any(isinstance(e,crate_class) for crate_class in cck):
		return True
	return False
def check_cstack():
	for cSD in scene.entities[:]:
		if is_crate(cSD) and not cSD.vnum == 3:
			for cST in scene.entities[:]:
				if is_crate(cST) and not cST.vnum == 3:
					if cST.x == cSD.x and cST.z == cSD.z:
						dsta=round(abs(cST.y-(cSD.y-cSD.scale_y*2)),2)
						if dsta == 0:
							cST.is_stack=True
							cSD.is_stack=True
def crate_fall_state(co):
	invoke(lambda:setattr(co,'falling',False),delay=.2)
def check_crates_over(c):
	if c.vnum in [3,7,8]:
		return
	for co in scene.entities[:]:
		if is_crate(co) and (co.x == c.x and co.z == c.z) and co.is_stack:
			if co.y > c.y:
				co.falling=True
				co.animate_y(co.y-.32,duration=.2)
				crate_fall_state(co)

## bonus level
def load_b_ui():
	ui.WumpaBonus()
	ui.CrateBonus()
	ui.LiveBonus()
def load_bonus(c):
	status.loading=True
	status.checkpoint=LC.bonus_checkpoint[st.level_index]
	collect_reset()
	if st.bonus_round:
		invoke(lambda:back_to_level(c),delay=.5)
		return
	invoke(lambda:enter_bonus(c),delay=.5)
def enter_bonus(c):
	ui.BlackScreen()
	status.bonus_round=True
	load_b_ui()
	status.day_mode='bonus'
	sn.BonusMusic(T=st.level_index)
	ui.BonusText()
	c.position=(0,-35,-3)
	camera.y=-35
	st.loading=False
	c.freezed=False
def back_to_level(c):
	ui.BlackScreen()
	if st.is_death_route:
		st.is_death_route=False
		st.gem_path_solved=True
	if st.bonus_round:
		st.bonus_round=False
		st.bonus_solved=True
	dMN=_loc.day_m
	st.day_mode=dMN[st.level_index]
	c.position=st.checkpoint
	c.freezed=False
	camera.y=c.y+.5
	st.loading=False

## gem route
def load_gem_route(c):
	st.loading=True
	if st.is_death_route:
		invoke(lambda:back_to_level(c),delay=.5)
		return
	invoke(lambda:load_droute(c),delay=.5)
def load_droute(c):
	ui.BlackScreen()
	if st.is_death_route:
		c.back_to_level(c)
		return
	st.is_death_route=True
	c.position=(200,1,-3)
	camera.position=(200,.5,-3)
	st.loading=False
	c.freezed=False
	sn.SpecialMusic(T=st.level_index)

## npc
def set_val_npc(m,di,cm=True):
	if m.vnum in [3,7,8,14]:
		cm=False
	m.can_move=cm
	m.spawn_pos=m.position
	m.is_hitten=False
	m.fly_direc=None
	m.is_purge=False
	m.m_direction=di
	m.anim_frame=0
	m.unlit=False
	m.fly_time=0
	m.turn=0
def npc_action(m):
	if m.is_purge:
		npc_purge(m)
		return
	if not m.is_hitten:
		if m.vnum in [10,11] and m.ro_mode > 0:
			ro_di={1:lambda:npc_circle_move_xz(m),2:lambda:npc_circle_move_y(m)}
			ro_di[m.ro_mode]()
			return
		if m.vnum != 12:
			npc_walk(m)
		return
	fly_away(m)
def npc_purge(m):
	m.collider=None
	m.can_move=False
	m.fly_time=0
	m.scale_z=max(m.scale_z-time.dt/100,0)
	if m.scale_z <= 0 or m.is_hitten:
		status.NPC_RESET.append(m)
		purge_instance(m)
def npc_walk(m):
	if status.gproc():
		return
	if m.can_move:
		s=m.move_speed
		m_D=m.m_direction
		if m.m_direction == 0:
			if m.turn == 0:
				m.x+=time.dt*s
				if m.x >= m.spawn_pos[0]+1:
					m.rotation_y=90
					m.turn=1
			elif m.turn == 1:
				m.x-=time.dt*s
				if m.x <= m.spawn_pos[0]-1:
					m.rotation_y=270
					m.turn=0
			return
		if m.m_direction == 1:
			if m.turn == 0:
				m.z+=time.dt*s
				if m.z >= m.spawn_pos[2]+1:
					m.turn=1
					m.rotation_y=0
			elif m.turn == 1:
				m.z-=time.dt*s
				if m.z <= m.spawn_pos[2]-1:
					m.rotation_y=180
					m.turn=0
def npc_circle_move_xz(m):
	m.angle-=time.dt*2
	m.angle%=(2*math.pi)
	new_x=m.spawn_pos[0]-1*math.cos(m.angle)
	new_z=m.spawn_pos[2]-1*math.sin(m.angle)
	m.position=Vec3(new_x,m.y,new_z)
	rot=math.degrees(math.atan2(new_z-m.spawn_pos[2],new_x-m.spawn_pos[0]))
	m.rotation_y=-rot
def npc_circle_move_y(m):
	m.angle+=time.dt*2
	m.angle%=(2*math.pi)
	new_x=m.spawn_pos[0]+1.7*math.cos(m.angle)
	new_y=m.spawn_pos[1]+1.7*math.sin(m.angle)
	m.position=Vec3(new_x,new_y,m.z)
	rot=math.degrees(math.atan2(new_y-m.spawn_pos[1],new_x-m.spawn_pos[0]))
	m.rotation_x=rot
	m.rotation_y=-90
def rotate_to_crash(m):
	relative_position=LC.ACTOR.position-m.position
	angle=atan2(relative_position.x,relative_position.z)*(180/pi)+180
	m.rotation_y=angle
	m.rotation_x=-90
def fly_away(n):
	n.position+=n.fly_direc*time.dt*40
	n.fly_time+=time.dt
	if n.fly_time > .5:
		npc_purge(n)
		return
	if n.intersects():
		PNL=n.intersects().entity
		if is_crate(PNL):
			if PNL.vnum in [3,11]:
				PNL.empty_destroy()
			else:
				if PNL.vnum != 6:# avoid checkp accidentally
					PNL.destroy()
		if is_enemie(PNL):
			PNL.fly_direc=n.fly_direc
			PNL.is_hitten=True
			wumpa_count(1)
			npc_purge(n)
def is_enemie(n):
	nnk=[N.Amadillo,N.Turtle,N.SawTurtle,
		N.Penguin,N.Hedgehog,N.Seal,
		N.EatingPlant,N.Rat,N.Lizard,
		N.Eel,N.Scrubber,N.Mouse,N.SewerMine,
		N.Vulture,N.Hippo,N.Gorilla]
	if any(isinstance(n,npc_class) for npc_class in nnk):
		return True
	return False
def bash_enemie(e,h):
	e.is_hitten=True
	e.fly_direc=Vec3(e.x-h.x,0,e.z-h.z)
	sn.obj_audio(ID=8)

## game progress
def save_game():
	return