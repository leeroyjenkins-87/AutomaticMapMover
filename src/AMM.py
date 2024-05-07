import os
import sys
import subprocess
import time
import shutil
import csv
from tkinter import *
from tkinter import filedialog

configFile = 'cfg/AMMconfig.csv'

def browseFiles():

    if runScript["state"] == 'disabled':
        stopThis()

    tempSrc = srcFile.cget("text")

    if tempSrc == "Select a File":
        srcInitDir = "/"
    else:
        tempStr = tempSrc.split("/")
        srcInitDir = tempSrc.rstrip(str("/" + tempStr[-1]))
        
    
    filename = filedialog.askopenfilename(initialdir = srcInitDir, title = "Select a File", filetypes = (("Map files", "*.udk*"), ("all files", "*.*")))

    # CHANGE LABEL CONTENTS
    srcFile.configure(text= filename)
    
    inExtText.config(state=NORMAL)
    inExtText.delete("1.0", END)
    tempExt1 = filename.split(".")
    inExtText.insert(END, str('.' + tempExt1[1]))
    inExtText.config(state=DISABLED)

def browseFolders():

    if runScript["state"] == 'disabled':
        stopThis()

    tempDest = destFile.cget("text")

    if tempDest == "Select a Folder":
        initDir = "/"
    else:
        initDir = tempDest
    
    foldername = filedialog.askdirectory(initialdir = initDir, title = "Select a Folder")
          
    # CHANGE LABEL CONTENTS
    destFile.configure(text= foldername)

def createConfig():

    readTemp = ''

    tempList = [srcFile.cget("text"), 
                destFile.cget("text"), 
                str("Output Extension: " + extText.get("1.0",'end-1c')),
                str("AutoLoad: " + autoVar.get())]
                
    for temp in tempList:
        readTemp += temp + "\n"

    readTemp = readTemp.rstrip('\n')

    f = open(configFile, 'w')
    f.writelines(readTemp)
    f.close()

def runThis():

    runScript.config(relief=SUNKEN)
    runScript.config(state=DISABLED)
    
    srcExplore.config(relief=SUNKEN)
    srcExplore.config(state=DISABLED)
    
    destExplore.config(relief=SUNKEN)
    destExplore.config(state=DISABLED)
    
    extText.config(state=DISABLED)
    extText['bg'] = 'grey91'
    extText['fg'] = 'black'
    
    autoLoad.config(state=DISABLED)
    
    stopScript.config(relief=RAISED)
    stopScript.config(state=NORMAL)
  
    createConfig()
    
    p = subprocess.Popen(str(os.path.abspath(os.getcwd())).replace('\\', '/') + '/subprocess/AMMwatcher.exe', shell=True)
    root.setvar(name ="runPID", value = p.pid)

def stopThis():

    runScript.config(relief=RAISED)
    runScript.config(state=NORMAL)

    srcExplore.config(relief=RAISED)
    srcExplore.config(state=NORMAL)
    
    destExplore.config(relief=RAISED)
    destExplore.config(state=NORMAL)
    
    extText.config(state=NORMAL)
    extText['bg'] = 'white'
    extText['fg'] = 'blue'
    
    autoLoad.config(state=NORMAL)
    
    stopScript.config(relief=SUNKEN)
    stopScript.config(state=DISABLED)
    
    print('\nStopping Monitoring Processes...')
    
    subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=root.getvar(name ="runPID")))
    
    print('\nMonitoring Has Been Stopped.\n')
    
    
############################################################################################################
#          CREATE ROOT WINDOW
############################################################################################################
root = Tk()
 
# WINDOW TITLE
root.title("LeeroyJenkins0G's Automatic Map Mover")

# SET WINDOW WIDTH X HEIGHT
root.geometry('755x307')

# VARIABLES FOR GUI
src = Label(root, text = "Source File:", font=('Segoe UI Semibold', 9))
srcFile = Label(root, text = "Select Source File...", width = 90, height = 1, fg = "blue", bg = "white")
srcExplore = Button(root, text = "Browse Files", font=('Segoe UI Semibold', 9), command = browseFiles)

dest = Label(root, text = "Destination Folder:", font=('Segoe UI Semibold', 9))
destFile = Label(root, text = "Select Destination Folder..", width = 90, height = 1, fg = "blue", bg = "white")
destExplore = Button(root, text = "Browse Folders", font=('Segoe UI Semibold', 9), command = browseFolders)

extFrame = Frame(root)

inLabel = Label(extFrame, text = "In Extension:", font=('Segoe UI Semibold', 9))
inExtText = Text(extFrame, width = 20, height = 1, bg = "grey91", state=DISABLED)

outLabel = Label(extFrame, text = "Out Extension:", font=('Segoe UI Semibold', 9), fg = "blue")
extText = Text(extFrame, height = 1, width = 20, bg = "white")

autoVar = StringVar(root, value='False')
autoLoad = Checkbutton(root, text='AutoLoad Map in Rocket League', font=('Segoe UI Semibold', 9), var = autoVar, onvalue = 'True', offvalue = 'False')

buttFrame = Frame(root)
runScript = Button(buttFrame, text = "Run", width = 15, bg = "lime green", font=('Segoe UI Semibold', 9), command = runThis)
stopScript = Button(buttFrame, text = "Stop", width = 15, bg = "red", font=('Segoe UI Semibold', 9), relief=SUNKEN, state=DISABLED, command = stopThis)

runPID = StringVar(root, name ="runPID")

# CHECK IF CONFIG FILE EXISTS -> SET PRESETS
if os.path.isfile(configFile) == True:
    f = open(configFile, 'r')
    templine = ''
    for row in f:
        templine += row

    line = templine.split("\n")

    srcFile.configure(text= line[0])
    destFile.configure(text= line[1])
    extText.insert(INSERT, line[2].lstrip("Output Extension: "))
    tempExt = line[0].split(".")
    inExtText.config(state=NORMAL)
    inExtText.insert(INSERT, str('.' + tempExt[1]))
    inExtText.config(state=DISABLED)
    
else:
    extText.insert(INSERT, '.upk')


# PLACE OBJECTS IN WINDOW
src.grid(column = 1, row = 1, sticky=W, pady = (20, 0), padx = (10, 5))
srcFile.grid(column = 1, row = 2, sticky=W, padx = (10, 5))
srcExplore.grid(column = 2, row = 2, padx = (5, 10))

dest.grid(column = 1, row = 3, sticky=W, pady = (20, 0), padx = (10, 5))
destFile.grid(column = 1, row = 4, sticky=W, padx = (10, 5))
destExplore.grid(column = 2, row = 4, padx = (5, 10))

extFrame.grid(column = 1, row = 5, sticky=W, padx = 10, pady = 30)

inLabel.pack(side = LEFT, padx = (0, 10))
inExtText.pack(side = LEFT, padx = (0, 10))

extText.pack(side = RIGHT)
outLabel.pack(side = RIGHT, padx = (120, 10))

autoLoad.grid(column = 1, row = 6, sticky=W, padx = (10, 10), pady = (0, 30))

buttFrame.grid(column = 1, row = 7, sticky=W, padx = 10, pady = 0)
runScript.pack(side = LEFT)
stopScript.pack(side = RIGHT)

# EXECUTE TKINTER
root.mainloop()