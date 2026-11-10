# WhiteYaka Düello kanıtları

WhiteYaka'nın "DÜELLO" videolarında iki yapay zekâ modeline aynı görev verilir. Bu repo her düellonun ham kanıtını olduğu gibi tutar:
istem, modeller koşulmadan önce yazılan ölçütler, iki modelin çıktısı ve puan kaydı. Modellerin dosyalarına dokunulmaz.

| No | Tarih | Görev | Sonuç | Klasör |
|---|---|---|---|---|
| 1 | 9 Kasım 2026 | Tek istemle tahsilat panosu (GPT-5.6 Terra – Claude Opus 5.5) | Berabere (4/4 – 4/4) | [2026-11-09_tahsilat-panosu](2026-11-09_tahsilat-panosu/) |

## Bir klasörde neler var

- `prompt.txt`: iki modele verilen istem (aynı metin, tek deneme)
- `RUBRIC.md`: ölçütler, modeller koşulmadan önce yazıldı
- `gpt.html`, `claude.html`: modellerin ürettiği dosyalar, düzeltilmeden
- `SCORES.md`, `measure.json`: puanlar ve otomatik ölçümün ham sonucu

Çıktıları kendin de deneyebilirsin: `gpt.html` ya da `claude.html` dosyasını indirip tarayıcıda aç.

Hüküm dar: "bu görevde, bu koşulda, tek denemede". Genel kalite iddiası yoktur.

Haber sayfası ve video: [whiteyaka.com](https://whiteyaka.com/)
