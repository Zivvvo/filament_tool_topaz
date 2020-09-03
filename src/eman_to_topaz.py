import os
import sys
sys.path.append(".")

args = sys.argv

if (len(args)!=3):
    print ("Usage: python eman_to_topaz.py eman_coord_path topaz_coord_path")
    exit(1)

os.chdir("..")
path_to_EMAN = args[1]
path_to_topaz = args[2]

from utils.parsers import parse_EMAN_coordinates

parse_EMAN_coordinates(path_to_EMAN, path_to_topaz)
print("Successfully transcribed EMAN coordinate files into Topaz coordinate files at "+str(args[2]))


exit(0)
