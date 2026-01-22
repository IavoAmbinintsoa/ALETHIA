# ALETHEIA

A pure TF-IDF implementation for PDF document retrieval — built from scratch with focus on algorithmic clarity and information retrieval fundamentals.

## Requirements

- Python 3.8+
- PyMuPDF (for PDF parsing)
- (optional) virtualenv

## Install

1. Clone the repo:
```bash
git clone https://github.com/IavoAmbinintsoa/ALETHEIA.git
cd ALETHEIA
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Place your PDF files in a folder named `PDF/` in the project root
2. Run the application:
```bash
python main.py
```

3. Interactive commands:
   - `list` — enumerate all indexed documents
   - `search <query>` — retrieve top-k documents by TF-IDF score
   - `describe <filename>` — extract salient terms for document
   - `stats` — corpus statistics (vocabulary size, DF distribution, IDF values)
   - `quit` — exit

### Example Session
```
[>] search information retrieval
[>] describe nlp_paper.pdf
[>] stats
```

## Algorithmic Overview

### 1. Document Processing Pipeline
```
PDF → Text Extraction → Unicode Normalization → Tokenization → Index Construction
```

**Text Cleaning** (`index.py:clean`):
- Unicode normalization (NFC → NFD) for consistent character representation
- Diacritic removal via category filtering
- Regex-based entity removal (URLs, emails, LaTeX expressions)
- Lowercasing and whitespace normalization

**Tokenization**: Simple whitespace splitting (can be extended with n-grams or stemming)

### 2. Inverted Index Construction

**Data Structures** (`tf_idf.py:corpuser`):
```python
corpus = {
    'nums_docs': N,                          # Total document count
    'documents': {                           # Per-document metadata
        doc_id: {
            'tokens': [...],                 # Token sequence
            'uniques_words': set(...),       # Vocabulary
            'word_count': int
        }
    },
    'df': defaultdict(int),                  # Document Frequency: word → count
    'inverted_index': defaultdict(list),     # Postings list: word → [doc_ids]
    'stopwords': set(...),                   # High-DF terms (DF/N ≥ 0.7)
    'vocab_size': int
}
```

**Complexity**:
- Time: O(N × M) where N = num_docs, M = avg_doc_length
- Space: O(V + N × M) where V = vocabulary_size

### 3. TF-IDF Scoring

**Term Frequency** (normalized):
```
TF(t, d) = count(t, d) / |d|
```

**Inverse Document Frequency** (log-scaled):
```
IDF(t) = log₁₀(N / DF(t))
```
where DF(t) = number of documents containing term t

**TF-IDF Score**:
```
TF-IDF(t, d) = TF(t, d) × IDF(t)
```

**Document Score** (query q, document d):
```
Score(q, d) = Σ TF-IDF(t, d)  for all t ∈ q \ stopwords
              t∈q
```

### 4. Retrieval Algorithm

**Ranking** (`search.py:search`):
1. Clean and tokenize query
2. For each document:
   - Compute query-document score (sum of term TF-IDF values)
   - Filter stopwords (high-DF terms with low discriminative power)
3. Sort by score (descending)
4. Return top-k results

**Complexity**: O(|q| × N × L) where L = avg lookup time in document tokens

### 5. Stopword Detection

Automatic stopword identification using document frequency threshold:
```python
stopword(w) ⟺ DF(w) / N ≥ 0.7
```

High-frequency terms (appearing in ≥70% of documents) are considered non-discriminative.

## Project Layout

```
ALETHEIA/
├─ README.md
├─ requirements.txt
├─ PDF/                    # Corpus directory
├─ src/
│  ├─ index.py            # Extraction, cleaning, tokenization
│  ├─ tf_idf.py           # Corpus construction, IDF computation
│  └─ search.py           # Retrieval and ranking algorithms
└─ main.py                # CLI interface
```

## Algorithmic Properties

**Strengths**:
- Simple and interpretable
- No training required
- Language-agnostic (with proper tokenization)
- Effective for keyword-based retrieval

**Limitations**:
- Bag-of-words model (no semantic understanding)
- No phrase or proximity modeling
- Linear scan for ranking (no early termination)
- No query expansion or relevance feedback

## Extensions

Potential algorithmic enhancements:
- **BM25**: Improved TF saturation and document length normalization
- **Cosine similarity**: Normalize query and document vectors
- **Positional indexing**: Enable phrase queries
- **Champion lists**: Pre-compute top-scoring documents per term
- **Query optimization**: Term-at-a-time vs. document-at-a-time processing

## Contributing

- Open an issue for discussion before large changes
- Create feature branches, keep commits focused
- Document algorithmic changes with complexity analysis

## References

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*
- Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval

## License

MIT
