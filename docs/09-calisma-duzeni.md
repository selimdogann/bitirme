# 9. Çalışma Düzeni

İki kişinin aynı projede **birbirinin işini bozmadan, ikisinin de her şeyi öğrenerek** çalışması için kurallar.

---

## 9.1 Rol dağılımı: dönüşümlü sahiplik

Sabit roller yok. Her işin bir **yapanı** ve bir **inceleyeni** var; benzer işlerde roller yer değiştirir.

| Aşama | Selim | Zehra |
|---|---|---|
| 0: Altyapı | Repo, CI, şablonlar | Ortamı kendi bilgisayarında kurup test etme |
| 1: Veri | PDF'ten metin çıkarma | Bölümlere ve paragraflara ayırma |
| 2: BM25 | Arayüze bağlama | Türkçe ön işleme ve BM25 |
| 3: Vektör | Embedding ve arama | Arayüzde yan yana gösterim |
| 4: Hibrit | Doğrusal birleştirme | RRF |
| 5: Test seti | **İkisi birlikte**, yarı yarıya | |
| 6: Cevap | Kanıt eşiği | İstem ve Ollama bağlantısı |
| 7: Cevap ölçümü | Cevap vermeme ölçümü | Cevap ve kaynak doğruluğu |
| 8: Ürün | Canlı demo | Arayüz sadeleştirme |
| 9: Rapor | Bölümler eşit dağıtılır | |

> Bu tablo bir öneri. Kural şu: **bir aşamada birinin yaptığını, bir sonraki benzer işte diğeri yapar.**

## 9.2 Git akışı

```
main  ──●───────────────●───────────────●──────►   (korumalı, her zaman çalışır)
         \             /  \             /
          ●──●──●─────●    ●──●──●─────●
          feat/bm25         feat/vektor-arama
```

