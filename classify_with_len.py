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
import itertools

def decode(characters, y, len_y):
    y_idx = numpy.argmax(numpy.array(y), axis=2)[:,0]
    y_pred = numpy.max(numpy.array(y), axis=2)[:,0]
    cap_len = numpy.argmax(numpy.array(len_y), axis=1)[0] + 1
    y_chars = numpy.argsort(y_pred)[-cap_len:]
    
    res = ''.join([characters[x] for i,x in enumerate(y_idx) if i in y_chars])
    # res = ",".join(["=".join([characters[x],str(y_pred[i])]) for i,x in enumerate(y_idx) if x < len(characters)])
    # res = ''.join([characters[x] for x in y_idx])
    # prob_res = ",". join([str(prb) for prb in y_pred])
    return res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--len-model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to use")
        exit(1)
    
    if args.len_model_name is None:
        print("Please specify the CNN model to use")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Classifying captchas with symbol set {" + captcha_symbols + "}")

    with tf.device('/cpu:0'):
        with open(args.output, 'w') as output_file:
            # char length model
            len_json_file = open(args.len_model_name+'/model.json', 'r')
            len_loaded_model_json = len_json_file.read()
            len_json_file.close()
            len_model = keras.models.model_from_json(len_loaded_model_json)
            len_model.load_weights(args.len_model_name+'/model_checkpoint.h5')
            len_model.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])

            # char pred model
            json_file = open(args.model_name+'/model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model = keras.models.model_from_json(loaded_model_json)
            model.load_weights(args.model_name+'/model_checkpoint.h5')
            model.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])

            for x in os.listdir(args.captcha_dir):
                # load image and preprocess it
                raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
                rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
                image = numpy.array(rgb_data) / 255.0
                (c, h, w) = image.shape
                image = image.reshape([-1, c, h, w])
                prediction = model.predict(image)
                len_prediction = len_model.predict(image)
                res = decode(captcha_symbols, prediction, len_prediction)
                output_file.write(x + "," + res + "\n")

                print('Classified ' + x)

if __name__ == '__main__':
    main()
