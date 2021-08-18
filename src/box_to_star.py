import sys
sys.path.append(".")
from utils.parsers import box_to_star_bulk

template_file_path = "../template_files/star3.0template.txt"
box_to_star_bulk("/storage2/labusr/Zhe/P15_J979_clustered_output_100_eps", "P15_J979_clustered", template_file_path, "..")




