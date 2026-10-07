# 5. Korpus Araştırması ve Sektör Seçimi

Hocanın ilk istediği iş bu: **açık korpusları araştırın, sektörü ona göre seçin.** Bu doküman bu araştırmanın nasıl yapılacağını, nereye bakılacağını ve kararın nasıl verileceğini anlatır.

> **Altın kural:** Sektörü veriye göre seçiyoruz, veriyi sektöre göre aramıyoruz. "Sağlık çok havalı" diye başlayıp sonra veri bulamamak, bitirme projelerinin en sık yaşadığı sorundur.

---

## 5.1 Hibrit RAG için iyi bir korpus nasıl olur?

| Özellik | Neden önemli | İdeal |
|---|---|---|
| **Erişilebilir** | Veriyi gerçekten indirebilmeliyiz | Toplu indirme, API ya da düzenli yapıda bir web sitesi |
| **Lisansı uygun** | Hem akademik hem ticari kullanım için | Kamu malı, açık lisans (CC-BY gibi) |
| **Yeterli hacim** | Arama farklarının ortaya çıkması için | 5.000+ belge ya da 50.000+ parça |
| **Türkçe ve kaliteli** | Projenin Türkçe odağı | OCR hatası az, düzgün metin |
| **Terim ve kod yoğun** | BM25'in parlayacağı sorgular olsun | Madde no, kanun no, ürün kodu, özel isimler |
| **Doğal dil soruları sorulabilir** | Vektör aramanın parlayacağı sorgular olsun | Halkın gerçekten sorduğu sorular |
| **Yapılı** | Parçalamayı kolaylaştırır | Madde, başlık, bölüm sınırları belli |
| **Gerçek kullanıcı ihtiyacı** | Ürün yüzü için | Bu belgelerde bilgi arayan birileri var |
| **Test seti üretilebilir** | Değerlendirme için | Hazır SSS ya da soru-cevap var, ya da soru yazmak kolay |

**Kilit nokta:** Hibrit aramanın değerini göstermek için korpusta **hem kelime eşleşmesi gerektiren hem anlam gerektiren** sorular olmalı. Yalnızca birinin kazandığı bir korpusta birleştirme deneyleri sıkıcı ve anlamsız olur.

## 5.2 Aday sektörler ve kaynaklar

Aşağıdakiler **araştırma başlangıç noktalarıdır**. Her birinin erişim yöntemini, kullanım koşullarını ve hacmini **sizin kontrol etmeniz** gerekiyor. Bulduklarınızı Bölüm 5.4'teki tabloya işleyin.

### A. Hukuk ve mevzuat
| Kaynak | İçerik |
|---|---|
| mevzuat.gov.tr | Kanun, yönetmelik, tüzük, genelge |
| Resmî Gazete (resmigazete.gov.tr) | Günlük yayımlanan mevzuat |
| Yargıtay karar arama | Yargıtay kararları |
| Anayasa Mahkemesi kararlar bilgi bankası | AYM kararları |
| Danıştay kararları | İdari yargı kararları |

- **Artısı:** Çok büyük hacim, yapılı (madde madde), terim yoğun ("4857 s. K. m.17"), gerçek ihtiyaç var (avukatlar, vatandaşlar, İK). Kanun, yönetmelik ve mahkeme kararları FSEK m.31 kapsamında genel olarak telif korumasına tabi değildir. Yine de sitelerin kullanım koşullarını ayrıca kontrol edin.
- **Eksisi:** Hukuki RAG çalışması çok sayıda var. Özgünlük için alt alan seçmek gerekebilir (ör. sadece iş hukuku). Selim'in GraphRAG projesi de hukuk/arşiv odaklı.

### B. Vergi ve mali mevzuat
| Kaynak | İçerik |
|---|---|
| Gelir İdaresi Başkanlığı (gib.gov.tr) | Kanunlar, tebliğler, sirküler, **özelgeler** (mükellef sorusuna verilen resmi cevaplar) |
| Hazine ve Maliye Bakanlığı | Mevzuat ve duyurular |

