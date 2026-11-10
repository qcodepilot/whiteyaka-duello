# DÜELLO #1 — Tahsilat panosu · puanlar

Koşum: 9 Kasım 2026 ~15.09 İstanbul, aynı istem (prompt.txt), tek deneme, düzeltme yok.
- GPT-5.6 Terra — `gpt_worker` iş `duel-01-tahsilat-gpt` (Codex, effort high, çevrimdışı; makbuz `.local/pipeline/jobs/duel-01-tahsilat-gpt/receipt.json`) → gpt.html (8.194 bayt)
- Claude Opus 5.5 — Claude Code alt ajanı, yalnız Write aracı, test/çalıştırma yok → claude.html (12.514 bayt)
Ölçüm: Playwright Chromium, `offline=True`, file:// açılış, 540×960 (2x) + 320×800 (`.local/duel-work/score_rec.py`, ham sonuç measure.json).

| Kural | GPT | Claude | Kanıt |
|---|---|---|---|
| 1 Çevrimdışı, harici istek yok, konsol hatası yok | 1 | 1 | measure.json: requests [], console [] (ikisi de) |
| 2 Toplamlar 31.500 / 12.500 / 19.000 / 12.300 TL | 1 | 1 | ekran metni (gpt-full.png, claude-full.png) |
| 3 Dört müşteri grafikte + tabloda, gecikenler uyarı renginde | 1 | 1 | iki çıktıda da Delta/Peri kırmızı çubuk + kırmızı rozet |
| 4 Filtre "gecikti" → yalnız Delta ve Peri | 1 | 1 | GPT `<select>`, Claude radyo düğmeleri; görünür satırlar ['Delta 8.400 TL Gecikti','Peri 3.900 TL Gecikti'] (ikisi de) |
| **Toplam** | **4/4** | **4/4** | |

Eşitlik kuralı (320 px'te yatay kaydırma yok, scrollWidth ≤ 320): GPT 320, Claude 320 → ikisi de geçti.
**Sonuç: BERABERE** (kazanan uydurulmadı).

Gözlem (puana girmez, videoda betimleme olarak): GPT sade pano + açılır menü filtresi; Claude filtreyi sayaçlı düğmelere koydu, "%40 tahsil oranı", "Gösterilen toplam" satırı ve grafik lejantı ekledi, filtre grafiği de soluklaştırıyor.
Not: ölçüm betiğinin ilk koşusunda Claude filtresi yanlış öğeye (lejant yazısına) tıklandığı için 4 satır görünmüştü; betik düzeltildi (label tıklaması), ikinci koşu yukarıdaki sonuç. Modellerin dosyalarına dokunulmadı.
