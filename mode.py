# libraries
# tensorflow
import tensorflow as tf
# keras
from tensorflow import keras
# model
from keras.models import Sequential
# layers
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# optimizer
from keras.optimizers import Adam
# one-hot encoding
from keras.utils import to_categorical
# data augmentation
from keras.preprocessing.image import ImageDataGenerator
# image manupulation
from keras.preprocessing import image
# cv2
import cv2
# Image display form python
from PIL import Image
# Learning rate scheduler
from keras.callbacks import LearningRateScheduler, ModelCheckpoint
# ploting library
import matplotlib.pyplot as plt
# pandas
import pandas as pd
# numpy
import numpy as np
# os
import os
# subprocess
from subprocess import check_output

print(tf.__version__)

# check content of the  directory
# get the data in the directory using git
#!git clone https://github.com/paldheeraj25/scrap.git
check_output(['ls', 'scrap']).decode('utf-8').splitlines()


shoe_list = np.asarray(check_output(
    ['ls', 'scrap/puma/Puma Training & Gym Shoes For Men']).decode('utf-8').splitlines())
print(shoe_list)

# load the csv to in pandas data frame
df = pd.read_csv('scrap/puma-shoe-collection.csv')

# code to remove the correpted image
# os.remove('scrap/puma/Puma Carson 2 Running Shoes For Men/1382-0.jpg')


# need to do this to manage directory error and maintain image
df['shoe'] = df['shoe'].str.replace('/', '-')

# check he correpted images
corrupted = 0
for shoe_dir in df['shoe'].unique():
    shoes = np.asarray(check_output(
        ['ls', 'scrap/puma/'+shoe_dir]).decode('utf-8').splitlines())
    for shoe in shoes:
        try:
            Image.open(os.path.join('scrap', 'puma', shoe_dir, shoe))
            # do stuff
        except IOError:
            corrupted += 1
            print('correpted image count ', corrupted)
            print('correpted image name ', 'scrap/puma/' + shoe_dir+'/'+shoe)


# check dataframe head
df.head()

# get unique classes from data frame
classes = df['shoe'].unique()

# check classes
print(len(classes))


# loading images in data
data = os.path.join('scrap', 'puma')


# our images need to be preprocesses before training, testng and predicting
def image_preprocessor(img):

    # resize the image to 256 by 256
    img_resize = cv2.resize(img, (256, 256))

    # Blurring the images to remove the false sense of edges and shines
    img_blurred = cv2.GaussianBlur(img_resize, (5, 5), 0)

    # normalize the values for better computation
    img_blurred = img_blurred / 255.0
    return img_blurred


# check the image
test_image = plt.imread(os.path.join(
    'scrap', 'puma', 'Puma 365 IGNITE CT Football Shoes For Men', '840-0.jpg'))
plot_test_img = image_preprocessor(test_image)
plt.imshow(plot_test_img)
plt.axis('off')
print(plot_test_img.shape)
# print(plot_test_img[0])


# create ImageDataGenerator object for data augmentation of training data, use our own function  for image processing as well
train_data = ImageDataGenerator(width_shift_range=0.1,
                                height_shift_range=0.1,
                                zoom_range=0.2,
                                shear_range=0.1,
                                rotation_range=10,
                                preprocessing_function=image_preprocessor).flow_from_directory(data, target_size=(256, 256), batch_size=20)

# add training and validation data here


# model
def build_model():
    model = Sequential()

    # first part of the network will be for feature map detection with convolution layers
    # convolutional part, filter_size =5, 5, keep strides and padding size same, activation relu and provide input_shape
    # we will follow vgg model pattern starting with less parameters increase it in subsequent layers
    model.add(Conv2D(256, (3, 3), activation=tf.nn.relu,
                     input_shape=(256, 256, 3)))
    # reduce the dimentiality of image with MaxPooling
    model.add(MaxPooling2D(pool_size=(3, 3)))
    # increase image parameters
    model.add(Conv2D(512, (3, 3), activation=tf.nn.relu))
    model.add(MaxPooling2D(pool_size=(3, 3)))

    # flatten layer before puting in classification layers
    model.add(Flatten())

    # second part will be Dense netwrok for classification
    model.add(Dense(256, activation=tf.nn.relu))
    # Dropout to avoid overfitting
    model.add(Dropout(0.2))
    model.add(Dense(512, activation=tf.nn.relu))
    model.add(Dropout(0.2))
    # final layer with class size
    model.add(Dense(696, activation=tf.nn.softmax))

    # compile the model with categorical_crossentropy, Adam optimizer for 0.0001 learning rate and metrics accuracy
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=0.001), metrics=['accuracy'])

    return model


model = build_model()
model.summary()


model.fit_generator(train_data, steps_per_epoch=40,
                    validation_steps=40, epochs=25, verbose=1)
