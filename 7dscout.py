#!/usr/bin/python3
"""
7 Days to Die TTS decoder
Copyright (C) 2017 Liam Brandt <brandt.liam@gmail.com>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Modified by ZZTong to analyze a POI instead of display one. That
makes this a derivitive work, so with respect to Liam's wishes this
variation is also protected by the GNU GPL 3.
"""

import struct
import time
import random
import sys
import json
import os

def unpack(bin_file, data_type, length_arg=0):
    #integer or unsigned integer
    if data_type == "i" or data_type == "I":
        return int(struct.unpack(data_type, bin_file.read(4))[0])
    #short or unsigned short
    elif data_type == "h" or data_type == "H":
        return int(struct.unpack(data_type, bin_file.read(2))[0])
    #string
    elif data_type == "s":
        return struct.unpack(str(length_arg) + data_type, bin_file.read(length_arg))[0]
    #char
    elif data_type == "c":
        return struct.unpack(data_type, bin_file.read(1))[0]
    #byte or unsigned byte
    elif data_type == "b" or data_type == "B":
        return int(struct.unpack(data_type, bin_file.read(1))[0])


def main():
    # The name of the POI to analyze should be the command line argument.
    # If the name comes with an extension, strip that off. That can
    # happen if somebody is trying to run the tool across a collection
    # (directory) of POI files. For instance... 7loot.py *.xml
    if ( len( sys.argv ) != 2 ):
        print( "Usage: poiscout <Directory>" )
        quit()

    dirName = sys.argv[1]
    print( "Directory " + dirName )

    outputBlockSummaryFileName = "7dscout-blocks.csv"
    outputLootSummaryFileName = "7dscout-loot.csv"

    outputFileBlocks = open( outputBlockSummaryFileName, "w" )
    outputFileBlocks.write( "POI,Block,Count\n" )

    outputFileLoot = open( outputLootSummaryFileName, "w" )
    outputFileLoot.write( "POI,Block,Count,Description\n" )

    #######################################################################################
    # Get the list of Loot Blocks and their Values
    # Value isn't used. That was a half-baked idea of trying to compute a POI "Loot Score".
    #######################################################################################

    with open( "loot.json" ) as f:
        data = f.read()

    lootDictionary = json.loads( data )

    #######################################################################################
    # Loop through each POI in the specified directory...
    #######################################################################################

    for fileName in os.listdir( dirName ):
        if ( fileName.endswith( ".xml" ) ):
            print( "File: " + fileName )

            poiName = dirName + "/" + fileName.rsplit( "." )[0]
            size = len( fileName )
            shortName = fileName[:size-4]
    
            blocksFileName = poiName + ".blocks.nim"
            ttsFileName = poiName + ".tts"

            #######################################################################################
            # BLOCKS.NIM File
            #######################################################################################

            blockDesc = {}
            bin_file = open(blocksFileName, "rb")

            versionBlocks = unpack( bin_file, "I" )
            numBlockIDs = unpack( bin_file, "I" )

            for currBlock in range( numBlockIDs ):
                blockID = unpack( bin_file, "I" )
                blockID = blockID & 2047

                lenName = unpack( bin_file, "B" )

                myBytes = bytearray()
                for currLetter in range( lenName ):
                    myBytes.append( int.from_bytes( unpack( bin_file, "c" ), "big" ) )

                blockName = myBytes.decode()
                blockDesc[ blockID ] = blockName

            # Debugging...
            #print( blockDesc )

            bin_file.close()

            #######################################################################################
            # TTS File
            #######################################################################################

            bin_file = open(ttsFileName, "rb")

            prefab = {}
            blockCounts = [0] * 2048

            prefab["header"] = unpack(bin_file, "s", 4)
            prefab["version"] = unpack(bin_file, "I")
            prefab["size_x"] = unpack(bin_file, "H")
            prefab["size_y"] = unpack(bin_file, "H")
            prefab["size_z"] = unpack(bin_file, "H")

            prefab["layers"] = []

            for layer_index in range(prefab["size_z"]):
                prefab["layers"].append([])
                for row_index in range(prefab["size_y"]):
                    prefab["layers"][layer_index].append([])
                    for block_index in range(prefab["size_x"]):
                        prefab["layers"][layer_index][row_index].append(None)
                        value = unpack(bin_file, "I")
                        #get rid of flags, block id can only be less than 2048
                        block_id = value & 2047
                        flags = value >> 11

                        prefab["layers"][layer_index][row_index][block_index] = block_id
                        blockCounts[ block_id ] += 1

            bin_file.close()

            #######################################################################################
            # Block Summary...
            #######################################################################################

            for x in range( len( blockCounts ) ):
                if ( blockCounts[x] != 0 ):
                    outputFileBlocks.write( shortName + "," +  blockDesc[x] + "," + str( blockCounts[x] ) + "\n" )

            #######################################################################################
            # Loot Summary...
            #######################################################################################

            for x in range( len( blockCounts ) ):
                if ( blockCounts[x] != 0 ):
                    if blockDesc[x] in lootDictionary:
                        outputFileLoot.write( shortName + "," +  blockDesc[x] + "," + str( blockCounts[x] ) + "," + lootDictionary[blockDesc[x]] + "\n" )

    outputFileBlocks.close()
    outputFileLoot.close()

#######################################################################################
# Driver
#######################################################################################

main()
