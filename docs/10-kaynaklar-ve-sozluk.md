# 10. Kaynaklar ve Sözlük

---

## 10.1 Okunacak makaleler

Önem sırasına göre dizildi. ⭐ işaretliler mutlaka okunmalı ve raporun literatür bölümünde yer almalı.

### RAG ve genel bakış
- ⭐ Lewis ve ark. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS. **RAG'i tanımlayan makale**
- ⭐ Gao ve ark. (2023). *Retrieval-Augmented Generation for Large Language Models: A Survey.* arXiv. **Alanın genel haritası**

### Kelime tabanlı arama
- ⭐ Robertson & Zaragoza (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in IR
- Manning, Raghavan & Schütze (2008). *Introduction to Information Retrieval.* Cambridge. **Ücretsiz çevrimiçi ders kitabı.** 1, 2, 6 ve 8. bölümler projeyle doğrudan ilgili

### Vektörel arama
- ⭐ Karpukhin ve ark. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP
- Chen ve ark. (2024). *BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings.* arXiv
- Malkov & Yashunin (2018). *Efficient and Robust Approximate Nearest Neighbor Search Using HNSW Graphs.* IEEE TPAMI

### Birleştirme (fusion): projenin çekirdeği
- ⭐ Cormack, Clarke & Büttcher (2009). *Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods.* SIGIR. **RRF**
- ⭐ Bruch, Gai & Ingber (2023). *An Analysis of Fusion Functions for Hybrid Retrieval.* ACM TOIS. **RRF ile doğrusal birleştirmenin karşılaştırması. Bizim projeye en yakın makale**
- Fox & Shaw (1994). *Combination of Multiple Searches.* TREC-2. **CombSUM, CombMNZ**
- Bassani & Romelli (2022). *ranx.fuse: A Python Library for Metasearch.* CIKM. **Fusion yöntemleri kataloğu**

### Yeniden sıralama ve gelişmiş yöntemler
- ⭐ Nogueira & Cho (2019). *Passage Re-ranking with BERT.* arXiv. **Cross-encoder reranking**
- Formal ve ark. (2021). *SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking.* SIGIR
- Khattab & Zaharia (2020). *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT.* SIGIR
- Gao ve ark. (2022). *Precise Zero-Shot Dense Retrieval without Relevance Labels.* **HyDE**
- Dinamik α için: Google Scholar'da *"dynamic alpha" hybrid retrieval* ve *"query-adaptive fusion"* diye arayın. 2024–2025'te bu yönde çalışmalar var

### Değerlendirme
- ⭐ Thakur ve ark. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS Datasets & Benchmarks
- Es ve ark. (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation.* arXiv
- Bassani (2022). *ranx: A Blazing-Fast Python Library for Ranking Evaluation and Comparison.* ECIR
- Smucker, Allan & Carterette (2007). *A Comparison of Statistical Significance Tests for Information Retrieval Evaluation.* CIKM

> **Makale okuma yöntemi:** Önce özet, giriş ve sonuç kısmını okuyun. Sonra şekil ve tablolara bakın. Ancak gerekirse yöntem bölümünü okuyun. Her makale için `docs/literatur/` altına 5 satırlık özet yazın: problem, yöntem, sonuç, bizim projeye etkisi.

## 10.2 Dokümantasyonlar

| Konu | Kaynak |
|---|---|
| Python proje yönetimi | docs.astral.sh/uv |
| Embedding ve cross-encoder | sbert.net |
| Model karşılaştırma | MTEB Leaderboard (Hugging Face) |
| Hugging Face temel kurs | huggingface.co/learn |
| Vektör veritabanı | qdrant.tech/documentation |
| BM25 kütüphanesi | github.com/xhluca/bm25s |
| Metrikler ve fusion | github.com/AmenRa/ranx |
| Yerel LLM | ollama.com |
| API | fastapi.tiangolo.com |
| Docker | docs.docker.com/get-started |
| Git dalları (interaktif) | learngitbranching.js.org |

## 10.3 Sözlük

| Terim | Türkçe | Kısa açıklama |
|---|---|---|
| **ANN** (Approximate Nearest Neighbor) | Yaklaşık en yakın komşu | Vektör aramasını hızlandıran, az bir doğruluktan ödün veren algoritmalar |
| **Bi-encoder** | Çift kodlayıcı | Soru ve belgeyi ayrı ayrı vektöre çeviren model. Hızlı |
| **BM25** | — | Kelime eşleşmesine dayalı standart sıralama fonksiyonu |
| **Chunk** | Parça | Belgenin bölündüğü küçük metin birimi |
| **Context window** | Bağlam penceresi | LLM'in tek seferde okuyabildiği en fazla token sayısı |
| **Corpus** | Korpus, derlem | Arama yapılan belge koleksiyonu |
| **Cosine similarity** | Kosinüs benzerliği | İki vektör arasındaki açıya dayalı benzerlik ölçüsü |
| **Cross-encoder** | Çapraz kodlayıcı | Soru ve belgeyi birlikte okuyup puanlayan model. İsabetli ama yavaş |
| **Dense retrieval** | Yoğun arama | Embedding vektörleriyle yapılan anlamsal arama |
| **Dev/Test split** | Geliştirme/Test bölmesi | Parametre ayarı ve final ölçümü için ayrılmış soru kümeleri |
| **Embedding** | Gömme, vektör temsili | Metnin anlamını temsil eden sayı dizisi |
| **Fusion** | Birleştirme | Birden fazla sonuç listesini tek listede birleştirme |
| **Ground truth** | Doğru etiket | Test setindeki "doğru cevap" bilgisi |
| **Hallucination** | Halüsinasyon | LLM'in kaynağa dayanmayan, uydurma bilgi üretmesi |
| **HNSW** | — | En yaygın ANN algoritması. Katmanlı graf yapısı kullanır |
| **Hybrid search** | Hibrit arama | Seyrek (kelime) ve yoğun (vektör) aramanın birleşimi |
| **IDF** | Ters belge frekansı | Bir kelimenin ne kadar nadir, yani ayırt edici olduğu |
| **Ingestion** | Veri alımı | Belgelerin toplanıp işlenip indekslenmesi |
| **Inverted index** | Ters indeks | Kelimeden belgeye giden dizin |
| **Learning-to-Rank (LTR)** | Öğrenerek sıralama | Sıralama fonksiyonunu makine öğrenmesiyle öğrenme |
| **Lemmatization** | Gövdeleme | Kelimenin sözlükteki kök hâlini morfolojik analizle bulma |
| **MRR** | Ortalama ters sıra | İlk doğru sonucun sırasının tersinin ortalaması |
| **nDCG** | Normalize indirimli kümülatif kazanç | Dereceli ilgililiği ve sırayı birlikte ölçen metrik |
| **Pooling** | Havuzlama | Birçok sistemin üst sonuçlarını birleştirip elle etiketleme |
| **Prompt** | İstem | LLM'e verilen talimat ve bağlam metni |
| **Prompt injection** | İstem enjeksiyonu | Belge ya da kullanıcı girdisi içine gizlenmiş kötü niyetli talimat |
| **qrels** | İlgililik etiketleri | Soru-belge-ilgililik derecesi üçlüleri |
| **Quantization** | Nicemleme | Model ağırlıklarını düşük bit sayısına indirip küçültme |
| **RAG** | Erişimle güçlendirilmiş üretim | Belge bulup LLM'e bağlam olarak verme yöntemi |
| **Recall@k** | Duyarlılık@k | İlgili belgelerin ilk k sonuçta bulunma oranı |
| **Reranking** | Yeniden sıralama | Aday listeyi daha güçlü bir modelle yeniden sıralama |
| **RRF** | — | Sıralara dayalı birleştirme yöntemi |
| **Run** | Çalıştırma çıktısı | Bir sistemin tüm sorular için döndürdüğü sıralı listeler |
| **Sparse retrieval** | Seyrek arama | Kelime tabanlı arama (BM25, SPLADE) |
| **Stemming** | Kök bulma | Kelimenin eklerini kurallarla kesme |
| **Stopword** | Durak kelime | "ve, ile, bu" gibi bilgi taşımayan sık kelimeler |
| **Token** | Belirteç | Metnin işlenen en küçük birimi |
| **Vector DB** | Vektör veritabanı | Vektörleri saklayıp hızlı benzerlik araması yapan veritabanı |
