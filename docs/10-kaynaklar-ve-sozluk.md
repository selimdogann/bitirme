# 10. Kaynaklar ve Sözlük

---

## 10.1 Okunacak makaleler

⭐ işaretliler mutlaka okunmalı ve raporun literatür bölümünde yer almalı.

### Projemize en yakın çalışmalar
- ⭐ Jamil, Kavak, **İlhan Omurca**, Fotouhi (2026). *Design and Evaluation of a Source-Grounded Medical LLM for Clinical Decision Support and Patient Care in Trustworthy Diagnostic Systems.* Diagnostics. [doi:10.3390/diagnostics16193142](https://doi.org/10.3390/diagnostics16193142). **Danışmanımızın TurkishMedLLM çalışması:** 210.791 Türkçe tıbbi soru-cevap ve 22.135 hastane makalesi üzerinde vektör tabanlı RAG
- ⭐ Xiong, Jin, Lu, Zhang (2024). *Benchmarking Retrieval-Augmented Generation for Medicine.* [arXiv:2402.13178](https://arxiv.org/abs/2402.13178). **MedRAG:** tıpta BM25, MedCPT ve bunların RRF ile birleşimi
- ⭐ Bruch, Gai, Ingber (2023). *An Analysis of Fusion Functions for Hybrid Retrieval.* ACM TOIS. [arXiv:2210.11934](https://arxiv.org/abs/2210.11934). **RRF ile doğrusal birleştirmenin karşılaştırması:** doğrusal birleştirme daha iyi ve az örnekle ayarlanabiliyor
- Aljohani, Alsanoosy (2026). *Enhancing Medical Question Answering with LLMs via a Hybrid Retrieval-Augmented Generation Framework.* Information. [doi:10.3390/info17020133](https://doi.org/10.3390/info17020133). Tıbbi soru-cevapta BM25 + MedCPT
- Köse ve ark. (2026). *RAGTurk: Best Practices for Retrieval Augmented Generation in Turkish.* SIGTURK. [ACL Anthology](https://aclanthology.org/2026.sigturk-1.15/). Türkçe RAG aşamalarının karşılaştırması
- Sun ve ark. (2026). *Retrieval-augmented generation for medication safety: A case study using drug package inserts.* Int. J. Medical Informatics. [PubMed](https://pubmed.ncbi.nlm.nih.gov/42435614/). İlaç kullanma talimatlarıyla RAG; uzman denetiminin gerekliliği
- Lu, Ma, Hall (2022). *Zero-shot Hybrid Retrieval and Reranking Models for Biomedical Literature.* CLEF. [Google Research](https://research.google/pubs/zero-shot-hybrid-retrieval-and-reranking-models-for-biomedical-literature/). Biyomedikal aramada hibrit ve RRF

### Temeller
- ⭐ Lewis ve ark. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS. **RAG'i tanımlayan makale**
- ⭐ Robertson & Zaragoza (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in IR
- ⭐ Cormack, Clarke & Büttcher (2009). *Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods.* SIGIR. **RRF**
- Karpukhin ve ark. (2020). *Dense Passage Retrieval for Open-Domain Question Answering.* EMNLP
- Manning, Raghavan & Schütze (2008). *Introduction to Information Retrieval.* Cambridge. Ücretsiz çevrimiçi ders kitabı; 1, 2, 6 ve 8. bölümler
- Thakur ve ark. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models.* NeurIPS
- Baysan & Güngör (2025). *TR-MTEB: A Comprehensive Benchmark and Embedding Model Suite for Turkish Sentence Representations.* EMNLP Findings. [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.471.pdf). Türkçe arama test setleri, NFCorpus-TR dahil

> **Makale okuma yöntemi:** Önce özet, giriş ve sonuç; sonra şekil ve tablolar; gerekirse yöntem bölümü. Her makale için `docs/literatur/` altına 5 satırlık özet yazın: problem, yöntem, sonuç, bizim projeye etkisi.

## 10.2 Veri setleri ve dokümantasyon

| Konu | Kaynak |
|---|---|
| Kullanma talimatları | [TİTCK KÜB / KT Sorgulama Portalı](https://www.titck.gov.tr/kubkt) |
| Türkçe tıbbi soru-cevap | [MedTurkQuAD](https://huggingface.co/datasets/incidelen/MedTurkQuAD) |
| Türkçe tıbbi arama testi | [NFCorpus-TR](https://huggingface.co/datasets/trmteb/nfcorpus-tr) |
| Türkçe sağlık arama testi | [TurkishRAGEval](https://huggingface.co/datasets/mteb/turkish-rag-eval) |
| Yedek korpus | [Türk hastane makaleleri](https://huggingface.co/datasets/alibayram/turkish-hospital-medical-articles) |
| Python proje yönetimi | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| Arayüz | [docs.streamlit.io](https://docs.streamlit.io) |
| Embedding | [sbert.net](https://sbert.net) |
| Model karşılaştırma | [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) |
| BM25 kütüphanesi | [github.com/xhluca/bm25s](https://github.com/xhluca/bm25s) |
| Yerel dil modeli | [ollama.com](https://ollama.com) |
| Git dalları (interaktif) | [learngitbranching.js.org](https://learngitbranching.js.org) |

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
