import json,ui,crate,item,status,sound,npc,settings,_loc,math,warproom
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
	for _a in ['rnfr','jmfr','idfr','spfr','ldfr','fafr','flfr','ssfr','sufr','srfr','smfr','blfr','walk_snd','fall_time','slide_fwd','in_water','space_time']:
		setattr(c,_a,0)#animation frames
	for _v in ['aq_bonus','walking','jumping','landed','tcr','frst_lnd','is_landing','is_attack','is_flip','warped','freezed','injured','is_slippery','wall_stop','h_lock','b_smash','standup']:
		setattr(c,_v,False)#flags
	c.move_speed=LC.dfsp
	c.gravity=LC.dfsp
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
		st.game_over=True
		game_over()
		return
	st.aku_hit=0
	if st.fails > 2:
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
def various_val(c):
	c.in_water=max(c.in_water-time.dt,0)
	c.indoor=max(c.indoor-time.dt,0)
	if not c.is_slippery:
		c.move_speed=LC.dfsp
	if st.bonus_solved and not st.wait_screen:
		c.aq_bonus=(st.wumpa_bonus > 0 or st.crate_bonus > 0 or st.lives_bonus > 0)
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
def c_attack(c):
	for k in scene.entities:
		if distance(c,k) < .5 and k.collider != None:
			if is_enemie(k) and not (k.is_hitten or k.is_purge):
				if (k.vnum in [1,11]) or (k.vnum == 5 and k.def_mode):
					get_damage(c,rsn=1)
				bash_enemie(k,h=c)
			if is_crate(k):
				if k.vnum in [3,11]:
					k.empty_destroy()
				else:
					k.destroy()
def c_smash(c):
	for wr in scene.entities:
		if distance(wr,c) < .4 and wr.collider != None:
			if is_crate(wr):
				if wr.vnum in [3,11]:
					wr.empty_destroy()
				if wr.vnum == 14:
					wr.c_destroy()
				else:
					wr.destroy()
			if is_enemie(wr):
				wr.is_purge=True

## camera actor
def cam_follow(c):
	ftt=time.dt
	camera.z=lerp(camera.z,c.z-c.CMS,ftt*3)
	camera.x=lerp(camera.x,c.x,ftt*2)
	if not c.jumping:
		if (c.indoor > 0 and c.landed):
			camera.y=lerp(camera.y,c.y+1,time.dt*1.5)
			camera.rotation_x=15
			return
		if (c.landed and not c.freezed):
			camera.y=lerp(camera.y,c.y+1.6,time.dt)
			camera.rotation_x=lerp(camera.rotation_x,20,time.dt/2.5)
		return
	if c.indoor <= 0:
		camera.rotation_x=lerp(camera.rotation_x,10,ftt/2)
def cam_bonus(c):
	ftt=time.dt*3
	camera.z=(c.z-3.2)
	camera.x=lerp(camera.x,c.x,ftt)
	camera.y=lerp(camera.y,c.y+1.4,time.dt*1.5)
	camera.rotation_x=16

## world, misc
def spawn_level_crystal(idx):
	cry_pos={0:(0,0,0),1:(0,1.5,-13),2:(35.5,6.4,28.5),3:(0,2.5,60.5),4:(14,4.25,66),5:(12,.8,-7),6:(0,.3,-15)}
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
	if st.aku_hit > 2:
		st.aku_hit=2
	st.NPC_RESET.clear()
	st.W_RESET.clear()
	st.C_RESET.clear()
	st.is_invincible=False
	st.level_crystal=False
	st.level_col_gem=False
	st.level_cle_gem=False
	st.gem_path_solved=False
	st.is_death_route=False
	st.bonus_solved=False
	st.bonus_round=False
	st.LEVEL_CLEAN=False
	st.death_event=False
	st.gem_death=False
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
	if is_crate(v):
		if not (v.poly == 1 or v.vnum == 16):
			st.C_RESET.append(v)
	if is_enemie(v):
		st.NPC_RESET.append(v)
	if isinstance(v,item.WumpaFruit):
		if not v.c_purge:
			st.W_RESET.append(v.spawn_pos)
	v.parent=None
	scene.entities.remove(v)
	v.disable()
	del v
