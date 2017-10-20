# import winsound

path = "./Thalli_Pogathey(160kbps)-StarMusiQ.Com.mp3"

with open(path, 'rb') as f:
    text = f.read()

parts = text[int(len(text) / 2):]

with open('./test.mp3','wb') as output:
    output.write(parts)

# from pygame import mixer # Load the required library

# mixer.init()
# mixer.music.load(path)
# mixer.music.play()


import playsound
##playsound.playsound("./test.mp3", True)
