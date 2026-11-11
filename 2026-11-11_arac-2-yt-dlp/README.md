# ARAÇ #2 · yt-dlp ile videoyu indir, sesini mp3 olarak ayır (11 Kasım 2026)

Bu klasör bir düello değil, WhiteYaka "ARAÇ" serisinin 2. bölümünün ham kanıtıdır.

- Araç: [yt-dlp](https://github.com/yt-dlp/yt-dlp) 2026.10.26 (The Unlicense).
- Örnek video: Big Buck Bunny fragmanı, `https://download.blender.org/peach/trailer/trailer_iphone.m4v`
  (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org, [CC BY 3.0](https://peach.blender.org/about/).
  YouTube ya da başka bir platformdan indirme yapılmadı.
- `komutlar.txt`: konsolda çalıştırılan üç komut, sırasıyla.
- `ekran-kaydi.mp4`: 11 Kasım 2026 15.10 (İstanbul), Windows konsolunun kesintisiz pencere kaydı (18 sn).
  1. komut 2,1. saniyede, indirme 8,7. saniyede bitiyor (yt-dlp satırı: `3.71MiB in 00:00:05`); 2. komut 10,2. saniyede, mp3 12,5. saniyede hazır.
  Videoda bu kayıt kısaltılarak kullanıldı; ekranda "bekleme kısaltıldı" notu var.
- `cikti-ses.mp3`: 2. komutun ürettiği ses dosyası (460.976 bayt, 33 sn). İndirilen video 3.889.885 bayt, 33 sn.

Sınırlar: tek bilgisayar, tek deneme; süre internet hızına bağlıdır. `-x` için bilgisayarda ffmpeg ve ffprobe gerekir (yt-dlp README).
Yalnız indirme izni olan içerikte kullanılmalı: kendi kaydın ya da lisansı indirmeye izin veren içerik.