def game_pause():
	if not st.pause:
		st.pause=True
		return
	st.pause=False
def game_over():
	invoke(lambda:ui.GameOverScreen(),delay=2)

## collisions
def check_ceiling(c):
	vc=c.intersects(ignore=[c,LC.shdw])
	ve=vc.entity
	if vc and vc.normal == Vec3(0,-1,0):
		if not (ve.name in LC.item_lst+LC.trigger_lst):
			if is_crate(ve) and not c.tcr:
				c.tcr=True
				ve.destroy()
				invoke(lambda:setattr(c,'tcr',False),delay=.1)
			c.y=c.y
			c.jumping=False
def check_wall(c):
	hT=c.intersects(ignore=[c,LC.shdw])
	jV=hT.entity
	xa=str(jV)
	if hT.hit and not (hT.normal in [Vec3(0,1,0),Vec3(0,-1,0)]):
		if isinstance(jV,crate.Nitro):
			jV.destroy()
			return
		if xa in LC.item_lst:
			jV.collect()
			return
		if is_enemie(jV):
			R=1
			if jV.vnum == 7:
				R=5
			if not c.is_attack:
				get_damage(c,rsn=R)
			return
		if not xa in LC.trigger_lst:
			c.position=lerp(c.position,c.position+hT.normal,time.dt*c.move_speed)
def check_floor(c):
	vj=boxcast(c.world_position,Vec3(0,1,0),distance=.01,thickness=(.13,.13),ignore=[c,LC.shdw],debug=False)
	vp=vj.entity
	if vj.normal and not (vp.name in LC.item_lst+LC.dangers+LC.trigger_lst):
		landing(c,e=vj.world_point.y,o=vp)
		spc_floor(c,e=vp)
		return
	c.landed=False
	fsp={False:(time.dt*c.gravity),True:(time.dt*c.gravity)*2}
	c.y-=fsp[c.b_smash]
	c.fall_time+=time.dt
	c.anim_fall()
def landing(c,e,o):
	c.y=e
	c.landed=True
	if c.frst_lnd:
		floor_interact(c,o)
		c.frst_lnd=False
		c.is_flip=False
		c.h_lock=False
		c.flfr=0
		c.ldfr=0
		c.jmfr=0
		c.is_landing=True
		c.space_time=0
		c.fall_time=0
		sn.landing_sound(c,o)
def floor_interact(c,e):
	if is_crate(e) and not ((e.vnum == 0) or (e.vnum in [9,10,11] and e.activ)) and c.fall_time > .05:
		if e.vnum in [7,8]:
			c.jump_typ(t=4)
			e.c_action()
			return
		if e.vnum == 3:
			c.jump_typ(t=3)
		else:
			if not e.vnum == 14:
				c.jump_typ(t=2)
		e.destroy()
		return
	if is_enemie(e) and not (e.is_hitten or e.is_purge):
		if (e.vnum in [2,9]) or (e.vnum == 5 and e.def_mode):
			get_damage(c,rsn=1)
		e.is_purge=True
		c.jump_typ(t=2)
		sn.pc_audio(ID=5)
def spc_floor(c,e):
	u=e.name
	c.is_slippery=(u == 'iceg')
	if u in ['bnpt','gmpt']:
		ptf_up(p=e,c=c)
		return
	if u in ['loos','swpt','HPP']:
		e.active=True
		return
	if (u == 'plnk' and e.typ == 1):
		e.pl_touch()
		return
	if (u == 'swpi' and e.typ == 3):
		get_damage(c,rsn=3)
		return
	if u == 'wtrh':
		dth_event(c,rsn=2)
		return
	if u == 'mptf' and not c.walking:
		e.mv_player()
