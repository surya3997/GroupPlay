import vlc
import time
import socket
import threading
import sys

host = 'localhost'
port = 3997
port1 = 3998

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address1 = (host, port1)

sock.connect(server_address)
sock1.connect(server_address1)

total = 4671603
count = 0
cnt = 0

counterUpdated = ''
def checkUpdate():
    global counterUpdated
    while True:
        received = sock1.recv(1)
        counterUpdated = received.decode()
        print(counterUpdated)

checkerUp = threading.Thread(target=checkUpdate)
checkerUp.daemon = True
checkerUp.start()

try:
    while True:
        # sock.send('1'.encode())
        # sock1.send('1'.encode())
        counterOld = counterUpdated
        response = sock.recv(500000)
        print("in")

        if cnt == 20:
            break
        if response:
            with open('./testing' + '.mp3','wb') as output:
                output.write(response)

            p = vlc.MediaPlayer("./testing" + ".mp3")
            try:
                p.play()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            time.sleep(1)
            while p.is_playing():
                if counterOld != counterUpdated:
                    # print(counterOld, ' ', counterUpdated)
                    p.stop()
        else:
            cnt += 1

    # counterOld = counterUpdated

    # while coun

except:
    print("Data is not received properly!")
finally:
    sock.close()
    sock1.close()

print("Program ended")
