from ursina import Entity

## one load level settings
checkpoint=None

## warp room music index
WARP_ROOM_MUSIC=1

## game progress items
COLOR_GEM=[]
CLEAR_GEM=[]
CRYSTAL=[]
RELIC=[]

## reset instances
BOX_RESET=[]
WMP_RESET=[]
NPC_RESET=[]
SWI_RESET=[]

## relic rule
current_relic_rank=2
level_relic_time=0
relic_time_stop=0

##player rule
p_last_direc=None
selected_level=1
aku_inv_time=20
level_index=0
aku_hit=0
fails=0

##npc count
npc_in_level=0

## wumpa count
wumpas_in_level=0
wumpa_fruits=0
wumpa_bonus=0

## crate count
crates_in_level=0
crates_in_bonus=0
crate_to_sv=0
crate_count=0
crate_bonus=0

## live count
lives_bonus=0
extra_lives=4

## collected gems/crystal/relic
ui_gem_anim_index=1
color_gem_id=0
relic_rank=2

## ui timer
show_wumpas=0
show_crates=0
show_lives=0
show_gems=0

## multible audio limit
wu_sn=0
br_sn=0
ex_sn=0
ni_sn=0

## level processing
LV_CLEAR_PROCESS=False
RELIC_TRIAL_DONE=False
DEV_LEVEL_INDEX=9
LEVEL_CLEAN=False
game_over=False

toggle_thunder=False
toggle_rain=False

level_crystal=False
level_col_gem=False
level_cle_gem=False

bonus_solved=False
bonus_round=False
death_route=False

weather_thunder=False
gem_path_solved=False

bonus_warp_room=False
relic_challange=False
is_invincible=False
wait_screen=False
death_event=False
aku_exist=False
gem_death=False
crd_seen=False
loading=False
pause=False

##memory debug
SNAP_NUM=0
snap1=None
snap2=None

## global funcs
def wtr_dist(w,p):
	return ((p.z < w.z+(w.scale_z/2)+4) and (p.z > w.z-(w.scale_z/2)-4) and (p.x < w.x+(w.scale_x/2)+2) and (p.x > w.x-w.scale_x/2-2))

def p_idle(c):
	return c.landed and not (c.jumping or c.is_spin or c.walking or c.is_landing or c.pushed)

def p_rst(c):
	return not c.warped or (c.standup or c.freezed or death_event)

def gproc():
	return (loading or pause or LV_CLEAR_PROCESS or game_over)