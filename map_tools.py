import crate,item,objects
from ursina import *

c=crate
o=objects
I=item

## multible crate spawn
def bounce_twin(POS,CNT):
	for cbt in range(CNT):
		c.place_crate(ID=3,p=(POS[0]+cbt/3.1,POS[1],POS[2]))
		c.place_crate(ID=3,p=(POS[0]+cbt/3.1,POS[1]+1.6,POS[2]))

def steel_bridge(POS,CNT):
	for cst in range(CNT):
		c.place_crate(ID=0,p=(POS[0]+cst/3.1,POS[1],POS[2]))

def crate_row(ID,POS,CNT,WAY):# WAY: 0=right,1=front,2=up
	for cro in range(CNT):
		if WAY == 0:
			c.place_crate(ID=ID,p=(POS[0]+cro/3.1,POS[1],POS[2]))
		elif WAY == 1:
			c.place_crate(ID=ID,p=(POS[0],POS[1],POS[2]+cro/3.1))
		else:
			c.place_crate(ID=ID,p=(POS[0],POS[1]+cro/3.1,POS[2]))

def crate_wall(ID,POS,CNT):
	for cwX in range(CNT):
		for cwY in range(CNT):
			c.place_crate(ID=ID,p=(POS[0]+cwX/3.1,POS[1]+cwY/3.1,POS[2]))

def crate_stair(ID,POS,CNT,WAY):# WAY: 0=up,1=down
	for cs in range(CNT):
		c_way={0:POS[1]+cs/3.1,1:POS[1]-cs/3.1}
		c.place_crate(ID=ID,p=(POS[0]+cs/3.1,c_way[WAY],POS[2]))

def crate_block(ID,POS,CNT):
	for cbX in range(CNT):
		for cbZ in range(CNT):
			for cbY in range(CNT):
				c.place_crate(ID=ID,p=(POS[0]+cbX/3.1,POS[1]+cbY/3.1,POS[2]+cbZ/3.1))

def crate_plane(ID,POS,CNT):
	for cwX in range(CNT):
		for cwZ in range(CNT):
			c.place_crate(ID=ID,p=(POS[0]+cwX/3.1,POS[1],POS[2]+cwZ/3.1))


## multible wumpa spawn
def wumpa_row(POS,CNT,WAY):
	for wr in range(CNT):#WAY: 0=right,1=front,2=up
		if WAY == 0:
			I.WumpaFruit(pos=(POS[0]+wr/3,POS[1],POS[2]))
		elif WAY == 1:
			I.WumpaFruit(pos=(POS[0],POS[1],POS[2]+wr/3))
		else:
			I.WumpaFruit(pos=(POS[0],POS[1]+wr/3,POS[2]))

def wumpa_double_row(POS,CNT):
	for wr in range(CNT):
		I.WumpaFruit(pos=(POS[0]+wr/3,POS[1],POS[2]))
		I.WumpaFruit(pos=(POS[0]+wr/3,POS[1]+.3,POS[2]))


def wumpa_wall(POS,CNT):
	for wx in range(CNT):
		for wy in range(CNT):
			I.WumpaFruit(pos=(POS[0]+wx/3,POS[1]+wy/3,POS[2]))

def wumpa_plane(POS,CNT):
	for wx in range(CNT):
		for wz in range(CNT):
			I.WumpaFruit(pos=(POS[0]+wx/3,POS[1],POS[2]+wz/3))

def wumpa_block(POS,CNT):
	for wx in range(CNT):
		for wy in range(CNT):
			for wz in range(CNT):
				I.WumpaFruit(pos=(POS[0]+wx/3,POS[1]+wy/3,POS[2]+wz/3))