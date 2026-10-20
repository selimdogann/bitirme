# 4. Teknolojiler

Bu doküman projede kullanacağımız her teknolojiyi, **ne işe yaradığını, neden seçildiğini ve hangi aşamada geleceğini** anlatır.

> **İlke:** İhtiyaç duymadan teknoloji eklemiyoruz. Her yeni araç bir sorunu çözdüğü için gelir.

---

## 4.1 Genel bakış

```
┌──────────────────────────────────────────────────────────────┐
│ ARAYÜZ        Streamlit                                       │
├──────────────────────────────────────────────────────────────┤
│ ÇEKİRDEK      Python 3.12                                     │
│               PDF okuma: pypdf                                │
│               BM25: kendi kodumuz (bm25s ile doğrulama)       │
│               Vektör: sentence-transformers + NumPy           │
│               Cevap: Ollama ile yerel dil modeli (Aşama 6)    │
├──────────────────────────────────────────────────────────────┤
│ GELİŞTİRME    uv · Git/GitHub · ruff · GitHub Actions         │
└──────────────────────────────────────────────────────────────┘
```

## 4.2 Ayrıntılı tablo

### Geliştirme ortamı

| Teknoloji | Ne işe yarıyor | Neden bu | Aşama |
|---|---|---|---|
| **Python 3.12** | Projenin dili | Yapay zekâ ve arama kütüphanelerinin hepsi Python'da. 3.12 kararlı ve kütüphanelerin hepsi destekliyor | 0 |
| **uv** | Python'u ve kütüphaneleri kurar, ortamı yönetir | Tek komutla ikimizde de birebir aynı ortam (`uv.lock`) | 0 |
| **Git + GitHub** | Sürüm kontrolü, PR ile ortak çalışma | Zorunlu | 0 |
| **ruff** | Kod stili ve sık hataları kontrol eder | Hızlı, tek araç; CI'da her PR'da çalışır | 0 |
| **GitHub Actions** | Her PR'da ruff'ı otomatik çalıştırır | Hatalı kod `main`'e girmesin | 0 |
| **VS Code** | Editör | İkimiz de kullanıyoruz | 0 |

### Veri

| Teknoloji | Ne işe yarıyor | Neden bu | Alternatif | Aşama |
|---|---|---|---|---|
| **pypdf** | PDF'ten metin çıkarır | Saf Python, kurulumu kolay | PyMuPDF (daha hızlı, düzen bilgisi verir) | 1 |
| **JSONL** | Parçaları satır satır saklar | Okunabilir, her satır bağımsız | CSV | 1 |

### Arama

| Teknoloji | Ne işe yarıyor | Neden bu | Aşama |
|---|---|---|---|
| **Kendi BM25'imiz** | Kelime eşleşmesiyle arama | Algoritmayı içinden anlamak için önce kendimiz yazıyoruz | 2 |
| **bm25s** | Hazır, hızlı BM25 | Kendi kodumuzun doğru sonuç verdiğini kontrol etmek için | 2 |
| **sentence-transformers** | Metni vektöre çeviren modelleri çalıştırır | Standart kütüphane, Hugging Face modelleriyle doğrudan çalışır | 3 |
| **NumPy** | Vektörler arası benzerliği hesaplar | Birkaç bin parça için yeterince hızlı, ayrı veritabanı gerekmiyor | 3 |

### Cevap üretimi

| Teknoloji | Ne işe yarıyor | Neden bu | Aşama |
|---|---|---|---|
| **Ollama** | Açık kaynak dil modelini kendi bilgisayarımızda çalıştırır | Veri dışarı çıkmaz, ücretsiz, Mac'te hızlı | 6 |

### Arayüz

| Teknoloji | Ne işe yarıyor | Neden bu | Aşama |
|---|---|---|---|
| **Streamlit** | Birkaç satır Python'la web arayüzü | Prototip ve demo için en hızlı yol | 0 |

## 4.3 Model adayları

Model adları hızla değişir. Aşağıdakiler **başlangıç adayları**; son karar kendi test setimizdeki ölçümle verilecek.

| Tür | Aday | Not |
|---|---|---|
| Embedding | `intfloat/multilingual-e5-base` | Çok dilli, Türkçe sağlık testinde iyi sonuç veriyor. Girdilere `query:` / `passage:` öneki ister |
| Embedding | `BAAI/bge-m3` | Çok dilli, uzun metin destekli; daha büyük |
| Embedding | Türkçeye özel arama modelleri (ör. `newmindai/Mursit-Large-TR-Retrieval`) | Türkçe sağlık testinde en iyi sonucu veren model; lisansı kontrol edilmeli |
| Dil modeli | Qwen3 (4B / 8B) | Türkçesi iyi; danışmanımızın TurkishMedLLM çalışması da Qwen3-8B kullanıyor |
| Dil modeli | Gemma 3 (4B / 12B) | Türkçesi iyi |

Referans sonuçlar (Türkçe sağlık testi, nDCG@10): multilingual-e5-base 0,668; Mursit-Large-TR-Retrieval 0,781; BM25 0,494. Kaynak: [TurkishRAGEval](https://huggingface.co/datasets/mteb/turkish-rag-eval).

> **Lisans kuralı:** Ürünü yayınlayabilmek için kullandığımız her modelin ve verinin lisansı buna izin vermeli. Seçilen her modelin lisansı bu tabloya yazılacak.

## 4.4 Bilerek eklemediklerimiz

| Teknoloji | Neden şimdi yok | Ne zaman gündeme gelir |
|---|---|---|
| Vektör veritabanı (Qdrant vb.) | Birkaç bin parça için NumPy yeterli | Belge sayısı on binleri geçerse |
| FastAPI, Docker | Prototipte Streamlit tek başına yeterli | Ürünü başka uygulamalara açarken |
| LangChain, LlamaIndex | Her şeyi kapalı kutuda yapıyorlar; aramayı ve birleştirmeyi biz anlamak ve kontrol etmek istiyoruz | Karşılaştırma amacıyla, isteğe bağlı |
| Cross-encoder ile yeniden sıralama | Önce temel hibrit arama çalışmalı | Aşama 7'de, arama yetersiz kalırsa |

## 4.5 Donanım

Geliştirme bilgisayarı Apple M4, 16 GB bellek. Bu proje için yeterli:

| İş | Durum |
|---|---|
| BM25 indeksleme ve arama | Rahat |
| Birkaç bin parçanın embedding'ini çıkarmak | Birkaç dakika |
| 4B–8B dil modelini Ollama ile çalıştırmak | Rahat (4-bit sürümler) |

## 4.6 Öğrenme sırası

```
Aşama 0 : uv, Git/GitHub, PR akışı, ruff
Aşama 1 : PDF'ten metin çıkarma, JSONL, parçalama
Aşama 2 : BM25 (elle), Türkçe ön işleme
Aşama 3 : embedding, sentence-transformers, NumPy
Aşama 4 : birleştirme yöntemleri (RRF, doğrusal)
Aşama 5 : test seti hazırlama, Recall / MRR / nDCG
Aşama 6 : Ollama, istem yazma, kanıt kontrolü
Aşama 7 : cevap değerlendirmesi
```
