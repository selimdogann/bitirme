# CLAUDE.md

Bu dosya, Claude Code bu klasörde her açıldığında otomatik okunur. Sohbet geçmişi kaybolsa bile projenin bağlamı ve "nerede kaldık" bilgisi burada durur.

## Proje

Kocaeli Üniversitesi Bilgisayar Mühendisliği bitirme projesi (2026–2027). Ekip: Selim Doğan ve Zehra.

**Hibrit RAG:** Seçilecek bir sektörün Türkçe açık korpusunda BM25 ile vektör aramasını ayrı ayrı kurup, sonuçları en az 5 birleştirme (fusion) yöntemiyle birleştirmek, yöntemleri standart metriklerle karşılaştırmak, üstüne reranking ve kaynaklı LLM cevabı eklemek. Sonunda API + web arayüzü + Docker ile canlıya alınabilir bir ürün.

- Repo: https://github.com/selimdogann/bitirme
- Tüm plan `docs/` altında. Okuma sırası ve içerik özeti için [README.md](README.md).
- Yol haritası ve faz görevleri: [docs/08-yol-haritasi.md](docs/08-yol-haritasi.md)

## Çalışırken uyulacak kurallar

- **Öğrenme ve sahiplik önce gelir.** Ekip her satırı anlamak istiyor. Çekirdek modülleri (BM25, fusion, metrikler) onlar yazacak. Claude kavram anlatır, ipucu verir, kodlarını inceler. Bir modülün tamamını istenmeden yazmaz. Ayrıntı: [docs/09-calisma-duzeni.md](docs/09-calisma-duzeni.md) §9.5
- İskelet, yapılandırma dosyası, grafik kodu gibi öğretici olmayan işler yazılabilir.
- LangChain/LlamaIndex ile başlanmıyor. Çekirdek elle yazılıp `ranx`, `bm25s` gibi kütüphanelerle doğrulanacak.
- Kod İngilizce, doküman ve yorumlar Türkçe. Commit mesajları Conventional Commits biçiminde.
- Selim ile Türkçe konuş.

## Nerede kaldık

> Her önemli oturumun sonunda bu bölüm güncellenir: tarih, ne yapıldı, sıradaki adım.

**Şu anki faz:** Faz 0, Hazırlık

### 2026-10-07
- GitHub reposu bağlandı ve masaüstüne klonlandı (`~/Desktop/bitirme`).
- Hocanın istediği yorumlandı: Hibrit RAG, korpus/açık kaynak araştırması, sektör seçimi, birden fazla fusion yönteminin karşılaştırılması.
- Plan dokümanları yazıldı: `README.md` + `docs/01`–`docs/10` (~1.900 satır).
- Bu `CLAUDE.md` eklendi.

**Bekleyen işler:**
- [ ] Dokümanlar henüz commit edilmedi ve GitHub'a gönderilmedi (repoda hiç commit yok).
- [ ] Zehra'nın GitHub kullanıcı adı alınıp collaborator olarak eklenecek.
- [ ] Faz 0'ın geri kalanı: `pyproject.toml`, `.gitignore`, `.env.example`, `src/hybridrag/__init__.py`, ruff + pre-commit, GitHub Project panosu, `main` dal koruması.
- [ ] Hocaya sorulacak teyit soruları ([docs/01-proje-tanimi.md](docs/01-proje-tanimi.md) §1.7) cevaplanacak.
