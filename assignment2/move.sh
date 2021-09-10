#!/bin/bash

# Ensure that the correct number of command-line arguments are supplied. 
if [[ "$#" != [2-3] ]] 
then
    echo "[ERROR] Unexpected number of arguments!"
    echo " - expected usage: move \<source directory\> \<target directory\> <file extension (OPTIONAL)>"
    exit 1
fi

src=$1
dst=$2
# ext defaults to * if 3rd arg is not supplied (i.e all files and folders are moved by default)
ext=${3:-*}

# Ensure that both of the supplied directories exist. 
if [ ! -d $src ]
then
    echo [ERROR] $src does not exist in your filesystem!
    exit 1
fi

# Check if the destination folder exists
if [ ! -d $dst ]
then
    echo "Directory $dst does not exist in your filesystem."
    read -p " - Do you wish to create this directory? (Y/N): " ans
    case $ans in
        [Yy]* ) echo You choose yes ;;
        [Nn]* ) exit 1 ;;
        * ) exit 1;; # Should exit regardless
    esac

    read -p "Do you with to append the time at the end of the new directory? (Y/N): " ans
    case $ans in
        [Yy]* ) dst+="_$(date '+%Y-%m-%d-%H-%M')" ;;
        [Nn]* ) ;;
        * ) ;;
    esac
    mkdir $dst
fi

mv $src/*$ext $dst
