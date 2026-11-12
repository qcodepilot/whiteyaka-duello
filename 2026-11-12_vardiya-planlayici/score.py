"""DÜELLO #3 ölçümü (vardiya planlayıcı): her modelin index.html'i çevrimdışı Chromium'da RUBRIC.md'ye göre denenir.
Kullanım: python -X utf8 d3_score.py [side ...]  -> d3-rec/<side>-*.png, d3-rec/<side>-*.csv, d3-rec/measure.json
Tıklamalar gerçek fare/klavye olaylarıdır (Playwright click/fill); model kendi PASS yazısı puan sayılmaz.
"""
import asyncio, csv, io, json, pathlib, re, sys
from playwright.async_api import async_playwright

BASE = pathlib.Path(r"C:\White Yaka\.local\duel-work")
OUT = BASE / "d3-rec"; OUT.mkdir(exist_ok=True)
UNAVAIL = {("P1", "Pzt", "S"), ("P2", "Sal", "A"), ("P3", "Çar", "S"), ("P4", "Per", "A")}
OPENER = {"P1", "P2"}
DAYS = ["Pzt", "Sal", "Çar", "Per", "Cum"]


def norm_shift(v):
    v = (v or "").strip()
    if v.upper().startswith("S") or v.startswith("09"):
        return "S"
    if v.upper().startswith("A") or v.startswith("13"):
        return "A"
    return v


def check_rows(rows):
    """rows: list of dicts from CSV. returns dict of checks."""
    a = []
    for r in rows:
        a.append((r.get("calisan", "").strip(), r.get("gun", "").strip(), norm_shift(r.get("vardiya", "")),
                  r.get("saat", "").strip()))
    res = {"rows": len(a)}
    cover = {(d, s): 0 for d in DAYS for s in "SA"}
    for p, d, s, h in a:
        if (d, s) in cover:
            cover[(d, s)] += 1
    res["coverAll1"] = all(v == 1 for v in cover.values())
    res["hours"] = sum(float(h.replace(",", ".") or 0) for *_, h in a)
    res["unavail"] = sum(1 for p, d, s, _ in a if (p, d, s) in UNAVAIL)
    res["badOpener"] = sum(1 for p, d, s, _ in a if s == "S" and p not in OPENER)
    perday = {}
    for p, d, s, _ in a:
        perday[(p, d)] = perday.get((p, d), 0) + 1
    res["double"] = sum(1 for v in perday.values() if v > 1)
    cnt = {}
    for p, *_ in a:
        cnt[p] = cnt.get(p, 0) + 1
    res["counts"] = cnt
    res["over3"] = sum(1 for v in cnt.values() if v > 3)
    res["sorted"] = sorted(cnt.get(p, 0) for p in ["P1", "P2", "P3", "P4"])
    res["allHours4"] = all(h.replace(",", ".") in ("4", "4.0", "4.00") for *_, h in a)
    res["assign"] = sorted(f"{d}-{s}-{p}" for p, d, s, _ in a)
    return res


async def click_text(pg, pattern):
    loc = pg.get_by_role("button", name=re.compile(pattern, re.I))
    n = await loc.count()
    if n == 0:
        return False
    await loc.first.click()
    await pg.wait_for_timeout(400)
    return True


async def get_csv(pg, tag, side):
    try:
        async with pg.expect_download(timeout=4000) as dl:
            ok = await click_text(pg, r"csv")
            if not ok:
                raise RuntimeError("CSV düğmesi yok")
        d = await dl.value
        p = OUT / f"{side}-{tag}.csv"
        await d.save_as(str(p))
        raw = p.read_bytes().decode("utf-8-sig")
        sep = ";" if raw.count(";") > raw.count(",") else ","
        rows = list(csv.DictReader(io.StringIO(raw), delimiter=sep))
        return raw, rows
    except Exception as e:  # noqa
        return f"HATA {e}", None


async def find_demand_input(pg):
    """Pzt-S talep alanını bul: etiket/aria/id/name içinde Pzt ve S/Sabah/09."""
    return await pg.evaluate(r"""() => {
      const els=[...document.querySelectorAll('input,select')].filter(e=>e.type!=='hidden'&&e.type!=='file');
      const lab=e=>{let t=(e.getAttribute('aria-label')||'')+' '+(e.id||'')+' '+(e.name||'')+' '+(e.title||'')+' '+(e.dataset?JSON.stringify(e.dataset):'');
        if(e.labels) for(const l of e.labels) t+=' '+l.innerText; return t;};
      const out=els.map((e,i)=>({i,tag:e.tagName,type:e.type,val:e.value,lab:lab(e).replace(/\s+/g,' ').trim()}));
      return out;}""")


