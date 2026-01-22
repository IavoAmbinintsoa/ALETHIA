from src.index import *
from src.search import *
from src.tf_idf import *
import sys
import time

def animate_text(message: str, delay: float = 0.03):

    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print() 

def main():
    corpus = indexes('PDF')
    
    if not corpus:
        print("Failed to build index.")
        return
    
    message = "Welcome to Aletheia :) !\nSearch EveryThing You Want locally.\n"

    animate_text(message)

    print("\nCommands: list | describe <name> | search <query> | stats | quit\n")
    
    while True:
        try:
            cmd = input("[>] ").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
            
            elif cmd.lower() == 'list':
                print("\nDocuments:")
                for i, doc_id in enumerate(sorted(corpus['documents'].keys()), 1):
                    tokens = len(corpus['documents'][doc_id]['tokens'])
                    print(f"  {i}. {doc_id} ({tokens:,} tokens)")
            
            elif cmd.lower().startswith('describe '):
                doc_name = cmd[9:].strip()
                if doc_name in corpus['documents']:
                    descriptions = describe(doc_name, corpus, top_k=15)
                    print(f"\nTop words for '{doc_name}':")
                    for i, (word, score) in enumerate(descriptions, 1):
                        print(f"  {i:2}. {word:20} {score:.4f}")
                else:
                    print(f"  ✗ Not found")
            
            elif cmd.lower().startswith('search '):
                query = cmd[7:].strip()
                results = search(query, corpus, top_k=10)
                
                if results:
                    print(f"\nResults for '{query}':\n")
                    for i, (doc_id, score) in enumerate(results, 1):
                        top_words = top_word(doc_id, corpus, top_k=5)
                        print(f"  {i}. {doc_id}")
                        print(f"     Score: {score:.4f}")
                        print(f"     Words: {', '.join(top_words)}\n")
                else:
                    print(f"  ✗ No results")
            
            elif cmd.lower() == 'stats':
                print("\nStatistics:")
                print(f"  • Documents: {corpus['nums_docs']}")
                print(f"  • Vocabulary: {corpus['vocab_size']:,}")
                print(f"  • Stopwords: {len(corpus['stopwords'])}")
                print(f"  • Informative: {corpus['vocab_size'] - len(corpus['stopwords']):,}")
                
                top_df = sorted(corpus['df'].items(), key=lambda x: x[1], reverse=True)[:10]
                print(f"\n  Top 10 frequent terms:")
                for word, df in top_df:
                    idf_val = idf(word, corpus)
                    pct = 100 * df / corpus['nums_docs']
                    print(f"    • {word:20} DF={df:3} ({pct:.1f}%) IDF={idf_val:.3f}")
            
            else:
                print("  ✗ Unknown command")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"  ✗ Error: {e}")


if __name__ == '__main__':
    main()