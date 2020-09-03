import os
import sys
sys.path.append(".")

args = sys.argv
if (len(args)!=3):
    print ("Usage: python eman_to_topaz.py eman_coord_path topaz_coord_path")
    exit(1)

from utils.parsers import parse_topaz_coordinates

parse_topaz_coordinates(args[1], args[2])

print("Successfully transcribed Topaz coordinate files into filament mode coordinate files at "+str(args[2]))
exit(0)
