# 9. Çalışma Düzeni

İki kişinin aynı projede **birbirinin işini bozmadan, ikisinin de her şeyi öğrenerek** çalışması için kurallar.

---

## 9.1 Rol dağılımı: rotasyonlu sahiplik

Sabit roller yok ("sen backend, ben frontend" gibi). Ama her işin bir **sürücüsü** (driver) ve bir **gözden geçireni** (reviewer) var. Bu roller her fazda yer değiştirir.

| Faz | Selim | Zehra | Not |
|---|---|---|---|
| 0: Hazırlık | Repo ayarları, CI | pyproject, pre-commit | Birlikte |
| 1: Korpus | 3 sektör | 3 sektör | Karar birlikte |
| 2: Veri hattı | Ayrıştırma, temizleme | Parçalama | Test seti: **ikisi birlikte** |
| 3: BM25 | Metrikler + runner | Türkçe ön işleme + BM25 | |
| 4: Vektör | Model karşılaştırma | Qdrant + Docker | |
| 5: Fusion | Puan tabanlı (Linear, Comb*) | Sıra tabanlı (RRF, Borda) | Analiz birlikte |
| 6: Rerank | Dinamik α | Reranker | |
| 7: LLM | RAGAS değerlendirme | İstem + istemci | |
| 8: API | Veritabanı | FastAPI uç noktaları | |
| 9: Ürün | Backend: kimlik doğrulama, önbellek, izleme | Frontend | |
| 10: Rapor | Bölümler eşit dağıtılır | | |

> Bu tablo bir öneridir. İlgi alanınıza göre değiştirin. Kural şu: **bir fazda bir kişinin yaptığını, bir sonraki benzer işte diğeri yapar.** Örnek: Faz 3'te Zehra arayıcı yazdıysa Faz 4'te arayıcıyı Selim yazar.

## 9.2 Git akışı

```
main  ─────●─────────────●─────────────●──────►   (her zaman çalışır, korumalı)
            \           /  \           /
feature/     ●──●──●───●    ●──●──●───●
bm25-turkish   (Zehra)       fusion-rrf (Selim)
```

1. Her iş bir **GitHub Issue** ile başlar
2. Issue'dan bir dal (branch) açılır: `feature/<kısa-ad>`, `fix/<kısa-ad>`, `exp/<deney-adı>`, `docs/<konu>`
3. Küçük ve sık commit atılır
4. İş bitince **Pull Request (PR)** açılır, açıklamada `Closes #12` yazılır
5. **Diğer kişi** inceler ve onaylar. CI yeşil olmalı
6. *Squash and merge* yapılır, dal silinir

### Commit mesajları ([Conventional Commits](https://www.conventionalcommits.org/))
```
feat(retrieval): BM25'e Türkçe kök bulma eklendi
fix(fusion): min-max'te tek elemanlı listede sıfıra bölme hatası
test(metrics): nDCG ranx ile karşılaştırma testi
docs(korpus): GİB özelgeleri envantere eklendi
exp(fusion): RRF k taraması sonuçları
```

### PR şablonu (`.github/pull_request_template.md`)
```markdown
## Ne yaptım?

## Neden?

## Nasıl test ettim?

## Öğrendiklerim / Zorlandığım yer

## Gözden geçirenin özellikle bakmasını istediğim yer

## Yapay zekâ kullanımı
- [ ] Kullanmadım
- [ ] Kullandım: ... (neyi, nasıl) — ve kodun her satırını anlatabilirim
```

## 9.3 Görev takibi

- **GitHub Projects** panosu: `Yapılacak → Yapılıyor → İncelemede → Bitti`
- Her faz bir **Milestone**
- Etiketler: `faz-3`, `deney`, `hata`, `dokümantasyon`, `öğrenme`
- Bir issue en fazla 1–2 günlük iş olmalı. Büyükse bölün

## 9.4 Toplantı ritmi

| Ne | Ne zaman | Süre | İçerik |
|---|---|---|---|
| **Kısa senkron** | Haftada 2–3 kez | 15 dk | Dün ne yaptım, bugün ne yapacağım, nerede takıldım |
| **Haftalık plan** | Pazartesi | 30 dk | Panoyu gözden geçir, haftanın issue'larını paylaştır |
| **Anlat-öğret** | Her faz sonunda | 1 saat | Her biriniz **diğerinin** yazdığı modülü tahtada anlatır. Anlatamadığınız yer varsa faz bitmemiştir |
| **Hoca görüşmesi** | 2 haftada bir | 30 dk | Önceden 1 sayfalık ilerleme notu gönderin (`docs/toplantilar/`) |
| **Birlikte kodlama** | Haftada 1 | 2 saat | Zor bir kısmı tek ekranda birlikte yazın |

