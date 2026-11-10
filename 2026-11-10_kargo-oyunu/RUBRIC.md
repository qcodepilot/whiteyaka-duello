# DÜELLO #2 — Kargo toplama mini oyunu · ölçüt (modeller koşulmadan önce yazıldı)

Yazılma: 10 Kasım 2026, ~15.20 İstanbul. Tek deneme, aynı istem (prompt.txt) + aynı dosya (warehouse.json, sentetik), düzeltme yok, insan eli yok.
Kaynak: GPT işçisi deney tasarımı (.local/pipeline/jobs/n1010-scan/duel-proposals.md, 9 Kas gece); test cevapları (duel-warehouse-tests.json, oracle) modellere VERİLMEDİ.

100 puan:
1. Hareket ve paket durumu — 40: duel-warehouse-tests.json 20 sabit durum, her doğru 2 puan (window.__duel ile, her test reset sonrası).
2. Rota hesabı — 20: optimalSteps=21 gösteriliyor/state'te (5), oracle rotası 21 hamlede teslim (5), A/B/C sırası doğru (5), ekrandaki konum = state (5).
3. Geri al / sıfırla — 20: paket alınmışken geri al (5), teslimden sonra geri al (5), engelli harekette geçmiş korunur (5), sıfırla (5).
4. Mobil — 10: 390x844 ve 1280x720 yatay taşma yok (5), yön düğmeleri ≥44x44 ve tuşla aynı iş (5).
5. Yerel teslim — 10: tek dosya + harici istek yok (5), konsol hatası yok + __duel arayüzü var (5).

Eşitlikte: kritik hata (oyun açılmıyor / teslim edilemiyor) az olan; yine eşitse "berabere". Kazanan uydurulmaz.
Hüküm dar: "bu görevde, bu koşulda, tek denemede". Genel kalite iddiası yok. 10 Kasım: sakin ton, zafer animasyonu yok.
