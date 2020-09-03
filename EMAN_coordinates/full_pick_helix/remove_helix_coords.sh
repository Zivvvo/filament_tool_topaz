#!/bin/bash
for file in *_helix_ptcl_coords.txt
do
	mv "$file" "${file/_helix_ptcl_coords.txt/.txt}"
done
