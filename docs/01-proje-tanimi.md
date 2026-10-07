# 1. Proje Tanımı

Bu doküman üç soruya cevap verir: **Hoca ne istiyor? Biz ne istiyoruz? İkisini birleştiren proje ne?**

---

## 1.1 Hocanın istediği (bizim anladığımız)

Görüşmede söylenenler ve bunların teknik karşılığı:

| Hocanın söylediği | Teknik anlamı | Projedeki karşılığı |
|---|---|---|
| "Hibrit RAG yapacaksınız" | İki farklı arama yöntemini birleştiren bir *Retrieval-Augmented Generation* sistemi | Sistemin tamamı |
| "Korpusları araştıracaksınız" | Arama yapılacak belge koleksiyonlarını (veri setlerini) inceleyin | [Faz 1: Korpus araştırması](05-korpus-arastirmasi.md) |
| "Açık kaynakları araştıracaksınız" | Hem **açık veri setleri** hem **açık kaynak araçlar/modeller** | Korpus raporu + [Teknolojiler](04-teknolojiler.md) |
| "Ona göre sektör belirleyeceksiniz" | Sektörü, iyi veri bulunan alana göre seçin | Faz 1 sonundaki karar |
| "Vektörel arama olacak" | Embedding modeliyle anlamsal arama (dense retrieval) | Faz 4 |
| "Birleştireceğiz" | Kelime araması ile vektör aramasının sonuçlarını tek listede birleştirme (fusion) | Faz 5 |
| "Farklı yöntemlerle birleştireceğiz" | Birden fazla fusion yöntemini deneyip **karşılaştırma** | [Birleştirme Yöntemleri](06-birlestirme-yontemleri.md) + [Değerlendirme](07-degerlendirme.md) |

**Özet:** Hoca, çalışan bir sistemin yanında **bilimsel bir karşılaştırma** bekliyor: *"Bu sektörün verisinde hangi birleştirme yöntemi, hangi koşulda, ne kadar daha iyi?"*

## 1.2 Bizim istediğimiz

1. **Öğrenmek.** Kullandığımız her teknolojiyi ve mimariyi gerçekten anlamak.
2. **Sahiplik.** Projenin kontrolü bizde olsun. Her modülü ikimiz de anlatabilelim, değiştirebilelim, savunabilelim.
3. **Adım adım ilerlemek.** Proje "oldu bitti"ye gelmesin. Her katman bir öncekinin üstüne, anlaşılarak eklensin.
4. **Kapsamlı ve piyasaya sürülebilir bir ürün.** Sonunda bir demo değil, gerçek kullanıcıya sunulabilecek bir sistem olsun.

## 1.3 İkisini birleştiren proje tanımı

> Seçilen bir sektöre ait **Türkçe açık korpus** üzerinde; **BM25** (seyrek/kelime tabanlı) ve **yoğun vektör** (anlamsal) aramayı ayrı ayrı kuran, bu iki aramanın sonuçlarını **en az 5 farklı birleştirme yöntemiyle** birleştirip **standart bilgi erişimi metrikleriyle** karşılaştıran, en iyi yapılandırmanın üstüne **yeniden sıralama (reranking)** ve **LLM ile kaynaklı cevap üretimi** ekleyen, **API + web arayüzü + Docker** ile canlıya alınabilir bir Hibrit RAG sistemi.

Bu tanımın iki yüzü var:

| Akademik yüz (hocaya) | Ürün yüzü (piyasaya) |
|---|---|
| Fusion yöntemlerinin karşılaştırmalı analizi | Sektör çalışanının belgelere doğal dille soru sorabildiği asistan |
| Deney tasarımı, metrikler, anlamlılık testleri | Hızlı, güvenilir, kaynak gösteren cevaplar |
| Türkçeye özgü ön işlemenin etkisi | KVKK uyumu, yerelde çalışabilme |
| Özgün katkı: soruya göre değişen birleştirme | Kullanıcı yönetimi, izleme, ölçeklenebilirlik |

## 1.4 Araştırma soruları

Raporun ve sunumun omurgası bu sorular olacak. Her deney en az birine cevap vermeli.

- **AS1:** Seçilen Türkçe korpusta BM25 ve vektör araması ayrı ayrı ne kadar başarılı? Hangi soru tiplerinde hangisi daha iyi?
- **AS2:** Hangi birleştirme yöntemi (RRF, ağırlıklı toplam, CombSUM, CombMNZ, ...) en yüksek başarıyı veriyor? Fark istatistiksel olarak anlamlı mı?
- **AS3:** Türkçe ön işleme (küçük harfe çevirme, kök bulma) BM25'i ve hibrit sonucu ne kadar etkiliyor?
- **AS4:** Yeniden sıralama (cross-encoder) hibrit aramanın üstüne ne kadar katkı sağlıyor? Bunun hız maliyeti ne?
- **AS5 (özgün katkı):** Birleştirme ağırlığını soruya göre dinamik seçmek, sabit ağırlıktan daha mı iyi?

