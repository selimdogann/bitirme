# 2. Temel Kavramlar

Bu doküman projeyi anlamak için gereken her kavramı **sıfırdan** anlatır. Her başlık dört sorunun cevabını verir: **Ne? Neden? Nasıl çalışır? Projede nerede?** Başlıkların sonunda kendinizi test edebileceğiniz sorular var. Bu soruları birbirinize sorun.

> Okuma önerisi: Her gün 2–3 başlık okuyun, ardından birbirinize anlatın. Anlatamadığınız yeri bir sonraki gün tekrar okuyun.

---

## 2.1 Büyük Dil Modeli (LLM)

**Ne?** Çok büyük metin verisiyle eğitilmiş ve bir metnin devamını tahmin eden model. ChatGPT, Claude, Llama, Qwen bu türden modellerdir.

**Sorunu:** Model yalnızca eğitildiği veriyi "bilir".
- Sizin şirketinizin belgelerini, dünkü yönetmelik değişikliğini **bilmez**.
- Bilmediği bir şey sorulduğunda emin bir tavırla **uydurabilir**. Buna **halüsinasyon** denir.

**Analoji:** Çok okumuş ama kütüphaneye giremeyen biri. Genel kültürü iyidir ama sizin arşivinizi hiç görmemiştir.

## 2.2 RAG (Retrieval-Augmented Generation)

**Ne?** LLM'e cevap vermeden önce ilgili belgeleri **bulup veren** yöntem. Kelime anlamı "erişimle güçlendirilmiş üretim".

```
1. Kullanıcı soru sorar
2. RETRIEVAL  → Sistem, belge koleksiyonunda soruyla en ilgili parçaları bulur
3. AUGMENT    → Bu parçalar soruyla birlikte bir isteme (prompt) yerleştirilir
4. GENERATION → LLM, yalnızca bu parçalara dayanarak cevap yazar ve kaynak gösterir
```

**Analoji:** Açık kitap sınavı. Öğrenci (LLM) cevabı ezberden değil, önündeki kitaptan (bulunan belgeler) bakarak yazar.

**Kritik nokta:** RAG'in kalitesi büyük ölçüde **2. adımın**, yani aramanın kalitesine bağlıdır. Yanlış belge bulunursa en iyi LLM bile yanlış cevap verir. **Projemizin bilimsel kısmı bu yüzden arama ve birleştirme üzerine kurulu.**

## 2.3 Korpus, Doküman, Parça (Chunk)

- **Korpus:** Arama yapılacak belgelerin tamamı. Örnek: 5.000 yönetmelik metni.
- **Doküman:** Tek bir belge. Örnek: "Kocaeli Üniversitesi Önlisans ve Lisans Eğitim-Öğretim Yönetmeliği".
- **Parça (chunk):** Dokümanın bölündüğü küçük metin parçaları. Örnek: tek bir madde ya da ~300 kelimelik bir paragraf grubu.

**Neden parçalara bölüyoruz?**
1. Embedding modellerinin bir girdi uzunluğu sınırı var.
2. LLM'e 200 sayfalık belgenin tamamını veremeyiz. Bağlam (context) sınırlı ve pahalıdır.
3. Küçük parça, daha **isabetli** arama sağlar. Cevap genelde tek bir paragraftadır.

**Parçalama (chunking) stratejileri:**

| Strateji | Nasıl | Artısı | Eksisi |
|---|---|---|---|
| Sabit boyut | Her N token'da bir böl | Basit | Cümleyi ortadan kesebilir |
| Örtüşmeli sabit boyut | N token'lık pencereyi M token örtüştürerek kaydır | Bağlam kaybı azalır | Tekrar eden veri |
| Yapısal | Madde, başlık, paragraf sınırlarından böl | Anlam bütünlüğü korunur | Belge yapısına özel kod gerekir |
| Anlamsal | Cümleler arası anlam değiştiğinde böl | Akıllı | Yavaş, ayarı zor |

