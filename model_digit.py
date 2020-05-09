
import tensorflow as tf
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K


import matplotlib.pyplot as plt
from random import randint

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)


a=randint(0,60000)
y=y_train[a]
plt.figure('Exploring the training set')
plt.title("this is image " + str(a) + " and it's supposed to be a " + str(y))
plt.imshow(x_train[a])
plt.colorbar()
plt.grid(False)
plt.show()



# Making sure that the values are float so that we can get decimal points after division
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')


#normalisation, to have pixel values from 0 to 1 (instead of 0 to 255)
x_train = x_train / 255.0
x_test = x_test / 255.0

# Why? I don'r get it but bassically the model need an imput shape with one more dimension.. so let's give it to him! lol
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)



#see the input shape? I don't know why it need this extra dim... 
model = keras.Sequential([
	keras.layers.Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(28,28,1)),
	keras.layers.MaxPooling2D(pool_size=(2, 2)),
	keras.layers.Conv2D(64, kernel_size=(3, 3),activation='relu'),
	keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')])


#model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(),metrics=['accuracy'])

#model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10)


test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)

print('\nTest accuracy:', test_acc)


model.save('mnist.h5')
print("Saving the model as mnist.h5")
