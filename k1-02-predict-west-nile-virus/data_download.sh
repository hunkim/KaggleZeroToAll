#!/bin/sh
competition="predict-west-nile-virus"
curr_dir=${PWD##*/}  
pushd $PWD
echo "Downlaoding $competition to $curr_dir ..."
cd ..; python3 kaggle_download.py $competition --destination $curr_dir
popd
