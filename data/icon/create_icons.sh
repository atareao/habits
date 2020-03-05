#!/bin/bash
for afile in $(ls scalable/*.svg)
do
    filename="${afile##*/}"
    echo $filename
    filename="${filename/\.svg/.png}"
    for i in 8 16 20 22 24 28 32 36 40 48 64 72 96 128 192 256 480 512 1024
    do
        directory="$i"x"$i"
        mkdir $directory
        inkscape -z -e "$directory"/"$filename" -w $i -h $i $afile
    done
done
