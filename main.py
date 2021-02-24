import tkinter.font as TkFont
import tkinter
import threading
import math
from time import time, sleep
from sys import exit
from pynput.keyboard import Listener
from pynput import *

def startimer():
    global timer;global splitTime;global startime;global splitBeg;global currentSplit;global start;global labels;global timeLabel;global tk;global timerready;global going;global saving
    timer = 0
    splitTime = 0
    timerready = True
    innerSplit = 0
    splitTimes = [0.0] * len(config["splits"])
    start.destroy()
    for i in range(len(labels)):
        labels[i].place(relx = 0, rely = 0.15*i, relwidth = 1, relheight = 0.15)
    timeLabel.place(relx = 0, rely = 0.75, relwidth = 1, relheight = 0.25)
    timeLabel.config(text = "0 : 00 : 00.00\nPress space to start")
    tk.update()
    while not going:
        tk.update()
    startime = time()
    splitBeg = startime
    while True:
        timer = time()-startime
        splitTime = time()-splitBeg
        try:
            splitTimes[innerSplit] = splitTime
        except:
            going = False
            currentSplit -= 1
        if currentSplit != innerSplit:
            innerSplit = currentSplit
            splitBeg = time()
        sleep(0.015)
        strtime = timeToString(timer)
        if True:
            top = -0.15*max(0, currentSplit-4)
            #for i in range(max(0, currentSplit-5), max(currentSplit, min(5, len(config["splits"])))):
            for i in range(0, len(config["splits"])):
                labels[i].place(relx = 0, rely = top)
                if i == currentSplit:
                    labels[i].config(text = config["splits"][i] + ": " + timeToString(splitTimes[i]), bg = "gray")
                else:
                    labels[i].config(text = config["splits"][i] + ": " + timeToString(splitTimes[i]), bg = tk.cget('bg'))
                top += 0.15
        timeLabel.config(text = strtime + "\nPress space to move on\nto the next split")
        tk.update()
        if going == False:
            if saving:
                if timer < dynamic["best"]:
                    dynamic["best"] = timer
                    dynamic["bestSplits"] = splitTimes
                    save = open("dynamicSave.txt", "w")
                    save.write(str(dynamic))
                    save.close()
                for i in range(len(splitTimes)):
                    if splitTimes[i] > dynamic["bestSplitsE"][i]:
                        dynamic["bestSplitsE"][i] = splitTimes[i]
            break
        
            
def toDict(i):
    lines = i.split("\n")
    for i in range(len(lines)-1):
        lines[i] = lines[i].split(":")
    toreturn = {}
    for i in range(len(lines)-1):
        try:
            toreturn[lines[i][0]] = eval(lines[i][1])
        except:
            toreturn[lines[i][0]] = lines[i][1]
    return toreturn

def timeToString(i):
    return str(math.floor(i/3600)) + " : " + str(math.floor(i/60)%60).zfill(2) + " : " + str(math.floor(i)%60).zfill(2) + "." + (str(round(i%1, 2)).split(".")[1])

timer = None
splitTime = None
splitBeg = None
startime = None
saving = True
currentSplit = -1
going = False
timerready = False
configFile = open("config.txt", "r")
configText = configFile.read()
configFile.close()
config = toDict(configText)
dynamicFile = open("dynamicSave.txt", "r")
dynamicText = dynamicFile.read()
dynamicFile.close()
dynamic = eval(dynamicText)
tk = tkinter.Tk()
tk.title("PySplits")
tk.geometry("250x400")
tk.resizable(1, 1)
tk.wm_attributes("-topmost", True)
start = tkinter.Button(tk, text = "Press to ready timer", command = startimer)
start.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
labels = [None] * len(config["splits"])
for i in range(len(labels)):
    labels[i] = tkinter.Label(tk)
timeLabel = tkinter.Label(tk)

def onPress(key):
    global going;global timerready;global currentSplit
    if(str(key) == config["moveOnKey"] and timerready):
        going = True
        currentSplit += 1;
        if currentSplit > len(config["splits"]):
            going = False
    if(str(key) == "Key.delete" and timerready):
        going = True
        currentSplit += 1;
        saving = False
        if currentSplit > len(config["splits"]):
            going = False

def onRelease(key):
    pass
        
def liste(e = None):
    Listener(on_press = onPress, on_release = onRelease).start()

e = threading.Thread(target = liste)
e.run()
