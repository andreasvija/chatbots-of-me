import csv
import time
from gensim.models.doc2vec import Doc2Vec
from chatterbot import ChatBot

data_input_filename = 'training_data.csv'
doc2vec_filename = 'doc2vecmodel'
punctuation = ['.',',',';','!','?','(',')']

data_input_file = open(data_input_filename, 'r', encoding='UTF-8', newline='')
csv_reader = csv.reader(data_input_file, delimiter=',', quotechar='"')

outputs = []

for line in csv_reader:
    outputs.append(line[1])

data_input_file.close()

doc2vecmodel = Doc2Vec.load(doc2vec_filename)

chatterbot = ChatBot('chatterbot',
                     storage_adapter=
                     # automatically loads data from SQLite
                     # database with the default name
                     'chatterbot.storage.SQLStorageAdapter',
                     preprocessors=[
                         'chatterbot.preprocessors.clean_whitespace',
                         'chatterbot.preprocessors.unescape_html'],
                     logic_adapters=[
                         {'import_path':
                              'chatterbot.logic.BestMatch',
                          'statement_comparison_function':
                              'chatterbot.comparisons.levenshtein_distance',
                          'response_selection_method':
                              'chatterbot.response_selection.get_most_frequent_response'
                          }],
                     # stop user interactions from training the bot
                     read_only=True
)

while True:
    print()
    new_input = input('you: ')
    
    if new_input.lower() == 'q' or new_input.lower() == 'quit':
        break
    
    chatterbot_input = new_input
    doc2vec_input = new_input.lower().split()

    for i in range(len(doc2vec_input)):
        if len(doc2vec_input[i]) > 2: #not emoji
            for c in punctuation:
                doc2vec_input[i] = doc2vec_input[i].replace(c, '')

    if ''.join(new_input) == '': #empty input
        continue

    start = time.clock()
    
    vect = doc2vecmodel.infer_vector(new_input)
    similars = doc2vecmodel.docvecs.most_similar([vect], topn=len(doc2vecmodel.docvecs))
    
    for (i, similarity) in similars:
        if 'input' in i:
            i = int(i.replace('input', ''))
            #corresponding response
            print('doc2vecbot: "' + outputs[i] + '"')
            break
    
    end = time.clock()
    print('doc2vecbot answered in ' + str(round(end-start, 1)) + 's')
    
    start = time.clock()
    
    response = str(chatterbot.get_response(chatterbot_input))
    print('chatterbot: "' + response + '"')
    
    end = time.clock()
    print('chatterbot answered in ' + str(round(end-start, 1)) + 's')
