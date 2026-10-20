# 7. Değerlendirme

"Sistem iyi çalışıyor" demek yetmez. **Ne kadar iyi, hangi soruda, ne zaman yanılıyor?** Bu soruların cevabı ölçümle verilir.

Üç şeyi ölçeceğiz:
1. **Arama:** Doğru paragrafı buluyor mu?
2. **Cevap:** Yazdığı cevap doğru mu, kaynağı cevabı destekliyor mu?
3. **Cevap vermeme:** Cevabı talimatta olmayan soruda susmayı biliyor mu?

---

## 7.1 Test seti

### Dosyalar

```
data/testset/
├── queries.jsonl   # sorular
├── qrels.tsv       # her sorunun doğru paragrafları
└── README.md       # test setinin nasıl hazırlandığı ve etiketleme kuralları
```

**queries.jsonl**
```json
{"qid": "q001", "text": "Parol'ü aç karnına içebilir miyim?", "ilac": "Parol", "tip": "anlam", "bolum": "dev"}
{"qid": "q002", "text": "Arveles 25 mg günde en fazla kaç tablet?", "ilac": "Arveles", "tip": "kelime", "bolum": "test"}
{"qid": "q003", "text": "Coraspin'i kahveyle içmek sorun olur mu?", "ilac": "Coraspin", "tip": "cevapsiz", "bolum": "test"}
```

**qrels.tsv** (`soru  paragraf  derece`)
```
q001  parol-3-002    2
q002  arveles-3-001  2
```

Cevabı talimatta olmayan sorular (`cevapsiz`) qrels'e yazılmaz.

**İlgililik dereceleri:**
| Derece | Anlamı |
|---|---|
| 2 | Paragraf soruyu doğrudan ve tam cevaplıyor |
| 1 | Kısmen ilgili, yardımcı bilgi var |

### Soru tipleri

| Tip | Açıklama | Örnek | Kim güçlü? |
|---|---|---|---|
| `kelime` | İlaç adı, doz, etkin madde gibi kesin terim içerir | "Augmentin 1000 mg kaç saatte bir?" | BM25 |
| `anlam` | Doğal dil, talimattaki kelimeler geçmiyor | "Emzirirken bu ilacı içebilir miyim?" | Vektör |
| `karma` | İkisi birden | "Majezik hamilelikte kullanılır mı?" | Hibrit |
| `cevapsiz` | Cevabı talimatta yok | "Parol'ün fiyatı ne kadar?" | Sistem cevap vermemeli |

**Hedef dağılım:** yaklaşık %30 kelime, %30 anlam, %25 karma, %15 cevapsız.

### Boyut ve bölme
- **200–300 soru.** Hocanın da belirttiği gibi büyük veri setine gerek yok; yöntemler arasındaki farkı görmek için bu boyut yeterli.
- **Bölme:** %30 `dev` (eşik ve α ayarlamak için), %70 `test` (yalnızca sonuçları raporlamak için).

> ⚠ **Altın kural:** Ayarlar `dev` sorularında yapılır. `test` sorularına en son ve bir kez bakılır. Aksi halde sonuçlar gerçeği yansıtmaz.

### Hazırlama yöntemi

```
1. Elle yazma (~100 soru)
   Talimatları okuyup gerçek bir hastanın soracağı soruları yazın.
   Her soru için cevabın geçtiği paragrafı işaretleyin.

2. Dil modeliyle taslak (~150 soru)
   Rastgele bir paragrafı modele verin: "Bu paragrafın cevapladığı, ama paragraftaki
   kelimeleri birebir kullanmayan bir hasta sorusu yaz."
   ⚠ Her soruyu elle kontrol edin; kötüleri atın ya da düzeltin.

3. Cevapsız sorular (~40 soru)
   Talimatta cevabı olmayan ama makul sorular: fiyat, başka ilaçla karşılaştırma,
   talimatta geçmeyen bir durum.

4. Eksik etiketleri tamamlama
   Bir sorunun cevabı başka paragraflarda da olabilir. Bütün yöntemlerin ilk 5 sonucunu
   birleştirip etiketlenmemiş olanlara elle bakın.
```

