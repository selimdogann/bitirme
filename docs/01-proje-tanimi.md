# 1. Proje Tanımı

Bu doküman üç soruya cevap verir: **Hoca ne istiyor? Biz ne istiyoruz? İkisini birleştiren proje ne?**

---

## 1.1 Hocanın istediği

| Hocanın söylediği | Teknik anlamı | Projedeki karşılığı |
|---|---|---|
| "Hibrit RAG yapacaksınız" | Kelime araması ile vektör aramasını birlikte kullanan, bulduğu belgelere dayanarak cevap üreten sistem | Sistemin tamamı |
| "Korpusları araştırın" | Arama yapılacak belge koleksiyonlarını inceleyin | Kullanma talimatları ([Korpus ve Veri](05-korpus-arastirmasi.md)) |
| "Soru-cevap korpuslarını da araştırın" | Cevabı belli olan soru setleri: sistemi ölçmek için gerekli | Test seti ([Değerlendirme](07-degerlendirme.md)) |
| "Vektörel arama olacak, birleştireceğiz" | Anlam araması + kelime araması, sonuçların tek listede birleştirilmesi | Hibrit arama ([Birleştirme Yöntemleri](06-birlestirme-yontemleri.md)) |
| "Büyük veri setine gerek yok" | Az ama doğru etiketlenmiş veri yeterli | 200–300 soruluk test seti |

## 1.2 Bizim istediğimiz

1. **Gerçekten işe yarayan bir ürün.** İnsanların gerçek bir sorununu çözsün.
2. **Öğrenmek ve sahiplik.** Her parçayı ikimiz de anlatabilelim, değiştirebilelim, savunabilelim.
3. **Adım adım ilerlemek.** Her aşamanın sonunda çalışan bir sistem olsun.
4. **Görünürlük.** Açık veri seti, bildiri, yarışma ve canlı demo ile adımızı duyuralım.

## 1.3 Proje: Türkçe İlaç Asistanı

**Sorun.** Kullanma talimatları uzun, yazıları küçük ve dili ağır; çoğu insan okumuyor. Ama soruları var: "Aç karnına mı içeceğim?", "Hamileyken kullanabilir miyim?", "Bir dozu unutursam ne yapayım?" Eczanenin kapalı olduğu saatlerde ya da birkaç ilaç kullanan yaşlı bir yakın için bu sorular daha da önemli.

**Çözüm.** Kullanıcı sorusunu doğal Türkçeyle yazar. Sistem resmî kullanma talimatında ilgili bölümü bulur, sade bir dille cevap verir ve **talimattaki kaynak paragrafı gösterir.** Talimatta yeterli bilgi yoksa **cevap uydurmaz**, "Bu bilgi talimatta bulunmuyor, eczacınıza danışın" der.

**Neden hibrit arama?** İlaç sorularında iki tür ihtiyaç var:

| Soru | Kim yakalar? |
|---|---|
| "Parol 500 mg günde kaç tane?" | **BM25:** ilaç adı ve doz gibi kesin terimler |
| "Ateşim var, emziriyorum, ne içebilirim?" | **Vektör araması:** belgedeki kelimeler geçmiyor, anlam benziyor |

İkisini birleştirmek iki tür soruda da doğru bölümü bulmayı sağlar.

**Ne değildir?** Tıbbi tavsiye vermez, teşhis koymaz, doz önermez. Yalnızca resmî talimattaki bilgiyi kaynağıyla aktarır.

## 1.4 Araştırma soruları

- **AS1:** İlaç sorularında BM25, vektör araması ve hibrit arama ne kadar başarılı? Hangi soru tipinde hangisi daha iyi?
- **AS2:** Hangi birleştirme yöntemi (RRF, doğrusal birleştirme) bu veride daha iyi çalışıyor?
- **AS3:** Türkçe ön işleme (Türkçeye uygun küçük harf, kök bulma) BM25'i ne kadar etkiliyor?
- **AS4:** Üretilen cevaplar ne kadar doğru, gösterilen kaynak cevabı gerçekten destekliyor mu?
- **AS5:** Sistem, cevabı talimatta olmayan sorularda cevap vermemeyi ne kadar başarıyor? Gereksiz yere de "bilmiyorum" diyor mu?

## 1.5 Kapsam

