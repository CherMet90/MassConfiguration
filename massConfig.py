import pexpect
import re
import sys


def login():		#	Функция авторизации
    sw.expect(['ame:', 'ogin:'])
    sw.sendline(' ')		#	Логин
    sw.expect('ord:')
    sw.sendline(' ')		#	Пароль
    
def inputCMD(file):		#	Функция выполнения команд из файла и контроль команды save
    for line in open(file, "r"):
        sw.sendline(line.rstrip('\n'))
        sw.expect('\r\n')
    sw.expect_exact('save')
    sw.expect(["to continue", "Success", "#"])

def saveHuawei():		#	Функция подтверждения сохранения для Huawei
    sw.expect_exact('Y/N')
    sw.sendline('y')
    sw.expect_exact('>')


modelList = ['DGS-1100-06', 'DES-3200-10', 'DGS-3000-10', 'DES-3200-26', 'DES-1210-28', 'DES-1228', 'DES-3028', 'DES-3200-28', 'DES-3052', 'DES-3200-52', "Login", "Connection closed"]
modelDict = {		#	Словарь соответсвия моделей D-Link общему числу портов коммутатора
    'DGS-1100-06': 6,
    'DES-3200-10': 10,
    'DGS-3000-10': 10,
    'DES-3200-26': 26,
    'DES-1210-28': 28,
    'DES-1228': 28,
    'DES-3028': 28,
    'DES-3200-28': 28,
    'DES-3052': 52,
    'DES-3200-52': 52
}
errConnect = open('unreachSW.txt', 'w') 	#	Файл для сохранения неудачных коннектов

for line in open("ipadd.txt", "r"):		#	Цикл перебора айпишников из файла
    try:
        sw = pexpect.spawn('telnet ' + line.rstrip('\n'))
        sw.logfile = sys.stdout.buffer
        
        topIndex = sw.expect(modelList)		#	Ожидание модели коммутатора в шапке
        portsLimit = modelDict[modelList[topIndex]]	#	Получение инфы о количестве портов по модели
		
#	Загрузка файла с командами в зависимости от числа портов

        if portsLimit == 6:
            login()
            inputCMD('6ports.txt')
            sw.sendline("logout\r")
            sw.expect('Connection closed')
        elif portsLimit == 10:
            login()
            inputCMD('10ports.txt')
            sw.sendline("logout\r")
            sw.expect('Connection closed')
        elif portsLimit == 26:
            login()
            inputCMD('26ports.txt')
            sw.sendline("logout\r")
            sw.expect('Connection closed')
        elif portsLimit == 28:
            login()
            inputCMD('28ports.txt')
            sw.sendline("logout\r")
            sw.expect('Connection closed')
        elif portsLimit == 52:
            login()
            inputCMD('52ports.txt')
            sw.sendline("logout\r")
            sw.expect('Connection closed')
			
#	Обработка ошибки отсутствия ключа в словаре (значит это Huawei)

    except KeyError:
        login()
        sw.sendline('disp vers')
        huaweiType = sw.expect(['S2326','S2352'])
        if huaweiType == 0:
            inputCMD('huawei26p.txt')
            saveHuawei()
            sw.sendline('q')
        elif huaweiType == 1:
            inputCMD('huawei52p.txt')
            saveHuawei()
            sw.sendline('q')
        sw.expect_exact('Connection closed')
		
#	Занесение айпи коммутатора при неудачном коннекте

    except:
        errConnect.write(line)

errConnect.close()

exit()
