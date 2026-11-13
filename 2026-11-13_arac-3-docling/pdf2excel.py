# PDF'teki tabloları Excel'e çevir (Docling, MIT). Kullanım: python pdf2excel.py dosya.pdf [sayfa]
import sys, pandas as pd
from docling.document_converter import DocumentConverter

def sayi(x):  # "22.126" / "-3,5" gibi Türkçe sayıları gerçek sayıya çevir
    try: return float(str(x).replace(".", "").replace(",", "."))
    except ValueError: return x

pdf = sys.argv[1]
sayfa = int(sys.argv[2]) if len(sys.argv) > 2 else None
aralik = {"page_range": (sayfa, sayfa)} if sayfa else {}
doc = DocumentConverter().convert(pdf, **aralik).document
out = pdf.rsplit(".", 1)[0] + ".xlsx"
with pd.ExcelWriter(out) as w:
    for i, t in enumerate(doc.tables, 1):
        t.export_to_dataframe(doc=doc).map(sayi).to_excel(w, sheet_name=f"Tablo {i}", index=False)
print(f"{len(doc.tables)} tablo bulundu -> {out}")
