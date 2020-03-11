import subprocess

def video_check(file_path, output_file_path, frames_expected):
	""" Rotating video (mobile front+back camera) using FFMPEG Library """
	
	try:
		command = "ffmpeg -i "+file_path+" -strict -2 -filter:v fps=fps="+frames_expected+" "+output_file_path
		p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			x = (line.decode('utf-8'))
		
		return True
	except:
		return False


# video_check("/home/prakash/Desktop/test.mp4", "/home/prakash/Desktop/out2.mp4", "14")