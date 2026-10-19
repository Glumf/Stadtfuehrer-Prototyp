import re, os, sys, asyncio
from playwright.async_api import async_playwright

BASE = sys.argv[1]          # folder holding the .dc.html files
FONTS = sys.argv[2]         # @fontsource files folder root (node_modules/@fontsource)
OUT = sys.argv[3]

FONT_CSS = f"""
@font-face{{font-family:'Atkinson Hyperlegible';font-weight:400;src:url('file://{FONTS}/atkinson-hyperlegible/files/atkinson-hyperlegible-latin-400-normal.woff2') format('woff2');}}
@font-face{{font-family:'Atkinson Hyperlegible';font-weight:700;src:url('file://{FONTS}/atkinson-hyperlegible/files/atkinson-hyperlegible-latin-700-normal.woff2') format('woff2');}}
@font-face{{font-family:'Atkinson Hyperlegible';font-weight:400;unicode-range:U+0100-024F;src:url('file://{FONTS}/atkinson-hyperlegible/files/atkinson-hyperlegible-latin-ext-400-normal.woff2') format('woff2');}}
@font-face{{font-family:'Bricolage Grotesque';font-weight:700;src:url('file://{FONTS}/bricolage-grotesque/files/bricolage-grotesque-latin-700-normal.woff2') format('woff2');}}
@font-face{{font-family:'Bricolage Grotesque';font-weight:800;src:url('file://{FONTS}/bricolage-grotesque/files/bricolage-grotesque-latin-800-normal.woff2') format('woff2');}}
body{{margin:0;background:#FFFFFF}}
a{{color:#14202E}}
"""

def read(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return f.read()

def body_markup(src):
    """Markup inside <x-dc> after </helmet>."""
    inner = src.split("<x-dc>", 1)[1].split("</x-dc>", 1)[0]
    if "</helmet>" in inner:
        inner = inner.split("</helmet>", 1)[1]
    return inner

def parse_palette(src, key):
    m = re.search(key + r":\s*\{([^}]*)\}", src)
    pairs = re.findall(r"(\w+):\s*'([^']*)'", m.group(1))
    return dict(pairs)

def fill(markup, prefix, pal):
    return re.sub(r"\{\{\s*" + prefix + r"\.(\w+)\s*\}\}", lambda m: pal[m.group(1)], markup)

def page_html(markup):
    return f"<!doctype html><html lang='de'><head><meta charset='utf-8'><style>{FONT_CSS}</style></head><body>{markup}</body></html>"

SAMPLE = body_markup(read("Sample.dc.html"))

def build(name):
    src = read(name)
    markup = body_markup(src)
    if name.startswith("Farben-"):
        light = parse_palette(src, "light")
        dark = parse_palette(src, "dark")
        markup = re.sub(r'<dc-import name="Sample" pal="\{\{ light \}\}"[^>]*></dc-import>', lambda m: fill(SAMPLE, "p", light), markup)
        markup = re.sub(r'<dc-import name="Sample" pal="\{\{ dark \}\}"[^>]*></dc-import>', lambda m: fill(SAMPLE, "p", dark), markup)
        markup = fill(markup, "light", light)
        markup = fill(markup, "dark", dark)
    assert "{{" not in markup, name
    return page_html(markup)

BOARDS = [
    ("Main.dc.html", "01-profil.png"),
    ("Tour.dc.html", "02-tour-erstellen.png"),
    ("Gruppen.dc.html", "02b-gruppen-tour.png"),
    ("Preview.dc.html", "03-vorschau.png"),
    ("Live.dc.html", "04-unterwegs.png"),
    ("MyTours.dc.html", "05-meine-touren.png"),
    ("Farben-Wegweiser.dc.html", "farben-1-wegweiser.png"),
    ("Farben-Stadtpark.dc.html", "farben-2-stadtpark.png"),
    ("Farben-Abend.dc.html", "farben-3-abendstimmung.png"),
    ("Farben-Hafen.dc.html", "farben-4-hafen.png"),
    ("Farben-Altstadt.dc.html", "farben-5-altstadt.png"),
]

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1000, "height": 1600}, device_scale_factor=2)
        for src_name, out_name in BOARDS:
            html_path = os.path.join(OUT, out_name.replace(".png", ".html"))
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(build(src_name))
            await page.goto("file://" + html_path)
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(200)
            await page.locator("body > div").first.screenshot(path=os.path.join(OUT, out_name))
            print("ok", out_name)
        await browser.close()

asyncio.run(main())
