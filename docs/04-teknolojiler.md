# 4. Teknolojiler

Bu doküman projede kullanacağımız her teknolojiyi listeler. Her teknoloji için **ne olduğu, neden seçildiği, alternatifi ve ne zaman öğrenileceği** yazar.

> **Not:** Model adları ve sürümleri hızla değişir. Burada yazanlar **başlangıç adaylarıdır**. Son karar her zaman **kendi test setimizde yapacağımız ölçümle** verilecek.

---

## 4.1 Genel bakış

```
┌────────────────────────────────────────────────────────────────────┐
│ ARAYÜZ       Streamlit (prototip)  →  Next.js + TypeScript (ürün)  │
├────────────────────────────────────────────────────────────────────┤
│ API          FastAPI · Pydantic · Uvicorn                          │
├────────────────────────────────────────────────────────────────────┤
│ ÇEKİRDEK     Python 3.12 · hybridrag paketi                        │
│              BM25: kendi kodumuz → bm25s                           │
│              Embedding: sentence-transformers (bge-m3, e5, ...)    │
│              Reranker: cross-encoder (bge-reranker-v2-m3, ...)     │
│              Fusion: kendi kodumuz (+ ranx ile doğrulama)          │
│              LLM: Ollama (Qwen, Gemma, Llama ...)                  │
├────────────────────────────────────────────────────────────────────┤
│ VERİ         Qdrant (vektör) · PostgreSQL (meta veri, log)         │
│              Redis (önbellek, v3)                                  │
├────────────────────────────────────────────────────────────────────┤
│ DEĞERLENDİRME ranx · pandas · matplotlib · RAGAS · MLflow          │
├────────────────────────────────────────────────────────────────────┤
│ ALTYAPI      uv · Git/GitHub · Docker Compose · GitHub Actions     │
│              pytest · ruff · mypy · pre-commit · Langfuse          │
└────────────────────────────────────────────────────────────────────┘
```

## 4.2 Ayrıntılı tablo

### Dil ve geliştirme ortamı

| Teknoloji | Ne işe yarar | Neden bu | Alternatif | Faz |
|---|---|---|---|---|
| **Python 3.12** | Ana dil | Yapay zekâ ve bilgi erişimi ekosisteminin tamamı Python'da | — | 0 |
| **uv** | Paket ve sanal ortam yöneticisi | Çok hızlı, `pyproject.toml` + kilit dosyası ile ikinizde de birebir aynı ortam | pip + venv, Poetry | 0 |
| **Git + GitHub** | Sürüm kontrolü, iş birliği | Zorunlu | — | 0 |
| **VS Code** | Editör | İkiniz de kullanıyorsunuz, Python + Jupyter desteği | PyCharm | 0 |
| **Jupyter** | Keşif ve analiz | Veriyi görerek tanımak için | — | 0 |

### Veri toplama ve ayrıştırma

| Teknoloji | Ne işe yarar | Neden bu | Alternatif | Faz |
|---|---|---|---|---|
| **httpx** | HTTP istekleri | Modern, async destekli | requests | 1–2 |
| **Playwright** | JavaScript ile yüklenen sayfaları gezme | Bazı kamu siteleri dinamik | Selenium | 2 (gerekirse) |
| **trafilatura** | HTML'den ana metni çıkarma | Menü ve reklam gibi gürültüyü iyi temizler | BeautifulSoup (elle) | 2 |
| **PyMuPDF** | PDF'ten metin çıkarma | Hızlı, sayfa ve konum bilgisi verir | pdfplumber | 2 |
| **Docling** | Karmaşık PDF (tablo, düzen) ayrıştırma | Yapıyı (başlık, tablo) korur | Unstructured | 2 (gerekirse) |

### Türkçe metin işleme

