# CLAUDE.md

Bu dosya, Claude Code bu klasörde her açıldığında otomatik okunur. Sohbet geçmişi kaybolsa bile projenin bağlamı ve "nerede kaldık" bilgisi burada durur.

## Proje

Kocaeli Üniversitesi Bilgisayar Mühendisliği bitirme projesi (2026–2027). Ekip: Selim Doğan ve Zehra Çetin (github.com/zehracetinn). Danışman: Prof. Dr. Sevinç İlhan Omurca (silhan@kocaeli.edu.tr; NLP, metin/doküman işleme).

**Türkçe İlaç Asistanı:** TİTCK ilaç kullanma talimatlarında (KT) hibrit arama (BM25 + vektör, birleştirilmiş) ile soruyla ilgili paragrafı bulan, sade Türkçe cevap veren, kaynak paragrafı gösteren ve kanıt yoksa cevap uydurmayan bir asistan. Önce Python + Streamlit prototipi; birleştirme yöntemleri ölçülerek seçilir, karşılaştırma raporda bir bölümdür.

- Repo: https://github.com/selimdogann/bitirme
- Plan `docs/` altında; okuma sırası için [README.md](README.md)
- Aşamalar: [docs/08-yol-haritasi.md](docs/08-yol-haritasi.md)

## Çalışırken uyulacak kurallar

- **Öğrenme ve sahiplik önce gelir.** Çekirdek modülleri (BM25, birleştirme, metrikler) ekip yazar. Claude kavram anlatır, ipucu verir, kodu inceler; istenmeden modülün tamamını yazmaz. İskelet ve ayar dosyaları gibi öğretici olmayan işler yazılabilir. Ayrıntı: [docs/09-calisma-duzeni.md](docs/09-calisma-duzeni.md) §9.6
- **Adım adım:** Selim'e her seferinde tek somut görev ver; sonucu paylaşmadan sonrakine geçme. Komutların nasıl çalıştırılacağını açıkla. Gereksiz teknoloji ekleme.
- **Git:** `main` korumalı (PR zorunlu, CI geçmeli, onay şartı yok, squash merge). Her değişiklik dalda yapılır, commit'lenir ve PR açılır.
- **Commit ve PR mesajları:** Türkçe Conventional Commits, kısa (başlık + en fazla 1–2 cümle). **Claude'un adı hiçbir yerde görünmez:** `Co-Authored-By` satırı ve "Generated with Claude Code" yazısı eklenmez.
- Kod İngilizce, doküman ve yorumlar Türkçe. Selim ile Türkçe konuş.
- Kodu çalıştırma: `uv run ...` (ör. `uv run streamlit run app.py`). Stil: `uv run ruff check --fix .` ve `uv run ruff format .`

## Nerede kaldık

> Her önemli oturumun sonunda bu bölüm güncellenir: tarih, ne yapıldı, sıradaki adım.

**Şu anki aşama:** Aşama 0 (altyapı) neredeyse bitti; sırada Aşama 1 (veri).

### 2026-10-07 – 2026-10-16
- Repo bağlandı, ilk plan dokümanları yazıldı. Sektör kararı: sağlık.
- Hocaya ön rapor (Claude Docs): https://claude.ai/code/artifact/8f0418e2-c865-4855-9cfb-05695ef1a6ff
- HAVELSAN SUİT başvurusu yapıldı. Değer önerisi: https://claude.ai/code/artifact/b3f735be-8c9c-4f01-8ec6-4d940c6f8d79 · Niyet mektubu: https://claude.ai/code/artifact/c423e695-7981-4eea-b925-cc465f3ced79

### 2026-10-20
- Soru-cevap veri seti araştırması (Claude Docs): https://claude.ai/code/artifact/a1f020b5-6ba7-4c82-a349-a1b3791bd07c. Hazır "Türkçe ilaç talimatı + soru" seti yok; test seti (200–300 soru) ekip tarafından hazırlanacak. İkinci kontrol: MedTurkQuAD (CC BY-NC-ND), NFCorpus-TR, TurkishRAGEval.
- Literatür: danışmanın TurkishMedLLM makalesi (Diagnostics 2026, vektör tabanlı Türkçe tıbbi RAG); proje bunun arama tarafını hibritle geliştiren devam olarak sunulacak.
- **Yön değişti:** Türkçe İlaç Asistanı (hoca onayı bekleniyor; sorular `docs/01` §1.7).
- Altyapı: uv + Python 3.12, Streamlit iskeleti, ruff, GitHub Actions CI, PR/issue şablonları, `main` koruması, etiketler. PR #1 (`chore/proje-altyapisi`).
- Dokümanlar yeni yöne göre yeniden yazıldı: PR #2 (`docs/ilac-asistani-yonu`).
- İlk iki commit tek commit'te birleştirildi (`docs: proje planı dokümanları ve CLAUDE.md eklendi`).

**Bekleyen işler:**
- [ ] PR #1 ve PR #2'nin incelenip birleştirilmesi
- [ ] Zehra'nın repoyu klonlayıp `uv sync` ile ortamı kurması
- [ ] GitHub'da aşama milestone'ları ve proje panosu
- [ ] Hocayla görüşme (`docs/01` §1.7)
- [ ] Görev 3: 5 ilacın KT PDF'ini `data/raw/`'a indirmek (Parol, Arveles, Augmentin, Coraspin, Majezik)
