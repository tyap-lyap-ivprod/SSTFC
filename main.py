import serial, json
from os import system
from sys import argv
from time import sleep
from collections import namedtuple


config = json.load(open("config.json", "r"))
config = namedtuple("config", config.keys())(*config.values())

def sendSMS(num, text):
	"""
	НУЖНО СДЕЛАТЬ ФУНКЦИЮ ОТПРАВКИИ СООБЩЕНИЙ!!!!
	"""
	pass

def sendCommand(command): #отправляет команду модему
	ser.write((command+'\r').encode("ascii"))
	sleep(1)
	return ser.read(ser.in_waiting).decode("ascii")

def decodeMsg(msg): #переводит текст из кодов в нормальный текст
	#print(len(msg))
	tmpArr = []
	for i in range(0, int(len(msg)/4)):
	#	print(i)
		tmpArr.append(msg[i*4: (i+1)*4])
	tmpArr = [ chr(int(i.encode("ascii"), 16)) for i in tmpArr ]
	#print(tmpArr)
	return "".join(tmpArr)

def initSIM(pin = config.pin): #инициализирует симкарту
	sleep(1)
	#тут должен быть код с подтягиванием пинкода из конфига
	if config.pin != '':
		print('ввод пинкода - ' + str(sendCommand('AT+CPIN='+str(pin))))#Эти строчки сотрутся
	sleep(5)
	print('Выбор режима' + str(sendCommand("AT+CMGF=1")))
	sleep(5)

def getRawSms(option="REC UNREAD"):
	raw_msg = sendCommand('AT+CMGL="'+str(option)+'"')
	msg1 = raw_msg.replace('\r\n','\n').split('\n+CMGL: ')
	return msg1

if __name__ == '__main__':
	config = json.load(open("config.json", "r"))
	config = namedtuple("config", config.keys())(*config.values())
	ser = serial.Serial(config.device, config.speed)
	while(1):
		msgs = getRawSms() #тут он долен получать сообщения вида [[num, text], [num, text]...]
		#и да, текст декодированный
		
		for i in msgs:#тут он проходится по ним, еспи пусто, то не походится(спс, кэп)
			for o in config.commands:
				
				if(i[1][:len(o['msg'])] == o['msg'] and o['activate']):
					
					if(o['type'] == 'system'):
						system(o['command'])
					
					if(o['type'] == 'send'):
						for p in confing.message_numbers:
							sendSMS(i[0], i[1])
	sleep(5)
else:
	
	ser = serial.Serial('/dev/ttyUSB2', '9600')
	print('Инициализация симкарты')
	initSIM() 
	sleep(1)
	print("Тест"),
	print(sendCommand("AT"))