- **Artısı:** Özelgeler hazır **soru-cevap yapısında**: "Mükellef şunu sordu, idare şunu cevapladı." Bu yapı test seti için altın değerinde. Çok terim ve kod içeriyor (KDV, GVK m.94, tevkifat oranları). Muhasebeci ve KOBİ'ler gibi gerçek bir pazar var.
- **Eksisi:** Mevzuat sık değişiyor, güncellik takibi gerekiyor.

### C. Finans ve şirket bilgileri
| Kaynak | İçerik |
|---|---|
| KAP (kap.org.tr) | Borsa şirketlerinin özel durum açıklamaları, finansal raporlar |
| TCMB | Para politikası metinleri, Finansal İstikrar Raporu |
| SPK, BDDK | Bültenler, düzenlemeler |

- **Artısı:** Şirket adı, tutar ve tarih gibi kesin bilgiler içeren bol veri. Yatırımcı ve analist pazarı var.
- **Eksisi:** Tablolar ve sayılar ağırlıklı, PDF ayrıştırması zor. KAP verisinin kullanım koşulları kontrol edilmeli.

### D. Sağlık ve ilaç
| Kaynak | İçerik |
|---|---|
| TİTCK | İlaç Kısa Ürün Bilgileri (KÜB) ve Kullanma Talimatları (KT) |
| Sağlık Bakanlığı | Klinik rehberler, halk sağlığı dokümanları |

- **Artısı:** Etken madde ve ilaç adları gibi kesin terimlerin yanında "baş ağrısına iyi gelen ilaçlar yan etki" gibi doğal dil soruları var. Hibrit için mükemmel.
- **Eksisi:** **Yüksek risk alanı.** Yanlış cevap zarar verebilir. Ürün olarak sunmak hukuki sorumluluk getirir. PDF'ler dağınık.

### E. Eğitim ve üniversite mevzuatı
| Kaynak | İçerik |
|---|---|
| Üniversitelerin mevzuat sayfaları | Yönetmelik, yönerge, senato kararları |
| YÖK mevzuatı | Yükseköğretim yönetmelikleri |
| ÖSYM kılavuzları | Sınav ve yerleştirme kuralları |

- **Artısı:** Öğrenci olarak alanı biliyorsunuz ve test sorusu yazmak kolay ("Kaç dersten kalınca uzarım?"). Kendi üniversiteniz için ürün demo'su etkileyici olur.
- **Eksisi:** Tek üniversitenin hacmi küçük. Hacmi büyütmek için çok üniversiteyi kapsamak gerekir.

### F. Hazır Türkçe veri setleri (yardımcı / test amaçlı)
| Kaynak | Kullanım |
|---|---|
| Hugging Face Datasets | "turkish" + "retrieval", "question-answering", "legal", "news" ile arayın |
| TQuAD, XQuAD (Türkçe bölümü) | Türkçe soru-cevap setleri. Yöntemi genel bir sette doğrulamak için |
| BEIR (İngilizce) | Bilgi erişiminde standart test seti. Kodumuzu doğrulamak için: "BM25'imiz BEIR'deki bilinen sonuçlara yakın mı?" |

