from tkinter import *
import os
import sys
import subprocess
import time
import shutil
import csv
import websockets
import asyncio

bakkesmod_folder = str(os.getenv('APPDATA') + '/bakkesmod/bakkesmod').replace('\\', '/')
print(bakkesmod_folder)

rcon_config = '/data/rcon_commands.cfg'
pw_config = '/cfg/config.cfg'
rcon_CMD = 'load_workshop'

config_file = os.path.join(os.path.abspath(os.getcwd()), 'cfg\\AMMconfig.csv')

async def main_loop(map_file, rcon_password, rcon_CMD):
    
    bakkesmod_server = 'ws://127.0.0.1:9002'
    
    try:
        async with websockets.connect(bakkesmod_server, timeout=.1) as websocket:
            
            await websocket.send('rcon_password ' + rcon_password)
            auth_status = await websocket.recv()
            assert auth_status == 'authyes'
            
            await websocket.send('rcon_refresh_allowed')

            print('RCON "{}" Enabled\n'.format(rcon_CMD))

            time.sleep(0.5)
            
            await websocket.send(str('{} "{}"'.format(rcon_CMD, map_file)))

            print('Workshop Map Loaded\n')

    except:
        print('MAP LOADING FAILED!!!')
        print('ROCKET LEAGUE MUST BE OPEN TO LOAD MAP.\n')
        
    return('Workshop Map Loaded')
    
def readFile(inFile):

    f = open(inFile, 'r')
    readTemp = ''
    for row in f:
        readTemp += row
    f.close()
    
    return(readTemp)

def fetchPassword(bakkesmod_folder):

    f3 = open(bakkesmod_folder + pw_config, 'r')
    passTemp = ''

    for row1 in f3:
        if 'rcon_password' in str(row1):
            rcon_password = row1.split(" ")[1]

    f3.close()
    
    print(rcon_password)

    return(rcon_password)

def checkRCON(bakkesmod_folder):
    
    if str(rcon_CMD) in str(readFile(bakkesmod_folder + rcon_config)):
        print('\nRCON "{}" Already Enabled\n'.format(rcon_CMD))
    else:
        f4 = open(bakkesmod_folder + rcon_config, 'a')
        f4.write("\n")
        f4.write(rcon_CMD)
        f4.close()
        print('\nRCON "{}" Added To Config\n'.format(rcon_CMD))

def getMapFile():
    
    tempFile = readFile(config_file).split("\n")

    map_file = tempFile[1] + "/" + tempFile[0].split("/")[-1].replace("udk", "upk")
    
    return(map_file)
    
checkRCON(bakkesmod_folder)
mapFile = getMapFile()

class Watcher(object):
    running = True
    refresh_delay_secs = 1

    def __init__(self, src, dest, autoLoad, mapFile, call_func_on_change=None, *args, **kwargs):
        self._cached_stamp = 0
        self.source = src
        self.destination = dest
        self.autoLoad = autoLoad
        self.mapFile = mapFile
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs

    def look(self):
        stamp = os.stat(self.source).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            
            print('File Changed.\n')
            
            if self.call_func_on_change is not None:
                self.call_func_on_change(self.source, self.destination, *self.args, **self.kwargs)
                print(self.autoLoad + "\n")
                if 'True' in str(self.autoLoad):
                    asyncio.run(main_loop(self.mapFile, fetchPassword(bakkesmod_folder), rcon_CMD))

                print('#########################################################')
                print('#               Monitoring For Changes...               #')
                print('#########################################################')
       
    def watch(self):
        while self.running: 
            try: 
                time.sleep(self.refresh_delay_secs) 
                self.look() 
            except KeyboardInterrupt: 
                print('\nDone')
                console.configure(text= 'Done')
                break 
            except FileNotFoundError:
                # Action on file not found
                pass
            except: 
                print('Unhandled error: %s' % sys.exc_info()[0])
                printString = 'Unhandled error: %s' % sys.exc_info()[0]
                console.configure(text= printString)

def custom_action(src, dest, text):
    print("Moving File...\n")

    # SOURCE FILE
    source = src
         
    # DESTINATION PATH
    destination = dest
    
    try:
        if os.path.isfile(destination) == True:
            idx = 0
            newDir = destination.split(".")[0] + "_Backup/"
            newDest = newDir + destination.split("/")[-1].rstrip() + "." + str(idx)
            while os.path.isfile(newDest) == True:
                newDest = newDir + destination.split("/")[-1].rstrip() + "." + str(idx)
                idx += 1
            else:
                if not os.path.exists(newDir):
                    os.makedirs(newDir)
                shutil.move(destination, newDest)
                print("Created Backup: " + newDest)
        shutil.copy(source, destination)
        print("\nFrom:  " + src)
        print("To:    " + destination)
        print("\nFile Copied Successfully.\n")
        print('---------------------------------------------------------\n')
         
    except shutil.SameFileError:
        print("Source And Destination Represents The Same File.\n")
         
    except PermissionError:
        print("Permission Denied.\n")
         
    except:
        print("Error Occurred While Copying File.\n")
        
# def readConfigFile():

    # with open('../cfg/AMMconfig.csv', 'r') as configFile:
          
        # readFile = csv.reader(configFile, delimiter="\n")

        # readtemp = ""

        # for row in readFile:
          # readtemp += str(row).lstrip("['").rstrip("']") + " \n"
                    
    # configFile.close()
    
    # readtemp = readtemp.split("\n")

    # source = readtemp[0].rstrip()

    # srcSplit = source.split("/")

    # inExt = "." + srcSplit[-1].split('.')[-1]

    # outExt = readtemp[2].lstrip("Output Extension: ")

    # destination = readtemp[1].rstrip() + "/" + srcSplit[-1].replace(inExt, outExt)


    
# OPEN CSV
with open(config_file, 'r') as configFile:
          
    readFile = csv.reader(configFile, delimiter="\n")

    readtemp = ""

    for row in readFile:
      readtemp += str(row).lstrip("['").rstrip("']") + " \n"
                
configFile.close()

readtemp = readtemp.split("\n")

source = readtemp[0].rstrip()

srcSplit = source.split("/")

inExt = "." + srcSplit[-1].split('.')[-1]

outExt = readtemp[2].lstrip("Output Extension: ")

destination = readtemp[1].rstrip() + "/" + srcSplit[-1].replace(inExt, outExt)

watcher = Watcher(source, destination, readtemp[3], mapFile, custom_action, text='')

watcher.watch()
