#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import numpy
import string
import random
import argparse
import tensorflow as tf
import tensorflow.keras as keras
import datetime
import numpy as np

#constants
dropout_factor = 0.15
model_pref = "Models"

import codecs

#encode
def encode_img_name(img_name):
    hex_string = codecs.encode(img_name.encode(), "hex")
    hex_string = hex_string.decode("ASCII")
    return hex_string

#decode
def decode_img_name(hex_img_name):
    bytes_object = bytes.fromhex(hex_img_name)
    ascii_string = bytes_object.decode("ASCII")
    return ascii_string

# Build a Keras model given some parameters
def create_model(captcha_length, captcha_num_symbols, input_shape, model_depth=5, module_size=2):
  input_tensor = keras.Input(input_shape)
  x = input_tensor
  for i, module_length in enumerate([module_size] * model_depth):
      for j in range(module_length):
          x = keras.layers.Conv2D(32*2**min(i, 3), kernel_size=3, padding='same', kernel_initializer='he_uniform')(x)
          x = keras.layers.BatchNormalization()(x)
          x = keras.layers.Activation('relu')(x)
         # x = keras.layers.Dropout(dropout_factor)(x)
      x = keras.layers.MaxPooling2D(2)(x)

  x = keras.layers.Flatten()(x)

  x = keras.layers.Dropout(dropout_factor)(x)

  x = keras.layers.Dense(captcha_length, activation='softmax', name='cap_length')(x)
  model = keras.Model(inputs=input_tensor, outputs=[x])

  return model

# A Sequence represents a dataset for training in Keras
# In this case, we have a folder full of images
# Elements of a Sequence are *batches* of images, of some size batch_size
class ImageSequence(keras.utils.Sequence):
    def __init__(self, directory_name, batch_size, captcha_length, captcha_symbols, captcha_width, captcha_height):
        self.directory_name = directory_name
        self.batch_size = batch_size
        self.captcha_length = captcha_length
        self.captcha_symbols = captcha_symbols
        self.captcha_width = captcha_width
        self.captcha_height = captcha_height

        file_list = os.listdir(self.directory_name)
        self.files = dict(zip(map(lambda x: x.split('.')[0], file_list), file_list))
        self.used_files = []
        self.count = len(file_list)

    def __len__(self):
        return int(numpy.floor(self.count / self.batch_size))

    def __getitem__(self, idx):
        #if (self.X is not None) and (self.y is not None):
        #    return self.X, self.y

        X = numpy.zeros((self.batch_size, self.captcha_height, self.captcha_width, 3), dtype=numpy.float32)
        #y = numpy.zeros((self.batch_size, len(self.captcha_symbols) * self.captcha_length), dtype=numpy.uint8)
        y = numpy.zeros((self.batch_size, self.captcha_length), dtype=numpy.uint8)

        for i in range(self.batch_size):
            if len(self.files.keys()) == 0:
                break
            random_image_label = random.choice(list(self.files.keys()))
            random_image_file = self.files[random_image_label]

            # We've used this image now, so we can't repeat it in this iteration
            self.used_files.append(self.files.pop(random_image_label))

            # We have to scale the input pixel values to the range [0, 1] for
            # Keras so we divide by 255 since the image is 8-bit RGB
            raw_data = cv2.imread(os.path.join(self.directory_name, random_image_file))
            rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
            processed_data = numpy.array(rgb_data) / 255.0
            X[i] = processed_data

            # We have a little hack here - we save captchas as TEXT_num.png if there is more than one captcha with the text "TEXT"
            # So the real label should have the "_num" stripped out.

            random_image_label = random_image_label.split('_')[0]
            random_image_label = decode_img_name(random_image_label)
            
            #Here we add '.' if the captcha length is shorter than max captcha length
            # if len(random_image_label) != self.captcha_length:
            #     random_image_label + '.'*(self.captcha_length - len(random_image_label))
            y[i, len(random_image_label)-1] = 1

        return X, y

