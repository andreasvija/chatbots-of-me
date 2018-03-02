import csv
from train_doc2vecbot import *
from train_chatterbot import *

data_input_filename = 'training_data.csv'
corpus_filename = 'corpus.txt'

data_input_file = open(data_input_filename, 'r', encoding='UTF-8', newline='')
csv_reader = csv.reader(data_input_file, delimiter=',', quotechar='"')

inputs = []
outputs = []

for line in csv_reader:
    inputs.append(line[0])
    outputs.append(line[1])

data_input_file.close()

corpus_file = open(corpus_filename, 'r', encoding='UTF-8')
corpus = []

for line in corpus_file:
    text = line.strip().lower()
    corpus.append(text)

corpus_file.close()

train_doc2vecbot(corpus, inputs)
train_chatterbot(inputs, outputs)
