# 7. Değerlendirme

"Hibrit arama daha iyi" demek yetmez. **Ne kadar daha iyi, hangi koşulda, bu fark tesadüf mü?** Bu soruların cevabı ölçümle verilir. Bu doküman ölçüm altyapısını anlatır.

> Değerlendirme altyapısı **Faz 2'de**, arama kodundan **önce** kurulmaya başlanır. Ölçemediğiniz bir şeyi geliştiremezsiniz.

---

## 7.1 Test seti

### Bileşenler
```
data/testset/
├── queries.jsonl      # sorular
├── qrels.tsv          # her soru için ilgili parçalar ve ilgililik derecesi
└── README.md          # test setinin nasıl üretildiği
```

**queries.jsonl**
```json
{"qid": "q001", "text": "Serbest meslek kazancında stopaj oranı nedir?", "type": "semantic", "split": "test"}
{"qid": "q002", "text": "GVK 94. madde 2/b bendi", "type": "keyword", "split": "dev"}
```

**qrels.tsv** (TREC formatı: `qid  0  chunk_id  derece`)
```
q001  0  gvk-m94-p3    2
q001  0  ozelge-1123   1
q002  0  gvk-m94-p3    2
```

**İlgililik dereceleri:**
| Derece | Anlamı |
|---|---|
| 2 | Soruyu doğrudan ve tam cevaplıyor |
| 1 | Kısmen ilgili, yardımcı bilgi içeriyor |
| 0 | İlgisiz (dosyaya yazılmasına gerek yok) |

### Soru tipleri
Sonuçları tipe göre kırarak analiz edebilmek için her sorunun tipi etiketlenir:

| Tip | Açıklama | Örnek | Beklenti |
|---|---|---|---|
| `keyword` | Kesin terim, kod, numara içerir | "4857 sayılı kanun 17. madde" | BM25 güçlü |
| `semantic` | Doğal dil, belgedekinden farklı kelimeler | "İşten atılırsam kaç gün önceden haber verilmeli?" | Vektör güçlü |
| `mixed` | İkisi birden | "4857'ye göre ihbar süreleri ne kadar?" | Hibrit güçlü |
| `unanswerable` | Korpusta cevabı yok | "Almanya'da kıdem tazminatı nasıl hesaplanır?" | Sistem "bilmiyorum" demeli |

**Hedef dağılım:** ~%30 keyword, ~%30 semantic, ~%30 mixed, ~%10 unanswerable.

### Boyut
- **En az 200, ideali 300+ soru.** Daha azında yöntemler arasındaki fark istatistiksel olarak anlamlı çıkmayabilir.
- **Bölme:** %30 `dev` (parametre ayarı: α, k ...), %70 `test` (sadece final raporu için).

> ⚠ **Altın kural:** Parametreleri `test` bölümüne bakarak ayarlamak **hile** sayılır (veri sızıntısı). Ayarlar `dev` bölümünde yapılır, `test` bölümüne en son ve bir kez bakılır.

### Üretim yöntemi

```
1. Elle yazma (~100 soru)
   Belgeleri okuyup gerçek bir kullanıcının soracağı soruları yazın.
   Gerçek kaynaklardan esinlenin: SSS sayfaları, forumlar, özelge soruları.

2. LLM destekli taslak (~200+ soru)
   Rastgele seçilen bir parçayı LLM'e verin: "Bu metnin cevapladığı, ama metindeki
   kelimeleri birebir kullanmayan bir soru yaz." İlgili parça otomatik olarak etiketlenmiş olur.
   ⚠ Her soruyu elle kontrol edin. Kötü soruları atın, düzeltin.

3. Havuzlama (pooling), eksik etiketleri tamamlamak için
   Bir sorunun cevabı başka parçalarda da olabilir. Etiketlenmemiş doğru parçalar
   sistemi haksız yere cezalandırır. Bu yüzden:
   - Tüm sistemlerin (BM25, dense, hibrit) ilk 10 sonucunu birleştirin
   - Daha önce etiketlenmemiş olanları elle değerlendirin (0/1/2)
   TREC'in standart yöntemi budur.
```