> **İpucu:** Hazır bir İngilizce benchmark (ör. BEIR'den küçük bir set: SciFact, NFCorpus) üzerinde kodumuzu doğrulamak, **"kodumuz doğru çalışıyor mu?"** sorusunu cevaplar. Literatürdeki sonuçlara yakın sonuç alırsak kendi Türkçe korpusumuzdaki sonuçlara da güvenebiliriz.

## 5.3 Araştırma süreci (Faz 1, 2–3 hafta)

```
Hafta 1 · Geniş tarama
  ├─ Her biriniz 3 sektöre bakar (toplam 6)
  ├─ Her kaynak için: URL, içerik türü, tahmini hacim, format, erişim yolu, lisans
  └─ Hafta sonu: kaynak listesi tablosu (Bölüm 5.4)

Hafta 2 · Derin inceleme (en iyi 3 aday)
  ├─ Her adaydan ~100 belge indirin (küçük bir örneklem)
  ├─ Metin kalitesine bakın: OCR hatası, tablo, gürültü
  ├─ Her aday için 20 örnek soru yazın:
  │     10 "kelime" sorusu   ör. "GVK 94. madde tevkifat oranları"
  │     10 "anlam" sorusu    ör. "serbest meslek kazancında kesinti ne kadar?"
  ├─ Örneklem üzerinde hızlı BM25 + vektör denemesi (notebook)
  └─ Puanlama tablosunu doldurun (Bölüm 5.5)

Hafta 3 · Karar
  ├─ Korpus raporu (docs/korpus-raporu.md)
  ├─ Hocayla görüşme ve onay
  └─ Seçilen + yedek sektör
```

## 5.4 Kaynak envanteri şablonu

İncelediğiniz her kaynağı bu tabloya ekleyin. Tabloyu `docs/korpus-raporu.md` dosyasında tutun.

| # | Sektör | Kaynak | URL | Format | Tahmini hacim | Erişim | Lisans/koşul | Kalite (1–5) | İnceleyen | Not |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Vergi | GİB Özelgeler | ... | HTML | ? belge | Web, sayfalı | Kamu | ? | Zehra | |
| 2 | ... | | | | | | | | | |

## 5.5 Puanlama matrisi

Her kriteri 1–5 arası puanlayın, ağırlıkla çarpıp toplayın. Ağırlıklar önerimizdir. Hocayla birlikte değiştirebilirsiniz.

| Kriter | Ağırlık | Sektör A | Sektör B | Sektör C |
|---|---|---|---|---|
| Erişilebilirlik ve indirme kolaylığı | 3 | | | |
| Lisans uygunluğu (akademik + ticari) | 3 | | | |
| Hacim | 2 | | | |
| Metin kalitesi | 2 | | | |
| Hibrite uygunluk (hem terim hem doğal dil) | **4** | | | |
| Test seti üretme kolaylığı | **4** | | | |
| Pazar ve gerçek ihtiyaç | 3 | | | |
| Özgünlük (literatürde az çalışılmış mı?) | 2 | | | |
| Risk (düşük risk = yüksek puan) | 2 | | | |
| Ekibin alana ilgisi | 1 | | | |
| **Toplam (ağırlıklı)** | | | | |

## 5.6 Hukuki ve etik kontrol listesi

- [ ] Sitenin kullanım koşulları otomatik veri toplamaya izin veriyor mu?
- [ ] `robots.txt` hangi yolları yasaklıyor?
- [ ] İstek hızını sınırlıyor muyuz? (ör. saniyede en fazla 1 istek, gece saatlerinde)
- [ ] Veride **kişisel veri** var mı (isim, TCKN, adres)? Varsa KVKK gereği maskelenmeli. Mahkeme kararlarında taraf isimleri bu kapsama girer
- [ ] Verinin kendisini repoda paylaşmıyoruz. Sadece **indirme betiğini** paylaşıyoruz
- [ ] Kaynak ve atıf bilgisi her belgenin meta verisinde tutuluyor

## 5.7 Korpus raporunun içeriği (Faz 1 teslimi)

`docs/korpus-raporu.md` dosyası şu bölümleri içerecek:

1. İncelenen sektörler ve kaynaklar (envanter tablosu)
2. Her aday için örnek belgeler ve örnek sorular
3. Örneklem deneyinin sonuçları (BM25 ve vektör, kaba ölçüm)
4. Puanlama matrisi
5. **Karar:** Seçilen sektör ve gerekçesi, yedek sektör
6. Veri toplama planı: nasıl indirilecek, ne kadar sürer, nasıl güncellenecek
7. Riskler
