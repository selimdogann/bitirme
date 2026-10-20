# 8. Yol Haritası

Proje 10 aşamaya bölündü. Her aşamanın **görevleri, teslimi ve "bitti sayılır" koşulu** var.

**Kurallar:**
- Bir aşamanın "bitti sayılır" koşulu karşılanmadan sonrakine geçilmez.
- Her aşamanın sonunda sistem **çalışır durumda** olur.
- Her aşamanın sonunda **anlat-öğret oturumu** yapılır: her biriniz diğerinin yazdığı kısmı anlatır.
- Her aşama GitHub'da bir **milestone**, her görev bir **issue** olur ([Çalışma Düzeni](09-calisma-duzeni.md)).
- Süreler tahminidir; bölümün teslim tarihleri öğrenilince güncellenecek.

```
Ekim      Kasım             Aralık            Ocak              Şubat         Mart          Nisan         Mayıs
│ A0 │──── A1 ────│── A2 ──│── A3 ──│── A4 ──│── A5 ──│ (sınav) │── A6 ──│── A7 ──│──── A8 ────│── A9 ──│
 altyapı  veri      BM25     vektör   hibrit   test seti          cevap     cevap      ürün        rapor
                                               + ölçüm  ▲                  ölçümü                    ▲
                                                    ara rapor                                      final
```

---

## Aşama 0: Altyapı

**Öğrenme hedefleri:** uv, Git/GitHub, dal-commit-PR akışı.

