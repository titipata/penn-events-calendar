import re
import json
from unidecode import unidecode
import pandas as pd

import spacy
import string
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import WhitespaceTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

import config

nlp = spacy.load('en_core_web_sm')
stemmer = PorterStemmer()
w_tokenizer = WhitespaceTokenizer()
punct_re = re.compile('[{}]'.format(re.escape(string.punctuation)))


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
    Generate location cadidate from a given row of events dataframe
    """
    location = nlp(event['location'])
    location_candidates = [
        ent.text for ent in location.ents
        if ent.label_ in ('ORG', 'LOC')
    ]
    for penn_location in config.locations:
        if penn_location in location.text:
            location_candidates.append(penn_location)
    return location_candidates


def generate_description_candidate(event):
    """
    Generate person, organization candidate using speaker, title and description
    from a given row of events dataframe
    """
    event_text = '{} {} {}'.format(
        event['speaker'], event['title'], event['description']
    )
    candidates = [ent.text
                  for ent in nlp(event_text).ents
                  if ent.label_ in ('PERSON', 'ORG')
                  ]
    return candidates


def generate_owner_candidate(event):
    """
    Generate alternative owner list from a given row of events dataframe
    """
    owner_candidates = []
    owner_candidates.append(event['owner'])
    owner_alternative = event['owner'].replace('Department of ', '')
    owner_alternative = owner_alternative.replace('Center for the ', '')
    owner_alternative = owner_alternative.replace('Center for ', '')
    owner_candidates.append(owner_alternative)

    if 'SAS' in owner_alternative:
        owner_candidates.extend(['Arts & Science', 'School of Arts & Science'])

    abbr = re.search(r'\((.*?)\)', event['owner'])
    if abbr is not None:
        owner_candidates.append(abbr.group(1))
    return owner_candidates


def create_events_features():
    # produce topic vectors using tf-idf and Laten Semantic Analysis (LSA) and search candidate list
    print('Compute LSA vectors...')
    events_json = json.loads(open(config.PATH_DATA, 'r').read())
    events_df = pd.DataFrame(events_json)
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
    print('Done!')

    # produce search candidate list
    print('Compute list of search candidates...')
    location_candidates = events_df.apply(
        generate_location_candidate, axis=1
    )
    description_candidates = events_df.apply(
        generate_description_candidate, axis=1
    )
    owner_candidates = events_df.apply(
        generate_owner_candidate, axis=1
    )

    suggest_candidates = (location_candidates + owner_candidates + description_candidates).\
        map(lambda x: list(pd.unique(
            [e.strip() for e in x if e is not '' and len(e.split()) <= 5])[0:15]))
    events_df['suggest_candidates'] = suggest_candidates
    print('Done!')

    # save to JSON file
    save_json(events_df[['event_index', 'event_vector', 'suggest_candidates']].to_dict(
        orient='records'), config.PATH_VECTOR)
    print('Save feature file in {}!'.format(config.PATH_VECTOR))


if __name__ == '__main__':
    create_events_features()
