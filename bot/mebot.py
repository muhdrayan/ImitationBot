import enum
import os

import nltk
from nltk.stem.lancaster import LancasterStemmer
nltk.download('punkt')
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

# Filepaths
curdir = str(os.getcwd())+"/bot/"
model_filepath = f"{curdir}tflies/model.tflearn"

# Loading intents and Processing WORDS and input data
with open(curdir+"intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty=[0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w)for w in doc]

        for w in words:
            bag.append(1) if w in wrds else bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    # Final Learning Input
    training = np.array(training)
    output = np.array(output) 

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output),f)

# Tensorflow-Things (AI THINGS)
tf.compat.v1.reset_default_graph()

# Neural Network Model
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load(model_filepath)
except:
    # Hyperparameters
    EPOCHS = 1000
    BATCH_SIZE = 8

    # Training
    model.fit(training, output, n_epoch=EPOCHS, batch_size=BATCH_SIZE, show_metric=True)
    model.save(model_filepath)

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)

def chat():
    print("Start talking with the bot")
    while True:
        inp = input("You:  ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        print(random.choice(responses))

chat()
    