## 9.5 Sahiplik ve yapay zekâ kullanım kuralları

Projenin kontrolünün **sizde** kalması için bu kurallara uyun. Bu kurallar Claude dahil tüm yapay zekâ araçları için geçerli.

### Yapay zekâyı şunlar için kullanın ✅
- **Kavram öğrenmek:** "BM25'te b parametresi ne işe yarar, örnekle anlat"
- **Takıldığınızda ipucu almak:** "Kodum şu hatayı veriyor, kök nedeni bulmama yardım et ama düzeltmeyi yazma"
- **Kodunuzu inceletmek:** "Yazdığım RRF fonksiyonunda hata veya iyileştirme var mı?"
- **Test fikri almak:** "Bu fonksiyon için hangi uç durumları test etmeliyim?"
- **Sıkıcı ve öğretici olmayan kodu yazdırmak:** Proje iskeleti, yapılandırma dosyaları, grafik çizim kodu

### Şunlardan kaçının ❌
- Bir modülün tamamını yazdırıp anlamadan commit etmek
- Hata mesajını yapıştırıp çıkan düzeltmeyi neden işe yaradığını anlamadan uygulamak
- Rapordaki analiz ve yorumları yazdırmak. Bunlar sizin düşünceniz olmalı

### Altın kural
> **"Bu satır ne yapıyor, neden böyle?" sorusuna cevap veremediğiniz kod `main`'e girmez.**
> PR'ı inceleyen kişi bu soruyu rastgele bir satır için sorma hakkına sahip.

### Önerilen yöntem: önce siz, sonra yapay zekâ
```
1. Konuyu dokümandan oku
2. Kendin yazmaya çalış (30–60 dk)
3. Takılırsan yapay zekâdan İPUCU iste, çözüm değil
4. Çalışan kodunu yapay zekâya inceletmek için ver
5. Önerilerden anladıklarını uygula
6. Öğrendiğini öğrenme günlüğüne yaz
```

## 9.6 Öğrenme günlüğü

Her biriniz `docs/gunluk/selim.md` ve `docs/gunluk/zehra.md` dosyalarında haftalık kısa notlar tutun:

```markdown
## Hafta 5 (2026-11-09)
**Öğrendim:** BM25'te uzunluk normalizasyonu neden gerekli...
**Zorlandım:** Türkçe 'İ' harfinin küçültülmesi...
**Sorularım:** Snowball mı Zeyrek mi daha iyi olur? → deneyle bakacağız
**Kaynak:** ...
```

**Neden?** (1) Raporu yazarken altın değerinde olur. (2) Savunmada "bu projede ne öğrendiniz?" sorusunun cevabını verir. (3) Öğrenmeyi kalıcı yapar.

## 9.7 "Bitti" tanımı (Definition of Done)

Bir iş ancak şu koşullar sağlanınca bitti sayılır:
- [ ] Kod çalışıyor ve testleri var (çekirdek modüller için)
- [ ] `ruff` ve `pytest` CI'da yeşil
- [ ] Diğer kişi PR'ı inceledi ve onayladı
- [ ] Gerekiyorsa doküman güncellendi
- [ ] Deneyse: sonuçlar `experiments/results/` altında, yorumu `experiments/notes/` altında
- [ ] Yazan kişi kodu diğerine anlatabiliyor

## 9.8 Kod standartları

- **Tip ipuçları** (type hints) her fonksiyonda
- **Docstring:** Herkese açık her fonksiyonda kısa açıklama. Türkçe olabilir
- **İsimlendirme:** Kod İngilizce (`fuse`, `retriever`), dokümanlar ve yorumlar Türkçe
- **Sihirli sayı yok:** `k=60` gibi değerler yapılandırmadan gelir
- **Gizli bilgiler** (API anahtarı, şifre) asla repoya girmez, `.env` içinde tutulur
- **Notebook'lar keşif içindir.** Kalıcı mantık `src/` altına taşınır
