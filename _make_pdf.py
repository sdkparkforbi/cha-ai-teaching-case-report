# -*- coding: utf-8 -*-
import sys, pathlib; sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

HTML = pathlib.Path(r"D:\Teaching\2026_1\BizStat\report\index.html").resolve()
OUT  = r"D:\Teaching\2026_1\BizStat\report\AI-Teaching-Case-Report.pdf"
url  = HTML.as_uri()

footer = ('<div style="font-size:9px;color:#777;width:100%;text-align:center;'
          'font-family:sans-serif;padding:0;margin:0;">'
          '<span class="pageNumber"></span> / <span class="totalPages"></span></div>')
empty = '<div></div>'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    # paged.js 차단 → 네이티브 페이지네이션만 사용(이중 번호 방지)
    pg.route("**/paged.polyfill.js", lambda r: r.abort())
    pg.route("**/pagedjs*", lambda r: r.abort())
    pg.goto(url, wait_until="networkidle")
    pg.emulate_media(media="print")
    # CSS @page @bottom-center 가 페이지번호를 렌더 → Playwright 푸터는 끔(이중 방지)
    pg.pdf(path=OUT, format="A4", print_background=True,
           display_header_footer=False, prefer_css_page_size=True)
    b.close()
print("PDF:", OUT)
