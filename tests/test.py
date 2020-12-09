#!/usr/bin/env python3

import zn
import cv2
import time
import zmq, base64
import numpy as np
from PIL import Image
import io
import time
import struct
import datetime
import sys


dtype_map = { 0: np.uint8, 1: np.int8,
              2: np.uint16, 3: np.int16,
              4: np.int32,  5: np.float32,
              6: np.float64
            }

depth_map = { 2:  0, # uint8
              1:  1, # int8
              4:  2, # uint16
              3:  3, # int16
              5:  4, # int32
              11: 5, # float32
              12: 6  # float64
            }

################ zmq
print("Current libzmq version is %s" % zmq.zmq_version())

context = zmq.Context(io_threads=1)
sock = context.socket(zmq.REP)
bind_address = "tcp://*:5555"
print("Subscribe Video at ", bind_address)

sock.bind(bind_address)

i = 0
while True:

  #### receive image
  '''
  data = sock.recv()
  meta=struct.unpack('iiii', data)

  dtype = dtype_map[meta[0]]
  shape0 = meta[1]
  shape1 = meta[2]
  shape2 = meta[3]
  data = sock.recv(zmq.RCVMORE)
  frame = np.fromstring(data, dtype=dtype).reshape(shape0, shape1, shape2)
  '''
  frame = zn.recv(sock)

  # process
  frame2 = frame.copy()

  #### send image
  zn.send(sock, frame2)
  '''
  shape = frame2.shape
  meta=struct.pack('iiii', depth_map[frame2.dtype.num], shape0, shape1, shape2)
  sock.send(meta, zmq.SNDMORE)
  sock.send(frame2)
  '''








