import pygetwindow as gw
import time,pyautogui

win=gw.getWindowsWithTitle('CrashEdit')
NAME='gorilla'
outf='C:\\Users\-_-\\Desktop\\evp\\'+NAME+'\\frame'
t=time
cnt=33

print('tool is starting in 3 sec')
t.sleep(3)
def run_tool(n):
	pyautogui.moveTo(95,107+(n*18))
	pyautogui.click()
	t.sleep(.3)
	pyautogui.moveTo(670,110)
	pyautogui.click()
	t.sleep(.2)
	pyautogui.write(outf+str(n))
	t.sleep(.1)
	pyautogui.press('enter')

if win:
	t_window=win[0]
	t_window.activate()
	for ext in range(cnt):
		run_tool(ext)
		t.sleep(.1)
input('fin')