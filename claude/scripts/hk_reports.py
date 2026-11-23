import requests, re, sys, json, urllib.parse, time, os
base = sys.argv[1]; names = sys.argv[2].split(",")
sdate = sys.argv[3] if len(sys.argv) > 3 else "2026-06-01"
out = {}
for n in names:
    q = urllib.parse.quote(n)
    url = f"https://consensus.hankyung.com/analysis/list?sdate={sdate}&edate=2026-11-23&now_page=1&search_value=&report_type=CO&pagenum=50&search_text={q}&business_code="
    for i in range(4):
        try:
            h = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36", "Accept": "text/html"}).text; break
        except Exception:
            time.sleep(2); h = ""
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", h, re.S)
    lst = []
    for r in rows:
        tds = re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)
        if len(tds) < 5: continue
        clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()
        date = clean(tds[0]); title = clean(tds[1]); tp = clean(tds[2]); op = clean(tds[3]); au = clean(tds[4]); src = clean(tds[5]) if len(tds) > 5 else ""
        m = re.search(r"report_idx=(\d+)", r)
        lst.append({"date": date, "title": title[:120], "tp": tp, "op": op, "author": au, "src": src, "idx": m.group(1) if m else None})
    out[n] = lst
    print(f"== {n}: {len(lst)} reports")
    for x in lst[:12]:
        print(f"  {x['date']} | {x['src']} | {x['tp']} | {x['op']} | {x['title'][:80]} | {x['idx']}")
json.dump(out, open(f"{base}/hk_reports_{int(time.time())}.json", "w"), ensure_ascii=False)