### Etiketleyiciler arası uyum
Etiketleme özneldir. Güvenilirliği ölçmek için:
- 50 soruluk ortak bir alt kümeyi **Selim ve Zehra ayrı ayrı** etiketlesin
- **Cohen's Kappa** hesaplayın (> 0.6 iyi, > 0.8 çok iyi)
- Anlaşmazlıkları tartışıp bir **etiketleme kılavuzu** yazın (`data/testset/README.md`)

Bu adım raporda test setinin güvenilirliğini kanıtlar.

---

## 7.2 Arama metrikleri

`rel(i)` = i. sıradaki belgenin ilgililik derecesi, `R` = sorunun tüm ilgili belgeleri.

| Metrik | Formül | Sorduğu soru |
|---|---|---|
| **Precision@k** | `|ilgili ∩ ilk k| / k` | İlk k sonucun yüzde kaçı ilgili? |
| **Recall@k** | `|ilgili ∩ ilk k| / |R|` | İlgili belgelerin yüzde kaçını ilk k'da bulduk? |
| **Hit@k** | İlk k'da en az 1 ilgili varsa 1, yoksa 0 | En az bir doğru belge bulabildik mi? |
| **MRR@k** | `1 / ilk ilgili belgenin sırası` (sorular üzerinden ortalama) | İlk doğru cevap ne kadar yukarıda? |
| **nDCG@k** | `DCG@k / IDCG@k` | Doğru belgeler, derecelerine göre ne kadar iyi sıralanmış? |

**nDCG ayrıntısı:**
```
           k   2^rel(i) − 1
DCG@k  =   Σ   ─────────────
          i=1   log₂(i + 1)

IDCG@k = mükemmel sıralamanın DCG'si    →    nDCG ∈ [0, 1]
```
Derece 2 olan belge, derece 1 olandan daha değerlidir. Üst sıralar alt sıralardan daha değerlidir.

**Hangi metrik ne için?**
- **Recall@50 / Recall@100:** Reranker'a giden aday havuzunun kalitesi. Doğru belge havuzda yoksa reranker onu kurtaramaz
- **nDCG@10:** Ana karşılaştırma metriği (literatür standardı)
- **MRR@10:** Kullanıcı deneyimi. İlk doğru cevabı ne kadar hızlı görüyor?
- **Recall@5:** LLM'e verilen bağlamın kalitesi

> Metrikleri önce `src/hybridrag/evaluation/metrics.py` içinde **kendiniz yazın**, sonra `ranx` ile aynı sonucu verdiğini test edin.

---

## 7.3 Cevap (generation) metrikleri (Faz 7)

| Metrik | Ölçtüğü | Nasıl |
|---|---|---|
| **Sadakat (Faithfulness)** | Cevaptaki iddialar verilen bağlamda var mı? (halüsinasyon) | RAGAS (LLM ile) |
| **Cevap ilgililiği** | Cevap soruya gerçekten cevap veriyor mu? | RAGAS |
| **Kaynak doğruluğu** | `[1]` etiketi gerçekten o iddiayı içeren parçayı mı gösteriyor? | Elle kontrol + otomatik eşleştirme |
| **Reddetme doğruluğu** | `unanswerable` sorularda "bilmiyorum" diyor mu? | Otomatik |
| **İnsan değerlendirmesi** | 50 cevaba 1–5 puan (doğruluk, tamlık, akıcılık) | Selim + Zehra + mümkünse bir alan uzmanı |

> LLM ile yapılan değerlendirme (LLM-as-a-judge) de hata yapabilir. 30–50 örnekte insan puanıyla karşılaştırıp ne kadar güvenilir olduğunu raporlayın.

---