### İki kişinin etiketlerinin uyumu
- 30 soruluk ortak bir kümeyi Selim ve Zehra **ayrı ayrı** etiketlesin.
- Ne kadar aynı etiketi verdiğinizi hesaplayın (Cohen's Kappa; 0,6 üstü iyi).
- Anlaşamadığınız yerleri konuşup etiketleme kurallarını `data/testset/README.md`'ye yazın.

Bu adım, raporda test setinin güvenilir olduğunu gösterir.

---

## 7.2 Arama metrikleri

| Metrik | Sorduğu soru | Neden önemli? |
|---|---|---|
| **Recall@5** | Doğru paragraf ilk 5 sonuçta var mı? | Dil modeline ilk 5 paragraf verilecek; doğru paragraf orada yoksa cevap da yanlış olur |
| **MRR@10** | İlk doğru paragraf kaçıncı sırada? | Kullanıcıya gösterilen kaynağın kalitesi |
| **nDCG@10** | Doğru paragraflar, derecelerine göre ne kadar üstte? | Literatürde standart; karşılaştırma için |

**Örnek:**
```
Soru 1: doğru paragraf 1. sırada   →  Recall@5 = 1,  MRR = 1/1 = 1.00
Soru 2: doğru paragraf 4. sırada   →  Recall@5 = 1,  MRR = 1/4 = 0.25
Soru 3: ilk 10'da yok              →  Recall@5 = 0,  MRR = 0
                                       ─────────────────────────────
                         Ortalama  →  Recall@5 = 0.67,  MRR = 0.42
```

Sonuçlar her zaman **soru tipine göre ayrı** da raporlanır. Asıl ilginç bulgu oradadır.

> Metrikleri önce `evaluate.py` içinde kendimiz yazacağız. Sonra küçük bir örnekte elle hesapladığımız sonuçla karşılaştıracağız.

---

## 7.3 Cevap metrikleri (Aşama 7)

| Metrik | Ölçtüğü | Nasıl |
|---|---|---|
| **Cevap doğruluğu** | Cevap talimattaki bilgiyle uyumlu mu? | Her cevap elle: doğru / kısmen / yanlış |
| **Kaynak doğruluğu** | Gösterilen paragraf cevabı gerçekten destekliyor mu? | Elle kontrol |
| **Sadelik** | Cevap anlaşılır mı? | Projeyi bilmeyen 3–5 kişiye okutma |

Elle değerlendirme için 50 cevaplık bir örneklem yeterli.

---

## 7.4 Cevap vermeme ölçümü

Sistem iki şekilde yanılabilir:

| | Talimatta cevap **var** | Talimatta cevap **yok** |
|---|---|---|
| **Sistem cevap verdi** | ✅ Doğru davranış | ❌ **Uydurma riski** (en tehlikelisi) |
| **Sistem "bilgi yok" dedi** | ⚠ Gereksiz susma | ✅ Doğru davranış |

İki sayı raporlanır:
- **Doğru susma oranı:** `cevapsiz` soruların yüzde kaçında sistem "bilgi yok" dedi? Yüksek olmalı.
- **Gereksiz susma oranı:** Cevabı olan soruların yüzde kaçında "bilgi yok" dedi? Düşük olmalı.

İkisi arasında denge var: eşik yükseldikçe sistem daha çok susar. Eşiği `dev` sorularında farklı değerlerle deneyip bu iki oranın grafiğini çizeceğiz ve dengeli noktayı seçeceğiz.

---

## 7.5 İkinci kontrol: Hazır veri setleri

Kendi test setimizin yanında, yöntemin başka sağlık metinlerinde de çalıştığını göstermek için:
- **MedTurkQuAD**'ın 820 soruluk test bölümü
- **TurkishRAGEval**: yayımlanmış referans sonuçlarla karşılaştırma

Ayrıntılar: [Korpus ve Veri](05-korpus-arastirmasi.md).

---

## 7.6 Her ölçümde kaydedilecekler

- Hangi yöntem, hangi ayarlar (k, α, eşik, model adı)
- Kodun git commit kimliği
- Soru bazında sonuçlar (hata analizi için şart)
- Toplam metrikler

**Hata analizi:** Her ölçümden sonra hibrit aramanın en çok kazandırdığı ve en çok kaybettirdiği 5'er soruya bakın, nedenini not edin. Bu notlar raporun "Tartışma" bölümüne dönüşür.

---

## 7.7 Sonuç tablosu şablonu

| Yöntem | Recall@5 | MRR@10 | nDCG@10 | Kelime | Anlam | Karma |
|---|---|---|---|---|---|---|
| BM25 (ön işlemesiz) | | | | | | |
| BM25 (Türkçe ön işleme) | | | | | | |
| Vektör | | | | | | |
| Hibrit: RRF | | | | | | |
| Hibrit: doğrusal (α*) | | | | | | |

*Kelime, Anlam, Karma sütunları o tipteki sorularda Recall@5. α\*: `dev` sorularında bulunan en iyi ağırlık.*
