# 8. Yol Haritası

Proje 11 faza bölündü. Her fazın **öğrenme hedefleri, görevleri, teslimi ve bitti sayılma koşulu** var.

**Kurallar:**
- Bir faz bitmeden sonrakine geçilmez. Bitti sayılma koşulu karşılanmalı.
- Her fazın sonunda sistem **çalışır durumda** olmalı.
- Her fazın sonunda **anlat-öğret oturumu** yapılır: her biriniz o fazda diğerinin yazdığı kısmı anlatır.
- Süreler tahminidir. Bölümün bitirme takvimine (ara rapor, final teslim) göre uyarlayın.

```
Ekim          Kasım          Aralık         Ocak           Şubat          Mart           Nisan          Mayıs
│ F0 │── F1 ──│── F2 ──│─ F3 ─│── F4 ──│─ F5 ─│(sınav)│── F6 ──│─ F7 ─│──── F8 ────│──── F9 ────│─ F10 ─│
 hazır  korpus   veri+    BM25   vektör  fusion          rerank   LLM    API+arayüz    ürün        rapor
                 test                    ▲                 +dinamik α                               ▲
                                    ara rapor?                                                    final
```

---

## Faz 0: Hazırlık (1 hafta)

**Öğrenme hedefleri:** Git ve GitHub ile birlikte çalışmak, Python proje yapısı, uv, kod stili araçları.

