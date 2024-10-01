# -*- coding: utf-8 -*-
"""next_word_predictor_LSTM

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Pha8yRXyyfLOWoR2_8GKjA4PBg0D5Pus
"""

# Open the file in read mode and store the content in a variable
with open('big.txt', 'r') as file:
    text_content = file.read()

# Now, 'text_content' contains all the text from 'big.txt'
# print(text_content)  # If you want to check the content
print(len(text_content))

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer

tokenizer  = Tokenizer()

tokenizer.fit_on_texts([text_content])

len(tokenizer.word_index)

cnt=0
for sentence in text_content.split('\n'):
    tokenizer.texts_to_sequences([sentence])
    ''' aa apde darek sentence ne vecotrize kri didhu che,
        badha whole numbers ma convert thai gya che ahiya '''
    cnt+=1
print('total sentences are : ',cnt)

''' have aa je sentences bnya ena thi apde dataset bnavsu  '''
input_sentences=[]
for sentence in text_content.split('\n'):
    tokenized_sentences = tokenizer.texts_to_sequences([sentence])[0]

    for i in range(1,len(tokenized_sentences)):
        input_sentences.append(tokenized_sentences[:i+1])

len(input_sentences)

max_len = max ( [len(x) for x in input_sentences] )
print(max_len)
'''anu meaning em thy ki koi ek sentence evo che jema 466 words che,
to apde have ZERO PADDING krisu and badha sentence in length 466 kri daisu'''

from tensorflow.keras.preprocessing.sequence import pad_sequences
padded_input_seq = pad_sequences(input_sentences, maxlen = max_len, padding='pre')

'''then we will seperate X and Y from padded_input_seq. How? Here the last digit will be
treated as Y and all other columns will be treated as X'''
X = padded_input_seq[:,:-1]

y = padded_input_seq[:,-1]

print(X.shape, y.shape)

'''Y ne one hot encoding krvi pdse'''
from tensorflow.keras.utils import to_categorical
y = to_categorical(y, num_classes=283)

y.shape

''' MODEL ARCHITECTURE :

EMBEDDING -> LSTM -> DENSE
'''

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Input

# Define the model
# model = Sequential()
# model.add(Embedding(input_dim=31667, output_dim=100))  # Embedding layer
# model.add(LSTM(150, return_sequences=True))  # LSTM layer
# model.add(LSTM(150))
# model.add(Dense(31667, activation='softmax'))  # Output layer

model = Sequential()
model.add(Input(shape=(56,)))  # Input layer with sequence length of 465
model.add(Embedding(283, 100))
model.add(LSTM(300, return_sequences=True))
model.add(LSTM(150))
model.add(Dense(283, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Display the model summary
model.summary()

y.shape

model.fit(X,y,epochs=200)

import numpy as np

text = 'yes'

# there are 3 steps here: tokenize, padding, predict

for i in range(10):
  # tokenize
  token_text = tokenizer.texts_to_sequences([text])[0]

  # padding
  padded_token_text = pad_sequences([token_text], maxlen=56, padding='pre')

  # predict
  pos = np.argmax(model.predict(padded_token_text))

  for word, index in tokenizer.word_index.items():
    if index == pos :
      text = text + " " + word
      print(text)

