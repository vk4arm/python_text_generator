# -*- coding: utf-8 -*-
from nltk import word_tokenize, pos_tag
import os
import random
import json

dict_of_lists = {}
corppath = "corpus"
list_plk = "list.pkl"
output_file = "generated.txt"
filelist = []

def add_to_dict_(key, word):
    "Add word to dictionary of lists"
    if key in dict_of_lists:
        dict_of_lists[key].append(word)
    else:
        dict_of_lists[key] = [word]



def add_to_dict(prev_2, prev_1, word, wordtype):
    "Add to dictionary"
    if prev_2 !=  '__' :
        add_to_dict_(prev_2+'~'+prev_1 + '~' + wordtype, word)
    add_to_dict_(prev_1+ '~' + wordtype, word)




def startOfBlock(tokens):
    "Blocks start. If no '.' in the block - return: -1"
    for i in range(500, 3000) :
        if tokens[i] == '.' :
            return i + 1
    return -1



def is_punctuation(param):
    "Checking for punctuation"
    return not param[0].isalpha()

def file_content(file_name):
    "Reading content"
    out =  open(file_name).read().decode('utf-8')
    out = out.replace( u'\u2018', "'").replace( u'\u2019', "'").replace( u'\u201c', '"').replace( u'\u201d', '"')
    return out.encode('ascii', 'ignore')

def prepare_corpus():
  "Prepare the text corpus"
  for root, dirs, files in os.walk(corppath, topdown=False):
      for name in files:
          print(os.path.join(root, name))
          print (len(dict_of_lists))
          str_input = file_content(os.path.join(root, name))
          tokens = word_tokenize(str_input)
          if len(tokens) < 3000 :
              continue
          print (len(tokens))
          pt = pos_tag(tokens)
          print (len(pt))
          start_position = startOfBlock(tokens)
          if start_position == -1:
              continue;
          prev_2 = '__'
          prev_1 = '__'
          for i in range(start_position, len(tokens)):
              if is_punctuation(pt[i][1]) : #punctuation
                  if tokens[i] == '.': #end of sentense
                      prev_2 = '__'
                      prev_1 = '__'
                  continue;
              add_to_dict(prev_2, prev_1, tokens[i].lower(), pt[i][1])
              prev_2 = prev_1
              prev_1 = tokens[i].lower()


def save_to_disk():
    "Saving results"
    output = open(list_plk, 'wb')
    json.dump(dict_of_lists, output)
    output.close()


def get_random_file_to_grammar():
    "Getting random file"
    if len(filelist) == 0:
        for root, dirs, files in os.walk(corppath, topdown=False):
            map(lambda name: filelist.append(os.path.join(root, name)), files)
    return random.choice(filelist)


def generate_pseudiotext():
    "Generate text"
    filename = get_random_file_to_grammar()
    string = file_content(filename)
    tokens = word_tokenize(string)
    start_position = startOfBlock(tokens)
    pt = pos_tag(tokens)
    prev_2 = '__'
    prev_1 = '__'
    words = 0
    is_sentence_start = True

    output = open(output_file, "w")

    row_length = [90]
    def write_up_first_if(word, to_up):
        wordS = word.encode('ascii', 'ignore')
        if to_up:
            output.write(wordS.capitalize())
        else:
            output.write(wordS)
        row_length[0] = row_length[0] - len(wordS)
        if row_length[0]<5 :
            row_length[0] = 100
            output.write('\n')

    def get_next_word(prev_2, prev_1, wordtype, curword):
        if wordtype == 'DT' :
            return curword.lower()
        key = prev_2 + '~' + prev_1 + '~' + wordtype
        if key in dict_of_lists:
            return  random.choice(dict_of_lists[key])
        key = prev_1 + '~' + wordtype
        if key in dict_of_lists:
            return  random.choice(dict_of_lists[key])
        return curword.lower()

    lines  = [random.randint(2, 10)]
    
    def random_paragraf():
        #print lines[0]
        if lines[0] == 0 :
            #print 'paragraf'
            output.write('\n\t\t'.encode("ascii"))
            lines[0 ]+= random.randint(2, 10)
            row_length[0] = 90
        else:
            lines[0] = lines[0] - 1

    output.write('\t\t'.encode("ascii"))
    for i in range(start_position, len(tokens)):
        if is_punctuation(pt[i][1]) : #punctuation
             write_up_first_if(tokens[i], False)
             if tokens[i] == '.' : #end of sentense
                    prev_2 = '__'
                    prev_1 = '__'
                    is_sentence_start = True
                    random_paragraf()
                    # end of file - if words > size
             continue
        next = get_next_word(prev_2, prev_1, pt[i][1], tokens[i])
        write_up_first_if(' ', False)
        write_up_first_if(next, is_sentence_start)
        if(next != next.capitalize()):
            is_sentence_start = False
        prev_2 = prev_1
        prev_1 = next

    output.close()


if __name__ == '__main__' :
    prepare_corpus()
    generate_pseudiotext()

