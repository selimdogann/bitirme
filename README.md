# Türkçe İlaç Asistanı

> **Ekip:** Selim Doğan · Zehra Çetin
> **Danışman:** Prof. Dr. Sevinç İlhan Omurca
> **Bölüm:** Kocaeli Üniversitesi, Bilgisayar Mühendisliği · 2026–2027
> **Durum:** Aşama 0, Altyapı

## Proje tek cümlede

Resmî ilaç kullanma talimatlarında **kelime araması (BM25)** ile **anlam aramasını (vektör)** birleştiren **hibrit arama** sayesinde kullanıcının sorusuyla ilgili bölümü bulan, **sade Türkçe** bir cevap veren, **kaynak paragrafı gösteren** ve kanıt yoksa **cevap uydurmayan** bir asistan.

```
                  ┌─► BM25 (ilaç adı, doz gibi kesin terimler) ─┐
Kullanıcı sorusu ─┤                                              ├─► Birleştir ─► En uygun paragraflar
                  └─► Vektör (doğal dille sorulan sorular) ──────┘                      │
                                                                                         ▼
                                          Kanıt yeterli mi? ── Hayır ──► "Talimatta bu bilgi yok"
                                                │ Evet
                                                ▼
                                  Sade Türkçe cevap + kaynak paragraf
```

> Tıbbi tavsiye vermez. Cevaplar yalnızca kullanma talimatındaki bilgiye dayanır.

## Hızlı başlangıç

Gereken tek araç [uv](https://docs.astral.sh/uv/). Python 3.12'yi ve kütüphaneleri uv kurar.

```bash
git clone https://github.com/selimdogann/bitirme.git
cd bitirme
uv sync                        # ortamı kur
uv run streamlit run app.py    # arayüzü aç: http://localhost:8501
```

## Dokümanlar

| # | Doküman | İçerik |
|---|---|---|
| 1 | [Proje Tanımı](docs/01-proje-tanimi.md) | Hocanın istediği, bizim amacımız, araştırma soruları, kapsam, hocaya sorular |
| 2 | [Temel Kavramlar](docs/02-temel-kavramlar.md) | RAG, BM25, embedding, hibrit arama, reranking: sıfırdan anlatım |
| 3 | [Mimari](docs/03-mimari.md) | Bileşenler, veri akışı, dosya yapısı, cevap verme kuralı |
| 4 | [Teknolojiler](docs/04-teknolojiler.md) | Hangi araç ne işe yarıyor, neden seçildi |
| 5 | [Korpus ve Veri](docs/05-korpus-arastirmasi.md) | Kullanma talimatları, soru-cevap veri setleri, hukuki kontroller |
| 6 | [Birleştirme Yöntemleri](docs/06-birlestirme-yontemleri.md) | RRF, doğrusal birleştirme ve diğerleri |
| 7 | [Değerlendirme](docs/07-degerlendirme.md) | Test seti, arama ve cevap metrikleri, cevap vermeme ölçümü |
| 8 | [Yol Haritası](docs/08-yol-haritasi.md) | Aşamalar, görevler, "bitti sayılır" koşulları |
| 9 | [Çalışma Düzeni](docs/09-calisma-duzeni.md) | Dal, commit ve PR akışı, görev paylaşımı, yapay zekâ kuralları |
| 10 | [Kaynaklar ve Sözlük](docs/10-kaynaklar-ve-sozluk.md) | Makaleler, veri setleri, terimler |

## Nasıl çalışıyoruz?

`main` dalı korumalı. Her değişiklik kendi dalında yapılır ve Pull Request ile birleşir. Ayrıntılar: [Çalışma Düzeni](docs/09-calisma-duzeni.md).

## Temel ilkemiz

> **Bu projede her satırı biz anlayacağız.** Çekirdek parçaları (arama, birleştirme, ölçüm) önce kendimiz yazıp sonra hazır kütüphanelerle doğrulayacağız. İkimizin de anlatamadığı hiçbir kod `main`'e girmeyecek.
