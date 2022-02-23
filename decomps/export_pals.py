# export_pals.py
#	export .pal file for all files in directory using irfanview
#
# written by: ghoulslash
#
import os, subprocess

src = input('Enter src: ')
dest = input('Enter dest: ')

for filename in os.listdir(src):
	if filename.endswith(".png"):
		name = str(os.path.splitext(os.path.basename(filename))[0])
		full_src = src + str(r"\\") + name
		full_dst = dest + str(r"\\") + name
		cmd = "i_view64.exe " +  full_src + ".png /export_pal=" + full_dst + ".pal /killmesoftly"
		#print(cmd) 	#debugging
		#exit()			#debugging
		subprocess.call(cmd)
