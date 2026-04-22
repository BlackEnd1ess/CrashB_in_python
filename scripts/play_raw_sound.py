import soundfile,sounddevice,io,SFX_DATABASE

def play_sound(snd,pit=1,vol=1):
	data,rate=soundfile.read(io.BytesIO(SFX_DATABASE.SND_DB[snd]),dtype='float32')
	sounddevice.play(data*vol,rate*pit)
	del snd,pit,vol
play_sound('box_air',pit=1,vol=1)

input('done')