import re
from configs import *
import os
from datetime import datetime
from textwrap import wrap
from timeit import default_timer as tictoc

def read_text(filename):
    with open(filename, 'r') as f:
        return ''.join([l for l in f.readlines()])

def compute_most_freq(m_string):
    m_string = re.sub("'", ' ', m_string)
    m_string = re.sub(r'-', ' ', m_string)
    m_string = re.sub(r'\s+', ' ', m_string)
    m_string = re.sub(r"[^a-zA-Z0-9~\- ]+", ' ', m_string)
    m_string = re.sub(r"[ ]+", ' ', m_string)
    freqs_dict = {}
    for word in m_string.split(' '):
        if word == '':
            continue
        else:
            if not word in freqs_dict.keys():
                freqs_dict[word] = 1
            else:
                freqs_dict[word] += 1
    #the model behind this sort, while simple, is the key to the program
    sol = [k  for k, v in
           sorted(freqs_dict.items(), 
           key = lambda x: (len(x[0]) - 1) * (x[1] - 1),
           reverse = True)]
    return sol            

def char_to_hex(c):
    if c == ' ':
        return '00'
    elif c.isalnum():
        if not c.isdigit():
            n = ord(c.upper()) - 64
            return hex(n)[2:].zfill(2)
        else:
            n = ord(c) - 16
            return hex(n)[2:].zfill(2)
    elif c == '.':
        return '1B'
    elif c == ',':
        return '1C'
    elif c == '!':
        return '1D'
    elif c == '?':
        return '1E'
    elif c == "'":
        return '1F'
    elif c == '"':
        return '2A'
    elif c == ':':
        return '2B'
    elif c == '$':
        return '2C'
    elif c == '(':
        return '2D'
    elif c == ')':
        return '2E'
    elif c == '-':
        return '2F'
    elif c == '\n':
        return '3D' #haha 3D
    elif c == '/':
        return '3E'
    elif c == end_of_string_char:
        return '3F'
    else:
        return ''

def compute_to_hex(m_word):
    res = []
    for ind in range(len(m_word)):
        next_char = char_to_hex(m_word[ind])
        if next_char != '':
            res.append(next_char)
    res.append('3F')
    return res

#just the core of the ALG. Returns the LUT and the raw string
def john_alg(filename, dict_size):
    str_out = read_text(filename)
    freq = compute_most_freq(str_out)
    LUT = freq[:min(dict_size, len(freq))] 
    return LUT, str_out

def create_lut_output(lut):
    lines = []
    for ind in range(len(lut)):
        numstr = hex(ind + 49).zfill(2)[2:].upper()
        res = 'word_' + numstr + ':  ;' 
        wrapped_comment = wrap(lut[ind], max_comment_line_length)
        res += wrapped_comment[0] + '\n'
        for extra_line in wrapped_comment[1:]:
            res += '           ' + extra_line + '\n'
        res += '  ' + '.db '
        num_adds_since_newline = 0
        for m in compute_to_hex(lut[ind]):
            if num_adds_since_newline == line_bytes - 1:
                res += '$' + m + '\n  .db '
                num_adds_since_newline = 0
            else:
                res += '$' + m + ','
                num_adds_since_newline += 1
        if res[-1] == ',':
            res = res[:-1] + '\n\n'
        if res[-1] == ' ': 
            res = res[:-6] + '\n'
        lines.append(res)
    return lines

def get_space_savings_rate(raw_text, LUT):
    num_raw_bytes = len(raw_text)
    def get_bytes_saved(substr):
        return (len(substr) - 1) * (len(re.findall(substr, raw_text)) - 1)
    num_bytes_saved = sum([get_bytes_saved(elem) for elem in LUT])
    return num_bytes_saved / num_raw_bytes

def create_messages_output(raw_text, LUT):
    messages = [[]]
    byte_counter = 0
    message_counter = 0
    split_text = raw_text.split(end_of_string_char)
    for message in split_text:
        message_str = ''
        num_adds_since_newline = 0
        index = 0
        message_bytes = 0
        message_str = 'msg_' + hex(message_counter)[2:].zfill(4) + ':  ;'
        wrapped_comment = wrap(message.replace('\n', r"[\n]").strip(), 
                               max_comment_line_length)
        if len(wrapped_comment) == 0:
            message_str += '\n'
        else:
            message_str += wrapped_comment[0] + '\n'
            for extra_line in wrapped_comment[1:]:
                message_str += '           ' + extra_line + '\n'
        message_str += '  .db '
        while index < len(message):
            hex_res_char = char_to_hex(message[index])
            flag = False
            for elem in LUT:
                if message[index : index + len(elem)] == elem:
                    hex_res_char = hex(LUT.index(elem) + 49)[2:].upper()
                    index += len(elem)
                    flag = True
                    break
            if not flag:
                index += 1
            if num_adds_since_newline == line_bytes - 1:
                message_str += '$' + hex_res_char + '\n  .db '
                num_adds_since_newline = 0
            else:
                message_str += '$' + hex_res_char + ','
                num_adds_since_newline += 1
            message_bytes += 1
        if message_str[-1] == ',':
            message_str = message_str[:-1] + '\n\n'
        if message_str[-1] == ' ': 
            message_str = message_str[:-6] + '\n'
        if byte_counter + message_bytes < byte_counter_max:
            byte_counter += message_bytes
        else:
            byte_counter = message_bytes
            messages.append([])
        messages[-1].append(message_str)
        message_counter += 1
    return messages

def run_program():
    st = tictoc()
    path = output_dir_name
    try:  
        os.mkdir(path)  
    except OSError:  
        pass 
    dict_size = 2 ** num_encoding_bits - 49
    LUT, RO = john_alg(input_file_path, dict_size)
    lut_lines = create_lut_output(LUT)
    msgs = create_messages_output(RO, LUT)
    ss = 100 * get_space_savings_rate(RO, LUT)
    timestr = ''
    if uses_timestamp:
        now = datetime.now()
        timestr = now.strftime('_%m_%d_%Y_%H_%M_%S')
    lut_name = output_dir_name + '/' 
    lut_name += base_output_LUT_file + timestr + '.txt'
    all_files = []
    with open(lut_name, 'w') as f:
        f.writelines(lut_lines)
        all_files.append(lut_name)
    for ind in range(1, len(msgs) + 1):
        cur_file_name = base_output_msg_file + timestr + '-' + str(ind)
        cur_file_name = output_dir_name + '/' + cur_file_name + '.txt'
        with open(cur_file_name, 'w') as f:
            f.writelines(msgs[ind - 1])
            all_files.append(cur_file_name)
    tot_size = sum([os.path.getsize(fn) for fn in all_files])
    if tot_size > 1024 * max_out_filesize and checks_out_filesize:
        raise Exception('ERROR! FILE SIZE TOO LARGE')   
    et = tictoc()
    print('Completed in ' + str(round(et - st, 4)) + ' seconds')
    print('Compression Ratio: ' + str(round(ss, 3)) + '%')
    

run_program()