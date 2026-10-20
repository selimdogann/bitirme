# 5. Korpus ve Veri

Bu doküman sistemin **hangi belgelerde arama yapacağını**, **test sorularının nereden geleceğini** ve **verinin hukuki açıdan nasıl kullanılacağını** anlatır.

> **Korpus:** Sistemin içinde arama yaptığı belge koleksiyonu. **Soru-cevap korpusu:** Her sorunun doğru cevabının bilindiği set; sistemi ölçmek için kullanılır.

---

## 5.1 Karar: TİTCK kullanma talimatları

Sistemin arayacağı belgeler, Türkiye İlaç ve Tıbbi Cihaz Kurumu'nun (TİTCK) yayımladığı **ilaç kullanma talimatları (KT)**.

| Özellik | Neden önemli |
|---|---|
| **Resmî ve güncel** | Kaynak gösterdiğimiz bilgi güvenilir olmalı |
| **Türkçe ve hasta için yazılmış** | Kullanıcımız hasta; kutunun içinden çıkan metin |
| **Aynı başlıklarla yazılmış** | "Nedir ve ne için kullanılır", "Kullanmadan önce dikkat edilmesi gerekenler", "Nasıl kullanılır", "Olası yan etkiler", "Saklanması". Parçalamayı ve kaynağı göstermeyi kolaylaştırır |
| **Hibrite uygun** | Hem kesin terimler (ilaç adı, etkin madde, doz) hem de doğal dille sorulan sorular var |

**KT ve KÜB farkı:**
- **KT (Kullanma Talimatı):** Hasta için. Kullanacağımız belge bu.
- **KÜB (Kısa Ürün Bilgisi):** Doktor ve eczacı için teknik belge. Şimdilik kullanmıyoruz.

**Nereden alınır:** [TİTCK KÜB / KT Sorgulama Portalı](https://www.titck.gov.tr/kubkt). İlaç adı, etkin madde ya da firma adıyla aranır; "Kt Dokümanı" sütunundan PDF indirilir.

**Plan:**
1. Önce 5 ilaç elle indirilir: Parol, Arveles, Augmentin, Coraspin, Majezik.
2. Metin çıkarma ve parçalama bu 5 belgeyle denenir.
3. Sonra 50+ ilaca çıkılır. Toplu indirme yapılacaksa önce sitenin kullanım koşulları kontrol edilir.

## 5.2 Test için soru-cevap veri setleri

Hazır bir "Türkçe ilaç talimatı + soru" seti bulunamadı. Bu yüzden ana test setini kendimiz hazırlayacağız ([Değerlendirme](07-degerlendirme.md)). Araştırmada bulunan hazır setler ikinci kontrol ve karşılaştırma için kullanılacak.

| Veri seti | Boyut | Paragraf var mı? | Lisans | Projedeki rolü |
|---|---|---|---|---|
| [MedTurkQuAD](https://huggingface.co/datasets/incidelen/MedTurkQuAD) | 8.200 tıbbi soru (test bölümü 820) | Evet | CC BY-NC-ND 4.0, ticari kullanım yasak | Yöntemin genel sağlık metinlerinde de çalıştığını göstermek |
| [NFCorpus-TR](https://huggingface.co/datasets/trmteb/nfcorpus-tr) | 3.630 belge, 3.240 soru, hazır etiketler | Evet | Belirtilmemiş | Türkçeye çevrilmiş tıbbi arama testi |
| [TurkishRAGEval](https://huggingface.co/datasets/mteb/turkish-rag-eval) | 58 soru, 54 sağlık makalesi | Evet | CC BY-SA 4.0 | Yayımlanmış referans sonuçlarla karşılaştırma |
| [turkish-drug-interaction-qa](https://huggingface.co/datasets/magahcicek/turkish-drug-interaction-qa) | 260 ilaç etkileşimi sorusu | Hayır | Belirtilmemiş | Soru tarzı için örnek |

Bütün setlerin ayrıntılı listesi ve değerlendirmesi ekip içinde paylaşılan araştırma raporunda: [Türkçe Soru-Cevap Veri Setleri Araştırması](https://claude.ai/code/artifact/a1f020b5-6ba7-4c82-a349-a1b3791bd07c) (erişim izni gerekir).

**Paragraf neden önemli?** Arama sistemini ölçmek için her sorunun cevabının **hangi belgede** olduğunu bilmemiz gerekiyor. Sadece soru ve cevap içeren setlerle arama ölçülemez.

## 5.3 Yedek korpus

TİTCK belgeleri kullanılamazsa: [Türk hastane makaleleri](https://huggingface.co/datasets/alibayram/turkish-hospital-medical-articles). 14 hastaneden 24.612 sağlık makalesi, CC BY 4.0 lisanslı. Bu durumda proje "ilaç" yerine "genel sağlık bilgisi" asistanına döner; mimari değişmez.

## 5.4 Hukuki ve etik kontrol listesi

- [ ] TİTCK sitesinin kullanım koşulları belgelerin indirilip kullanılmasına izin veriyor mu?
- [ ] Toplu indirme yapılacaksa hız sınırına uyuluyor mu? (ör. saniyede en fazla 1 istek)
- [ ] PDF'ler repoda paylaşılmıyor (`data/raw/` git'e girmez); sadece nasıl indirileceği yazılıyor
- [ ] Her parçanın hangi PDF'ten ve hangi sayfadan geldiği kayıtlı
- [ ] Kullanılan her veri setinin lisansı yazılı ve ürüne konacaksa ticari kullanıma izin veriyor
- [ ] Hasta–doktor soruları gibi kişisel sağlık verisi içerebilecek setler kullanılırsa KVKK'ya uygun şekilde, kimlik bilgilerinden arındırılarak kullanılıyor
- [ ] Arayüzde "tıbbi tavsiye değildir" uyarısı var
