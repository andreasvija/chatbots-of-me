# for safely printing in console
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#safe_text = text.translate(non_bmp_map)

chat_leave_message = ('<p><span class="warning">You are no ' +
                      'longer in this conversation.</span></p>')
p = '<p>'
double_p = '<p><p>'
p_end = '</p>'
double_p_end = '</p></p>'
at_sign_ascii = '&#064;'
apostrophe_ascii = '&#039;'

chat_opener = '<title>'
chat_start = 'Conversation with'
chat_closer = '</title>'
names_opener = '</h3>'
names_start = 'Participants:'
names_closer = '<div class="message">'

sender_opener = '<span class="user">'
sender_closer = '</span>'
text_opener = '<p>'
text_closer = '</p>'
call_giveaway = 'float:right'
message_closer = '</div>'

reaction_opener = '<ul class="meta">'
reaction_closer = '</ul>'
image_opener = '<img src='
image_closer = '/>'
video_opener = '<video src='
video_closer = '</video>'
audio_opener = '<audio src='
audio_closer = '</audio>'
file_opener = '<a href='
file_closer = '</a>'

def get_data(content, start_string, end_string, index):
    
    start = content.find(start_string, index) + len(start_string)
    end = content.find(end_string, index)
    data = content[start:end].strip()
    
    index = end + len(end_string)
    
    return index, data

import os.path

output_filename = 'data.csv'
output_file = open(output_filename, 'w', encoding='UTF-8')
output_file.write('thread,names,sender,time,text\n')

input_filenames = os.listdir('messages')

for input_filename in input_filenames:
    
    input_filename = 'messages\\' + input_filename
    input_file = open(input_filename, 'r', encoding='UTF-8')
    content = input_file.read().strip()
    input_file.close()
    
    index = 0;
    #changing beginning index improves performance
    #over remaking content text all the time
    
    content = content.replace(chat_leave_message, '')
    content = content.replace(double_p, p).replace(double_p_end, p_end)
    # two common characters that get replaced
    content = content.replace(at_sign_ascii, '@').replace(apostrophe_ascii, "'")

    index, chat = get_data(content, chat_opener, chat_closer, index)
    chat = chat.replace(chat_start, '').strip()
    print('from ' + input_filename + ' got ' + chat.translate(non_bmp_map))

    index, names = get_data(content, names_opener, names_closer, index)
    names = names.replace(names_start, '').replace(', ', ',').strip()
    
    has_next_message = True
    # Only conversations with data in them are included, however
    # "You are now connected on Messenger" is also counted as data
    message_count = 0
    current_data = ''
    wrote_data = False
    
    while has_next_message:

        index, sender = get_data(content, sender_opener, sender_closer, index)
        index, text = get_data(content, text_opener, text_closer, index)
        
        if len(text) > 10000:
            # I genuinely had one ~160k char long emoji spam message in a
            # groupchat from 2012. pandas could not handle storing it and
            # neither IDLE nor even Messenger itself could handle displaying it
            continue

        if call_giveaway in text:
            #if the message is just a voice/video call report, skip it
            continue
        
        attachment_bounds = [(reaction_opener, reaction_closer),
                             (video_opener, video_closer),
                             (image_opener, image_closer),
                             (audio_opener, audio_closer),
                             (file_opener, file_closer)]
    
        for (opener, closer) in attachment_bounds:
            while opener in text:
                
                i = text.find(opener)
                j = text.find(closer, i) + len(closer)
                text = text.replace(text[i:j], '')
            
        while content[index].isspace():
            index = index + 1

        current_data += ('"' + names + '",' +
                         '"' + sender + '",' +
                         '"' + text + '"\n')
        message_count += 1

        if message_count > 1:
            # discount "You are now connected on Messenger"s
            # (and maybe some special case where only one
            # message was sent, but we don't care about that)
            output_file.write(current_data)
            wrote_data = True
            current_data = ''

        if content[index: index + len(message_closer)] == message_closer:
            has_next_message = False

    if not wrote_data:
        print('Discounted ' + names)
            

output_file.close()
