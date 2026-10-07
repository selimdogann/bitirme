# Hibrit RAG: Bitirme Projesi

> **Ekip:** Selim Doğan · Zehra
> **Bölüm:** Kocaeli Üniversitesi, Bilgisayar Mühendisliği
> **Dönem:** 2026–2027
> **Durum:** Faz 0, Hazırlık

## Proje tek cümlede

Seçeceğimiz bir sektörün belgelerinde **anahtar kelime araması (BM25)** ile **vektörel (anlamsal) aramayı** birleştiren, **farklı birleştirme (fusion) yöntemlerini ölçerek karşılaştıran** ve kullanıcının sorusuna **kaynak göstererek** cevap veren, gerçek kullanıma hazır bir **Hibrit RAG** sistemi.

```
              ┌─► BM25 (kelime eşleşmesi) ─┐
Soru ─► Ön işleme                           ├─► Birleştirme ─► Yeniden sıralama ─► LLM ─► Kaynaklı cevap
              └─► Vektör (anlam benzerliği)┘     (RRF, ağırlıklı, ...)
```

## Dokümanlar

Bu repo projenin **kodunu ve öğrenme rehberini** birlikte tutar. Dokümanları aşağıdaki sırayla okuyun.

| # | Doküman | İçerik | Ne zaman okunur |
|---|---|---|---|
| 1 | [Proje Tanımı](docs/01-proje-tanimi.md) | Hocanın istediği, bizim istediğimiz, kapsam, başarı ölçütleri | İlk gün |
| 2 | [Temel Kavramlar](docs/02-temel-kavramlar.md) | RAG, BM25, embedding, vektör DB, fusion, reranking: sıfırdan anlatım | İlk hafta |
| 3 | [Mimari](docs/03-mimari.md) | Sistem bileşenleri, veri akışı, klasör yapısı, arayüzler | Faz 0 sonunda |
| 4 | [Teknolojiler](docs/04-teknolojiler.md) | Hangi araç, neden, alternatifi ne, ne zaman öğrenilecek | Faz 0 sonunda |
| 5 | [Korpus Araştırması](docs/05-korpus-arastirmasi.md) | Açık veri kaynakları, sektör seçimi, puanlama tablosu | Faz 1 |
| 6 | [Birleştirme Yöntemleri](docs/06-birlestirme-yontemleri.md) | RRF'den öğrenerek sıralamaya tüm fusion yöntemleri | Faz 5–6 |
| 7 | [Değerlendirme](docs/07-degerlendirme.md) | Test seti, metrikler, deney protokolü | Faz 2'den itibaren |
| 8 | [Yol Haritası](docs/08-yol-haritasi.md) | Faz faz görevler, öğrenme hedefleri, teslimler | Her faz başında |
| 9 | [Çalışma Düzeni](docs/09-calisma-duzeni.md) | Git akışı, görev paylaşımı, yapay zekâ kullanım kuralları | İlk gün |
| 10 | [Kaynaklar ve Sözlük](docs/10-kaynaklar-ve-sozluk.md) | Makaleler, dokümantasyonlar, terimler | Gerektikçe |

## Temel ilkemiz

> **Bu projede her satırı biz anlayacağız.** Hazır bir kütüphaneyi kullanmadan önce o kütüphanenin yaptığını bir kez kendimiz yazacağız. Hiçbir kod, ikimiz de anlatamıyorsak `main`'e girmeyecek.

Ayrıntılar: [Çalışma Düzeni → Sahiplik kuralları](docs/09-calisma-duzeni.md#95-sahiplik-ve-yapay-zekâ-kullanım-kuralları)