Projede bu stratejileri **deneyip karşılaştıracağız**. Parçalama, arama başarısını ciddi ölçüde etkiler.

## 2.4 Token ve Türkçe Ön İşleme

**Token:** Metnin işlenen en küçük birimi. Arama motorunda genelde bir **kelimedir**. LLM'lerde ise kelime parçasıdır (`"kitaplarımızdan"` → `kitap` `lar` `ımız` `dan` gibi).

**Türkçe neden zor?** Türkçe **eklemeli** bir dildir. Tek bir kökten yüzlerce kelime türeyebilir:

```
"vergi" → vergiler, vergisi, vergiden, vergilendirme, vergilendirilmesi, ...
```

Kullanıcı "vergilendirme" diye ararsa ve belgede "vergisi" geçiyorsa, basit kelime araması bunları **eşleştiremez**.

**Çözümler:**
- **Küçük harfe çevirme (lowercasing).** Dikkat, Türkçede tuzak var:
  ```python
  "İSTANBUL".lower()  # 'i̇stanbul'  → 'i' + görünmez nokta işareti (9 karakter!)
  "ISPARTA".lower()   # 'isparta'   → Türkçede 'ısparta' olmalıydı
  ```
  Bu yüzden Türkçeye özel bir küçültme fonksiyonu yazacağız.
- **Kök bulma (stemming):** Ekleri kaba kurallarla kesmek. Örnek: Snowball Turkish stemmer.
- **Gövdeleme (lemmatization):** Morfolojik analizle gerçek kökü bulmak. Örnek: Zemberek ya da Zeyrek.
- **Durak kelimeler (stopwords):** "ve, ile, bu, da" gibi bilgi taşımayan kelimeleri çıkarmak.

Bu yöntemlerin etkisini ölçmek **AS3** araştırma sorumuzun konusu.

## 2.5 Kelime Tabanlı Arama: Ters İndeks, TF-IDF, BM25

### Ters indeks (inverted index)
Kitabın arkasındaki **dizin** gibi düşünün: her kelimenin hangi sayfalarda geçtiği yazar.

```
"vergi"   → [doc3, doc7, doc12]
"istisna" → [doc7, doc9]
```

"vergi istisna" diye arandığında iki listenin kesişimine ve birleşimine bakılır. Milyonlarca belgede bile milisaniyeler içinde sonuç döner.

### TF-IDF
Bir kelimenin bir belge için ne kadar önemli olduğunu ölçer:
- **TF (Term Frequency):** Kelime bu belgede kaç kez geçiyor? Çok geçiyorsa belge muhtemelen o konuyla ilgilidir.
- **IDF (Inverse Document Frequency):** Kelime kaç belgede geçiyor? Her belgede geçiyorsa ("madde" gibi) ayırt edici değildir, değeri düşüktür. Az belgede geçiyorsa ("mükellefiyet" gibi) değeri yüksektir.

### BM25 (Best Matching 25)
TF-IDF'in geliştirilmiş hâlidir ve günümüzde kelime aramasının standardıdır. İki iyileştirme getirir:

1. **Doygunluk:** Bir kelime 100 kez geçince puan 100 kat artmaz, belli bir noktada doyar (`k1` parametresi).
2. **Uzunluk dengesi:** Uzun belgeler doğal olarak daha çok kelime içerir. BM25 bunu cezalandırarak dengeler (`b` parametresi).

```
               Σ                 f(q,D) · (k1 + 1)
BM25(D,Q) =  q∈Q  IDF(q) · ─────────────────────────────────────
                            f(q,D) + k1 · (1 − b + b · |D|/avgdl)

f(q,D) : q kelimesinin D belgesinde geçme sayısı
|D|    : belgenin uzunluğu,  avgdl: ortalama belge uzunluğu
k1     : genelde 1.2–2.0,   b: genelde 0.75
```

**Güçlü yanı:** Kesin terimler, kodlar, isimler, madde numaraları ("5510 sayılı kanun", "GVK 94. madde").
**Zayıf yanı:** Anlamı bilmez. "araç" ile "taşıt"ı, "işten çıkarılma" ile "iş akdinin feshi"ni eşleştiremez.

