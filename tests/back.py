#!/usr/bin/env python3

import zn
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from utils import label_map_util
from utils import visualization_utils as vis_util

import cv2
import time
import zmq, base64
import numpy as np
from PIL import Image
import io
import time

import datetime
import sys

MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = '/workspace/assets/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = '/workspace/models/research/object_detection/data/mscoco_label_map.pbtxt'

NUM_CLASSES = 90


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)



################ zmq

context = zmq.Context()
sock = context.socket(zmq.REP)
port = 5555
bind_address = "tcp://*:{}".format(port) # 'tcp://*:5555'
print("Subscribe Video at ", bind_address)
sock.bind(bind_address)

sumt = 0
sumq = 0
n = 0

def proces_img(image_np):

    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    return image_np



with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    image=np.zeros(shape=[10, 10, 3], dtype=np.uint8)
    proces_img(image)
    print('ready...')
    while True:
        try:
          image_in = zn.recv(sock)

          q0= datetime.datetime.now()
          image_out = proces_img(image_in)
          q1= (datetime.datetime.now() - q0).total_seconds()

          zn.send(sock, image_out)
          sumq += q1
          n += 1

          print('FPS={:.2f}'.format((1.0/(sumq/n))))

        except KeyboardInterrupt:
          sys.exit()
        except:
          print("error...")





