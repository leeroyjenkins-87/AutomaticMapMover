import sys
import os
import shutil
import websockets
import time
import asyncio
import csv

bakkesmod_folder = str(os.getenv('APPDATA') + '/bakkesmod/bakkesmod').replace('\\', '/')

rcon_config = '/data/rcon_commands.cfg'
pw_config = '/cfg/config.cfg'
rcon_CMD = 'load_workshop'

config_file = '../cfg/AMMconfig.csv'

async def main_loop(map_file, rcon_password, rcon_CMD):
    
    bakkesmod_server = 'ws://127.0.0.1:9002'
    
    try:
        async with websockets.connect(bakkesmod_server, timeout=.1) as websocket:
            
            await websocket.send('rcon_password ' + rcon_password)
            auth_status = await websocket.recv()
            assert auth_status == 'authyes'
            
            await websocket.send('rcon_refresh_allowed')

            time.sleep(0.5)
            
            await websocket.send(str('{} "{}"'.format(rcon_CMD, map_file)))

    except:
        await websocket.send('rcon_refresh_allowed')

        time.sleep(0.5)
        
        await websocket.send(str('{} "{}"'.format(rcon_CMD, map_file)))
        
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

    return(rcon_password)

def checkRCON(bakkesmod_folder):
    
    if str(rcon_CMD) in str(readFile(bakkesmod_folder + rcon_config)):
        print('RCON "{}" Already Enabled'.format(rcon_CMD))
    else:
        f4 = open(bakkesmod_folder + rcon_config, 'a')
        f4.write("\n")
        f4.write(rcon_CMD)
        f4.close()
        print('RCON "{}" Added To Config'.format(rcon_CMD))

def getMapFile():
    
    tempFile = readFile(config_file).split("\n")

    map_file = tempFile[1] + "/" + tempFile[0].split("/")[-1].replace("udk", "upk")
    
    return(map_file)
    
checkRCON(bakkesmod_folder)
asyncio.run(main_loop(getMapFile(), fetchPassword(bakkesmod_folder), rcon_CMD))
