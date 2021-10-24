import random
import time
import os

def ServerStatus(server):
    # check if we can ping the server
    proxyIp = server
    response = os.system("ping -c 1 " + proxyIp)
    
    if response == 0:
        return True
    else:
        return False

def proxyJump(intervalo):
    print('')
    print('Comenzando...')

    while True:
        #generate proxy
        seed = random.randint(0, 2238)
        f = open("proxyList.txt", "r")
        proxy = f.readlines()[seed]
        f.close

        proxyWithoutPort = proxy.split(':')
        # check if generated proxy is working and execute it
        if ServerStatus(proxyWithoutPort[0]):
            os.system('setproxy ' + proxy)
            print(proxy + 'es nuestro proxy ahora mismo!')
            # countdown
            for x in range(0,intervalo):
                minutosRestantes = intervalo - x
                print('Quedan ' + str(minutosRestantes) + ' minutos para el siguiente salto...')
                time.sleep(60)
        else:
            # try with another proxy
            print('El proxy no responde, probando con otro.')
            time.sleep(2)

def proxyJumpManual():
    seed = random.randint(0, 2238)
    f = open("proxyList.txt", "r")
    proxy = f.readlines()[seed]
    f.close
    proxyWithoutPort = proxy.split(':')

    if ServerStatus(proxyWithoutPort[0]):
            os.system('setproxy ' + proxy)
            print(proxy + 'es nuestro proxy ahora mismo!')
            print('Enter para saltar al siguiente nodo...')
            input()
            proxyJumpManual()
    else:
            # try with another proxy
            print('El proxy no responde, probando con otro.')
            time.sleep(2)
            proxyJumpManual()

def showCommandList():
    # help command content
    print('Lista comandos:')
    print('     help | ver lista de comandos.')
    print('     proxy.start [intervalo entre saltos(minutos)] | comienza a saltar por los servidores disponibles.')
    print('     proxy.start.manual | genera proxys aleatorios pero salta manualmente.')
    print('     proxy.none | quita el proxy establecido detiene la cola de saltos.')
    print('     proxy.set [proxyserverip:port] | establece manualmente el servidor proxy que deseas.')
    print('')

def start():
    res = input().split(' ')
    print('')
    if res[0] == 'proxy.start':
        if len(res) == 2:
            t = int(res[1])
            return proxyJump(t)
        else:
            print('Debes indicar el tiempo entre intervalos (en minutos).')
            return start()
    elif res[0] == 'proxy.start.manual':
        return proxyJumpManual()
    elif res[0] == 'proxy.none':
        os.system('setproxy none')
        return start()
    elif res[0] == 'proxy.set':
        if len(res) == 2:
            p = res[1]
            os.system('setproxy ' + p)
            return start()
        else:
            print('Debes introducir el servidor a continuación del comando: serverIP:PORT')
            return start()
    elif res[0] == 'help':
        showCommandList()
        return start()
    else:
        print('Revisa la sintaxis.')
        return start()

print('# # # # # #')
print('Bienvenido de nuevo Admin, usa el comando "help" para ver los comandos.')
print('...')
time.sleep(1)
start()
