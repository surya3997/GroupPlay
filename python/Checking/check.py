# import winsound
import vlc
import time
import threading

path = "/media/surya/Base/Programs/PACKAGE/Acadamic/SEM 5/CN/repo/GroupPlay/python/Checking/Thalli.mp3"

with open(path, 'rb') as f:
    text = f.read()

check = 0

def player(s):
    checker = check
    parts = text[int((int(s) / 100) * len(text)):]
    print(parts)

    if parts:
        with open('./testcheck'+ '.mp3', 'wb') as output:
            output.write(parts)

        p = vlc.MediaPlayer("./testcheck" + ".mp3")
        p.play()
        time.sleep(1)
        while True:
            if p.is_playing():
                if checker != check:
                    p.stop()
            else:
                break


while True:
    s = input("percent : ")
    check += 1
    playerThread = threading.Thread(target=player, args=(s,))
    playerThread.daemon = True
    playerThread.start()