def ptf_up(p,c):
	if not c.freezed:
		c.freezed=True
		c.position=(p.x,c.y,p.z)
		c.rotation_y=0
	p.y+=time.dt/1.5
	if p.y > p.start_y+3:
		p.y=p.start_y
		go_to={'bnpt':lambda:load_bonus(c),'gmpt':lambda:load_gem_route(c)}
		go_to[p.name]()

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
		cR.texture='res/crate/crate_t'+str(cR.time_stop)+'.tga'
	else:
		cR.texture='res/crate/'+str(cR.vnum)+'.tga'
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
	st.loading=True
	st.checkpoint=LC.bonus_checkpoint[st.level_index]
	collect_reset()
	if st.bonus_round:
		invoke(lambda:back_to_level(c),delay=.5)
		return
	invoke(lambda:enter_bonus(c),delay=.5)
def enter_bonus(c):
	ui.BlackScreen()
	st.bonus_round=True
	load_b_ui()
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
save_file='savegame.json'
def save_game():
	save_data={
		'SV_WU':st.wumpa_fruits,#wumpa fruits
		'SV_LF':st.extra_lives,#extra lives
		'SV_CR':st.collected_crystals,#crystal count
		'SV_CG':st.color_gems,#color gem count
		'SV_CL':st.clear_gems,#clear gem count
		'SV_AK':st.aku_hit,#aku mask
		'LS_CR':st.CRYSTAL,#Lv ID crystal
		'LS_CL':st.CLEAR_GEM,#Lv ID clear gem
		'LS_CG':st.COLOR_GEM,#Color Gem ID
		'M_VOL':settings.MUSIC_VOLUME,
		'S_VOL':settings.SFX_VOLUME}
	with open(save_file,'w') as f:
		json.dump(save_data,f)
def load_game():
	with open(save_file,'r') as f:
		save_data=json.load(f)
	st.wumpa_fruits=save_data['SV_WU']
	st.extra_lives=save_data['SV_LF']
	st.collected_crystals=save_data['SV_CR']
	st.color_gems=save_data['SV_CG']
	st.clear_gems=save_data['SV_CL']
	st.aku_hit=save_data['SV_AK']
	st.CRYSTAL=[(x) for x in save_data['LS_CR']]
	st.CLEAR_GEM=[(x) for x in save_data['LS_CL']]
	st.COLOR_GEM=[(x) for x in save_data['LS_CG']]
	settings.SFX_VOLUME=save_data['S_VOL']
	settings.MUSIC_VOLUME=save_data['M_VOL']

## Level of Detail
class LODSystem(Entity):
	def __init__(self):
		s=self
		super().__init__()
		si=st.level_index
		CLW={1:LC.LV1_LOD,2:LC.LV2_LOD,3:LC.LV3_LOD,4:LC.LV4_LOD,5:LC.LV5_LOD,6:LC.LV3_LOD}
		s.dst_bck={1:(2),2:(2),3:(4),4:(3),5:(4),6:(16)}[si]
		s.dst_far=LC.fog_distance[si]
		s.MAIN_LOD=CLW[si]
		s.dst_cam=8
		s.rt=.6
	def refr(self):
		p=LC.ACTOR
		s=self
		for v in scene.entities[:]:
			if isinstance(v,item.WumpaFruit):
				v.enabled=(distance(p,v) < 6)
			kv=(v.z < p.z+s.dst_far and p.z < v.z+s.dst_bck and abs(p.x-v.x) < s.dst_cam)
			if (is_enemie(v) or v.name in s.MAIN_LOD):
				v.enabled=kv
			if is_crate(v):
				if v.vnum in [3,9,10,11,12,13]:
					v.visible=kv
				else:
					v.enabled=kv
	def update(self):
		s=self
		if st.pause:
			return
		s.rt=max(s.rt-time.dt,0)
		if s.rt <= 0:
			s.rt=.6
			s.refr()