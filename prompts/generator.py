# libs
import os 
import json
import math
from datetime import datetime
from random import random

# config
path_concepts = './concepts.json'
dirpath_output = './'
nbr_of_prompts = 1000
nbr_of_words_per_concepts = 2


# load dict
with open(path_concepts, 'r') as f:
    concepts = json.load(f)

# helper functions
def return_today_str():
    return str(datetime.now()).split(' ')[0]


def generate_uid():
    return round(random() * 100000000.0)


def return_random_sample(arr, n):
    
    # generate a random index
    rand_indexes = set()
    while len(rand_indexes) != n:
        rand_index = math.floor(random() * len(arr))
        rand_indexes.add(rand_index)

    # select
    df = []
    for rand_index in rand_indexes:
        datum = arr[rand_index]
        df.append(datum)

    return df


def return_random_prompt():

    # init
    datum = {}
    words = []
    
    # go through each concept
    for concept_key in concepts.keys():

        # select one subconcept
        subconcept_keys = list(concepts[concept_key].keys())
        subconcept_key = return_random_sample(subconcept_keys, 1)[0]

        # get a random samples of the words for this subconcept
        subconcept_words = concepts[concept_key][subconcept_key]

        # select random
        random_words = return_random_sample(subconcept_words, 2)

        # set
        datum[concept_key] = subconcept_key

        # append
        for random_word in random_words:
            words.append(random_word)

    # set prompt
    datum['prompt'] = ', '.join(words)

    # set uid
    datum['uid'] = generate_uid()

    return datum


def main():

    # generate random prompts
    dataframe = [return_random_prompt() for i in range(0, nbr_of_prompts)]

    # create output path
    path_output = f'{dirpath_output}prompts-{return_today_str()}.json'

    # write to disk
    with open(path_output, 'w') as f:
        json.dump(dataframe, f)

    # log
    print(f'Prompts saved at {path_output}')


# run
main()