> Projede BM25'i **önce kendimiz sıfırdan yazacağız** (~80 satır Python). Sonra hazır kütüphaneyle karşılaştıracağız.

## 2.6 Embedding ve Vektörel Arama

### Embedding nedir?
Bir metni, **anlamını temsil eden sayı dizisine** (vektöre) çeviren model çıktısıdır.

```
"Araç muayene ücreti ne kadar?"       → [0.12, -0.45, 0.88, ..., 0.03]   (ör. 1024 sayı)
"Taşıt kontrol bedeli hakkında bilgi" → [0.11, -0.43, 0.85, ..., 0.05]   ← çok yakın!
"Bugün hava güzel"                    → [-0.70, 0.22, -0.10, ..., 0.91]  ← uzak
```

Anlamca benzer metinlerin vektörleri uzayda **birbirine yakın** durur. Kelimeleri hiç ortak olmasa bile.

**Analoji:** Kütüphanedeki kitapları konuya göre rafa dizmek. Yemek kitapları bir köşede, tarih kitapları başka köşede durur. Bir kitap ararken onun durduğu "köşeye" gidersiniz.

### Benzerlik nasıl ölçülür?
**Kosinüs benzerliği (cosine similarity):** İki vektör arasındaki açıya bakar. 1 aynı yön (çok benzer), 0 ilgisiz, −1 zıt anlamına gelir.

```
cos(A, B) = (A · B) / (‖A‖ · ‖B‖)
```

Vektörler önceden normalize edilirse (uzunlukları 1 yapılırsa) kosinüs benzerliği basit bir **iç çarpıma** dönüşür.

### Bi-encoder
Soru ve belgeler **ayrı ayrı** vektöre çevrilir. Belgeler önceden bir kez çevrilip saklanır. Arama anında yalnızca soru çevrilir ve en yakın vektörler bulunur. Bu yüzden hızlıdır.

**Güçlü yanı:** Eş anlamlılar, farklı ifade biçimleri, doğal dil soruları.
**Zayıf yanı:** Kesin kodlar, nadir özel isimler, sayılar. "5510" ile "5520"yi neredeyse aynı görebilir.

## 2.7 Vektör Veritabanı ve Yaklaşık En Yakın Komşu (ANN)

1 milyon parçanın her biriyle soruyu tek tek karşılaştırmak (**brute force**) yavaştır.

**ANN (Approximate Nearest Neighbor)** algoritmaları, %100 kesinlikten biraz ödün vererek aramayı çok hızlandırır. En yaygını **HNSW**'dir (Hierarchical Navigable Small World): vektörleri katmanlı bir graf hâlinde dizer ve aramada üst katmanda büyük adımlarla, alt katmanda küçük adımlarla hedefe yaklaşır.

**Vektör veritabanı** (Qdrant, Milvus, pgvector, ...) vektörleri saklar, ANN indeksini yönetir ve filtreleme yapar ("sadece 2024 sonrası belgeler" gibi).

> Projede önce **NumPy ile brute force** arama yazacağız. Böylece işin özünü göreceğiz. Sonra Qdrant'a geçip hız farkını ölçeceğiz.

## 2.8 Hibrit Arama ve Birleştirme (Fusion)

**Fikir:** BM25 ile vektör araması **farklı hatalar** yapar. İkisini birleştirmek, birinin kaçırdığını diğerinin yakalamasını sağlar.

```
Soru: "5510 sayılı kanuna göre işten çıkarılan işçinin hakları"
  BM25    → "5510" ve "kanun" kelimelerini yakalar
  Vektör  → "işten çıkarılma" ≈ "iş akdinin feshi" anlamını yakalar
  Hibrit  → İkisini de içeren belgeyi en üste taşır
```

**Sorun:** İki aramanın puanları **farklı ölçeklerde**. BM25 puanı 0–30 arası gibi sınırsız bir sayıyken kosinüs benzerliği −1 ile 1 arasında. Doğrudan toplanamazlar.

