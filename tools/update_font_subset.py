# -*- coding: utf-8 -*-
"""logo 圓體（粉圓 Huninn）只載「logo 用到的字」，網頁才不會變重。
改了標題、作品名稱、區塊名稱之後跑一次：python tools/update_font_subset.py
它會掃 index.html 與 marketing.html 裡用圓體顯示的文字，重寫兩頁 <link id="headFont"> 的 text= 參數。
沒跑也不會壞：缺的字會改用系統黑體顯示，只是那幾個字不是圓體。
注意：字太多（約 500 字以上）時 Google 會改送整套字型（4.6MB），所以只收標題類文字。"""
import re, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [ROOT / "index.html", ROOT / "marketing.html"]
# 2026-10-22 起圓體只用在 logo 字標（大標改宋體、內文黑體），所以只收 logo 的字
PATTERNS = [r'<span class="wm"><b>(.*?)</b>']
EXTRA = "芷均的自動化小鎮"

chars = set(EXTRA)
for page in PAGES:
    s = page.read_text(encoding="utf-8")
    for pat in PATTERNS:
        for m in re.findall(pat, s, re.S):
            t = re.sub(r"\$\{[^}]*\}", "", m)          # 拿掉 JS 樣板變數
            t = re.sub(r"<[^>]+>", "", t)              # 拿掉內層標籤
            t = re.sub(r"&\w+;", "", t)                # 拿掉 &amp; 之類
            chars |= {c for c in t if not c.isspace()}
text = "".join(sorted(chars))
href = "https://fonts.googleapis.com/css2?family=Huninn&display=swap&text=" + urllib.parse.quote(text, safe="")
for page in PAGES:
    s = page.read_text(encoding="utf-8")
    new = re.sub(r'(<link id="headFont" rel="stylesheet" href=")[^"]*(")', lambda m: m.group(1) + href.replace("&", "&amp;") + m.group(2), s)
    page.write_text(new, encoding="utf-8", newline="\n")
    print(page.name, "已更新" if new != s else "（沒有變化或找不到 headFont）")
print("共", len(text), "個字")