**Kapsamda**
- TİTCK'nın yayımladığı ilaç kullanma talimatları (KT); önce 5, sonra 50+ ilaç
- BM25, vektör araması ve hibrit arama
- 200–300 soruluk Türkçe ilaç sorusu test seti
- Kaynak gösteren cevap üretimi ve "kanıt yetersiz" kontrolü
- Streamlit ile çalışan prototip, sonra canlı demo

**Şimdilik kapsam dışı**
- İlaç etkileşimi analizi (iki ilacın birlikte kullanımı)
- Kişisel sağlık verisi işleyen özellikler (kullanıcı hesabı, ilaç geçmişi)
- Mobil uygulama
- Kendi modelimizi eğitmek

## 1.6 Başarı ölçütleri

| Alan | Ölçüt |
|---|---|
| **Arama** | Hibrit arama, test setinde BM25'ten ve vektör aramasından daha yüksek Recall@5 alıyor |
| **Cevap** | Cevapların büyük çoğunluğu doğru ve her cevabın kaynağı onu destekliyor |
| **Güvenlik** | Cevabı talimatta olmayan soruların büyük çoğunluğunda sistem cevap vermiyor |
| **Ürün** | Projeyi bilmeyen biri arayüzü yardımsız kullanabiliyor |
| **Öğrenme** | Herhangi bir modülü ikimiz de 5 dakikada anlatabiliyoruz |

Sayısal hedefler ilk ölçümden sonra hocayla birlikte belirlenecek.

## 1.7 Hocaya sorulacaklar

- [ ] Konuyu ilaç kullanma talimatları üzerinde soru-cevap asistanı olarak daraltmak uygun mu? → *Cevap:*
- [ ] "Birleştirme" ile en iyi çalışan yöntemi seçmek mi bekleniyor, yoksa yöntemleri ayrıntılı karşılaştırmak mı? → *Cevap:*
- [ ] Projeyi TurkishMedLLM çalışmanızın arama tarafını hibrit aramayla geliştiren bir devam olarak kurabilir miyiz? Kullandığınız veriyi paylaşabilir misiniz? → *Cevap:*
- [ ] Test setini kendimiz hazırlayacağız; kaç soru yeterli? → *Cevap:*
- [ ] Sonuçları hangi konferansta bildiri olarak sunabiliriz? → *Cevap:*
- [ ] Ara rapor ve final teslim tarihleri, rapor biçimi? → *Cevap:*
- [ ] Kodun lisansı konusunda üniversitenin bir kuralı var mı? → *Cevap:*

## 1.8 Bağlantılı çalışma

Danışmanımızın ortak yazarı olduğu **TurkishMedLLM** ([Diagnostics, 2026](https://doi.org/10.3390/diagnostics16193142)) çalışması, 210.791 Türkçe tıbbi soru-cevap çifti ve 22.135 hastane makalesi üzerinde vektör tabanlı bir RAG sistemi kuruyor. Bizim projemiz, arama tarafına kelime aramasını ekleyip birleştirerek bu çizginin devamı olarak konumlanabilir. Diğer çalışmalar: [Kaynaklar](10-kaynaklar-ve-sozluk.md).

## 1.9 Riskler

| Risk | Olasılık | Önlem |
|---|---|---|
| TİTCK belgelerinin toplu kullanımına izin olmaması | Orta | Kullanım koşulları baştan kontrol edilecek; yedek: CC BY 4.0 lisanslı hastane makaleleri ([Korpus ve Veri](05-korpus-arastirmasi.md)) |
| PDF'lerden düzgün metin çıkmaması | Orta | Önce 5 belgeyle denenecek, gerekirse farklı PDF aracı |
| Yanlış cevabın zarar vermesi | Yüksek etki | Her cevapta kaynak paragraf, kanıt yoksa cevap vermeme, ekranda tıbbi tavsiye uyarısı |
| Test sorusu hazırlamanın uzun sürmesi | Orta | Dil modeliyle taslak + elle kontrol, iş ikiye bölünecek |
| Kapsamın büyümesi | Yüksek | Her aşamanın sonunda çalışan sistem; kapsam dışı listesi korunacak |
| Kodun anlaşılmadan eklenmesi | Orta | PR kuralları ve anlat-öğret oturumları ([Çalışma Düzeni](09-calisma-duzeni.md)) |
