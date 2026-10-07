# 6. Birleştirme (Fusion) Yöntemleri

Hocanın "farklı yöntemlerle birleştireceğiz" dediği kısım bu. Projenin **bilimsel çekirdeği** burası.

Bu doküman her yöntemi **formülü, örneği, artısı ve eksisiyle** anlatır. Yöntemler üç seviyeye ayrılmıştır:

| Seviye | Yöntemler | Faz |
|---|---|---|
| 🟢 **Temel** | RRF, Ağırlıklı RRF, Borda, Linear (min-max / z-score), CombSUM, CombMNZ, CombMAX | 5 |
| 🟡 **Orta** | Cross-encoder reranking, DBSF, sorgu tipine göre yönlendirme | 6 |
| 🔴 **İleri** | Dinamik α, Learning-to-Rank, LLM ile sıralama, öğrenilmiş seyrek arama | 6 + |

---

## 6.1 Problem tanımı

Elimizde aynı soru için iki (ya da daha fazla) sıralı liste var:

```
BM25 sonuçları                       Vektör sonuçları
sıra  belge  puan                    sıra  belge  puan
 1     A     18.2                     1     D     0.89
 2     C     15.7                     2     B     0.86
 3     B     11.4                     3     A     0.81
 4     E      9.9                     4     F     0.79
```

**Amaç:** Bunları tek bir sıralı listeye dönüştürmek. En ilgili belgeler en üstte olmalı.

**Zorluklar:**
1. Puanlar **farklı ölçeklerde**. 18.2 ile 0.89 karşılaştırılamaz.
2. Bazı belgeler **sadece bir listede** var (C, E, D, F). Diğer listedeki puanları ne kabul edilecek?
3. İki yöntem **eşit güvenilir değil**. Hangisine ne kadar ağırlık verilecek?

Yöntemler bu zorlukları farklı biçimlerde çözer.

---

## 6.2 🟢 Sıra tabanlı yöntemler

Puanları tamamen yok sayar, **sadece sıralamaya** bakar. Ölçek sorunu ortadan kalkar.

### Reciprocal Rank Fusion (RRF)
*Cormack, Clarke & Büttcher, SIGIR 2009*

```
RRF(d) = Σ   1 / (k + rank_i(d))       k genelde 60
         i
```

Belge bir listede yoksa o listeden katkı almaz.

**Örnek (k=60):**
| Belge | BM25 sırası | Vektör sırası | Hesap | RRF |
|---|---|---|---|---|
| A | 1 | 3 | 1/61 + 1/63 | **0.03227** |
| B | 3 | 2 | 1/63 + 1/62 | **0.03200** |
| D | — | 1 | 1/61 | 0.01639 |
| C | 2 | — | 1/62 | 0.01613 |

**`k` neden 60?** `k` küçük olursa birinci ile ikinci sıra arasındaki fark çok büyür. `k` büyük olursa sıralar arasındaki fark azalır ve listeler daha "demokratik" birleşir. 60 değeri orijinal makalede deneysel olarak bulunmuştur. **Biz de `k ∈ {1, 10, 30, 60, 100}` deneyeceğiz.**

