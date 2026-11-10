"""DÜELLO #2 ölçümü: her modelin index.html'i çevrimdışı Chromium'da, RUBRIC.md'ye göre puanlanır.
Kullanım (bu klasörde, pip install playwright): python -X utf8 score.py  -> d2-rec/<side>-*.png, d2-rec/measure.json
"""
import asyncio, json, pathlib
from playwright.async_api import async_playwright

BASE = pathlib.Path(__file__).resolve().parent
DUEL = pathlib.Path(r"C:\White Yaka\docs\creative-lab\duels\2026-11-10_kargo-oyunu")
OUT = BASE / "d2-rec"; OUT.mkdir(exist_ok=True)
TESTS = json.loads((DUEL / "duel-warehouse-tests.json").read_text(encoding="utf-8"))["test_cases"]
ROUTE = json.loads((DUEL / "duel-warehouse-oracle.json").read_text(encoding="utf-8"))["valid_route"]
KEYS = {"up": "ArrowUp", "down": "ArrowDown", "left": "ArrowLeft", "right": "ArrowRight"}


def norm(s):
    if not isinstance(s, dict):
        return s
    return {k: (list(s.get(k)) if k == "picked" and s.get(k) is not None else s.get(k))
            for k in ("x", "y", "picked", "steps", "delivered", "optimalSteps")}


async def run_ops(pg, ops):
    for op in ops:
        if op == "undo":
            await pg.evaluate("window.__duel.undo()")
        elif op == "reset":
            await pg.evaluate("window.__duel.reset()")
        else:
            await pg.evaluate(f"window.__duel.step({json.dumps(op)})")


