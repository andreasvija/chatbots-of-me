import csv

input_filename = 'data.csv'
data_output_filename = 'training_data.csv'
corpus_output_filename = 'corpus.txt'

input_file = open(input_filename, 'r', encoding='UTF-8', newline='')
columns = input_file.readline().strip()
csv_reader = csv.reader(input_file, delimiter=',', quotechar='"')

corpus_output_file = open(corpus_output_filename, 'w',
                          encoding='UTF-8', newline='')

conversations = {}
name = 'Andreas Vija'
quote = '&quot;'
punctuation = ['.',',',';','!','?','(',')']

#line: names,sender,text
for line in csv_reader:
    conversation = line[0]
    sender = line[1]
    
    text = line[2].strip().lower().replace(quote, "'")
    textlist = text.split()
    for i in range(len(textlist)):
        if len(textlist[i]) > 2: # not emoji
            for c in punctuation:
                textlist[i] = textlist[i].replace(c, '')
    text = ' '.join(textlist)

    corpus_output_file.write(text + '\r\n') 
    
    if len(conversation.split(',')) < 5 and conversation != name:
        # only use data if there is me and <5 people
        # and I'm not the only person in the chat
        if conversation in conversations:
            conversations[conversation].append((sender, text))
        else:
            conversations[conversation] = [(sender, text)]

input_file.close()
corpus_output_file.close()

inputs = []
outputs = []

for conversation in conversations:
    data = conversations[conversation]
    data.reverse()
    # the data is originally in reversed order
    
    # data.sort(key=lambda d: d[1]) 
    # 'lambda d: d[1]' is shorthand for 'def f(d): return d[1]'
    
    previous_sender = ''
    sender = ''
    potential_input = ''
    text_buffer = ''
    
    for message in data:
        previous_sender = sender
        sender = message[0]
        text = message[1]
        
        if previous_sender != name and sender == name:
            potential_input = text_buffer
            text_buffer = ''
            
        elif previous_sender == name and sender != name:
            potential_input = potential_input.strip()
            text_buffer = text_buffer.strip()
            
            if potential_input != '' and text_buffer != '':
                if len(potential_input) < 2000 and len(text_buffer) < 1000:
                    if len(potential_input) / len(text_buffer) < 50 and len(text_buffer) / len(potential_input) < 50:
                        
                        inputs.append(potential_input)
                        outputs.append(text_buffer)
                
            potential_input = ''
            text_buffer = ''
            
        if len(text) > 0:
            text_buffer += text + ' '

data_output_file = open(data_output_filename, 'w', encoding='UTF-8')

for i in range(len(inputs)):
    data_output_file.write('"' + inputs[i] + '"' + ',' + 
                      '"' + outputs[i] + '"' + '\n')

data_output_file.close()