- ✅ Ayar gerektirmez, sağlamdır, hemen her yerde iyi çalışır. Endüstri standardıdır
- ❌ Puandaki bilgiyi atar. BM25 bir belgeye çok emin olsa bile (18.2'ye karşı 3.1) yalnızca sırası sayılır

### Ağırlıklı RRF
```
wRRF(d) = Σ  w_i / (k + rank_i(d))
          i
```
Bir aramaya daha çok güveniyorsak ağırlığını artırırız. Örnek: `w_bm25 = 0.3`, `w_vektör = 0.7`.

### Borda Sayımı (Borda Count)
Seçim sistemlerinden gelir. N belgelik bir listede birinci sıra N puan, ikinci sıra N−1 puan alır, ve böyle devam eder.
```
Borda(d) = Σ  (N − rank_i(d) + 1)
           i
```
- ✅ Basit, sezgisel
- ❌ Listedeki sıralar arasındaki farkı doğrusal kabul eder. RRF ise üst sıralara daha çok önem verir

---

## 6.3 🟢 Puan tabanlı yöntemler

Önce puanları **aynı ölçeğe çeker** (normalizasyon), sonra birleştirir.

### Adım 1: Normalizasyon

| Yöntem | Formül | Yorum |
|---|---|---|
| **Min-Max** | `(s − min) / (max − min)` | 0–1 aralığına çeker. En yaygın yöntem. Uç değerlere hassastır |
| **Z-Score** | `(s − μ) / σ` | Ortalama 0, standart sapma 1. Dağılım şekline duyarlıdır |
| **Max** | `s / max` | En basit yöntem |
| **Sum** | `s / Σs` | Puanları olasılık gibi yorumlar |
| **Teorik Min-Max** | `(s − teorik_min) / (max − teorik_min)` | Kosinüs için teorik min = −1. Liste dışı belgelere yaklaşımı daha tutarlıdır |

**Örnek (Min-Max):**
```
BM25:   A=18.2 → 1.00   C=15.7 → 0.70   B=11.4 → 0.18   E=9.9 → 0.00
Vektör: D=0.89 → 1.00   B=0.86 → 0.70   A=0.81 → 0.20   F=0.79 → 0.00
```

> ⚠ **Tuzak:** Min-Max'te listenin son belgesi her zaman 0 olur. Yani o belge "hiç ilgili değil" sayılır. Bu da listeye kaç belge alındığına (k) bağlı bir yanlılık yaratır. Bu etkiyi deneylerde gözlemleyin, raporda iyi bir tartışma konusu olur.

### Adım 2: Birleştirme

#### Doğrusal Birleştirme (Linear / Convex Combination)
```
Linear(d) = α · s_vektör(d) + (1 − α) · s_bm25(d)        0 ≤ α ≤ 1
```
- `α = 0` ise saf BM25, `α = 1` ise saf vektör araması.
- **Deney:** `α ∈ {0.0, 0.1, ..., 1.0}` için bir eğri çizin. Bu eğri raporun en önemli grafiklerinden biri olacak.
- ✅ Doğru ayarlanırsa genelde RRF'den iyi sonuç verir (Bruch ve ark. 2023)
- ❌ α değerinin ayarlanması gerekir. Bu ayar da etiketli veri ister ve korpusa göre değişir

#### CombSUM
*Fox & Shaw, 1994*
```
CombSUM(d) = Σ  norm_s_i(d)
             i
```
Linear yönteminin `α = 0.5` hâline denktir (sabit çarpan hariç).

#### CombMNZ
```
CombMNZ(d) = CombSUM(d) × |{i : d, i listesinde var}|
```
Belgeyi kaç liste bulduysa puanını o sayıyla çarpar. **İki aramanın da bulduğu belgeyi ödüllendirir.**

#### CombMAX / CombMIN
Listelerdeki en yüksek ya da en düşük normalize puanı alır. Genelde zayıftır ama karşılaştırma için tabloya eklenir.

**Örnek (Min-Max sonrası):**
| Belge | norm BM25 | norm Vektör | CombSUM | Listede | CombMNZ |
|---|---|---|---|---|---|
| A | 1.00 | 0.20 | 1.20 | 2 | **2.40** |
| B | 0.18 | 0.70 | 0.88 | 2 | **1.76** |
| D | — | 1.00 | 1.00 | 1 | 1.00 |
| C | 0.70 | — | 0.70 | 1 | 0.70 |

CombSUM'da D, B'nin önüne geçiyor. CombMNZ'de ise iki listede de bulunan B, D'yi geçiyor. **Yöntem değişince sıralama değişir.** Deneylerin amacı da hangi yöntemin bizim verimizde doğru sıralamayı verdiğini bulmak.

---

## 6.4 🟡 Orta seviye

### Cross-Encoder ile Yeniden Sıralama (Reranking)
Teknik olarak bir fusion yöntemi değil, **fusion'dan sonra gelen bir aşama**. Ama sonuca etkisi genelde en büyük olan adım budur.

```
Hibrit arama (ilk 50 aday)  →  Cross-encoder her (soru, aday) çiftini puanlar  →  İlk 5
```

**Deneyler:**
- Reranker'a kaç aday verilmeli? (20 / 50 / 100). Gecikme ile başarı arasındaki dengeye bakın
- Reranker hangi fusion'ın üstünde daha iyi çalışıyor?
- Reranker varken fusion yöntemi hâlâ fark yaratıyor mu? **Bu çok iyi bir araştırma sorusu**

### DBSF (Distribution-Based Score Fusion)
Normalizasyonu, puan dağılımının ortalama ± 3 standart sapma aralığına göre yapar. Uç değerlere Min-Max'ten daha dayanıklıdır. Qdrant'ta hazır bulunur. Biz kendimiz de yazabiliriz.

### Sorgu Tipine Göre Yönlendirme (Query Routing)
Basit kurallarla soru tipini belirleyip yöntemi ona göre seçmek:
```
Soruda sayı, madde no, kod, tırnak içinde ifade var mı?  →  BM25 ağırlıklı
Soru 8 kelimeden uzun ve soru kalıbında mı?               →  Vektör ağırlıklı
Değilse                                                   →  Dengeli
```

---

## 6.5 🔴 İleri seviye (özgün katkı adayları)

### Dinamik α (Soruya Göre Değişen Ağırlık), **önerdiğimiz özgün katkı**
Linear birleştirmedeki α'yı **her soru için ayrı tahmin etmek**.

**Yaklaşımlar (basitten zora):**
1. **Kural tabanlı:** Bölüm 6.4'teki yönlendirmenin sürekli versiyonu
2. **Öznitelik tabanlı sınıflandırıcı:** Sorudan öznitelik çıkarılır (uzunluk, sayı var mı, nadir kelime oranı, IDF ortalaması, iki listenin örtüşme oranı, iki listenin en yüksek puanı). Bu özniteliklerden α'yı tahmin eden küçük bir model (lojistik regresyon, LightGBM) eğitilir. Eğitim verisi: test setinin bir bölümünde her soru için en iyi α değeri
3. **LLM tabanlı:** LLM'e "bu soru anahtar kelime mi, anlam mı gerektiriyor?" diye sorulur

**Neden özgün:** Literatürde bu yönde çalışmalar var, ancak **Türkçe ve sizin sektörünüzde** yapılmış bir çalışma büyük ihtimalle yok. Bu, hocaya "projemizin katkısı ne?" sorusunun cevabı olur.

### Learning-to-Rank (LTR)
Her (soru, belge) çifti için öznitelikler çıkarılır: BM25 puanı, vektör puanı, iki sıra değeri, belge uzunluğu, başlıkta eşleşme var mı, ... Ardından bir sıralama modeli (ör. LightGBM LambdaMART) en iyi birleşimi **öğrenir**.
- ✅ En güçlü klasik yöntemlerden biri
- ❌ Çok etiketli veri ister. Ürün canlıya çıktıktan sonra kullanıcı geri bildirimleriyle beslenebilir

### LLM ile Sıralama (LLM Reranking)
Adaylar LLM'e verilir ve "soruya en uygun olanları sırala" denir.
- ✅ Çok güçlü
- ❌ Yavaş ve pahalı. Uzun listelerde tutarsız olabilir. Karşılaştırma için bir üst sınır (upper bound) olarak kullanılabilir

### Öğrenilmiş Seyrek Arama (SPLADE, BGE-M3 sparse)
BM25'in yerine geçen, kelime ağırlıklarını bir modelle öğrenen arama türü. Fusion yöntemi değildir, **üçüncü bir arayıcıdır**. Üç listeyi (BM25 + dense + learned sparse) birleştirmek ilginç bir deney olur. BGE-M3 tek modelle hem dense hem sparse çıktı verdiği için kolayca denenebilir.

### Sorgu Genişletme (Query Expansion)
Fusion değil, ama hibrit pipeline'ı güçlendirir:
- **Multi-query:** LLM sorudan 3 farklı soru üretir. Hepsiyle aranır ve RRF ile birleştirilir (RAG-Fusion)
- **HyDE:** LLM önce varsayımsal bir cevap yazar, arama bu cevabın vektörüyle yapılır

---

## 6.6 Deney planı

### Deney 1: Temel karşılaştırma (Faz 5)
| Değişken | Değerler |
|---|---|
| Arayıcılar | BM25, Dense (en iyi model) |
| Fusion | RRF, wRRF, Borda, Linear(min-max), Linear(z-score), CombSUM, CombMNZ, CombMAX |
| Her arayıcıdan alınan liste uzunluğu | 20, 50, 100, 200 |
| RRF k | 1, 10, 30, 60, 100 |
| Linear α | 0.0 → 1.0 (0.1 adımlarla) |
| Metrikler | nDCG@10, Recall@10, Recall@50, MRR@10 |

**Çıktılar:**
- Ana sonuç tablosu (yöntem × metrik)
- α eğrisi grafiği
- RRF k duyarlılık grafiği
- **Soru tipine göre kırılım:** Hangi yöntem kelime sorularında, hangisi anlam sorularında iyi?

### Deney 2: Reranking (Faz 6)
En iyi 3 fusion yöntemi × reranker (var / yok) × aday sayısı (20 / 50 / 100)

### Deney 3: Dinamik α (Faz 6)
Sabit en iyi α ile dinamik α karşılaştırması. Eğitim ve test bölmesi **ayrı** olmalı (bkz. [Değerlendirme](07-degerlendirme.md)).

### Doğrulama
Kendi yazdığımız fusion fonksiyonlarının sonuçlarını **ranx kütüphanesinin `fuse()` fonksiyonuyla karşılaştıracağız.** Aynı girdide aynı sonucu vermeliler. Bu kontrol `tests/` altında otomatik bir test olacak.

---

## Kendinizi test edin

1. RRF'de `k = 0` olsaydı birinci ve ikinci sıradaki belgelerin katkıları arasındaki oran ne olurdu? `k = 60` iken ne olur?
2. Bir belge sadece BM25 listesinde varsa Linear yönteminde vektör puanını kaç kabul etmeliyiz? Bunun farklı seçenekleri neler?
3. CombMNZ hangi durumda CombSUM'dan kötü sonuç verebilir?
4. α eğrisi her korpusta aynı mı olur? Neden?
5. Dinamik α modelini test setinin tamamıyla eğitip yine aynı test setinde ölçersek ne olur?
