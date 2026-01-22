import math
from collections import defaultdict

def corpuser(document:dict) -> dict:
    corpus = {
        'nums_docs':len(document),
        'documents': {},
        'df':defaultdict(int),
        'inverted_index':defaultdict(list)
    }

    for doc_id , doc_data in document.items():
        tokens = doc_data['tokens']
        ensemble = set(tokens)

        corpus['documents'][doc_id] = {
            'tokens':tokens,
            'uniques_words':ensemble,
            'word_count':len(tokens)
        }

        for word in ensemble:
            corpus['df'][word] += 1
            corpus['inverted_index'][word].append(doc_id)
    corpus['stopwords'] = stopword(corpus)
    corpus['vocab_size'] = len(corpus['df'])
    return corpus

def idf(word: str, corpus: dict) -> float:
    N = corpus['nums_docs']
    df = corpus['df'].get(word, 0)
    if df == 0:
        return 0.0
    return math.log10(N / df)

def tfidf(word:str,doc_tokens:list,corpus:dict) -> float:
    tf = doc_tokens.count(word) / len(doc_tokens)
    __idf = idf(word,corpus)
    return tf*__idf

def stopword(corpus:dict,threshold:float=0.7) -> set:
    stp_wrd = set()
    N = corpus['nums_docs']

    for word,df in corpus['df'].items():
        if (df/N) >= threshold:
            stp_wrd.add(word)

    return stp_wrd