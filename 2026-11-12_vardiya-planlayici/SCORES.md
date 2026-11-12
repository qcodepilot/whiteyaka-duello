# DÜELLO #3 — Vardiya planlayıcı: puanlar

Koşum: 12 Kasım 2026. GPT-6.1 Sol (gpt_worker/Codex `gpt-6.1-sol`, effort high, ağ kapalı, 15.08–15.11 İstanbul, 195 sn) ve Claude Opus 5.5 (Claude Code alt ajanı, yalnız Write, ~89 sn). Aynı istem (`prompt.txt`), tek deneme, takip istemi yok. Ölçütler (`RUBRIC.md`) koşudan önce yazıldı.
Ölçüm: `score.py` — çevrimdışı Chromium (Playwright), 1280×720 ve 390×844; gerçek tıklama/seçim, CSV gerçek indirme. Ham çıktı `measure.json`, CSV'ler `*-default.csv`.

| Ölçüt | GPT-6.1 Sol | Claude Opus 5.5 |
|---|---|---|
| 1. Çalışır teslim (file://, 0 harici istek, 0 JS hatası, düğmeler) | 20 | 20 |
| 2. Kapsama ve aritmetik (10 vardiya, fazla atama yok, 40 saat) | 20 | 20 |
| 3. Kısıtlar ve denge (uygunsuz 0, yetkisiz açılış 0, çift 0, >3 yok, [2,2,3,3]) | 20 | 20 |
| 4. Olanaksızı yakalama (Pzt-S=3 → "uygun plan yok", eski plan gösterilmez, CSV kapanır; sıfırla → geçerli 10) | 20 | 20 |
| 5. Kullanılabilir çıktı (CSV 10 satır × 4 saat, ekranla aynı; 390 px gövde taşmaz, düğmeler erişilir) | 20 | 20 |
| **Toplam** | **100** | **100** |

**Sonuç: berabere.** İki model de aynı atamayı buldu (Pzt S=P2/A=P1; Sal S=P1/A=P3; Çar S=P1/A=P4; Per S=P2/A=P3; Cum S=P2/A=P4; P1=3, P2=3, P3=2, P4=2). Klavyeyle (odak + Enter) oluşturma ikisinde de 10 satır verdi.

**Puana girmeyen gözlemler (ölçütte yok, sonradan puan eklenmedi):**
- GPT'nin CSV başlığı `gün,vardiya,…` (istem `gun` diyordu; ü harfi). Excel/içe aktarmada başlık adı birebir aranıyorsa bu fark önemlidir.
- Claude'un girdi tablosu 390 px'te kendi kaydırma alanında (yatay kaydırma gerekir); gövde taşmıyor.
- GPT ekranı daha "ürün" görünümlü (özet kartları, yük çubukları); Claude daha sade ve talep-karşılama tablosu ayrıntılı.
