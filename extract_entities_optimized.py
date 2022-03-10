import pandas as pd
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter
import time

def extract():
    t0 = time.time()

    tagger = SequenceTagger.load('pos')
    splitter = SegtokSentenceSplitter()

    df = pd.read_json('data/processed_issues.json')
    df['title'] = df['title'].str.lower()
    noun_list = []

    data = list(df['title'].values)
    data_joined = '. '.join(data)
    split_sentences = splitter.split(data_joined)
    tagger.predict(split_sentences)

    for sentence in split_sentences:
        for entity in sentence.get_spans('pos'):
            if(entity.tag == 'NN'):
                noun_list.append(entity.text)

    return(0)

    print("Total time ",time.time() - t0)

if __name__ == '__main__':
    return_val = extract()
