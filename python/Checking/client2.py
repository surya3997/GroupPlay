import vlc
import time
import socket

host = 'localhost'
port = 3997

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)
sock.connect(server_address)

total = 4671603
count = 0
cnt = 0

try:
    while count < total:
        response = sock.recv(500000)
        print("in")
        
        count += len(response)
        cnt += 1
        if response:
            with open('./test' + str(cnt) + '.mp3','wb') as output:
                output.write(response)

            p = vlc.MediaPlayer("./test" + str(cnt) + ".mp3")
            p.play()
            time.sleep(1)
            while True:
               if p.is_playing():
                   pass
               else:
                   break

except:
    print("Data is not sent properly!")
finally:
    sock.close()

print("Program ended")
