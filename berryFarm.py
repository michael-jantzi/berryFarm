import minescript
from minescript import entities
from minescript import player
import os
import time
import sys
import math

def stopMovement(): #stops all player movement and crouching
    minescript.player_press_sneak(False)
    minescript.player_press_left(False)
    minescript.player_press_right(False)
    minescript.player_press_forward(False)
    minescript.player_press_backward(False)

def tapSneak(): #crouches and uncrouches player
    minescript.player_press_sneak(True)
    minescript.player_press_sneak(False)

def harvestBerry(): #momentarily pressese player's use key
    minescript.player_press_use(True)
    minescript.player_press_use(False)

def getBlock(): #gets block player is standing in
    x, y, z = [p for p in player().position]
    if x < 0:
        x -= 1
    if z < 0:
        z -= 1
    return int(x), int(y), int(z)

def getPOS(): #exact player position
    x, y, z = [p for p in player().position]
    return x, y, z

def coordRadius(radius, playerCentered=True, coords=(0, 0, 0)): #generates list of blocks with specified radius around player or specified coordinates
    if playerCentered == False:#uses specified coords if playerCentered is False
        x, y, z = coords
    else: #uses players position by default
        x, y, z = getBlock()
    coordList = []
    for xval in range(x-radius, x+radius+1):
        for yval in range(y-radius, y+radius+1):
            for zval in range(z-radius, z+radius+1):
                coordList.append([xval, yval, zval])
    return coordList

def blockAttr(block, attribute): #gets the desired attribute of a block
    if block.find(f"{attribute}=") == -1:
        return "block doesnt have attribute"
    index = block.find(f"{attribute}=") + len(attribute) + 1
    end = block[index:].find("]") + (len(block[:index])) - 1
    value = block[index:end+1]
    return value

def getBlockType(block): #gets block type
    end = block.find("[")
    if end == -1:
        return block[10:]
    else:
        return block[10:end]

def lookAt(block, side="middle"): #makes player look at a side of the specified block
    # Get player position
    player_x, player_y, player_z = getPOS()
    
    # Add player eye height offset (player's eyes are approximately 1.62 blocks above their feet)
    player_y += 1.62
    
    # Block coordinates
    block_x, block_y, block_z = block
    
    # Calculate target position based on the side of the block
    target_x, target_y, target_z = block_x + 0.5, block_y + 0.5, block_z + 0.5
    
    # Adjust target position based on the side we want to look at
    if side == "top":
        target_y += 0.5
    elif side == "bottom":
        target_y -= 0.5
    elif side == "north":
        target_z -= 0.5
    elif side == "south":
        target_z += 0.5
    elif side == "east":
        target_x += 0.5
    elif side == "west":
        target_x -= 0.5
    # "middle" case doesn't need adjustment as we're already targeting the center
    
    # Calculate direction vector
    dx = target_x - player_x
    dy = target_y - player_y
    dz = target_z - player_z
    
    # Calculate yaw (horizontal rotation) in degrees
    yaw = -math.degrees(math.atan2(dx, dz))
    
    # Calculate pitch (vertical rotation) in degrees
    distance = math.sqrt(dx * dx + dz * dz)
    pitch = -math.degrees(math.atan2(dy, distance))
    
    # Set player rotation
    minescript.player_set_orientation(yaw, pitch)
    
    return True

def emptySlots(): #gets number of empty slots in player inventory
    return 36 - len(minescript.player_inventory())

def goTo(x, y, z, params=[]): #uses baritone to travel to specified coordinates, after changing specified baritone settings
    for param in params:
        if param[0] == "#":
            minescript.chat(param)
    minescript.chat(f"#goto {x} {y} {z}")

def main():
    state = "farm"
    while True:#main loop
        if state == "test":
            entities = minescript.entities()
            for entity in entities:
                minescript.echo(entity.name)
            break
        elif state == "farm":
            coordList = coordRadius(3)
            blockList = minescript.getblocklist(coordList)
            tapSneak()
            for block in range(0, len(blockList)):
                if getBlockType(blockList[block]) == "sweet_berry_bush" and int(blockAttr(blockList[block], "age")) == 3:
                    lookAt(coordList[block], "top")
                    minescript.player_press_use(True)
                    tapSneak()
                    continue
                    # harvestBerry()
                    #time.sleep(0.01)
            minescript.player_press_use(False)
            if emptySlots() <= 0:
                minescript.execute("sell handall")

            #state = "done"
        '''
        elif state == "wardenwalk":
            minescript.execute("warden")
            goTo(3, 62, 1, ["#set maxFallHeightNoWater 10"])
            state = "wardenwait"
            #state = "done"

        elif state == "wardenwait":
            minescript.chat("#eta")
            if


        elif state == "wardenattack":
            entities = minescript.entities()
            for entity in entities:
                if entity.name == "Warden":
                    x, y, z = entity.position
                    goTo(x, y, z)
        '''
        elif state == "done":
            break

main()