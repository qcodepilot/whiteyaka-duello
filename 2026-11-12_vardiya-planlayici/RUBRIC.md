# DÜELLO #3 — Vardiya planlayıcı: ölçütler (model koşumundan ÖNCE yazıldı)

Yazım: 12 Kasım 2026 00.4x (gece aday turu, GPT işçisi tasarımı `n1112-scan`), dosyaya kopya 12 Kas 15.1x; modeller 15.1x'te başlatıldı.
Modeller: GPT-6.1 Sol (gpt_worker/Codex, effort high, çevrimdışı) ve Claude Opus 5.5 (Claude Code alt ajanı, yalnız Write). Aynı istem: prompt.txt.

**Ortak deney düzeni:** Yeni ve ayrı oturumlar; aynı istem, aynı dosya yetkisi, aynı tarayıcı, internet kapalı ve harici bağımlılık yok. Tek deneme, model başına 8 dakika üst sınır; takip istemi veya sonuç görüldükten sonra ölçüt değişikliği yok. Üretim süresi ile tarayıcıda inceleme süresi ayrı kaydedilir. Çıktılar tarafsız A/B adlarıyla incelenir; eşitlik mümkündür. Beş ölçüt × 20 puan. Çalışmayan çıktı, doğruluk testlerini geçmiş gibi gösterilmez. Kullanılan plan/araç yetkileri farklıysa sonuç bu iki kuruluma bağlanır. Ücretli çağrı başlatılmaz.


**Önceden belirlenen beş ölçüt:**

1. **Çalışır teslim, 20:** `file://` açılışı, 0 harici istek ve 0 yakalanmamış JavaScript hatası; oluştur/sıfırla düğmeleri çalışır. Üç teknik koşuldan biri bozuksa 0.
2. **Kapsama ve aritmetik, 20:** Varsayılan 10 vardiya tam karşılanır, fazladan atama yoktur, toplam 40 saat çıkar. Üç koşul birlikte aranır.
3. **Kısıtlar ve denge, 20:** Uygunsuz atama 0; yetkisiz açılış 0; aynı gün çift vardiya 0; haftada 3’ü aşan kişi 0; kişi vardiya sayıları sıralandığında `[2,2,3,3]` olur. Beş alt kontrolün her biri 4 puan.
4. **Olanaksız durumu yakalama, 20:** Pzt-S talebi 3 yapılır. P1 uygun değil, P3/P4 yetkisiz; yalnız P2 kalır. Sayfa uygun plan yok demeli, eski planı geçerli saymamalı; sıfırlayınca yeniden geçerli 10 vardiya üretmeli. Uyarı 10, doğru sıfırlama 10.
5. **Kullanılabilir çıktı, 20:** CSV’de başlık dışında tam 10 atama, her birinde 4 saat ve ekrandakiyle aynı atamalar bulunur (10). 390 piksel görünümde gövde yatay taşmaz; çizelge kendi etiketli kaydırma alanında olabilir; bütün düğmelere erişilir (10).

**Ekran kanıtı:** Aynı 1280×720 ve 390 piksel tarayıcıda önce boş çizelge → Planı oluştur → renkli 10 atama → Pzt-S=3 ile kırmızı uygun plan yok → sıfırlama → indirilen CSV. Ekran değişimi gerçek dosyadan alınır; hazırlanmış başarılı ekran görüntüsü kullanılamaz.

**Riskler:** Gerçek personel verisi/sağlık/izin gerekçesi yüklenmez. Uydurma hukuk uygunluğu veya optimum maliyet iddiası istenmez. Geçerli birçok plan olabilir; hücreler referans çözümle birebir aynı olmak zorunda değildir. Modelin kendi PASS yazısı puan sayılmaz. Gerçek hayatta mola, dinlenme ve mevzuat kuralları ayrıca gerekir.

**Bağımsız hesap referansı:** Pzt S=P2/A=P3; Sal S=P1/A=P4; Çar S=P2/A=P4; Per S=P1/A=P3; Cum S=P1/A=P2. Sayılar P1=3, P2=3, P3=2, P4=2; toplam 40 saat. Bu deterministik kontrol örneği model koşumu değildir.