async def side_run(p, side):
    res = {"side": side, "requests": [], "console": [], "tests": {}, "points": {}}
    f = BASE / f"{side}.html"
    res["bytes"] = f.stat().st_size
    b = await p.chromium.launch()
    ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, offline=True)
    pg = await ctx.new_page()
    pg.on("console", lambda m: res["console"].append(f"{m.type}: {m.text}") if m.type == "error" else None)
    pg.on("pageerror", lambda e: res["console"].append(f"pageerror: {e}"))
    pg.on("request", lambda r: res["requests"].append(r.url) if not r.url.startswith(("file:", "data:", "blob:")) else None)
    await pg.goto(f.as_uri()); await pg.wait_for_timeout(1200)
    res["hasApi"] = await pg.evaluate("!!(window.__duel && ['step','undo','reset','state'].every(k=>typeof window.__duel[k]==='function'))")
    await pg.screenshot(path=str(OUT / f"{side}-start.png"))
    res["startText"] = (await pg.inner_text("body"))[:1500]
    # 1) 20 durum testi
    t_ok = 0
    if res["hasApi"]:
        for c in TESTS:
            try:
                await pg.evaluate("window.__duel.reset()")
                await run_ops(pg, c["operations"])
                got = norm(await pg.evaluate("window.__duel.state()"))
                ok = got == c["expected"]
                if c["id"] == "W20" and ok:
                    await pg.evaluate("(()=>{const s=window.__duel.state(); s.x=99; (s.picked||[]).push('FAKE');})()")
                    ok = norm(await pg.evaluate("window.__duel.state()")) == c["expected"]
            except Exception as e:  # noqa
                got, ok = f"HATA {e}", False
            res["tests"][c["id"]] = {"ok": ok, "got": got}
            t_ok += ok
    res["points"]["hareket_paket"] = 2 * t_ok
    T = lambda i: res["tests"].get(i, {}).get("ok", False)
    # 2) rota (görsel eşlik ayrıca gözle: rota kareleri)
    opt_text = "21" in res["startText"]
    res["optimalOnScreen"] = opt_text
    res["points"]["rota_auto"] = 5 * (T("W01") and opt_text) + 5 * T("W11") + 5 * (T("W06") and T("W08") and T("W10"))
    # 3) geri al / sıfırla
    res["points"]["geri_sifirla"] = 5 * T("W13") + 5 * T("W12") + 5 * T("W18") + 5 * T("W14")
    # 4) rota oyunu gerçek ok tuşlarıyla + her adımda kare (video kanıtı)
    key_ok = None
    if res["hasApi"]:
        await pg.evaluate("window.__duel.reset()"); await pg.wait_for_timeout(200)
        await pg.screenshot(path=str(OUT / f"{side}-route-00.png"))
        # duvara çarpma denemesi (sağ = duvar)
        await pg.keyboard.press("ArrowRight"); await pg.wait_for_timeout(250)
        await pg.screenshot(path=str(OUT / f"{side}-bump.png"))
        res["afterBump"] = norm(await pg.evaluate("window.__duel.state()"))
        for i, mv in enumerate(ROUTE, 1):
            await pg.keyboard.press(KEYS[mv]); await pg.wait_for_timeout(180)
            await pg.screenshot(path=str(OUT / f"{side}-route-{i:02d}.png"))
        res["afterKeysRoute"] = norm(await pg.evaluate("window.__duel.state()"))
        key_ok = res["afterKeysRoute"] == TESTS[10]["expected"]
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(OUT / f"{side}-delivered.png"), full_page=True)
        res["deliveredText"] = (await pg.inner_text("body"))[:1500]
    res["keyboardRouteOk"] = key_ok
    # 5) mobil: taşma + düğmeler
    async def overflow(w, h):
        await pg.set_viewport_size({"width": w, "height": h}); await pg.wait_for_timeout(400)
        return await pg.evaluate("({sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth})")
    o1 = await overflow(1280, 720); await pg.screenshot(path=str(OUT / f"{side}-1280.png"))
    o2 = await overflow(390, 844)
    res["overflow"] = {"1280": o1, "390": o2}
    no_over = o1["sw"] <= o1["cw"] and o2["sw"] <= o2["cw"]
    btns = await pg.evaluate("""[...document.querySelectorAll('button')].map(b=>{const r=b.getBoundingClientRect();
        return {t:(b.innerText||'').trim(), a:b.getAttribute('aria-label')||'', w:r.width, h:r.height}})""")
    res["buttons"] = btns
    words = {"up": ["yukarı", "↑", "▲", "up"], "down": ["aşağı", "↓", "▼", "down"], "left": ["sol", "←", "◀", "left"], "right": ["sağ", "→", "▶", "right"]}
    dir_btns = {}
    for d, ws in words.items():
        for bt in btns:
            s = (bt["t"] + " " + bt["a"]).lower()
            if any(w in s for w in ws):
                dir_btns[d] = bt; break
    res["dirButtons"] = dir_btns
    big = len(dir_btns) == 4 and all(v["w"] >= 44 and v["h"] >= 44 for v in dir_btns.values())
    # düğme tıklaması = tuş: aşağı düğmesi
    click_ok = False
    if res["hasApi"] and "down" in dir_btns:
        await pg.evaluate("window.__duel.reset()")
        lab = dir_btns["down"]["a"] or dir_btns["down"]["t"]
        loc = pg.locator(f'button[aria-label="{dir_btns["down"]["a"]}"]') if dir_btns["down"]["a"] else pg.locator("button", has_text=dir_btns["down"]["t"])
        await loc.first.click(); await pg.wait_for_timeout(250)
        click_ok = norm(await pg.evaluate("window.__duel.state()")) == TESTS[4]["expected"] | {} if False else (await pg.evaluate("window.__duel.state().y")) == 1
        res["clickLabel"] = lab
        await pg.screenshot(path=str(OUT / f"{side}-click-down.png"))
    res["points"]["mobil"] = 5 * no_over + 5 * (big and click_ok and bool(key_ok))
    res["points"]["yerel"] = 5 * (len(res["requests"]) == 0) + 5 * (len(res["console"]) == 0 and res["hasApi"])
    res["autoTotal"] = sum(res["points"].values())
    await ctx.close(); await b.close()
    return res


async def main():
    async with async_playwright() as p:
        out = {}
        for side in ("gpt", "claude"):
            if (BASE / f"{side}.html").exists():
                out[side] = await side_run(p, side)
    (OUT / "measure.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for s, r in out.items():
        print(s, r["bytes"], "B", r["points"], "auto", r["autoTotal"], "/ 95 (+5 görsel eşlik gözle)", "req", len(r["requests"]), "con", r["console"][:3])
        print("  fails:", {k: v["got"] for k, v in r["tests"].items() if not v["ok"]})


asyncio.run(main())
