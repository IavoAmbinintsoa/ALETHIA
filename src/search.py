from src.index import * 
from src.tf_idf import *

def score(query:str,doc_id:str,corpus:dict) -> float:
    doc_tokens = corpus['documents'][doc_id]['tokens']
    total = 0.0

    for word in query:
        if word in corpus['stopwords']:
            continue
        scr = tfidf(word,doc_tokens,corpus)
        total += scr
    return total

def search(query:str,corpus:dict,top_k:int = 10) -> list:
    cleaned = clean(query)
    tokens_query = tokenize(cleaned)

    scrs = {}
    for doc_id in corpus['documents']:
        scr = score(query,doc_id,corpus)
        if scr > 0:
            scrs[doc_id] = scr
    
    ranked = sorted(scrs.items(), key=lambda x: x[1], reverse=True)
    
    return ranked[:top_k]

def describe(doc_id:str,corpus:dict,top_k:int = 10) -> list:
    if doc_id not in corpus['documents']:
        return []
    tokens = corpus['documents'][doc_id]['tokens']
    ensemble = corpus['documents'][doc_id]['uniques_words']

    word_scores = {}
    for word in ensemble:
        if word in corpus['stopwords']:
            continue
        scr = tfidf(word,tokens,corpus)
        word_scores[word] = scr
    sorted_words = sorted(word_scores.items(),key=lambda x: x[1],reverse=True)
    return sorted_words[:top_k]

def top_word(doc_id:str,corpus:dict,top_k: int = 5) -> list:
    descriptions = describe(doc_id=doc_id,corpus=corpus,top_k=top_k)
    return [word for word,_ in descriptions]