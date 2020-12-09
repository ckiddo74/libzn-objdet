#!/usr/bin/env python3

import cv2
import time
import zmq, base64
import pickle
import numpy as np
import datetime
import zn


################ zmq


context = zmq.Context()
footage_socket = context.socket(zmq.REQ)
ip = "127.0.0.1"
port = 5555
target_address = "tcp://{}:{}".format(ip, port)
print("Publish Video to ", target_address)
footage_socket.connect(target_address)


(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

#cap = WebcamVideoStream(src=0).start()
cap = cv2.VideoCapture('/workspace/assets/male.mp4')

sum = 0
n = 0
while True:
    ret, frame = cap.read()

    if not ret:
        break

    t0 = datetime.datetime.now()

    zn.send(footage_socket, frame)

    frame2 = zn.recv(footage_socket)

    t1 = (datetime.datetime.now() - t0).total_seconds()

    sum += t1
    n += 1
    print('FPS={:.2f}'.format((1.0/(sum/n))))

    cv2.imshow('object detection', frame2)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        #cap.stop()
        break
