#!/bin/sh

#Input <Model folder> <environment folder> <target folder>

copy_resources()
{
    #cleanup old models 
    rm $TARGET_DIR/model.tflite

    #copy new models
    cp $MODEL_DIR/model_char.tflite $TARGET_DIR/model.tflite
}

push_package()
{
    C_DIR=$PWD
    cd $TARGET_DIR
    git add .
    git commit -m "updating new version"
    git push origin main
    cd $C_DIR
}

usage(){
    echo "Invalid Arguments!!"
    echo "Usage: ./setup.sh <Model Dir> <Target Dir>"
}

echo "Got $# arguments"

if [[ $# -lt 2 ]]
then
    usage
    exit 1
fi

MODEL_DIR=$1
TARGET_DIR=$2

copy_resources
push_package

echo "Successfully pushed the package to $TARGET_DIR"

