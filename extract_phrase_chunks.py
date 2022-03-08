import pandas as pd
import collections
import json
import re
import time
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter

def regex_filter(col):
    #regex_pattern = re.compile('\[([^]]+)\]')
    return(re.sub('\[([^]]+)\]', '', col))

def extract():
    t0 = time.time()

    tagger = SequenceTagger.load('flair/chunk-english')
    splitter = SegtokSentenceSplitter()
    nounphrase_dict = collections.defaultdict(int)
    verbphrase_dict = collections.defaultdict(int)

    # ----------------------- Data processing ----------------------- #
    df = pd.read_json('data/processed_issues.json')
    df['title'] = df['title'].str.lower()
    df['title_cleaned'] = df['title'].apply(lambda x: regex_filter(x))
    feature_requests_df = df[df['labels'].apply(lambda x: 'enhancement' in x)]
    data = list(feature_requests_df['title_cleaned'].values)

    # ----------------------- Format data for flair ----------------- #
    data_joined = '. '.join(data)
    split_sentences = splitter.split(data_joined)

    # ----------------------- Extract phrases ----------------------- #
    tagger.predict(split_sentences)

    for sentence in split_sentences:
        for entity in sentence.get_spans('np'):
            if(entity.tag == 'NP'):
                nounphrase_dict[entity.text] += 1
            if(entity.tag == 'VP'):
                verbphrase_dict[entity.text] += 1

    print(nounphrase_dict)
    print('===============================')
    print(verbphrase_dict)

    # -------------------- Write out phrases ------------------------ #
    with open('data/nounphrase_dict.json', 'w') as f:
        json.dump(dict(nounphrase_dict),f)

    with open('data/verbphrase_dict.json', 'w') as f:
        json.dump(dict(verbphrase_dict),f)

    print("Total time ",time.time() - t0)

    return(0)

if __name__ == '__main__':
    ret = extract()
    print('Phrase chunks written out ',ret)