## 7.4 Sistem metrikleri

| Metrik | Neden |
|---|---|
| Gecikme p50 / p95 (her aşama için ayrı) | Kullanıcı deneyimi |
| İndeksleme süresi (parça/saniye) | Ölçeklenebilirlik |
| İndeks boyutu (MB) ve bellek kullanımı | Maliyet |
| LLM token sayısı (soru başına) | Maliyet |

Raporda bunları **"başarı ve maliyet"** grafiğinde birlikte gösterin. Örnek: reranker nDCG'yi %8 artırıyor ama gecikmeyi 400 ms artırıyor.

---

## 7.5 İstatistiksel anlamlılık

İki yöntem arasında 0.012'lik bir nDCG farkı gerçek bir fark mı, yoksa şans mı?

- **Eşleştirilmiş test:** İki yöntem de aynı sorularda ölçüldüğü için *paired t-test* ya da daha sağlam olan **randomization (permutation) test** kullanılır.
- **Çoklu karşılaştırma düzeltmesi:** 8 yöntemi karşılaştırırsak şans eseri "anlamlı" çıkma olasılığı artar. **Holm** ya da **Bonferroni** düzeltmesi uygulanır.
- **Raporlama:** Tabloda anlamlı farklar † ya da * ile işaretlenir. `p < 0.05` eşiği kullanılır.

`ranx`'in `compare()` fonksiyonu bu testleri hazır yapar. Önce mantığını anlayın, sonra kullanın.

---

## 7.6 Deney protokolü

### Yapılandırma dosyası
Her deney bir YAML dosyasıdır. Kod değişmez, sadece yapılandırma değişir.

```yaml
# experiments/configs/fusion_rrf_k60.yaml
name: fusion_rrf_k60
corpus: data/processed/chunks.jsonl
testset:
  queries: data/testset/queries.jsonl
  qrels: data/testset/qrels.tsv
  split: dev
retrievers:
  - type: bm25
    k: 100
    params: {k1: 1.2, b: 0.75}
    preprocessing: {lowercase: turkish, stemmer: snowball, stopwords: true}
  - type: dense
    k: 100
    model: BAAI/bge-m3
fusion:
  type: rrf
  params: {k: 60}
rerank: null
metrics: [ndcg@10, recall@10, recall@50, mrr@10]
```

### Her deneyde kaydedilecekler
- Yapılandırmanın tamamı
- Git commit kimliği (hangi kodla çalıştı?)
- Korpus ve test seti sürümü (dosyaların checksum değeri)
- Soru bazında sonuçlar (*run* dosyası, TREC formatı). Anlamlılık testi ve hata analizi için şart
- Toplam metrikler
- Süre ve donanım bilgisi

### Hata analizi
Sadece ortalama metriklere bakmak yetmez. Her deneyden sonra:
1. Hibritin **en çok kazandırdığı** 10 soruyu inceleyin. Neden kazandı?
2. Hibritin **en çok kaybettirdiği** 10 soruyu inceleyin. Neden kaybetti?
3. Bulguları `experiments/notes/` altına yazın. Bu notlar doğrudan raporun "Tartışma" bölümüne dönüşür.

---

## 7.7 Sonuç tablosu şablonu (rapor için)

| Yöntem | nDCG@10 | Recall@10 | Recall@50 | MRR@10 | p95 (ms) |
|---|---|---|---|---|---|
| BM25 (stemming yok) | | | | | |
| BM25 (Snowball) | | | | | |
| Dense (bge-m3) | | | | | |
| RRF (k=60) | | | | | |
| wRRF | | | | | |
| Linear min-max (α*) | | | | | |
| Linear z-score (α*) | | | | | |
| CombSUM | | | | | |
| CombMNZ | | | | | |
| En iyi fusion + Reranker | | | | | |
| Dinamik α | | | | | |

*α\*: dev bölümünde bulunan en iyi α değeri*
