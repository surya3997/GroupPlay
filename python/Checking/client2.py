import vlc
import time
import socket
import threading

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
    while True:
        counterUpdated = sock1.recv(5).decode()

checkerUp = threading.Thread(target=checkUpdate)
checkerUp.daemon = True
checkerUp.start()

try:
    while True:
        # sock.send('1'.encode())
        # sock1.send('1'.encode())
        response = sock.recv(500000)
        print("in")
        
        # count += len(response)
        if cnt == 20:
            break
        if response:
            cntr = sock1.recv(10000)
            cntr = cntr.decode()
            with open('./testing' + '.mp3','wb') as output:
                output.write(response)

            p = vlc.MediaPlayer("./testing" + ".mp3")
            p.play()
            time.sleep(1)
            while True:
               if p.is_playing():
                    cnter = sock1.recv(10000)
                    cnter = cnter.decode()

                    if cnter != cntr:
                        p.stop()
               else:
                   break
        else:
            cnt += 1

except:
    print("Data is not received properly!")
finally:
    sock.close()
    sock1.close()

print("Program ended")
