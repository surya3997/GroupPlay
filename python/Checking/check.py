# import winsound
import vlcs
import time
import threading

checkNew = ''
   
def player(parts):
    global checkNew
    checker = checkNew
    
    if parts:
        with open('./testcheck'+ '.mp3', 'wb') as output:
            output.write(parts)

        p = vlcs.MediaPlayer("./testcheck" + ".mp3")
        p.play()
        time.sleep(1)
        while True:
            if p.is_playing():
                if checker != checkNew:
                    p.stop()
            else:
                break



if __name__ == '__main__':
    path = "./Thalli.mp3"
    with open(path, 'rb') as f:
        text = f.read()
        
    check = 0
    
    def checkUpdate():
        global checkNew
        while True:
            checkNew = str(check)

    checkerThread = threading.Thread(target=checkUpdate)
    checkerThread.daemon = True
    checkerThread.start()

    while True:
        s = input("percent : ")
        check += 1
        parts = text[int((int(s) / 100) * len(text)):]
        
        playerThread = threading.Thread(target=player, args=(parts,))
        playerThread.daemon = True
        playerThread.start()