**Çözüm ailesi:**
- **Sıra tabanlı (rank-based):** Puanları yok say, sadece sıralamaya bak. Örnek: **RRF**.
- **Puan tabanlı (score-based):** Puanları önce aynı ölçeğe çek (normalize et), sonra ağırlıklı topla. Örnek: **Linear Combination**, **CombSUM**.

Tüm yöntemler formülleriyle birlikte → [Birleştirme Yöntemleri](06-birlestirme-yontemleri.md)

## 2.9 Yeniden Sıralama (Reranking) ve Cross-Encoder

**Bi-encoder** soru ile belgeyi ayrı ayrı okur. Hızlıdır ama yüzeyseldir.
**Cross-encoder** ise soru ile belgeyi **birlikte** okur ve "bu belge bu soruyu ne kadar cevaplıyor?" diye tek bir puan verir. Çok daha isabetlidir ama yavaştır, çünkü her (soru, belge) çifti için modeli yeniden çalıştırır.

**Çözüm: iki aşamalı arama.**
```
1. aşama (hızlı, geniş):  Hibrit arama ile 1.000.000 parça içinden 50 aday seç
2. aşama (yavaş, isabetli): Cross-encoder ile 50 adayı yeniden sırala ve en iyi 5'i seç
```

**Analoji:** İşe alım. İK önce 1000 CV'yi anahtar kelimelerle 50'ye indirir (1. aşama), sonra bu 50 kişiyle tek tek mülakat yapar (2. aşama).

## 2.10 Cevap Üretimi, İstem (Prompt) ve Kaynak Gösterme

Bulunan parçalar bir istem şablonuna yerleştirilir:

```
Aşağıdaki belgelere dayanarak soruyu cevapla.
Belgelerde cevap yoksa "Bu bilgi belgelerde bulunmuyor" de.
Her cümlenin sonunda kullandığın belgeyi [1], [2] biçiminde belirt.

[1] (Kaynak: GVK Madde 94) ... metin ...
[2] (Kaynak: GİB Özelge 2024/123) ... metin ...

Soru: ...
```

**Kaynak göstermek** ürünün güvenilirliği için şarttır. Kullanıcı cevabı belgeden **doğrulayabilmelidir**. Hukuk ve finans gibi alanlarda kaynaksız cevap kullanılamaz.

## 2.11 Değerlendirme (kısa giriş)

"Sistem iyi mi?" sorusunun cevabı bir sayı olmalı. Bunun için:
1. **Test seti:** Sorular ve her soru için "doğru belgeler" listesi (buna *qrels* denir)
2. **Metrikler:**
   - **Recall@k:** Doğru belgelerin yüzde kaçı ilk k sonuçta?
   - **MRR:** İlk doğru belge kaçıncı sırada?
   - **nDCG@k:** Doğru belgeler ne kadar üst sıralarda?

Ayrıntılar → [Değerlendirme](07-degerlendirme.md)

---

## Kendinizi test edin

Bu soruları birbirinize sorun. Ezberden değil, kendi cümlelerinizle cevaplayın.

1. RAG olmadan bir LLM'e şirketinizin izin yönetmeliğini sorsanız ne olur? Neden?
2. "Kitaplarımızdan" kelimesi BM25'te neden sorun çıkarır? İki farklı çözümünü söyleyin.
3. BM25'teki `b` parametresi 0 olsaydı ne değişirdi?
4. "GVK 94. madde" sorusunda vektör araması neden zorlanabilir?
5. BM25 puanı ile kosinüs benzerliğini neden doğrudan toplayamayız?
6. Cross-encoder bu kadar iyiyse neden 1 milyon belgenin hepsine uygulamıyoruz?
7. Bir parça çok küçük olursa ne kaybederiz? Çok büyük olursa ne kaybederiz?
8. Python'da `"İ".lower()` neden Türkçe için yanlış sonuç verir?