**Görevler:**
- [ ] Zehra'yı repoya *collaborator* olarak ekle
- [ ] İkiniz de repoyu klonlayın, `uv` kurun
- [ ] `pyproject.toml`, `.gitignore`, `.env.example`, `src/hybridrag/__init__.py` oluşturun
- [ ] `ruff` ve `pre-commit` kurun
- [ ] GitHub'da **Project (Kanban) panosu** açın, fazları *milestone* olarak ekleyin
- [ ] `main` dalını koruma altına alın (PR'sız doğrudan push yasak)
- [ ] [Temel Kavramlar](02-temel-kavramlar.md) dokümanını okuyun, "Kendinizi test edin" sorularını birbirinize sorun
- [ ] Hocayla görüşüp [Proje Tanımı → teyit soruları](01-proje-tanimi.md#17-hocaya-teyit-ettirilecek-sorular) bölümünü cevaplayın

**Teslim:** Boş ama düzgün kurulmuş bir proje iskeleti. İkinizin de açtığı ve birbirinizin onayladığı en az bir PR.
**Bitti sayılır:** İkiniz de kendi bilgisayarınızda `uv run python -c "import hybridrag"` komutunu çalıştırabiliyorsunuz.

---

## Faz 1: Korpus araştırması ve sektör seçimi (2–3 hafta)

**Öğrenme hedefleri:** Açık veri kaynakları, veri lisansları, korpus özelliklerinin hibrit aramaya etkisi.

**Görevler:** [Korpus Araştırması](05-korpus-arastirmasi.md) dokümanındaki süreç.
- [ ] En az 6 sektör için kaynak envanteri
- [ ] En iyi 3 aday için örneklem indirme ve 20'şer örnek soru
- [ ] Puanlama matrisi
- [ ] Korpus raporu ve hoca onayı

**Teslim:** `docs/korpus-raporu.md`
**Bitti sayılır:** Sektör ve yedek sektör hocayla onaylandı.

---

## Faz 2: Veri hattı ve test seti (3 hafta)

**Öğrenme hedefleri:** Web'den veri toplama, HTML/PDF ayrıştırma, metin temizleme, parçalama stratejileri, test seti tasarımı.

**Görevler:**
- [ ] `scripts/download.py`: kaynaktan veri indirme (hız sınırlamalı, kaldığı yerden devam edebilen)
- [ ] `ingestion/parsers.py`: HTML/PDF'ten metin ve yapı (başlık, madde) çıkarma
- [ ] `ingestion/cleaning.py`: Unicode normalizasyonu, gürültü temizliği
- [ ] `ingestion/chunking.py`: **en az 2 strateji** (sabit boyut + yapısal)
- [ ] Çıktı biçimi: `data/processed/chunks.jsonl`
- [ ] Korpus istatistikleri notebook'u (belge sayısı, uzunluk dağılımı, kelime frekansları)
- [ ] **Paralel iş:** Test setinin ilk 100 sorusu ve etiketleme kılavuzu ([Değerlendirme §7.1](07-degerlendirme.md#71-test-seti))

**Teslim:** Temiz korpus + korpus istatistikleri + 100 soruluk test seti v0.
**Bitti sayılır:** Tek komutla (`uv run python scripts/build_corpus.py`) sıfırdan korpus üretilebiliyor.

---

## Faz 3: Kelime tabanlı arama, BM25 (2 hafta)

**Öğrenme hedefleri:** Ters indeks, TF-IDF, BM25 matematiği, Türkçe ön işleme, birim testi, metrik hesaplama.

**Görevler:**
- [ ] `text/turkish.py`: Türkçe küçük harf, normalizasyon, stopword listesi, kök bulma (Snowball). **Birim testleriyle**
- [ ] `retrieval/bm25.py`: **Önce sıfırdan kendi BM25'imiz**, sonra `bm25s` ile hızlı sürüm
- [ ] İki sürümün aynı sonucu verdiğini gösteren test
- [ ] `evaluation/metrics.py`: Recall, MRR, nDCG. Kendi yazdığımız sürüm `ranx` ile karşılaştırılarak test edilecek
- [ ] `evaluation/runner.py`: YAML yapılandırmasından deney çalıştırma (ilk sürüm)
- [ ] **Deney:** Ön işleme yok / küçük harf / + stopword / + Snowball / + Zeyrek → BM25 sonuçları (AS3)
- [ ] **Deney:** k1 ve b parametre taraması
- [ ] GitHub Actions: her PR'da `pytest` + `ruff`

**Teslim:** BM25 arayıcı + ilk deney sonuçları tablosu.
**Bitti sayılır:** `uv run python -m hybridrag.evaluation.runner experiments/configs/bm25.yaml` çalışıyor ve metrikleri yazdırıyor.

---

## Faz 4: Vektörel arama (2–3 hafta)

**Öğrenme hedefleri:** Embedding, kosinüs benzerliği, bi-encoder, ANN/HNSW, Docker, vektör veritabanı.

**Görevler:**
- [ ] `retrieval/dense.py`: önce **NumPy ile brute force** arama
- [ ] 4–5 embedding modelini test setinde karşılaştırma (başarı + hız + lisans). Bkz. [Teknolojiler §4.2](04-teknolojiler.md#modeller-adaylar-ölçerek-seçilecek)
- [ ] Büyük korpus için embedding'i Colab/Kaggle GPU'da üretme betiği
- [ ] `docker-compose.yml`: Qdrant servisi
- [ ] Qdrant'a geçiş. Brute force ile Qdrant'ın sonuçlarını ve hızlarını karşılaştırma (ANN ne kadar doğruluk kaybettiriyor?)
- [ ] **Deney:** Parçalama stratejisi × embedding modeli

**Teslim:** Dense arayıcı + model karşılaştırma tablosu + seçilen model ve gerekçesi.
**Bitti sayılır:** BM25 ve dense, aynı runner ile aynı test setinde ölçülebiliyor.

---

## Faz 5: Hibrit birleştirme v1 (2–3 hafta) ⭐ projenin kalbi

**Öğrenme hedefleri:** Sıra ve puan tabanlı fusion, normalizasyon, deney tasarımı, istatistiksel anlamlılık, deney takibi.

**Görevler:** [Birleştirme Yöntemleri](06-birlestirme-yontemleri.md)
- [ ] `fusion/base.py` arayüzü
- [ ] `fusion/rrf.py`, `fusion/linear.py`, `fusion/comb.py`, `fusion/normalization.py`
- [ ] Her yöntem için `ranx.fuse` ile karşılaştırma testi
- [ ] `pipeline.py`: `HybridPipeline` (BM25 ve dense paralel çalışır)
- [ ] MLflow ile deney takibi
- [ ] Test setini 200+ soruya çıkarma ve havuzlama (pooling) ile eksik etiketleri tamamlama
- [ ] **Deney 1** ([§6.6](06-birlestirme-yontemleri.md#66-deney-planı)): tüm yöntemler, α eğrisi, k duyarlılığı, soru tipine göre kırılım, anlamlılık testleri
- [ ] Hata analizi notları
- [ ] Streamlit ile basit demo: soru gir, BM25 / dense / hibrit sonuçlarını yan yana gör

**Teslim:** Ana sonuç tablosu + grafikler + demo. **Ara rapor/sunum için ideal nokta.**
**Bitti sayılır:** AS1 ve AS2'ye verilerle cevap verebiliyorsunuz.

---

## Faz 6: Reranking ve gelişmiş birleştirme (3 hafta)

**Öğrenme hedefleri:** Cross-encoder, iki aşamalı arama, öznitelik mühendisliği, basit makine öğrenmesi modeli eğitme.

**Görevler:**
- [ ] `rerank/cross_encoder.py`
- [ ] **Deney 2:** fusion × reranker × aday sayısı (AS4)
- [ ] DBSF ve sorgu tipine göre yönlendirme
- [ ] **Dinamik α** (AS5): öznitelik çıkarma → en iyi α'yı tahmin eden model → dev bölümünde eğitim, test bölümünde ölçüm
- [ ] (İsteğe bağlı) BGE-M3 sparse ile üçüncü arayıcı
- [ ] (İsteğe bağlı) Multi-query / HyDE

**Teslim:** Gelişmiş sonuç tablosu + özgün katkı analizi.
**Bitti sayılır:** AS4 ve AS5 cevaplandı.

---

## Faz 7: Cevap üretimi, LLM (2 hafta)

**Öğrenme hedefleri:** Yerel LLM çalıştırma, istem mühendisliği, kaynak gösterme, halüsinasyonu ölçme.

**Görevler:**
- [ ] Ollama kurulumu, 2–3 Türkçe yetenekli modeli deneme
- [ ] `generation/llm_client.py`: OpenAI uyumlu tek arayüz
- [ ] `generation/prompts.py`: kaynak gösteren ve gerektiğinde reddeden istem şablonu
- [ ] Akış (streaming) desteği
- [ ] RAGAS + elle değerlendirme ([§7.3](07-degerlendirme.md#73-cevap-generation-metrikleri-faz-7))
- [ ] **Deney:** Arama kalitesi (BM25 / dense / hibrit / hibrit+rerank) cevap kalitesini nasıl etkiliyor?
- [ ] (İsteğe bağlı) Aynı pipeline'ı LlamaIndex ile kurup karşılaştırma

**Teslim:** Uçtan uca RAG: soru → kaynaklı cevap.
**Bitti sayılır:** Streamlit demosunda kaynaklı cevap görünüyor.

---

## Faz 8: API ve uygulama (3 hafta)

**Öğrenme hedefleri:** REST API tasarımı, async programlama, ilişkisel veritabanı, konteynerleştirme.

**Görevler:**
- [ ] `api/`: FastAPI. Uç noktalar: `POST /search`, `POST /ask` (akışlı), `GET /documents/{id}`, `POST /feedback`, `GET /health`
- [ ] Pydantic şemaları, hata yönetimi, girdi doğrulama
- [ ] PostgreSQL + SQLAlchemy + Alembic: belgeler, sorgu kayıtları, geri bildirimler
- [ ] Yeni belge yükleme → arka planda indeksleme
- [ ] API için entegrasyon testleri
- [ ] `docker-compose.yml`: api + qdrant + postgres + ollama
- [ ] Streamlit'i API'ye bağlama

**Teslim:** `docker compose up` ile çalışan uygulama + Swagger dokümantasyonu.
**Bitti sayılır:** Temiz bir bilgisayarda README'deki adımlarla 15 dakikada kurulabiliyor.

---

## Faz 9: Ürünleştirme (3–4 hafta)

**Öğrenme hedefleri:** Modern frontend, kimlik doğrulama, önbellek, gözlemlenebilirlik, CI/CD, güvenlik, canlıya alma.

**Görevler:**
- [ ] `frontend/`: Next.js + TypeScript + Tailwind
  - Soru-cevap ekranı (akışlı cevap, tıklanabilir kaynaklar, kaynağın belgede vurgulanması)
  - Belge kütüphanesi ve yükleme
  - Geri bildirim (👍/👎 + yorum)
  - Yönetici paneli: sorgu istatistikleri, gecikme, en çok sorulanlar
- [ ] Kimlik doğrulama (JWT) ve rol tabanlı yetki (kullanıcı / yönetici)
- [ ] Redis ile önbellek
- [ ] Langfuse ile LLM izleme
- [ ] **Güvenlik:** istem enjeksiyonu (prompt injection) testleri, hız sınırlama, KVKK uyumu (kişisel veri maskeleme, kayıtların saklama süresi)
- [ ] CI/CD: test → Docker imajı → sunucuya dağıtım
- [ ] Yük testi (ör. `locust`): eşzamanlı 20 kullanıcıda p95 gecikmesi
- [ ] Canlı ortam: bir sunucuda (VPS) demo adresi

**Teslim:** Canlı demo adresi + ürün dokümantasyonu.
**Bitti sayılır:** Projeyi hiç görmemiş bir arkadaşınız arayüzü yardımsız kullanabiliyor.

---

## Faz 10: Rapor, sunum ve savunma (2–3 hafta)

**Görevler:**
- [ ] Bitirme raporu: giriş, literatür, yöntem, deneyler, sonuçlar, tartışma, sonuç. `experiments/notes/` ve sonuç tabloları burada kullanılır
- [ ] Sunum ve canlı demo senaryosu (internet kesilirse diye video yedeği)
- [ ] Repo temizliği: README, kurulum, lisans, ekran görüntüleri
- [ ] **Savunma provası:** Birbirinize jüri gibi soru sorun. Herhangi bir modülü ikiniz de anlatabilmelisiniz
- [ ] (İsteğe bağlı) Sonuçları bir konferans bildirisine (ör. ASYU, SIU, UBMK) ya da arXiv'e dönüştürme

---

## Zaman kalırsa (Faz 11+)

- GraphRAG ile üçüncü bir kaynak (Selim'in [arsiv-zekasi-graphrag](https://github.com/selimdogann/arsiv-zekasi-graphrag) deneyimi)
- Embedding modelini kendi korpusumuza göre ince ayarlama (fine-tuning)
- Kullanıcı geri bildirimleriyle Learning-to-Rank
- Çoklu kiracı (multi-tenant): her müşteriye ayrı belge alanı
- İkinci sektöre genişleme: genelleme testi
