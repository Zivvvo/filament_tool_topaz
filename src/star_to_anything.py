from utils.star_parser import star3_to_topaz

parser = star3_to_topaz("../../P15_J979.star", "/storage2/labusr/Zhe/P15_J979_filament_coords", [3,4], [3,4,7,8], 2.74, name_index = 2, optional_attributes = [-6,], header = "x_coord\ty_coord\tscore\n")

parser.parse()