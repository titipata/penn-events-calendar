import os
import re
import json
from unidecode import unidecode
import numpy as np
import pandas as pd

import spacy
import string
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import WhitespaceTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors


PATH_DATA = os.path.join('data', 'events.json')
PATH_VECTOR = os.path.join('data', 'events_vector.json')

nlp = spacy.load('en_core_web_sm')
stemmer = PorterStemmer()
w_tokenizer = WhitespaceTokenizer()
punct_re = re.compile('[{}]'.format(re.escape(string.punctuation)))


PENN_LOCATIONS = [
    'Wu and Chen Auditorium',
    'Levine Hall',
    'Towne',
    'Fireside Lounge',
    'Penn Museum',
    'Annenberg Center',
    'The Ambler Theater',
    'Lightbox Film Center',
    'Kleinman Center',
    'Perelman Center for Political Science',
    'Montgomery Theater',
    'PCPSE',
    'Fisher-Bennett Hall',
    'Barchi Library',
    'John Morgan Building',
    'Hayden Hall',
    'Blockley Hall'
]


def save_json(ls, file_path):
    """
    Save list of dictionary to JSON
    """
    with open(file_path, 'w') as fp:
        fp.write('[\n  ' + ',\n  '.join(json.dumps(i) for i in ls) + '\n]')


def preprocess(text, stemming=True):
    """
    Apply Snowball stemmer to string
    Parameters
    ----------
    text : str, input abstract of papers/posters string
    stemming : boolean, apply Porter stemmer if True,
        default True
    """
    text = text or ''
    text = unidecode(text).lower()
    text = punct_re.sub(' ', text)  # remove punctuation
    if stemming:
        words = w_tokenizer.tokenize(text)
        text_preprocess = ' '.join([stemmer.stem(word) for word in words])
    else:
        words = w_tokenizer.tokenize(text)
        text_preprocess = ' '.join([stemmer.stem(word) for word in words])
    return text_preprocess


def generate_location_candidate(event):
    """
    Generate location cadidate
    """
    location = nlp(event['location'])
    location_candidate = [
        ent.text for ent in location.ents if ent.label_ in ('ORG', 'LOC')]
    for penn_location in PENN_LOCATIONS:
        if penn_location in location.text:
            location_candidate.append(penn_location)
    return list(pd.unique(location_candidate))


def generate_description_candidate(event):
    """
    Generate person, organization candidate from speaker, title and description
    """
    event_text = event['speaker'] + ' ' + \
        event['title'] + ' ' + event['description']
    candidates = [ent.text for ent in nlp(
        event_text).ents if ent.label_ in ('PERSON', 'ORG')]
    return list(pd.unique(candidates))


if __name__ == '__main__':
    # produce topic vectors using tf-idf and Laten Semantic Analysis (LSA) and search candidate list
    print('Compute LSA vectors...')
    print('Done!')
    events_df = pd.DataFrame(json.loads(open(PATH_DATA, 'r').read()))
    events_text = [' '.join([e[1] for e in r.items()])
                   for _, r in events_df[['title', 'description', 'location', 'owner']].iterrows()]
    events_preprocessed_text = [preprocess(text) for text in events_text]
    tfidf_model = TfidfVectorizer(min_df=3, max_df=0.85,
                                  lowercase=True, norm='l2',
                                  ngram_range=(1, 2),
                                  use_idf=True, smooth_idf=True, sublinear_tf=True,
                                  stop_words='english')
    X_tfidf = tfidf_model.fit_transform(events_preprocessed_text)
    lsa_model = TruncatedSVD(n_components=30,
                             n_iter=100,
                             algorithm='arpack')
    lsa_vectors = lsa_model.fit_transform(X_tfidf)
    events_vector = [list(vector) for vector in lsa_vectors]
    events_df['event_vector'] = events_vector

    # produce search candidate list
    print('Compute search candidate list...')
    location_candidates = events_df.apply(generate_location_candidate, axis=1)
    description_candidates = events_df.apply(
        generate_description_candidate, axis=1)
    owner_candidates = events_df.owner.map(lambda x: [x])

    suggest_candidates = (location_candidates + owner_candidates + description_candidates).\
        map(lambda x: list(pd.unique(
            [e.strip() for e in x if e is not '' and len(e.split()) <= 4])[0:10]))
    events_df['suggest_candidates'] = suggest_candidates
    print('Done!')

    # save to JSON file
    save_json(events_df[['event_index', 'event_vector', 'suggest_candidates']].to_dict(
        orient='records'), PATH_VECTOR)
    print('Save feature file in {}!'.format(PATH_VECTOR))
