import matplotlib.pyplot as plt
import tensorflow as tf
import pathlib
import os
import cv2
from tensorflow import keras
from keras import layers
from keras.models import Sequential


class tensorData():
    def __init__(self, trainSplit):
        self.trainSplit = trainSplit
        data_dir = "test"
        data_dir = pathlib.Path(data_dir)
        image_count = len(list(data_dir.glob('*.jpg')))
        batch_size = 32
        img_height = 180
        img_width = 180



# Saving
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

# images input
def convert_to(image, output_directory, name):
    rows = image.shape[0]
    cols = image.shape[1]
    depth = 1

    filename = os.path.join(output_directory, name + '.tfrecords')
    print('Writing', filename)
    writer = tf.compat.v1.python_io.TFRecordWriter(filename)
    print(image.shape)
    image_raw = tf.io.encode_jpeg(image).numpy()
    example = tf.train.Example(features=tf.train.Features(feature={
        'height': _int64_feature(rows),
        'width': _int64_feature(cols),
        'depth': _int64_feature(depth),
        'image_raw': _bytes_feature(image_raw)}))
    writer.write(example.SerializeToString())

def read_image(file_name, images_path):
    image = cv2.imread(images_path +"\\"+ file_name)
    return image

def get_name(img_name):
    remove_ext = img_name.split(".")[0]
    name = remove_ext.split("_")
    return name[0]

images_path = "training"
image_list = os.listdir(images_path)
for img_name in image_list:
    tfrec_name = get_name(img_name)
    print(tfrec_name)
    img_data = read_image(img_name, images_path)
    convert_to(img_data, "data", tfrec_name+"humans")


# Loading:
PHOTO_FILENAMES = tf.io.gfile.glob(str('data/*.tfrecords'))

IMAGE_SIZE = [256, 256]

def decode_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = (tf.cast(image, tf.float32) / 127.5) - 1
    # Changed this from reshape 
    # Consider reshape if all your images have the same shape
    image = tf.image.resize(image, IMAGE_SIZE)
    return image

def read_tfrecord(example):
    tfrecord_format = {
    'height': tf.io.FixedLenFeature([], tf.int64),
    'width': tf.io.FixedLenFeature([], tf.int64),
    'depth': tf.io.FixedLenFeature([], tf.int64),
    'image_raw': tf.io.FixedLenFeature([], tf.string),
    }
    example = tf.io.parse_single_example(example, tfrecord_format)
    image = decode_image(example['image_raw'])
    return image

def load_dataset(filenames, labeled=True, ordered=False):
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(read_tfrecord, num_parallel_calls=tf.data.AUTOTUNE)
    return dataset

photo_ds = load_dataset(PHOTO_FILENAMES, labeled=False).batch(1)
example_photo = next(iter(photo_ds))