import serial, json
from os import system
from sys import argv
from time import sleep
from collections import namedtuple
import re

config = json.load(open("config.json", "r")) #открываем конфиг
config = namedtuple("config", config.keys())(*config.values())

def sendSMS(num, text): #блок для отправки SMS. 
    ser.write(('AT+CMGS="'+ num+'"\r').encode("ascii")) #на этот блок можно не обращать внимание. 
    print(ser.read_all()) #мы пытались реализовать отправку с кодировкой GSM, но что то пошло не так
    sleep(1)
    ser.write(''.join('%04X'%ord(i) for i in text).encode('utf-8')) 
    print(ser.read_all())
    sleep(1)
    ser.write(chr(26).encode("ascii"))
    print(ser.read_all())
    sleep(1)

#AT+CMGS - отправка Сообщений
#AT+CMGL - получение сообщений

def sendCommand(command): #отправляет команду модему
    ser.write((command+'\r').encode("ascii")) #кодировка в ascii - обязательна
    sleep(1)
    return ser.read_all().decode("ascii") #преведение в человекоподобный вид

def decodeMsg(msg): #переводит текст из кодов в нормальный текст
    #print(len(msg))
    tmpArr = []
    for i in range(0, int(len(msg)/4)):
    #   print(i)
        tmpArr.append(msg[i*4: (i+1)*4])

    tmpArr = [ chr(int(i.encode("ascii"), 16)) for i in tmpArr ]
    #print(tmpArr)
    return "".join(tmpArr)

def initSIM(pin = config.pin): #инициализирует симкарту
    sleep(1)
    if config.pin != '':
        #print('ввод пинкода - ' + str(sendCommand('AT+CPIN='+str(pin))))#Эти строчки сотрутся
        sendCommand('AT+CPIN='+str(pin)) #AT+CPIN - ввод пинкода
    sleep(2) #паузы - обязательно
    #print('Выбор режима' + str(sendCommand("AT+CMGF=1")))
    sendCommand("AT+CMGF=1") #AT+CMGF- выбор режима, где 0 - цифровой, 1 - текстовый
    sleep(2)

#в этом блоке возникла ошибка. Если сообщения приожит в ascii, то оно приходит в чистом виде.
# но если сообщение приходит с символами из юникода, то его нужно декодировать
# и мы ещё не добавили поддержку длинных сообщений. Поэтому максимальная длина - 70 символов

def getSms(option="REC UNREAD"): #Функция получения СМС
    raw_string = sendCommand('AT+CMGL="'+str(option)+'"') #AT+CMGL - получение СМС по спискам
    medium_strings = re.findall(r"\+CMGL: .+\r\n.+\r\n", raw_string) #регулярка для поиска записей с сообщениями среди мусора
   # print(medium_strings)
    cooked_strings = [] #переменная для хранения записей в формате [номер:текст]
    for i in medium_strings: 
        #print(i) 
        cooked_strings.append(list())
        cooked_strings[-1].append(re.findall(r'\"\+?\d+\"',i)[0])
        message_str = i.split('\r\n')[-2]
        if len(re.findall(r'[1234567890ABCDEF]{4,}', message_str)): #регулярка для опознания юникода. Слова, по типу ACAB
            cooked_strings[-1].append(decodeMsg(message_str))       #будут декодироваться, и получится что-то в роде "겫"
        else:
            cooked_strings[-1].append(message_str)                  #если не получилось декодировать, то всё кидается в
								    #исключение и добавляется "как есть"

        #print(str(cooked_strings[0]) + str(cooked_strings[-1]))

    return cooked_strings

if __name__ == '__main__':
    config = json.load(open("config.json", "r"))
    config = namedtuple("config", config.keys())(*config.values())
    ser = serial.Serial(config.device, config.speed)
    #print('Инициализация симкарты')
    initSIM(6835) 
    sleep(1)
    print(getSms())

    sleep(5)
else:
    
    ser = serial.Serial(config.device, config.speed)
    print('Инициализация симкарты')
    initSIM(6835) 
    sleep(1)
    print("Тест"),
    print(sendCommand("AT"))
