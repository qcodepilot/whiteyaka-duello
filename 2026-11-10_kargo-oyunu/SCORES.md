# DÜELLO #2 — Kargo toplama mini oyunu · sonuç

Koşum: 10 Kasım 2026. Aynı istem (prompt.txt) + aynı sentetik harita (warehouse.json), tek deneme, düzeltme yok.
- **GPT**: `gpt-6.1-sol`, efor high, Codex (gpt_worker, çevrimdışı), 12:09:16–12:11:46 UTC (150,5 sn iş süresi; dosya 12:11:31Z son yazım) → gpt.html, 13.985 bayt.
- **Claude**: Claude Opus 5.5 (Claude Code alt ajanı; yalnız Read + Write), 12:09:15'ten ~76 sn → claude.html, 16.160 bayt.
Ölçüm: çevrimdışı Chromium (Playwright 390×844 2x ve 1280×720), `.local/duel-work/d2_score.py`, measure.json.

| Kural | GPT | Claude |
|---|---:|---:|
| Hareket ve paket durumu (20 test × 2) | 40 | 40 |
| Rota hesabı (21 ekranda + 21 hamlede teslim + A/B/C sırası + ekrandaki konum = state; konum 0/7/14/21. hamle karelerinden gözle) | 20 | 20 |
| Geri al / sıfırla | 20 | 20 |
| Mobil (iki görünümde taşma yok; 4 yön düğmesi ≥44 px, düğme = tuş) | 10 | 10 |
| Yerel teslim (harici istek 0, konsol hatası 0, __duel var) | 10 | 10 |
| **Toplam** | **100** | **100** |

Eşitlik kuralı: kritik hata ikisinde de 0 → **BERABERE**. Kazanan uydurulmadı. Süre ölçüte yazılmadığı için hükme girmedi (gözlem: Claude ~76 sn, GPT ~150 sn; tek koşum, genel hız kanıtı değil).
Gözlem (puana girmedi): GPT ilerleme çipleri (A✓ B✓ C✓ S✓) ve teslimden sonra yön düğmelerini kilitliyor; Claude konum (x, y) ve alınan paketleri yazıyor, düğmeler açık kalıyor.
Hüküm dar: bu görevde, bu koşulda, tek denemede.
