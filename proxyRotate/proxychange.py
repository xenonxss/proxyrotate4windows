from ast import For
from random import randint
from time import sleep
from os import system

def color_print(color, msg):

    from colorama import Fore

    if color == 'red':
        print(Fore.RED, msg, Fore.WHITE, sep='')
    elif color == 'green':
        print(Fore.GREEN, msg, Fore.WHITE, sep='')
    elif color == 'yellow':
        print(Fore.YELLOW, msg, Fore.WHITE, sep='')
    else:
        print(msg)

def server_status(server):

    # Check if we can ping the server
    response = system("ping -c 1 " + server)
    
    if response == 0:
        return True
    else:
        return False

def proxy_jump(intervalo):

    color_print('green', '\n[+]Comenzando')

    while True:

        # Generate proxy
        seed = randint(0, 2238)

        f = open("proxyList.txt", "r")
        proxy = f.readlines()[seed]
        f.close

        proxyWithoutPort = proxy.split(':')

        # Check if generated proxy is working and execute it
        if server_status(proxyWithoutPort[0]):

            system('setproxy ' + proxy)
            color_print('green', '[+]' + proxy + 'es nuestro proxy ahora mismo!')

            # Countdown
            for x in range(0,intervalo):
                minutosRestantes = intervalo - x
                color_print('yellow', '[i]Quedan ' + str(minutosRestantes) + ' minutos para el siguiente salto...' )
                sleep(60)
        else:
            # try with another proxy
            color_print('red', '[-]El proxy no responde, probando con otro.')
            sleep(2)

def proxyJumpManual():
    seed = randint(0, 2238)
    f = open("proxyList.txt", "r")
    proxy = f.readlines()[seed]
    f.close
    proxyWithoutPort = proxy.split(':')

    if server_status(proxyWithoutPort[0]):
            system('setproxy ' + proxy)
            color_print('green', '[+]' + proxy + 'es nuestro proxy ahora mismo!')
            color_print('yellow','[i]Enter para saltar al siguiente nodo...')
            input()
            proxyJumpManual()
    else:
            # try with another proxy
            color_print('red', 'El proxy no responde, probando con otro.')
            sleep(2)
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
            return proxy_jump(t)
        else:
            color_print('red', '[!]Debes indicar el tiempo entre intervalos (en minutos).')
            return start()
    elif res[0] == 'proxy.start.manual':
        return proxyJumpManual()
    elif res[0] == 'proxy.none':
        system('setproxy none')
        return start()
    elif res[0] == 'proxy.set':
        if len(res) == 2:
            p = res[1]
            system('setproxy ' + p)
            return start()
        else:
            color_print('red', '[!]Debes introducir el servidor a continuación del comando: serverIP:PORT')
            return start()
    elif res[0] == 'help':
        showCommandList()
        return start()
    else:
        color_print('red', '[!]Revisa la sintaxis.')
        return start()

color_print('green','\n[+]Bienvenido de nuevo Admin, usa el comando "help" para ver los comandos.')
start()
