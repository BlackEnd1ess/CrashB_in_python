import crate,item,objects
from ursina import *

c=crate
o=objects
I=item

## pos info
def pos_info(c):
	sx=f"{c.x:.1f}"
	sy=f"{c.y+.16:.2f}"#c
	#sy=f"{c.y+.3:.2f}"#w
	sz=f"{c.z:.1f}"
	#print(len(scene.entities))
	#map_tools.pos_info(self)
	#print('Entities: '+str(len(scene.entities)))
	#print('CRATE reset: '+str(len(st.C_RESET)))
	#print(scene.entities[-1])
	#print(f"c.place_crate(ID=3,p=({sx},{sy},{sz}))")
	#print(f"mt.crate_wall(ID=1,POS=({sx},{sy},{sz}),CNT=[1,3])")
	#print(f"mt.crate_block(ID=1,POS=({sx},{sy},{sz}),CNT=[2,2,2])")
	#print(f"mt.wumpa_row(POS=({sx},{sy},{sz}),CNT=5,WAY=2)")
	#print(f"mt.wumpa_double_row(POS=({sx},{sy},{sz}),CNT=4)")
	#print(f"mt.bounce_twin(POS=({sx},{sy},{sz}),CNT=1)")

## multible crate spawn
def bounce_twin(POS,CNT,trs=1.55):
	for cbt in range(CNT):
		pO=.32*cbt
		c.place_crate(ID=3,p=(POS[0]+pO,POS[1],POS[2]))
		c.place_crate(ID=3,p=(POS[0]+pO,POS[1]+trs,POS[2]))

def steel_bridge(POS,CNT):
	for cst in range(CNT):
		c.place_crate(ID=0,p=(POS[0]-.32*cst,POS[1],POS[2]))

def crate_row(ID,POS,CNT,WAY,l=None,m=None):# WAY: 0=right,1=front,2=up
	for cro in range(CNT):
		pO=.32*cro
		if WAY == 0:
			if ID == 13:
				c.place_crate(ID=ID,p=(POS[0]+pO,POS[1],POS[2]),m=m,l=l)
			else:
				c.place_crate(ID=ID,p=(POS[0]+pO,POS[1],POS[2]))
		elif WAY == 1:
			if ID == 13:
				c.place_crate(ID=ID,p=(POS[0],POS[1],POS[2]+pO),m=m,l=l)
			else:
				c.place_crate(ID=ID,p=(POS[0],POS[1],POS[2]+pO))
		else:
			if ID == 13:
				c.place_crate(ID=ID,p=(POS[0],POS[1]+pO,POS[2]),m=m,l=l)
			else:
				c.place_crate(ID=ID,p=(POS[0],POS[1]+pO,POS[2]))

def crate_wall(ID,POS,CNT):#[x,y]
	for cwX in range(CNT[0]):
		for cwY in range(CNT[1]):
			c.place_crate(ID=ID,p=(POS[0]+.32*cwX,POS[1]+.32*cwY,POS[2]))

def crate_stair(ID,POS,CNT,WAY):# WAY: 0=up,1=down
	for cs in range(CNT):
		pO=.32*cs
		c_way={0:POS[1]+pO,1:POS[1]-pO}
		c.place_crate(ID=ID,p=(POS[0]+pO,c_way[WAY],POS[2]))

def crate_block(ID,POS,CNT):#[x,y,z]
	for cbX in range(CNT[0]):
		for cbZ in range(CNT[1]):
			for cbY in range(CNT[2]):
				pO=.32*cbX
				pA=.32*cbY
				pE=.32*cbZ
				c.place_crate(ID=ID,p=(POS[0]+pO,POS[1]+pA,POS[2]+pE))

def crate_plane(ID,POS,CNT):#[x,z]
	for cwX in range(CNT[0]):
		for cwZ in range(CNT[1]):
			c.place_crate(ID=ID,p=(POS[0]+.32*cwX,POS[1],POS[2]+.32*cwZ))


## multible wumpa spawn
def wumpa_row(POS,CNT,WAY):#WAY: 0=right,1=front,2=up
	for wr in range(CNT):
		if WAY == 0:
			I.place_wumpa((POS[0]+wr/3,POS[1],POS[2]),cnt=1)
		elif WAY == 1:
			I.place_wumpa((POS[0],POS[1],POS[2]+wr/3),cnt=1)
		else:
			I.place_wumpa((POS[0],POS[1]+wr/3,POS[2]),cnt=1)

def wumpa_double_row(POS,CNT):
	for wr in range(CNT):
		I.place_wumpa((POS[0]+wr/3,POS[1],POS[2]),cnt=1)
		I.place_wumpa((POS[0]+wr/3,POS[1]+.3,POS[2]),cnt=1)

def wumpa_wall(POS,CNT):#[x,y]
	for wx in range(CNT[0]):
		for wy in range(CNT[1]):
			I.place_wumpa((POS[0]+wx/3,POS[1]+wy/3,POS[2]),cnt=1)

def wumpa_plane(POS,CNT):#[x,z]
	for wx in range(CNT[0]):
		for wz in range(CNT[1]):
			I.place_wumpa((POS[0]+wx/3,POS[1],POS[2]+wz/3),cnt=1)

def wumpa_block(POS,CNT):#[x,y,z]
	for wx in range(CNT[0]):
		for wy in range(CNT[1]):
			for wz in range(CNT[2]):
				I.place_wumpa((POS[0]+wx/3,POS[1]+wy/3,POS[2]+wz/3),cnt=1)