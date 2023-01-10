# Find reliable data stream (from google maps or tagged images)
# Train classic CNN; 3 models: continent, country, (state?) city
# Use existing object detection/train new model for detecting landmarks, liscence plates, signs, etc.
# Train third classification model to map objects to places
# Apply confidence function to find location
# ez

import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical
import cv2

from data_collection import get_data


# TODO: create automation script for data collection
images_data, labels_data = get_data()

classes_convert = {}
for i, label in set(labels_data):
    classes_convert[i] = label    
classes_count = len(classes_convert)

print(np.shape(np.array(images_data)))
print(np.shape(np.array(labels_data)))
images_data = np.array(images_data)
labels_data = np.array(labels_data)
image_reduction = 0.25

for i, image in images_data:
    images_data[i] = cv2.resize(image, (0, 0), None, image_reduction, image_reduction)
dimensions = images_data[0].shape
images_data = images_data / 255.0  # normalize pixel values
images_data = images_data.reshape(-1, dimensions[1], dimensions[0], 3)  # 4 dimension reshape
labels_data = to_categorical(labels_data)  # normalize to one-hot vectors (binary encoding)

permutation = np.random.permutation(len(labels_data))  # set permutation for random shuffle
images_data = images_data[permutation]
labels_data = labels_data[permutation]
# split 80-20 train-test
train_images = images_data[:int(len(images_data)//1.25)]
train_labels = labels_data[:int(len(labels_data)//1.25)]
test_images = images_data[int(len(images_data)//1.25):]
test_labels = labels_data[int(len(labels_data)//1.25):]


# Continent Model
model = models.Sequential()
model.add(layers.Conv2D(256, (9, 9), padding='same', activation='relu', input_shape=(dimensions[1], dimensions[0], 3)))
# model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (7, 7), padding='same', activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.2))
model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
# model.add(layers.Dropout(0.2))
# model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(classes_count, activation='softmax'))

model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),    # process the binary label inputs
              optimizer=SGD(learning_rate=0.01),
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=30, batch_size=32,
                    validation_data=(test_images, test_labels))

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print(model.summary())
print('Test accuracy:', test_acc)

####################
# save model and trained weights
# open('saved_model_weights', 'w').close()
# json_file = model.to_json()
# with open('saved_model_weights', "w") as file:
#     file.write(json_file)

# model.save_weights('h5_file')
# print('Model saved')
