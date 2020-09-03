import argparse
import os

from utils.filament_fit import visualize_file

parser = argparse.ArgumentParser()

parser.add_argument("filename", help="The specified filament coordinate file")

parser.add_argument("--SAVE_PATH", help="If specified, will save the file to the specified location")

args = parser.parse_args()




