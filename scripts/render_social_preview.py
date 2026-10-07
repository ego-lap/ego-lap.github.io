"""Render a 1200×630 JPEG social card from the project's existing assets."""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'assets/images/egolap-social-preview.jpg'

def main():
    photo = (ROOT / 'assets/images/keynote/robot-yam.webp').as_uri()
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
    *{{box-sizing:border-box}}body{{margin:0;font-family:Arial,sans-serif;background:white;color:#1a1a1a}}
    .card{{width:1200px;height:630px;display:grid;grid-template-columns:720px 480px}}
    .copy{{padding:57px 55px;display:flex;flex-direction:column;border-top:9px solid #ec5800}}
    .wordmark{{font-size:89px;font-weight:750;letter-spacing:-5px;line-height:1.05;margin:0 0 30px}}.wordmark span{{color:#ec5800}}
    h1{{font-size:35px;line-height:1.27;letter-spacing:-.8px;font-weight:600;margin:0;max-width:590px}}
    .footer{{margin-top:auto}}.institutions{{font-size:16px;line-height:1.7;color:#777;margin:0 0 15px}}
    .url{{font-size:21px;font-weight:600;color:#c45e00}}.photo{{width:480px;height:630px;object-fit:cover;object-position:50% 56%}}
    </style></head><body><div class="card"><div class="copy"><div class="wordmark">Ego<span>LAP</span></div><h1>Learning from Egocentric Human Data through Language-Action Reasoning</h1><div class="footer"><p class="institutions">Princeton University · Toyota Research Institute<br>Physical Intelligence</p><div class="url">ego-lap.github.io</div></div></div><img class="photo" src="{photo}" alt="Bimanual YAM robot"></div></body></html>'''
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/google-chrome', headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
        with TemporaryDirectory(prefix='egolap-social-') as temporary:
            card = Path(temporary) / 'card.html'
            card.write_text(html)
            page.goto(card.as_uri())
        page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        page.screenshot(path=str(TARGET), type='jpeg', quality=90)
        browser.close()
    print(f'{TARGET.name}: {TARGET.stat().st_size:,} bytes')

if __name__ == '__main__':
    main()
