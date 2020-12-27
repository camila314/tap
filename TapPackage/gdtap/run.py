from __future__ import print_function
import clk
import os
import shutil
import requests
import io
from tqdm import tqdm
import zipfile
import time
import glob
from distutils.spawn import find_executable

def clearscreen():
	for i in range(20):
		print( ("\033[A" + " "*78) *99)
	print( ("\033[A" + " "*7) *99, end="\r")

def runit():
	os.environ["PATH"] += os.pathsep + os.path.expanduser('~')

	if find_executable('ffmpeg') is None:
		url = "https://evermeet.cx/ffmpeg/ffmpeg-4.3.1.zip" #big file test
		# Streaming, so we can iterate over the response.
		response = requests.get(url, stream=True)
		total_size_in_bytes= int(response.headers.get('content-length', 0))
		block_size = 1024 #1 Kibibyte
		progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc='Downloading \u001b[32;1mffmpeg\u001b[0m', colour='green')
		file = io.BytesIO()
		for data in response.iter_content(block_size):
			progress_bar.update(len(data))
			file.write(data)
		progress_bar.close()
		if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
			print("\u001b[31mERROR, something went wrong\u001b[0m")
			exit()

		print("Pouring \u001b[32;1mffmpeg\u001b[0m...")

		ffzip = zipfile.ZipFile(file).open('ffmpeg')
		fileobj = open(os.path.join(os.path.expanduser('~'),'ffmpeg'), 'wb')
		fileobj.write(ffzip.read())
		fileobj.close()
		os.chmod(os.path.join(os.path.expanduser('~'),'ffmpeg'), 0o777)

		print('Done.')
		time.sleep(1)
		clearscreen()
	try:
		os.makedirs(os.path.join(os.path.expanduser('~'), 'Desktop/holds'))
	except OSError:
		pass
	try:
		os.makedirs(os.path.join(os.path.expanduser('~'), 'Desktop/releases'))
	except OSError:
		pass

	if len(glob.glob(os.path.join(os.path.expanduser('~'),"Desktop/holds/*.wav"))) == 0 or len(glob.glob(os.path.join(os.path.expanduser('~'),"Desktop/releases/*.wav"))) == 0:
		print("\u001b[31;1m[Error]\u001b[0m No clicks found. Put your recorded clicks into the holds/releases folder on your desktop")
		print("Exiting")
		exit()
	if len(glob.glob(os.path.join(os.path.expanduser('~'),"Desktop/holds/s*.wav"))) == 0:
		print("\u001b[31;1m[Warning]\u001b[0m No soft clicks found. Tap will still work, but will not be as realistic. Add soft clicks by putting an 's' in front of the file name in the holds folder")
	clk.main()
if __name__ == '__main__':
	runit()