def saveTfLiteModel(model, model_name="tfl_model"):
    tf_converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = tf_converter.convert()
    destModel = os.path.join(model_name, "model_len.tflite")
    with open(destModel, "wb") as tfl_model:
        tfl_model.write(tflite_model)

class SaveTfLite(keras.callbacks.Callback):
    def __init__(self, model_name):
        self.model_name = model_name

    def on_epoch_end(self, batch, logs={}):
        saveTfLiteModel(self.model, self.model_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', help='Width of captcha image', type=int)
    parser.add_argument('--height', help='Height of captcha image', type=int)
    parser.add_argument('--length', help='Length of captchas in characters', type=int)
    parser.add_argument('--batch-size', help='How many images in training captcha batches', type=int)
    parser.add_argument('--train-dataset', help='Where to look for the training image dataset', type=str)
    parser.add_argument('--validate-dataset', help='Where to look for the validation image dataset', type=str)
    parser.add_argument('--output-model-name', help='Where to save the trained model', type=str)
    parser.add_argument('--input-model', help='Where to look for the input model to continue training', type=str)
    parser.add_argument('--epochs', help='How many training epochs to run', type=int)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.width is None:
        print("Please specify the captcha image width")
        exit(1)

    if args.height is None:
        print("Please specify the captcha image height")
        exit(1)

    if args.length is None:
        print("Please specify the captcha length")
        exit(1)

    if args.batch_size is None:
        print("Please specify the training batch size")
        exit(1)

    if args.epochs is None:
        print("Please specify the number of training epochs to run")
        exit(1)

    if args.train_dataset is None:
        print("Please specify the path to the training data set")
        exit(1)

    if args.validate_dataset is None:
        print("Please specify the path to the validation data set")
        exit(1)

    if args.output_model_name is None:
        print("Please specify a name for the trained model")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    captcha_symbols = None
    with open(args.symbols) as symbols_file:
        captcha_symbols = symbols_file.readline()

    # physical_devices = tf.config.experimental.list_physical_devices('GPU')
    # assert len(physical_devices) > 0, "No GPU available!"
    # tf.config.experimental.set_memory_growth(physical_devices[0], True)

    with tf.device('/device:GPU:0'):
    # with tf.device('/device:CPU:0'):
    # with tf.device('/device:XLA_CPU:0'):
    # with tf.device('/device:XLA_GPU:0'):
        model = create_model(args.length, len(captcha_symbols), (args.height, args.width, 3), model_depth=6, module_size=2)

        if args.input_model is not None:
            model.load_weights(args.input_model)

        model.compile(loss='categorical_crossentropy',
                      optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                      metrics=['accuracy'])

        model.summary()

        training_data = ImageSequence(args.train_dataset, args.batch_size, args.length, captcha_symbols, args.width, args.height)
        validation_data = ImageSequence(args.validate_dataset, args.batch_size, args.length, captcha_symbols, args.width, args.height)

        if not os.path.exists(args.output_model_name):
            os.mkdir(args.output_model_name)

        save_tflite = SaveTfLite(args.output_model_name)
        tlogdir = args.output_model_name + "/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tb_callback = keras.callbacks.TensorBoard(log_dir=tlogdir, histogram_freq=1, update_freq='batch')
        callbacks = [keras.callbacks.EarlyStopping(monitor='loss', patience=3),
                     # keras.callbacks.CSVLogger('log.csv'),
                     keras.callbacks.ModelCheckpoint(args.output_model_name+'/model_checkpoint.h5', save_best_only=True, save_freq='epoch'),
                     tb_callback,
                     save_tflite]

        # Save the model architecture to JSON
        with open(args.output_model_name+"/model.json", "w") as json_file:
            json_file.write(model.to_json())

        try:
            model.fit_generator(generator=training_data,
                                validation_data=validation_data,
                                epochs=args.epochs,
                                callbacks=callbacks,
                                use_multiprocessing=True)
        except KeyboardInterrupt:
            print('KeyboardInterrupt caught, saving current weights as ' + args.output_model_name+'_/model_resume.h5')
            model.save_weights(args.output_model_name+'/model_resume.h5')
        

if __name__ == '__main__':
    main()
