import vlc
import socket
ip="localhost"
#ip=input("Enter server output : ");
portsn=8080
portms=3997
ser_add=(ip,portms)

sock=socket.socket()
sock.connect(ser_add)
#start="hi"
#sock.send(start.encode())
songname="song.mp3"
loc="http://"+ip+":"+str(portsn)+"/"+songname
req=sock.recv(1024);
songname="song.mp3"
a=req.decode()
print(a)
if a:
    if(a[0:4]=="play"):
        p = vlc.MediaPlayer(loc)
        a=a.split();
        pos=float(a[1])
        p.set_position(pos)
        p.play()
    while(True):
        req=sock.recv(1024);
        a=req.decode()
        print(a)
        if a:
            if(a[0:4]=="play"):
                #global p
                a=a.split();
                if(a[1]=="0"):
                   p.stop()
                   p = vlc.MediaPlayer(loc)
                   p.play()
                else:
                   p.play()
            elif(a[0:4]=="paus"):
                #p = vlc.MediaPlayer(loc)
                p.pause()

            elif(a[0:4]=="fwrd"):
                po=p.get_position();
                p.stop()
                p = vlc.MediaPlayer(loc)
                p.play()
                p.set_position(po+0.01)        
            if(a[0:4]=="bwrd"):
                po=p.get_position();
                p.stop()
                p = vlc.MediaPlayer(loc)
                p.play()
                p.set_position(po-0.01)
            if(a[0:4]=="seek"):
                a=a.split()
                po=p.get_position();
                po=po+int(a[1])/100
                #p.set_position(po)
                
                p.stop()
                p = vlc.MediaPlayer(loc)
                p.play()
                p.set_position(po)
        else:
            break
