#!/bin/bash

IMAGE_NAME="libzn-test"
CONTAINER_NAME="libzn-test-container"
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

IMAGE=`docker images 2> /dev/null | grep $IMAGE_NAME`

if [[ -z "$IMAGE" || "$1" == "--rebuild" || "$1" == "--reset" ]]; then
   if [[ "$1" == "--reset" ]]; then
      docker rmi -f $IMAGE_NAME
   fi
   docker build -t $IMAGE_NAME $ROOT_DIR
   STATUS=$?
   if [[ "$STATUS" != "0" ]]; then
     echo -e "\n=> Error building image '$IMAGE_NAME'!"
     exit $STATUS
   fi
   echo -e "Image built! Please run this script again to start the shell."
   exit 0
fi

CONTAINER=`docker ps -aq -f name=$CONTAINER_NAME`

#docker run --rm -ti --gpus all  -v $ROOT_DIR/assets/:/test/assets --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --net=host --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -w /test/assets $IMAGE_NAME /bin/bash

if [ ! $CONTAINER ]; then
   docker run --rm -ti -v $ROOT_DIR/assets/:/workspace/assets -v $ROOT_DIR/tests/:/workspace/tests --name $CONTAINER_NAME --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --net=host --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -w /workspace/tests $IMAGE_NAME /bin/bash
else
   echo "entering container: $CONTAINER_NAME"
   docker exec -ti $CONTAINER_NAME bash
fi


#docker run --rm -ti -v $ROOT_DIR/assets/:/test/assets -w /test/models/research/object_detection $IMAGE_NAME /bin/bash


