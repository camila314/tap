from pydub import AudioSegment
import struct
from pydub.playback import play
from tqdm import tqdm
import random
import math
import sys
import os
import glob

def getRandomPath(hold=True, soft=False):
	s_char = 's' if soft else ''
	if hold:
		paths = glob.glob(os.path.join(os.path.expanduser('~'),"Desktop/holds/{}*.wav".format(s_char)))
		if len(paths) == 0:
			paths = glob.glob(os.path.join(os.path.expanduser('~'),"Desktop/holds/*.wav"))
	else:
		paths = glob.glob(os.path.join(os.path.expanduser('~'),"Desktop/releases/*.wav"))
	return random.choice(paths)

audLength = 1
input = input if sys.version[0]=='3' else raw_input
def db2mag(db):
	return 10**(db/20.)
def mag2db(mag):
	return 20.*math.log10(mag)

def nerve(x):
	return math.tanh(math.exp(0.1*x -0.9))/2.

class Click(object):
	def __init__(self, data):
		self.position, _, self.hold = struct.unpack("di?xxx", data)
		self.useful = self.position!=0
		self.position += 0.1

		if self.hold:
			self.audio = AudioSegment.from_wav(getRandomPath())
		else:
			self.audio = AudioSegment.from_wav(getRandomPath(hold=False))
	def multVolume(self, amount):
		#print(math.log2(amount)*10)
		try:
			self.audio = self.audio.apply_gain(mag2db(db2mag(self.audio.dBFS)*amount)-self.audio.dBFS)
			#self.audio = self.audio.pan(amount-1).split_to_mono()[1]
		except Exception as e:
			print(e)
			exit()
	def process(self, lastClick):
		bias = random.uniform(0.8, 1.2)
		if self.position/audLength>0.5:
			bias += nerve(100*self.position/audLength)
		if lastClick==None:
			self.multVolume(bias)
			return
		if (self.position-lastClick.position)/2 < 0.1 and self.hold:
			self.audio = AudioSegment.from_wav(getRandomPath(soft=True))

		timeSince = (self.position-lastClick.position)/2
		#print(timeSince)
		if timeSince>0.1  or ~-self.hold:
			self.multVolume(bias)
		else:
			ret = (90.*timeSince*timeSince)+0.0613
			self.multVolume(ret*bias)

		octaves = random.uniform(-0.1,0.1)
		self.audio = self.audio._spawn(self.audio.raw_data, overrides={'frame_rate': int(self.audio.frame_rate * (2.0 ** octaves))})

def main():
	global audLength	
	macro = open(input("Drag the macro file here:").strip().replace('\\',''),'rb').read()
	try:
		clicks_ = list([Click(macro[i:i+16]) for i in range(0, len(macro), 16)])
	except struct.error:
		print('\u001b[31;1m[Error]\u001b[0m Invalid macro file')
		exit()
	clicks = []
	for i in clicks_:
		if clicks==[] or clicks[-1].position<i.position:
			clicks.append(i)
		else:
			break

	audLength = max([c.position for c in clicks])+1
	mainClip = AudioSegment.silent(duration=round(audLength*1100))

	lastH = None
	lastC = None
	for c in tqdm(clicks, colour='yellow', desc='Mapping clicks'):
		if lastC==None or c.hold != lastC.hold:
			c.process(lastH)
			#print(c.hold)
			if c.hold:
				lastH = c
			lastC = c
			mainClip = mainClip.overlay(c.audio, position=c.position*1000)
	mainClip.export(os.path.join(os.path.expanduser('~'),"Desktop/tapOutput.wav"))
	print("Success. Check your desktop for the output file")