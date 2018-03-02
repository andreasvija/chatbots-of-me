import time
from chatterbot import ChatBot
from CustomListTrainer import CustomListTrainer

def train_chatterbot(inputs, outputs):

    chatterbot = ChatBot('chatterbot',
                         storage_adapter=
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
                              }]
    )

    chatterbot.set_trainer(CustomListTrainer)
    print('Training chatterbot on every 5th datapoint')
    
    start = time.clock()
    
    for i in range(len(inputs)):
        if i % 5 == 0:
            chatterbot.train([ inputs[i], outputs[i] ])
        
    end = time.clock()
    print('Training chatterbot completed in ' +
          str(int((end-start)) // 60) + 'm ' +
          str(int((end-start)) % 60) + 's')
