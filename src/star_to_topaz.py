import argparse
import os

def main():
    parser = argparse.ArgumentParser(description = "conversion of .star files to .txt topaz format")

    parser.add_argument("star_file", help = "the .star file to be converted")
    parser.add_argument("destination_path", help = "the location you want to store the topaz output file")
    parser.add_argument("pixel_size", help = "the pixel size in Angstroms of the micrographs", type=float)

    parser.add_argument("--default_threshold",nargs = "?", default = -6 ,help = "adding a default threshold value to all coordinates, this"
                                                      "is synonymous to topaz log-likelihood scores")
    parser.add_argument("--keep_path", default = 0,nargs = "?", help = "Set to 1 if you want to keep the relative path in the micrograph names of"
                                                         "the star file")
    parser.add_argument("--file_type", default = ".mrc",nargs = "?", help = "micrograph file type, by default this is set to .mrc")

    args = parser.parse_args()

    print(args)

    star_to_topaz(args.star_file, args.pixel_size, args.destination_path, args.star_file.replace(".star", ".txt"), args.default_threshold, bool(args.keep_path))


def star_to_topaz(filename, pixel_size, output_path, output_name, default_threshold, keep_path):
    file = open(filename, "r")
    Lines = file.readlines()
    o =  open(os.path.join(output_path,output_name), "w")
    for i in range(32, len(Lines)):
        parts = Lines[i].split()
        x = float(parts[2])-float(parts[5])/pixel_size
        y = float(parts[3])-float(parts[6])/pixel_size

        if not keep_path:
            o.write(os.path.basename(parts[1])+"\t"+str(x)+"\t"+str(y)+"\t"+str(default_threshold)+"\n")
        else:
            o.write(parts[1] + "\t" + str(x) + "\t" + str(y) + "\t" + str(default_threshold) + "\n")

if __name__ == "__main__":
    main()



