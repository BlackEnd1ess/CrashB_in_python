import time,pyautogui,os,shutil
import pygetwindow as gw

MAIN_S='C:\\Users\\-_-\\Desktop\\evp\\_stored_\\'
MAIN_P='C:\\Users\\-_-\\Desktop\\evp\\'
MODEL='gorilla_fall'

pv=pyautogui
t=time

frames=11
wait=3

def start(idx):
	os.system('cd '+MAIN_P+' && start CB2Export.exe')
	t.sleep(5.5)
	if os.path.isdir(MAIN_P+MODEL):
		write_inp(idx)

def write_inp(idx):
	pyautogui.write(MODEL,interval=.1)#folder name
	pv.press('enter')#confirm folder
	t.sleep(.5)
	pv.press('enter')#confirm version
	t.sleep(1)
	pv.press('enter')#export call
	t.sleep(1)
	pyautogui.write(str(idx),interval=.1)#write index as name
	t.sleep(.3)
	pv.press('enter')#export name ok
	t.sleep(.5)
	pv.press('enter')#confirm .ply
	t.sleep(wait)
	pv.press('enter')
	pv.press('escape')#confirm .tga
	t.sleep(.3)
	delete_frame(idx)

def delete_frame(idx):
	fi=os.listdir(MAIN_P+MODEL)
	for file in fi:
		fp=os.path.join(MAIN_P+MODEL,file)
		if os.path.isfile(fp):
			if file == 'frame':
				os.remove(fp)
	check_next_frame(idx)

def check_next_frame(idx):
	files=os.listdir(MAIN_P+MODEL)
	for file in files:
		file_path=os.path.join(MAIN_P+MODEL,file)
		if os.path.isfile(file_path):
			if file == 'frame'+str(idx+1):
				npa=os.path.join(MAIN_P+MODEL,'frame')
				os.rename(file_path,npa)

def mv_ex_models():
	f=os.listdir(MAIN_P+MODEL)
	for file in f:
		file_p=os.path.join(MAIN_P+MODEL,file)
		if os.path.isfile(file_p):
			if '.ply' in file or file == '0.tga':
				sp=os.path.join(MAIN_P+MODEL,file)
				dp=os.path.join(MAIN_S,file)
				shutil.move(sp,dp)

for vn in range(frames):
	start(vn)
	print(f'extractions phase... current model Frame: {vn}')
	t.sleep(1)

mv_ex_models()
input('tool successfully executed')