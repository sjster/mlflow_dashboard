import pandas as pd
from flair.data import Sentence
from flair.models import SequenceTagger
import time

t0 = time.time()

tagger = SequenceTagger.load('pos')

def apply_flair(x):
    noun_list = []
    sentence = Sentence(x.split(' '))
    tagger.predict(sentence)
    for entity in sentence.get_spans('pos'):
        if(entity.tag == 'NN'):
            noun_list.append(entity.text)
    return(noun_list)

df = pd.read_json('data/processed_issues.json')
df['title'] = df['title'].str.lower()
df['entities'] = df['title'].apply(lambda x: apply_flair(x))
df.to_json('data/processed_issues_entities.json')
print(df['entities'])

print("Total time ",time.time() - t0)
