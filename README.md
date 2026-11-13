# WhiteYaka Düello kanıtları

WhiteYaka'nın "DÜELLO" videolarında iki yapay zekâ modeline aynı görev verilir. Bu repo her düellonun ham kanıtını olduğu gibi tutar:
istem, modeller koşulmadan önce yazılan ölçütler, iki modelin çıktısı ve puan kaydı. Modellerin dosyalarına dokunulmaz.

| No | Tarih | Görev | Sonuç | Klasör |
|---|---|---|---|---|
| 1 | 9 Kasım 2026 | Tek istemle tahsilat panosu (GPT-5.6 Terra – Claude Opus 5.5) | Berabere (4/4 – 4/4) | [2026-11-09_tahsilat-panosu](2026-11-09_tahsilat-panosu/) |
| 2 | 10 Kasım 2026 | Tek istemle kargo toplama mini oyunu (GPT-6.1 Sol – Claude Opus 5.5) | Berabere (100 – 100) | [2026-11-10_kargo-oyunu](2026-11-10_kargo-oyunu/) |
| 3 | 12 Kasım 2026 | Tek istemle küçük işletme vardiya planlayıcı (GPT-6.1 Sol – Claude Opus 5.5) | Berabere (100 – 100) | [2026-11-12_vardiya-planlayici](2026-11-12_vardiya-planlayici/) |

Ayrıca "ARAÇ" bölümlerinin ham kayıtları: [ARAÇ #2 · yt-dlp (11 Kasım 2026)](2026-11-11_arac-2-yt-dlp/), [ARAÇ #3 · Docling (13 Kasım 2026)](2026-11-13_arac-3-docling/).

## Bir klasörde neler var

- `prompt.txt`: iki modele verilen istem (aynı metin, tek deneme)
- `RUBRIC.md`: ölçütler, modeller koşulmadan önce yazıldı
- `gpt.html`, `claude.html`: modellerin ürettiği dosyalar, düzeltilmeden
- `SCORES.md`, `measure.json`: puanlar ve otomatik ölçümün ham sonucu
- DÜELLO #2'den itibaren: girdi dosyası (`warehouse.json`), modellere verilmeyen test cevapları (`duel-warehouse-tests.json`, `duel-warehouse-oracle.json`) ve ölçüm betiği (`score.py`, Playwright)

Çıktıları kendin de deneyebilirsin: `gpt.html` ya da `claude.html` dosyasını indirip tarayıcıda aç.

Hüküm dar: "bu görevde, bu koşulda, tek denemede". Genel kalite iddiası yoktur.

Haber sayfası ve video: [whiteyaka.com](https://whiteyaka.com/)