**`main` dalının kuralları** (GitHub'da ayarlı):
- `main`'e doğrudan push **yasak**. Her değişiklik bir PR ile gelir.
- PR'ın birleşebilmesi için **CI'ın (ruff) geçmesi** ve PR'daki yorumların çözülmesi gerekir.
- Onay şartı yok. Ama birleştirmeden önce diğer kişinin PR'a bakması beklenir.
- PR'lar **squash** ile birleşir: PR'daki bütün commit'ler `main`'e tek bir commit olarak girer.
- Birleşen dal otomatik silinir.

### Dal adları

| Önek | Ne için | Örnek |
|---|---|---|
| `feat/` | Yeni özellik | `feat/bm25` |
| `fix/` | Hata düzeltme | `fix/turkce-kucuk-harf` |
| `docs/` | Doküman | `docs/test-seti-kurallari` |
| `chore/` | Ortam, ayar, araç | `chore/ruff-ayari` |
| `exp/` | Deney | `exp/rrf-k-taramasi` |

### Commit mesajları

[Conventional Commits](https://www.conventionalcommits.org/) biçiminde, **Türkçe ve kısa**: bir başlık ve gerekiyorsa 1–2 cümlelik açıklama.

```
feat: BM25 araması eklendi
fix: Türkçe büyük İ harfinin küçültülmesi düzeltildi
docs: test seti etiketleme kuralları yazıldı
chore: sentence-transformers bağımlılığı eklendi
test: RRF için elle hesaplanmış örnek testi eklendi
```

| Tür | Ne zaman |
|---|---|
| `feat` | Yeni bir özellik |
| `fix` | Hata düzeltme |
| `docs` | Sadece doküman |
| `chore` | Ortam, bağımlılık, ayar |
| `ci` | GitHub Actions |
| `test` | Test ekleme veya düzeltme |
| `refactor` | Davranışı değiştirmeden kodu düzenleme |

## 9.3 Bir işin baştan sona akışı

**1. Issue aç.** GitHub'da **Issues → New issue → Görev**. Ne yapılacağını ve "bitti sayılır" koşulunu yaz, etiket ve milestone seç.

**2. Güncel `main`'den dal aç.**
```bash
git switch main
git pull
git switch -c feat/bm25
```

**3. Çalış, küçük ve sık commit at.**
```bash
git status                       # ne değişti?
git add search.py                # commit'e girecek dosyayı seç
git commit -m "feat: BM25 için ters indeks eklendi"
```

**4. Göndermeden önce kontrol et.**
```bash
uv run ruff check --fix .        # hataları bul, düzeltilebilenleri düzelt
uv run ruff format .             # biçimi düzelt
```

**5. Dalı GitHub'a gönder ve PR aç.**
```bash
git push -u origin feat/bm25
```
GitHub sayfasında çıkan **"Compare & pull request"** düğmesine bas. Açıklamayı şablona göre doldur; issue'yu kapatmak için `Closes #12` yaz.

**6. İnceleme.** Diğer kişi PR'daki değişiklikleri okur, anlamadığı satırı yorumla sorar. Yorumlar çözülür.

**7. Birleştir.** CI yeşilse **"Squash and merge"**. Dal kendiliğinden silinir.

**8. Yerelde temizle.**
```bash
git switch main
git pull
git branch -d feat/bm25
```

## 9.4 Görev takibi

- **Issues:** Her iş bir issue. Bir issue en fazla 1–2 günlük iş olmalı; büyükse bölün.
- **Etiketler:** `görev`, `hata`, `veri`, `arama`, `cevap`, `değerlendirme`, `arayüz`, `dokümantasyon`, `altyapı`, `öğrenme`
- **Milestone:** Her aşama bir milestone ([Yol Haritası](08-yol-haritasi.md)).
- **Proje panosu:** `Yapılacak → Yapılıyor → İncelemede → Bitti`

## 9.5 Toplantı ritmi

| Ne | Ne zaman | Süre | İçerik |
|---|---|---|---|
| **Kısa senkron** | Haftada 2–3 kez | 15 dk | Ne yaptım, ne yapacağım, nerede takıldım |
| **Haftalık plan** | Pazartesi | 30 dk | Issue'ları gözden geçir, haftanın işlerini paylaş |
| **Anlat-öğret** | Her aşama sonunda | 1 saat | Her biriniz **diğerinin** yazdığı kodu anlatır. Anlatamadığınız yer varsa aşama bitmemiştir |
| **Hoca görüşmesi** | 2 haftada bir | 30 dk | Önceden 1 sayfalık ilerleme notu (`docs/toplantilar/`) |
| **Birlikte kodlama** | Haftada 1 | 2 saat | Zor bir kısmı tek ekranda birlikte yazın |

## 9.6 Sahiplik ve yapay zekâ kuralları

Projenin kontrolü **sizde** kalsın diye bu kurallar Claude dahil bütün yapay zekâ araçları için geçerli.

### Yapay zekâyı şunlar için kullanın ✅
- **Kavram öğrenmek:** "BM25'te b parametresi ne işe yarar, örnekle anlat"
- **Takıldığınızda ipucu almak:** "Kodum bu hatayı veriyor, nedenini bulmama yardım et"
- **Kodunuzu inceletmek:** "Yazdığım RRF fonksiyonunda hata var mı?"
- **Test fikri almak:** "Bu fonksiyon için hangi uç durumları test etmeliyim?"
- **Öğretici olmayan işler:** proje iskeleti, ayar dosyaları, grafik kodu

### Şunlardan kaçının ❌
- Bir modülün tamamını yazdırıp anlamadan commit etmek
- Çıkan düzeltmeyi neden işe yaradığını anlamadan uygulamak
- Rapordaki analiz ve yorumları yazdırmak; bunlar sizin düşünceniz olmalı

### Altın kural
> **"Bu satır ne yapıyor, neden böyle?" sorusuna cevap veremediğiniz kod `main`'e girmez.**
> PR'ı inceleyen kişi bu soruyu rastgele bir satır için sorabilir.

## 9.7 Öğrenme günlüğü

Her biriniz `docs/gunluk/selim.md` ve `docs/gunluk/zehra.md` dosyalarında haftalık kısa notlar tutun:

```markdown
## Hafta 3 (2026-11-02)
**Öğrendim:** BM25'te uzunluk normalizasyonu neden gerekli...
**Zorlandım:** Türkçe 'İ' harfinin küçültülmesi...
**Sorularım:** Kök bulma ilaç adlarını bozar mı? → deneyle bakacağız
```

Raporu yazarken ve savunmada "ne öğrendiniz?" sorusunda çok işe yarar.

## 9.8 "Bitti" tanımı

Bir iş ancak şu koşullar sağlanınca bitmiş sayılır:
- [ ] Kod çalışıyor
- [ ] CI yeşil
- [ ] Diğer kişi PR'a baktı
- [ ] Gerekiyorsa doküman güncellendi
- [ ] Yazan kişi kodu diğerine anlatabiliyor

## 9.9 Kod standartları

- **Tip ipuçları** her fonksiyonda: `def search(query: str, k: int) -> list[dict]:`
- **Docstring:** Her fonksiyonda kısa açıklama; Türkçe olabilir
- **İsimlendirme:** Kod İngilizce (`search`, `chunk`), doküman ve yorumlar Türkçe
- **Sihirli sayı yok:** `k=60` gibi değerler dosyanın başında adlandırılmış sabit olur
- **Gizli bilgiler** (şifre, API anahtarı) asla repoya girmez, `.env` dosyasında tutulur
