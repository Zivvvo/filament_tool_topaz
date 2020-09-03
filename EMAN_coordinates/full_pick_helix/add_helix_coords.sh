#!/bin/bash
for file in *.txt
do
	mv "$file" "${file/.txt/_helix_ptcl_coords.txt}"
done
