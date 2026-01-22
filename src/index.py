import pymupdf
import re
import unicodedata
from src.tf_idf import *
import os

def extract(pdf:str) -> str:
    text = ""
    try:
        doc = pymupdf.open(pdf)
        for page in doc:
            text += page.get_text("text")
        doc.close()
    except Exception as e:
        print(f"Error reading the pdf {e}")
    finally:
        return text

def clean(text:str) -> str:
    text = re.sub(r'^\s*\d+\s*$','',text,flags=re.MULTILINE)
    text = unicodedata.normalize('NFC',text)
    text = text.lower()
    text = unicodedata.normalize('NFD',text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'https?://\S+|www\.\S+','',text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\$[^\$]*\$', '', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text:str) -> list:
    return text.split() if text else []

def indexes(pdf_dir:str) -> dict:
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

    documents = {}
    for i,filename in enumerate(pdf_files,1):
        pdf_path = os.path.join(pdf_dir,filename)
        raw = extract(pdf_path)
        cleaned = clean(text=raw)
        tokens = tokenize(text=cleaned)

        documents[filename] = {
            'path': pdf_path,
            'tokens':tokens
        }
    
    corpus = corpuser(documents)

    return corpus