- [x] Repo, uv ve Python 3.12 ortamı
- [x] Boş Streamlit arayüzü
- [x] ruff ve her PR'da çalışan CI
- [x] PR ve issue şablonları, `main` dal koruması
- [ ] Zehra repoyu klonlayıp `uv sync` ve `uv run streamlit run app.py` çalıştırıyor
- [ ] Hocayla görüşme: [teyit soruları](01-proje-tanimi.md#17-hocaya-sorulacaklar)

**Bitti sayılır:** İkiniz de kendi bilgisayarınızda uygulamayı açabiliyor ve en az birer PR açıp birleştirdiniz.

---

## Aşama 1: Veri (kullanma talimatlarından parçalara)

**Öğrenme hedefleri:** PDF'ten metin çıkarma, metin temizleme, parçalama.

- [ ] 5 ilacın kullanma talimatını TİTCK'dan indirmek ([Korpus ve Veri](05-korpus-arastirmasi.md))
- [ ] PDF'ten metin çıkarmak, Türkçe karakterleri kontrol etmek
- [ ] Metni talimatın bölüm başlıklarına ve paragraflara ayırmak
- [ ] `data/processed/chunks.jsonl` üretmek ([Mimari §3.3](03-mimari.md#33-veri-biçimi-chunksjsonl))
- [ ] TİTCK kullanım koşullarını kontrol etmek

**Teslim:** `ingest.py`
**Bitti sayılır:** `uv run python ingest.py` komutu 5 PDF'ten `chunks.jsonl` üretiyor ve her parçanın ilacı, bölümü ve sayfası doğru.

---

## Aşama 2: BM25

**Öğrenme hedefleri:** Ters indeks, TF-IDF, BM25, Türkçe ön işleme.

- [ ] Türkçeye uygun küçük harfe çevirme ve kelimelere bölme
- [ ] BM25'i sıfırdan yazmak ([Temel Kavramlar §2.5](02-temel-kavramlar.md))
- [ ] Sonucu `bm25s` kütüphanesiyle karşılaştırmak
- [ ] Streamlit'te soru kutusuna göre ilk 5 paragrafı göstermek

**Teslim:** `search.py` içinde BM25
**Bitti sayılır:** Arayüzde "Parol hamilelik" yazınca ilgili paragraf ilk sonuçlarda çıkıyor.

---

## Aşama 3: Vektör araması

**Öğrenme hedefleri:** Embedding, kosinüs benzerliği.

- [ ] Paragrafları bir embedding modeliyle vektöre çevirmek ve kaydetmek
- [ ] NumPy ile benzerlik araması
- [ ] Arayüzde BM25 ve vektör sonuçlarını yan yana göstermek

**Bitti sayılır:** "Emzirirken içebilir miyim?" gibi talimattaki kelimeleri içermeyen sorularda vektör araması doğru paragrafı buluyor.

---

## Aşama 4: Hibrit arama

**Öğrenme hedefleri:** RRF, doğrusal birleştirme, puan normalizasyonu ([Birleştirme Yöntemleri](06-birlestirme-yontemleri.md)).

- [ ] RRF
- [ ] Doğrusal birleştirme (min-max)
- [ ] Arayüzde üç yöntemin sonuçlarını yan yana göstermek

**Bitti sayılır:** Arayüzde BM25, vektör ve hibrit sonuçlarını karşılaştırabiliyorsunuz. Bu, **arama prototipinin (v0)** tamamlanması demek.

---

## Aşama 5: Test seti ve ölçüm

**Öğrenme hedefleri:** Test seti tasarımı, Recall, MRR, nDCG.

- [ ] Talimatları 50+ ilaca çıkarmak
- [ ] 200–300 soruluk test seti ve etiketleme kuralları ([Değerlendirme §7.1](07-degerlendirme.md#71-test-seti))
- [ ] `evaluate.py`: arama metrikleri
- [ ] Sonuç tablosu ve soru tipine göre kırılım

**Teslim:** İlk sonuç tablosu. **Ara rapor ve sunum için ideal nokta.**
**Bitti sayılır:** "Hibrit arama, BM25'e göre Recall@5'te şu kadar daha iyi" diyebiliyorsunuz.

---

## Aşama 6: Cevap üretimi

**Öğrenme hedefleri:** Yerel dil modeli, istem yazma, kanıt kontrolü.

- [ ] Ollama ile 2 Türkçe yetenekli modeli denemek
- [ ] `answer.py`: yalnızca verilen paragraflara dayanan, kaynak gösteren istem
- [ ] Kanıt eşiği: yeterli kanıt yoksa "bilgi yok" ([Mimari §3.5](03-mimari.md#35-cevap-verme-kuralı))
- [ ] Arayüzde cevap ve altında kaynak paragraf

**Bitti sayılır:** Arayüzde soru sorunca kaynaklı cevap geliyor; cevabı olmayan soruda sistem cevap vermiyor.

---

## Aşama 7: Cevap değerlendirmesi

- [ ] 50 cevaplık örneklemde cevap ve kaynak doğruluğu ([Değerlendirme §7.3](07-degerlendirme.md#73-cevap-metrikleri-aşama-7))
- [ ] Cevap vermeme ölçümü ve eşik seçimi ([§7.4](07-degerlendirme.md#74-cevap-vermeme-ölçümü))
- [ ] MedTurkQuAD ile ikinci kontrol
- [ ] Gerekirse cross-encoder ile yeniden sıralama

**Bitti sayılır:** AS4 ve AS5'e ([Proje Tanımı §1.4](01-proje-tanimi.md#14-araştırma-soruları)) verilerle cevap verebiliyorsunuz.

---

## Aşama 8: Ürünleştirme

- [ ] Arayüzü sadeleştirmek: yaşlı bir kullanıcının da kullanabileceği kadar
- [ ] Daha fazla ilaç
- [ ] Canlı demo adresi
- [ ] Projeyi bilmeyen 3–5 kişiyle kullanılabilirlik denemesi

**Bitti sayılır:** Projeyi hiç görmemiş biri arayüzü yardımsız kullanabiliyor.

---

## Aşama 9: Rapor, sunum ve görünürlük

- [ ] Bitirme raporu ve sunum (internet kesilirse diye demo videosu)
- [ ] Test setini Hugging Face'te yayınlamak (lisans hocayla netleştirilerek)
- [ ] Hocayla bildiri ([Proje Tanımı §1.7](01-proje-tanimi.md#17-hocaya-sorulacaklar))
- [ ] Savunma provası: birbirinize jüri gibi soru sorun

---

## Zaman kalırsa

- Dinamik α: birleştirme ağırlığını her soruya göre seçmek
- Danışmanımızın TurkishMedLLM sistemine hibrit arama modülü olarak entegrasyon
- İlaç kutusundaki karekodu okutunca talimatın açılması
- İki ilacın birlikte kullanımı hakkındaki soruları cevaplama
