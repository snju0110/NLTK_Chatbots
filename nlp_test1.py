import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('Bot.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]

words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(words, open('classes.pkl', 'wb'))

print(words)
print(documents)
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    word_pattern = doc[0]
    word_pattern = [lemmatizer.lemmatize(word.lower()) for word in word_pattern]

    for word in words:
        bag.append(1) if word in word_pattern else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    print(bag, output_row)

    training.append([bag, output_row])
#
# random.shuffle(training)
training = np.array(training)


print(training)

# train_x = list(training[:, 0])
#
# train_y = list(training[:, 1])
