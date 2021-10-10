import pexpect
import re
import sys


def login():
    sw.expect(['ame:', 'ogin:'])
    sw.sendline(' ')
    sw.expect('ord:')
    sw.sendline(' ')
    
def inputCMD(file):
    for line in open(file, "r"):
        sw.sendline(line.rstrip('\n'))
        sw.expect('\r\n')
    sw.expect_exact('save')
    sw.expect(["to continue", "Success", "#"])

def saveHuawei():
    sw.expect_exact('Y/N')
    sw.sendline('y')
    sw.expect_exact('>')


modelList = ['DGS-1100-06', 'DES-3200-10', 'DGS-3000-10', 'DES-3200-26', 'DES-1210-28', 'DES-1228', 'DES-3028', 'DES-3200-28', 'DES-3052', 'DES-3200-52', "Login", "Connection closed"]
modelDict = {
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
errConnect = open('unreachSW.txt', 'w')

for line in open("ipadd.txt", "r"):
    try:
        sw = pexpect.spawn('telnet ' + line.rstrip('\n'))
        sw.logfile = sys.stdout.buffer
        
        topIndex = sw.expect(modelList)
        portsLimit = modelDict[modelList[topIndex]]
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
    except:
        errConnect.write(line)

errConnect.close()

exit()
