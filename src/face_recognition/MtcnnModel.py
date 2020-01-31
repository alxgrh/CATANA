# -*- coding: utf-8 -*-

'''
Model file module, so that model files are only loaded once when imported
'''

import os
import sys
import tensorflow as tf

from facenet.src import facenet
from facenet.src.align import detect_face


session = None
graph = None

# Actual models used for face detection
pnet = None
rnet = None
onet = None


graph = tf.Graph()
session = tf.compat.v1.Session(graph=graph) #config=tf.ConfigProto(inter_op_parallelism_threads=24, intra_op_parallelism_threads=24))
with graph.as_default():
    with session.as_default():
        pnet, rnet, onet = detect_face.create_mtcnn(session, None)
graph.finalize()
