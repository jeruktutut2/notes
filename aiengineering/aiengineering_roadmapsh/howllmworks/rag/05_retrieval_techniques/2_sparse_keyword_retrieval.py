import math
from collections import Counter

class BM25Searcher:
    """Implementasi algoritma BM25 (Best Matching 25) dari nol untuk Sparse Keyword Retrieval."""
    def __init__(self, corpus: list, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_tokens = [self._tokenize(doc) for doc in corpus]
        self.doc_len = [len(tokens) for tokens in self.doc_tokens]
        self.avg_doc_len = sum(self.doc_len) / max(len(self.doc_len), 1)
        self.doc_freqs = self._calc_doc_freqs()

    def _tokenize(self, text: str) -> list:
        return text.lower().replace('.', '').replace(',', '').split()

    def _calc_doc_freqs(self) -> dict:
        df = {}
        for tokens in self.doc_tokens:
            for token in set(tokens):
                df[token] = df.get(token, 0) + 1
        return df

    def search(self, query: str, top_k: int = 3) -> list:
        query_tokens = self._tokenize(query)
        N = len(self.corpus)
        scores = [0.0] * N

        for token in query_tokens:
            if token not in self.doc_freqs:
                continue
            df = self.doc_freqs[token]
            # Calculating Inverse Document Frequency (IDF)
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)

            for idx, tokens in enumerate(self.doc_tokens):
                tf = tokens.count(token)
                if tf == 0:
                    continue
                denom = tf + self.k1 * (1 - self.b + self.b * (self.doc_len[idx] / self.avg_doc_len))
                score = idf * (tf * (self.k1 + 1)) / denom
                scores[idx] += score

        results = [
            {"doc_id": idx + 1, "document": self.corpus[idx], "score": float(scores[idx])}
            for idx in range(N)
        ]
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

def main():
    print("=== 02. Sparse Keyword Retrieval (BM25) ===")

    corpus = [
        "Error SKU-99421: Kegagalan koneksi ke server database PostgreSQL.",
        "Error SKU-99422: Permintaan API mengalami HTTP 504 Gateway Timeout.",
        "Panduan konfigurasi koneksi PostgreSQL pada environment staging.",
        "Tips optimasi query SQL dan indek B-Tree di PostgreSQL."
    ]

    bm25 = BM25Searcher(corpus)

    query = "SKU-99421 PostgreSQL error"
    print(f"Query  : '{query}'")
    print(f"Corpus : {len(corpus)} dokumen\n")

    results = bm25.search(query, top_k=2)

    print("Hasil Sparse Keyword Search (BM25 Scores):")
    for r in results:
        print(f"  - [Doc #{r['doc_id']}] Score: {r['score']:.4f}")
        print(f"    Content: \"{r['document']}\"\n")

if __name__ == "__main__":
    main()