## 1.5 Kapsam

### Kapsamda
- Bir sektör, bir ana korpus (gerekirse ikinci bir korpusla genelleme testi)
- Türkçe belgeler ve sorular
- BM25 + vektör araması + en az 5 fusion yöntemi + reranking
- Kaynak gösteren LLM cevabı
- Değerlendirme altyapısı (test seti, metrikler, deney kayıtları)
- REST API, web arayüzü, Docker ile kurulum
- Temel ürün özellikleri: kullanıcı girişi, belge yükleme, sorgu geçmişi, izleme

### Şimdilik kapsam dışı (zaman kalırsa)
- Çoklu dil desteği
- Bilgi grafı (GraphRAG): Selim'in [arsiv-zekasi-graphrag](https://github.com/selimdogann/arsiv-zekasi-graphrag) projesinde zaten var, ileride üçüncü bir kaynak olarak eklenebilir
- Kendi embedding modelimizi eğitmek (fine-tuning)
- Mobil uygulama

## 1.6 Başarı ölçütleri

| Alan | Ölçüt |
|---|---|
| **Akademik** | En az 5 fusion yöntemi aynı test setinde karşılaştırılmış, sonuçlar tablo ve grafikle raporlanmış, anlamlılık testi yapılmış |
| **Teknik** | Hibrit arama, en iyi tekil yöntemden (BM25 ya da vektör) nDCG@10'da anlamlı biçimde daha iyi. Deneyler tek komutla tekrarlanabilir |
| **Ürün** | `docker compose up` ile ayağa kalkıyor. Arama gecikmesi p95 < 1 sn (LLM hariç). Her cevapta kaynak var |
| **Öğrenme** | Rastgele seçilen herhangi bir modülü ikimiz de 5 dakikada tahtada anlatabiliyoruz |

## 1.7 Hocaya teyit ettirilecek sorular

Bir sonraki görüşmeden önce bu listeyi netleştirin. Cevapları buraya yazın.

- [ ] Korpus **Türkçe** mi olmalı, İngilizce de kabul mü? → *Cevap:*
- [ ] Ağırlık **karşılaştırmalı deney/analiz** mi, **çalışan uygulama** mı, yoksa ikisi eşit mi? → *Cevap:*
- [ ] LLM **yerel/açık kaynak** mı olmalı, yoksa ticari API (ör. Claude, GPT) kullanmak serbest mi? → *Cevap:*
- [ ] Sektör seçimi için **kaç korpus** incelenip raporlanmalı? → *Cevap:*
- [ ] Hangi birleştirme yöntemlerini **mutlaka** görmek istiyor? (RRF ve ağırlıklı toplam yeterli mi?) → *Cevap:*
- [ ] Ara rapor ve final **teslim tarihleri** ve **rapor formatı** ne? → *Cevap:*
- [ ] Görüşme sıklığı ne olacak? (önerimiz: 2 haftada bir) → *Cevap:*

## 1.8 Riskler ve önlemler

| Risk | Olasılık | Önlem |
|---|---|---|
| Uygun Türkçe korpus bulunamaması | Orta | Faz 1'de en az 4 sektör incelenecek, yedek sektör belirlenecek |
| Hazır test seti (soru-cevap etiketi) olmaması | Yüksek | Kendi test setimizi üreteceğiz (LLM ile taslak + elle doğrulama). Bkz. [Değerlendirme](07-degerlendirme.md) |
| Donanım yetersizliği (embedding/LLM yavaş) | Orta | Toplu işler için Colab/Kaggle GPU. Küçük ve nicemlenmiş (quantized) modeller |
| Kapsamın büyüyüp zamanın yetmemesi | Yüksek | Fazlar sırayla tamamlanacak, her fazın sonunda **çalışan** bir sistem olacak |
| Kodun anlaşılmadan eklenmesi | Orta | PR kuralları ve anlat-öğret oturumları. Bkz. [Çalışma Düzeni](09-calisma-duzeni.md) |
| Model lisanslarının ticari kullanıma izin vermemesi | Orta | Her modelin lisansı [Teknolojiler](04-teknolojiler.md) tablosunda takip edilecek |
