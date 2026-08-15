# Catatan RAG (Retrieval-Augmented Generation) AI Engineering

Dokumen ini berisi rangkuman teori, konsep arsitektur, metrik matematika, dan praktik terbaik dalam membangun sistem RAG modern skala produksi.

---

## 1. Document Loading & Parsing
* **Tujuan**: Mengubah dokumen heterogen (PDF, Markdown, HTML, JSON, CSV) menjadi teks bersih terstruktur beserta metadata (author, created_at, source, page_number).
* **Tantangan Utama**: Menjaga struktur hierarki dokumen (headers, tabel, daftar) dan membuang elemen non-informatif (header/footer berulang, skrip HTML, iklan).
* **Metadata Enrichment**: Menambahkan metadata berharga ke setiap segmen dokumen membantu filtering presisi saat tahap retrieval (misal: memfilter dokumen ber-tag `tahun: 2024`).

---

## 2. Chunking Strategies
* **Fixed-size & Overlap**: Membagi teks berdasarkan panjang karakter/token tetap dengan overlap (misal 500 karakter, overlap 50). Mencegah hilangnya konteks di batas pemotongan.
* **Recursive Character Chunking**: Menggunakan daftar pembatas bertingkat (`["\n\n", "\n", " ", ""]`). Mencoba memotong di paragraf dulu; jika terlalu besar, potong di kalimat; lalu kata.
* **Structural Chunking**: Memotong berdasarkan struktur spesifik dokumen (misal: Markdown Header `#`, `##` atau fungsi/kelas pada source code).
* **Semantic Chunking**: Mengukur jarak similaritas antar kalimat berurutan. Jika terjadi lonjakan jarak semantik (perubahan topik), teks dipotong.

---

## 3. Embeddings & Vectorization
* **Dense Vectors**: Teks diubah menjadi array bilangan riil kontinu $V \in \mathbb{R}^d$ (misal $d=1536$ untuk `text-embedding-3-small`). Teks dengan makna serupa berada berdekatan di ruang vektor.
* **Similarity Metrics**:
  * **Cosine Similarity**: Mengukur sudut antar dua vektor:
    $$\text{Cosine}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
  * **Dot Product**: Mengukur magnitudo dan arah (identik dengan Cosine jika vektor ternormalisasi $\|A\|=\|B\|=1$).
  * **Euclidean Distance ($L_2$)**: Jarak lurus antar ujung vektor:
    $$d(A, B) = \sqrt{\sum (A_i - B_i)^2}$$
* **Normalisasi Vektor**: Mengubah magnitudo vektor menjadi $1$ ($\|V\|_2 = 1$). Sangat mempercepat perhitungan similaritas karena $A \cdot B$ langsung menghasilkan Cosine Similarity.

---

## 4. Vector Databases & Indexing
* **Flat Index (Exact Search)**: Membandingkan query vector dengan SELURUH vector di DB (K-Nearest Neighbors). Hasil $100\%$ presisi tetapi lambat ($O(N \cdot d)$).
* **HNSW (Hierarchical Navigable Small World)**: Algoritma Approximate Nearest Neighbor (ANN) berbasis graf berlapis. Mengurangi kompleksitas waktu pencarian dari $O(N)$ menjadi $O(\log N)$.
* **ChromaDB / Qdrant / Pinecone**: Database khusus untuk menyimpan vector, metadata, dan melakukan similarity search dalam skala besar.

---

## 5. Retrieval Techniques
* **Dense Retrieval**: Menggunakan semantic embeddings. Sangat baik menangkap konsep, sinonim, dan maksud konteks, tetapi bisa gagal pada keyword spesifik (misal kode produk `"SKU-99421"`).
* **Sparse Retrieval (BM25 / TF-IDF)**: Mengukur frekuensi kata kunci spesifik dan memenalti kata umum (IDF). Sangat akurat untuk pencarian kata pasti (exact keyword lookup).
* **Hybrid Search (Dense + Sparse)**: Menggabungkan keunggulan keduanya. Hasil pencarian dari kedua metode digabung menggunakan **Reciprocal Rank Fusion (RRF)**:
  $$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
  di mana $r_m(d)$ adalah peringkat dokumen $d$ dalam sistem pencarian $m$, dan $k$ adalah konstanta (biasanya $60$).

---

## 6. Reranking & Context Refinement
* **Cross-Encoder Reranking**: Model Bi-Encoder (embedding biasa) memproses query dan doc secara terpisah. Cross-Encoder memproses `(Query, Doc)` bersamaan via perhatian silang (cross-attention), menghasilkan skor relevansi jauh lebih presisi.
* **Maximal Marginal Relevance (MMR)**: Mengoptimalkan keberagaman hasil pencarian agar hasil Top-K tidak duplikat/redundant:
  $$\text{MMR} = \arg\max_{d_i \in R \setminus S} \left[ \lambda \cdot \text{Sim}_1(d_i, Q) - (1-\lambda) \cdot \max_{d_j \in S} \text{Sim}_2(d_i, d_j) \right]$$
* **Context Compression**: Mengeliminasi kalimat atau paragraf yang tidak relevan dari dokumen yang diambil sebelum dikirim ke LLM untuk menghemat token dan mengurangi noise.

---

## 7. Advanced RAG Architectures
* **Query Transformation**:
  * **Query Rewriting**: Memperbaiki query pengguna yang samar atau ambigu.
  * **Multi-Query**: Menghasilkan 3-5 variasi kalimat dari query asli untuk memperluas jangkauan pencarian.
  * **Sub-Query Decomposition**: Memecah pertanyaan kompleks menjadi beberapa sub-pertanyaan yang dicari secara independen.
* **HyDE (Hypothetical Document Embeddings)**: LLM diminta membuat contoh jawaban hipotetis dulu, kemudian jawaban hipotetis tersebut di-embed dan digunakan untuk mencari dokumen nyata di Vector DB.
* **Agentic RAG & Router**: Agent LLM secara dinamis menentukan sumber retrieval (Vector DB produk, Vector DB regulasi, atau Web Search) berdasarkan intent query.

---

## 8. Generation & Grounding
* **Prompt Construction**: Memasukkan konteks yang diambil ke dalam System Prompt secara ketat: *"Jawab pertanyaan HANYA berdasarkan konteks di bawah ini. Jika tidak ada di konteks, katakan tidak tahu."*
* **Citation & Source Attribution**: Meminta LLM menyertakan sitasi tag `[Doc ID]` dan me-referensikan paragraf sumber untuk mempermudah verifikasi pengguna.
* **Structured Output**: Menggunakan JSON Schema (OpenAI Structured Outputs / Pydantic) untuk mengembalikan respon terstruktur mencakup jawaban, skor keyakinan, dan daftar dokumen referensi.

---

## 9. Evaluasi & Observability
* **RAG Triad**:
  1. **Context Relevance**: Seberapa relevan dokumen yang di-retrieve dengan query pengguna?
  2. **Groundedness / Faithfulness**: Seberapa akurat jawaban LLM berdasarkan konteks (tidak ada halusinasi)?
  3. **Answer Relevance**: Seberapa tepat jawaban LLM menjawab pertanyaan awal pengguna?
* **LLM-as-a-Judge**: Menggunakan LLM yang lebih kuat (misal GPT-4o) untuk menilai kualitas pipeline RAG secara otomatis dalam skala besar.
* **Tracing & Logging**: Merekam latency tiap stage (embedding time, DB retrieval time, LLM generation time) dan skor kognitif pipeline.
