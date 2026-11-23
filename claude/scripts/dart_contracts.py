import requests, re, sys, json, time, os
H = {"User-Agent": "Mozilla/5.0", "Referer": "https://dart.fss.or.kr/dsab007/main.do", "X-Requested-With": "XMLHttpRequest"}
S = requests.Session(); S.get("https://dart.fss.or.kr/dsab007/main.do", headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
def listing(cik, name, start, end):
    out = []
    for page in range(1, 8):
        data = {"currentPage": page, "maxResults": 50, "maxLinks": 10, "sort": "date", "series": "desc", "textCrpCik": cik, "textCrpNm": name,
                "startDate": start, "endDate": end, "reportName": "", "finalReport": "recent", "option": "corp"}
        h = S.post("https://dart.fss.or.kr/dsab007/detailSearch.ax", data=data, headers=H, timeout=40).text
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", h, re.S); got = 0
        for r in rows:
            m = re.search(r"rcpNo=(\d+)", r)
            if not m: continue
            tds = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip() for x in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            out.append({"rcpNo": m.group(1), "title": tds[2] if len(tds) > 2 else "", "date": tds[4] if len(tds) > 4 else ""}); got += 1
        if got < 50: break
        time.sleep(0.8)
    return out
def doc_text(rcp):
    h = S.get(f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcp}", headers={"User-Agent": "Mozilla/5.0"}, timeout=40).text
    m = re.search(r'viewDoc\("\d+",\s*"(\d+)"', h)
    if not m: return None
    dcm = m.group(1)
    v = S.get(f"https://dart.fss.or.kr/report/viewer.do?rcpNo={rcp}&dcmNo={dcm}&eleId=0&offset=0&length=0&dtd=HTML", headers={"User-Agent": "Mozilla/5.0"}, timeout=40)
    v.encoding = v.apparent_encoding or "utf-8"
    t = re.sub(r"<[^>]+>", " | ", v.text); t = re.sub(r"(\s*\|\s*)+", " | ", t); t = re.sub(r"\s+", " ", t)
    return t
if __name__ == "__main__":
    cik, name, start, end, outp = sys.argv[1:6]
    L = listing(cik, name, start, end)
    C = [x for x in L if "단일판매" in x["title"]]
    print(name, "total", len(L), "contracts", len(C))
    res = []
    for x in C:
        t = doc_text(x["rcpNo"]); time.sleep(0.6)
        res.append({**x, "text": t})
        print(x["date"], x["title"], (t or "")[:0])
    json.dump({"list": L, "contracts": res}, open(outp, "w"), ensure_ascii=False)
