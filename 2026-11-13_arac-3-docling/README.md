# ARAÇ #3 · Docling ile PDF'teki tabloyu Excel'e çevir (13 Kasım 2026)

Bu klasör bir düello değil, WhiteYaka "ARAÇ" serisinin 3. bölümünün ham kanıtıdır.

- Araç: [Docling](https://github.com/docling-project/docling) 2.150.0 (MIT; LF AI & Data projesi, IBM Research Zürih'te başladı).
  Kullanılan yapay zekâ modellerinin lisansları ayrıdır (Docling README: "please refer to the model licenses").
- Örnek PDF: TCMB, *Ödemeler Dengesi İstatistikleri – Eylül 2026* (13 Kasım 2026'da yayımlandı), 2. sayfa "Tablo 1. Analitik Sunum".
  PDF'i buraya koymadık; TCMB sayfası: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Odemeler+Dengesi+ve+Ilgili+Istatistikler/Odemeler+Dengesi+Istatistikleri/
  (indirdiğimiz dosyanın sha256'sı: aşağıda).
- `pdf2excel.py`: kullandığımız betik (Docling `DocumentConverter` + pandas; Türkçe sayıları gerçek sayıya çevirir). Kullanım: `python pdf2excel.py dosya.pdf [sayfa]`.
- `komutlar.txt`: kurulum ve çalıştırma komutu.
- `ekran-kaydi.mp4`: 13 Kasım 2026 ~15.15 (İstanbul), Windows konsolunun kesintisiz pencere kaydı (40 sn). Komut 3,8. saniyede, "1 tablo bulundu" 34,3. saniyede
  (yaklaşık 30 sn, yalnız işlemci, ilk çalıştırma değil: modeller önceden indirilmişti). Videoda bekleme kısaltıldı; ekranda yazıyor.
- `cikti-odemeler-dengesi.xlsx`: betiğin ürettiği Excel (39 satır × 14 sütun). `excel-ekrani.png`: aynı dosya Excel'de açıkken.

Sınırlar (gördüklerimiz): 3. satırda tablo başlığı, "CARİ İŞLEMLER HESABI" ve "İhracat" satırları tek hücrede birleşti; o satırın sayıları ikili metin olarak geldi.
Diğer satırlarda sayılar doğru ve hesaplanabilir. TCMB'nin 6 sayfalık başka bir raporunda (TCMB Piyasa Katılımcıları Anketi) ızgara olmayan özet sayfasını tablo
olarak bulmadı. Çıktıyı kullanmadan önce PDF ile karşılaştırın. TCMB bu verileri ayrıca Excel/ZIP olarak da yayımlıyor; araç asıl işe, elinde yalnız PDF olan tablolarda yarar.

PDF sha256: b21a4ec1b201def5f188b90760c7bfc338e5461039e5d947bf6a906a37553e76