async def side_run(p, side):
    res = {"side": side, "requests": [], "console": []}
    f = BASE / f"d3-{side}" / "index.html"
    res["bytes"] = f.stat().st_size
    b = await p.chromium.launch()
    ctx = await b.new_context(viewport={"width": 1280, "height": 720}, offline=True, accept_downloads=True)
    pg = await ctx.new_page()
    pg.on("console", lambda m: res["console"].append(f"{m.type}: {m.text}") if m.type == "error" else None)
    pg.on("pageerror", lambda e: res["console"].append(f"pageerror: {e}"))
    pg.on("request", lambda r: res["requests"].append(r.url) if not r.url.startswith(("file:", "data:", "blob:")) else None)
    await pg.goto(f.as_uri()); await pg.wait_for_timeout(1000)
    res["synthetic"] = "Sentetik örnek" in (await pg.inner_text("body"))
    await pg.screenshot(path=str(OUT / f"{side}-01-start.png"), full_page=True)
    res["buttons"] = await pg.evaluate("[...document.querySelectorAll('button')].map(b=>b.innerText.trim())")
    res["inputs"] = await find_demand_input(pg)
    # generate default plan
    res["genClick"] = await click_text(pg, r"olu[sş]tur")
    await pg.wait_for_timeout(500)
    await pg.screenshot(path=str(OUT / f"{side}-02-plan.png"), full_page=True)
    res["planText"] = (await pg.inner_text("body"))[:3000]
    raw, rows = await get_csv(pg, "default", side)
    res["csvDefaultRaw"] = raw[:1500]
    res["default"] = check_rows(rows) if rows is not None else None
    res["csvHeader"] = raw.splitlines()[0] if rows is not None else None

    # 4) olanaksız durum: Pzt-S talebi 3
    idx = None
    for it in res["inputs"]:
        L = it["lab"]
        if "Pzt" in L and re.search(r"(Pzt[ _-]S[^a-zçğıöşü]|Pzt[ _-]S$|Sabah|09)", L):
            idx = it["i"]; break
    res["pztSIndex"] = idx
    if idx is not None:
        el = pg.locator("input:not([type=hidden]):not([type=file]),select").nth(idx)
        tag = await el.evaluate("e=>e.tagName")
        if tag == "SELECT":
            await el.select_option("3")
        else:
            await el.fill("3"); await el.press("Tab")
        await pg.wait_for_timeout(300)
        await click_text(pg, r"olu[sş]tur")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(OUT / f"{side}-03-impossible.png"), full_page=True)
        txt = await pg.inner_text("body")
        res["impossibleText"] = txt[:3000]
        res["impossibleWarn"] = bool(re.search(r"uygun (bir )?plan (yok|bulunamad)|karşılanam|mümkün değil|olanaksız|plan oluşturulamad|çözüm (yok|bulunamad)", txt, re.I))
        raw2, rows2 = await get_csv(pg, "impossible", side)
        res["csvImpossibleRaw"] = raw2[:800]
        res["impossibleCsvRows"] = None if rows2 is None else len(rows2)
        # sıfırla + yeniden oluştur
        res["resetClick"] = await click_text(pg, r"varsay[ıi]lan|s[ıi]f[ıi]rla")
        await pg.wait_for_timeout(300)
        res["afterResetVal"] = await el.input_value()
        await click_text(pg, r"olu[sş]tur")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(OUT / f"{side}-04-reset.png"), full_page=True)
        raw3, rows3 = await get_csv(pg, "reset", side)
        res["reset"] = check_rows(rows3) if rows3 is not None else None
    # 5) 390 px
    await pg.set_viewport_size({"width": 390, "height": 844})
    await pg.wait_for_timeout(400)
    res["mobile"] = await pg.evaluate("""() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
        bodySw: document.body.scrollWidth,
        buttons: [...document.querySelectorAll('button')].map(b=>{const r=b.getBoundingClientRect();return {t:b.innerText.trim(),w:Math.round(r.width),h:Math.round(r.height),x:Math.round(r.x),right:Math.round(r.right)}})})""")
    await pg.screenshot(path=str(OUT / f"{side}-05-mobile.png"), full_page=True)
    # klavye: odak + Enter ile oluştur
    await pg.set_viewport_size({"width": 1280, "height": 720})
    await pg.reload(); await pg.wait_for_timeout(600)
    btn = pg.get_by_role("button", name=re.compile(r"olu[sş]tur", re.I)).first
    await btn.focus(); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(500)
    raw4, rows4 = await get_csv(pg, "keyboard", side)
    res["keyboardRows"] = None if rows4 is None else len(rows4)
    await b.close()
    return res


async def main(sides):
    async with async_playwright() as p:
        allr = {}
        for s in sides:
            allr[s] = await side_run(p, s)
        (OUT / "measure-stage1.json").write_text(json.dumps(allr, ensure_ascii=False, indent=1), encoding="utf-8")
        for s, r in allr.items():
            print(s, json.dumps({k: r.get(k) for k in ("bytes", "requests", "console", "synthetic", "buttons", "genClick", "default", "csvHeader", "pztSIndex", "impossibleWarn", "impossibleCsvRows", "resetClick", "afterResetVal", "reset", "mobile", "keyboardRows")}, ensure_ascii=False))
            print(" inputs:", json.dumps(r["inputs"][:16], ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or ["gpt", "claude"]))
