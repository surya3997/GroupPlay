import socket

host = 'localhost'
port = 3997

# from pygame import mixer
import vlc
import time

##while True:
    # Create a TCP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (host, port)

sock.connect(server_address)

# message = input()

total = 4671603
count = 0
cnt = 0

try:
    while count < total:
        data = sock.recv(500000)
        print("in")
        response = data

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
                #    print("playing")
               else:
                #    print("Stopped")
                   break

except:
    print("Data is not sent properly!")
finally:
    sock.close()

print("Program ended")