| Teknoloji | Ne işe yarar | Neden bu | Alternatif | Faz |
|---|---|---|---|---|
| **Kendi `turkish.py`'miz** | Türkçe küçük harf, normalizasyon | Python'un `lower()` fonksiyonu Türkçede hatalı | — | 3 |
| **snowballstemmer** (Turkish) | Kural tabanlı kök bulma | Hafif, hızlı | — | 3 |
| **Zeyrek** | Morfolojik analiz (Zemberek'in Python portu) | Daha doğru kök bulur | Zemberek (Java) | 3 (deney) |

### Arama

| Teknoloji | Ne işe yarar | Neden bu | Alternatif | Faz |
|---|---|---|---|---|
| **Kendi BM25'imiz** | Öğrenme amaçlı BM25 | Algoritmayı içinden anlamak için | — | 3 |
| **bm25s** | Üretim için hızlı BM25 | Saf Python ve çok hızlı | rank_bm25 (yavaş), OpenSearch | 3 |
| **sentence-transformers** | Embedding ve cross-encoder modellerini çalıştırma | Standart kütüphane, Hugging Face ile entegre | Hugging Face transformers (alt seviye) | 4 |
| **NumPy (brute force)** | Öğrenme amaçlı vektör arama | İşin özünü görmek için | FAISS | 4 |
| **Qdrant** | Vektör veritabanı | Açık kaynak, Docker ile tek komutla kurulur, filtreleme ve seyrek (sparse) vektör desteği var, Rust ile yazılmış ve hızlı | pgvector, Milvus, Weaviate, Chroma | 4 |
| **OpenSearch** | Hem BM25 hem vektör içeren arama motoru | Ürün aşamasında Türkçe analizörüyle BM25'i ölçeklemek için | Elasticsearch | 9 (isteğe bağlı) |

### Modeller (adaylar, ölçerek seçilecek)

| Tür | Aday | Lisans (kontrol edin!) | Not |
|---|---|---|---|
| Embedding | `BAAI/bge-m3` | MIT | Çok dilli, 8192 token, aynı modelden dense + sparse + çok-vektör çıktısı |
| Embedding | `intfloat/multilingual-e5-large` | MIT | Güçlü temel model. Girdilere `query:` / `passage:` öneki ister |
| Embedding | `Qwen/Qwen3-Embedding-0.6B` (ve büyükleri) | Apache 2.0 | Yeni nesil, çok dilli |
| Embedding | `google/embeddinggemma-300m` | Gemma şartları | Küçük ve hızlı |
| Embedding | Türkçeye ince ayarlı modeller | Değişken | Hugging Face'te "turkish sentence embedding" diye arayın |
| Reranker | `BAAI/bge-reranker-v2-m3` | Apache 2.0 | Çok dilli cross-encoder, başlangıç için ideal |
| Reranker | `Qwen/Qwen3-Reranker-0.6B` | Apache 2.0 | Yeni nesil |
| Reranker | `jinaai/jina-reranker-v2-base-multilingual` | **CC-BY-NC**: ticari kullanıma kapalı | Sadece akademik karşılaştırma için |
| LLM | Qwen3 (4B / 8B / 14B) | Apache 2.0 | Türkçesi iyi |
| LLM | Gemma 3 (4B / 12B) | Gemma şartları | Türkçesi iyi |
| LLM | Llama 3.x (8B) | Llama lisansı | Yaygın |
| LLM | Türkçe odaklı modeller (ör. ytu-ce-cosmos) | Değişken | Denenebilir |

> **Lisans kuralı:** Ürünü piyasaya sürebilmek için kullandığımız **her model ve veri setinin lisansı ticari kullanıma izin vermeli**. Seçilen her modelin lisansını bu tabloya ve rapora yazın.

**Model seçim yöntemi (Faz 4):**
1. [MTEB liderlik tablosunda](https://huggingface.co/spaces/mteb/leaderboard) çok dilli ya da Türkçe retrieval görevlerinde iyi olan 4–5 adayı seçin.
2. Hepsiyle **kendi test setimizde** Recall@10 ve nDCG@10 ölçün.
3. Hız (parça/saniye) ve bellek kullanımını da kaydedin.
4. Başarı, hız ve lisansa birlikte bakarak karar verin.

### LLM çalıştırma

| Teknoloji | Ne işe yarar | Neden bu | Alternatif | Faz |
|---|---|---|---|---|
| **Ollama** | Açık modelleri yerelde çalıştırma | Tek komutla kurulum, Mac'te Metal GPU desteği, OpenAI uyumlu API | llama.cpp, LM Studio | 7 |
| **vLLM** | Üretimde yüksek verimli LLM sunucusu | Çok kullanıcıda hızlı | TGI | 9 (GPU sunucuda) |
| **Ticari API** (Claude, GPT) | Karşılaştırma ve yedek | Kaliteyi kıyaslamak için | — | 7 (hoca izin verirse) |

> LLM istemcisini, OpenAI uyumlu API üzerinden **tek bir arayüzle** yazın. Böylece Ollama, vLLM ve ticari API arasında yalnızca yapılandırmayla geçiş yapılır.

### Değerlendirme ve deney

| Teknoloji | Ne işe yarar | Neden bu | Faz |
|---|---|---|---|
| **Kendi `metrics.py`'miz** | Recall, MRR, nDCG | Formülleri içinden anlamak için | 2–3 |
| **ranx** | Bilgi erişimi metrikleri, istatistiksel testler, **hazır fusion yöntemleri** | Kendi kodumuzun sonuçlarını doğrulamak için birebir uygun | 3–6 |
| **pandas, matplotlib, seaborn** | Sonuç tabloları ve grafikler | Standart | 3+ |
| **RAGAS** | Üretilen cevabın kalitesi (sadakat, ilgililik) | LLM cevabını ölçmek için | 7 |
| **MLflow** | Deney takibi (parametre, metrik, çıktı) | Yüzlerce deneyi karıştırmamak için | 5+ |

### API, arayüz, ürün

| Teknoloji | Ne işe yarar | Neden bu | Alternatif | Faz |
|---|---|---|---|---|
| **FastAPI** | REST API | Hızlı, otomatik dokümantasyon (Swagger), Pydantic ile tip güvenliği | Flask, Django | 8 |
| **Streamlit** | Hızlı prototip arayüz | Birkaç satır Python ile demo, hocaya göstermek için ideal | Gradio | 5–8 |
| **Next.js + TypeScript + Tailwind** | Ürün arayüzü | Selim'in deneyimi var (maas-radar), modern ve hızlı | Angular (Selim stajda kullandı), React + Vite | 9 |
| **PostgreSQL** | Kullanıcılar, belgeler, sorgu geçmişi | Güvenilir, standart | — | 8–9 |
| **SQLAlchemy + Alembic** | ORM ve veritabanı göçleri (migration) | Python standardı | SQLModel | 8–9 |
| **Redis** | Önbellek (aynı soruya tekrar LLM çağırmamak) | Basit, hızlı | — | 9 |
| **JWT / OAuth2** | Kullanıcı girişi | FastAPI ile yerleşik destek | — | 9 |

### Altyapı ve kalite

| Teknoloji | Ne işe yarar | Faz |
|---|---|---|
| **Docker + Docker Compose** | Tüm servisleri tek komutla ayağa kaldırma | 4 (Qdrant ile başlar), 8–9 (tamamı) |
| **pytest** | Birim ve entegrasyon testleri | 3+ |
| **ruff** | Lint ve format (kod stili) | 0 |
| **mypy** | Tip kontrolü | 3+ |
| **pre-commit** | Commit öncesi otomatik kontrol | 0 |
| **GitHub Actions** | Her PR'da test ve lint çalıştırma (CI) | 3+ |
| **Langfuse** | LLM çağrılarını izleme (istem, cevap, süre, maliyet) | 9 |

## 4.3 Neden LangChain / LlamaIndex ile başlamıyoruz?

Bu kütüphaneler RAG'i birkaç satırda kurmanızı sağlar. Ama:

1. **Öğrenme hedefimize ters.** Her şeyi kapalı kutuda yaparlar. "Fusion nasıl çalışıyor?" sorusuna cevap veremeyiz.
2. **Deney kontrolü zor.** Bilimsel karşılaştırma için her adımı (normalizasyon, k değeri, sıralama) ayrı ayrı kontrol etmemiz gerekiyor.
3. **Projenin çekirdeği zaten bizim yazacağımız kısım.** Arama, birleştirme ve değerlendirme. Bunları bir kütüphaneye devredersek projede "biz" kalmaz.

**Plan:** Çekirdeği kendimiz yazacağız. Faz 7 civarında aynı pipeline'ı LlamaIndex ile de kurup **kendi kodumuzla karşılaştırmak** raporda güzel bir bölüm olur.

## 4.4 Donanım ihtiyacı

| İş | Mac (Apple Silicon) | Ne zaman bulut GPU |
|---|---|---|
| BM25 indeksleme ve arama | Rahat | Hiçbir zaman |
| Embedding, küçük korpus (< 50 bin parça) | Olur (MPS hızlandırma) | — |
| Embedding, büyük korpus veya çok model karşılaştırması | Yavaş | **Google Colab / Kaggle** (ücretsiz GPU). Vektörleri dosyaya kaydedip indirin |
| Reranking deneyleri | Olur, yavaş | Çok deney varsa Colab |
| LLM (7–8B, 4-bit) | Olur (16 GB RAM ile rahat) | Canlıya alırken GPU sunucu |

## 4.5 Öğrenme sırası

Teknolojileri aynı anda değil, **ihtiyaç duyuldukça** öğreneceğiz:

```
Faz 0 : Git, GitHub, uv, ruff, Jupyter
Faz 1 : httpx, veri lisansları, Markdown raporlama
Faz 2 : trafilatura/PyMuPDF, JSONL, test seti tasarımı
Faz 3 : BM25 (elle), Türkçe NLP, pytest, bm25s, ranx
Faz 4 : embedding, sentence-transformers, NumPy, Docker, Qdrant
Faz 5 : fusion yöntemleri, normalizasyon, deney yapılandırması (YAML), MLflow
Faz 6 : cross-encoder, reranking
Faz 7 : Ollama, istem mühendisliği, RAGAS
Faz 8 : FastAPI, Streamlit, Docker Compose, PostgreSQL
Faz 9 : Next.js, kimlik doğrulama, Redis, CI/CD, Langfuse, canlıya alma
```
