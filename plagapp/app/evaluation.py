import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import pandas as pd
import tensorflow as tf
import keras as kr
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
import talos as ta

from keras.optimizers import Adam, Nadam
from keras.activations import softmax, relu, elu
from keras.losses import binary_crossentropy, logcosh, mean_squared_error, sparse_categorical_crossentropy


#merge all csv files to one csv file
def concatenatecsv(indir="/home/son1i/PycharmProjects/IRProject/IntrinsicPD/evaluate/txtdata", outfile="/home/son1i/PycharmProjects/IRProject/IntrinsicPD/evaluate/concatSPUN.csv"):
    os.chdir(indir)
    fileList=glob.glob("*-SPUN*.csv")
    dfList=[]
    for filename in fileList:
        print(filename)
        df=pd.read_csv(filename, header=None)
        df=df[1:]
        dfList.append(df)
    concatDf=pd.concat(dfList,axis=0, sort=True)
    concatDf.to_csv(outfile, index=None)

#for creating the csv file call the function
#concatenatecsv()

#read the concatenated csv file
def readcsv(csvfile):
    df=pd.read_csv(csvfile, header=0)
    #drop first two columns, (are not necessary for NN)
    df=df.drop('0', axis=1)
    df=df.drop('1', axis=1)
    return df

#DATA PREPARATION
#get the input data
dataORIG = readcsv("/home/son1i/PycharmProjects/IRProject/IntrinsicPD/evaluate/concatORIG.csv")
dataSPUN = readcsv("/home/son1i/PycharmProjects/IRProject/IntrinsicPD/evaluate/concatSPUN.csv")

#add output column to current data frame
dataORIG = dataORIG.assign(output = "ORIG")
dataSPUN = dataSPUN.assign(output = "SPUN")

print(dataORIG.head())
print(dataSPUN.head())

data = pd.concat([dataORIG, dataSPUN])
#get the output column
Y = data['output']
#drop the output column
X = data.drop('output', axis=1)

#train and test data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

#integer encoding
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.fit_transform(y_test)

#normalize input
X_train = kr.utils.normalize(X_train, axis=-1, order=2)
X_test = kr.utils.normalize(X_test, axis=-1, order=2)

x,y = X_train.shape
print(X_train.shape)

#NEURAL NETWORK
#Feed Forward
#hyperparameter optimization
p = {'batch_size': [20,30],
     'epochs': [10, 20],
     'dropout': [0.2, 0.4, 0.5],
     'optimizer': ['adam', 'Nadam'],
     'losses': [binary_crossentropy, mean_squared_error, logcosh],
     'activation':[relu, elu]}


def model(X_train, y_train, X_test, y_test, params):
    model = kr.models.Sequential()
    model.add(kr.layers.Dense(128, input_dim=X_train.shape[1], activation=params['activation']))
    model.add(kr.layers.Dropout(params['dropout']))
    model.add(kr.layers.Dense(128, activation=params['activation']))
    model.add(kr.layers.Dropout(params['dropout']))
    model.add(kr.layers.Dense(1))

    model.compile(optimizer=params['optimizer'], loss=params['losses'], metrics=['accuracy'])

    out = model.fit(X_train, y_train,
                    epochs=params['epochs'],
                    batch_size=params['batch_size'],
                    verbose=0,
                    validation_data=(X_test, y_test))

    return out, model

# talos scan for best hyperparameter
#t = ta.Scan(x=X_train,
#            y=y_train,
#           model=model,
#            params=p,
#            dataset_name='model',
#           experiment_no='1')


def model2(X_train, X_test, y_train, y_test):
    model2 = kr.models.Sequential()
    model2.add(kr.layers.Dense(128, input_dim=X_train.shape[1], activation='relu'))
    model2.add(kr.layers.Dropout(0.2))
    model2.add(kr.layers.Dense(128, activation='relu'))
    model2.add(kr.layers.Dropout(0.2))
    model2.add(kr.layers.Dense(1))

    model2.compile(optimizer='Nadam', loss='logcosh', metrics=['accuracy'])

    out = model2.fit(X_train, y_train,
                    epochs=20,
                    batch_size=20,
                    verbose=1,
                    validation_data=(X_test, y_test))

    return out, model2

history, model2 = model2(X_train, X_test, y_train, y_test)

# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()